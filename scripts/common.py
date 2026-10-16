# タスクのスクリプトで共通の処理（パスの解析、ビルド、サンプルの取得とテスト）
import hashlib
import json
import os
import shlex
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

import config

# リポジトリのフォルダ名やマウント先に依存しないよう、このファイルの場所から求める
WORKSPACE = Path(__file__).resolve().parent.parent
CONTESTS = WORKSPACE / 'contests'
BUILD = WORKSPACE / 'build'
INPUT = WORKSPACE / 'input.txt'
# デバッグ（launch.json）が参照する「最後にビルドした問題」
CURRENT_BINARY = BUILD / 'debug' / 'current'
CURRENT_JSON = BUILD / 'current.json'
SOURCE_SUFFIXES = ('.cpp', '.py')


@dataclass(frozen=True)
class Problem:
    contest: str  # abc325
    name: str     # a

    @property
    def contest_dir(self):
        return CONTESTS / self.contest

    @property
    def tests_dir(self):
        return self.contest_dir / 'tests' / self.name

    @property
    def stress_dir(self):
        return self.contest_dir / 'stress' / self.name

    @property
    def url(self):
        # new contest が保存した問題の URL。無ければ AtCoder でよくある形から作る
        try:
            with open(self.contest_dir / 'contest.json', encoding='utf-8') as f:
                return json.load(f)['problems'][self.name]
        except (OSError, KeyError, ValueError):
            return 'https://atcoder.jp/contests/{0}/tasks/{0}_{1}'.format(self.contest, self.name)


def parse_path(path, use_current=False):
    """開いているファイルから、問題と解答ファイルを判定する

    - contests/<contest>/<problem>.cpp / .py   : そのファイルが解答
    - contests/<contest>/stress/<problem>/...  : gen.py・naive.py など。解答は下の find_source で選ぶ
    - contests/<contest>/tests/<problem>/...   : サンプルの入出力。同上
    use_current: どれでもないとき（input.txt を編集中など）は、最後に debug ビルドした解答を使う
    """
    try:
        parts = Path(path).resolve().relative_to(CONTESTS).parts
    except ValueError:
        parts = ()
    if len(parts) == 2 and Path(parts[1]).suffix in SOURCE_SUFFIXES:
        return Problem(parts[0], Path(parts[1]).stem), CONTESTS.joinpath(*parts)
    if len(parts) >= 3 and parts[1] in ('stress', 'tests'):
        problem = Problem(parts[0], parts[2])
        return problem, find_source(problem)
    if use_current and CURRENT_JSON.exists():
        source = json.loads(CURRENT_JSON.read_text())['source']
        print('最後にビルドした解答を使います: ' + source, flush=True)
        return parse_path(source)
    sys.exit('解答ファイル（contests/<contest>/<problem>.cpp か .py）を開いて、アクティブにした状態で実行してください: {}'.format(path))


def find_source(problem):
    # .cpp と .py の両方があるときは、更新が新しい方（書いている方）を解答とみなす
    sources = [problem.contest_dir / (problem.name + suffix) for suffix in SOURCE_SUFFIXES]
    sources = [s for s in sources if s.exists()]
    if not sources:
        sys.exit('解答ファイルがありません: {}/{}.cpp か .py'.format(problem.contest_dir, problem.name))
    source = max(sources, key=lambda s: s.stat().st_mtime)
    print('解答ファイル: ' + str(source.relative_to(WORKSPACE)), flush=True)
    return source


# ---- ビルド ----

def build(problem, source, release=False):
    """解答をビルドし、実行するコマンド（oj test -c に渡す文字列）を返す。失敗したら終了する"""
    if source.suffix == '.cpp':
        command = shlex.quote(str(compile_cpp(problem, source, release)))
    else:
        check_python(source)
        command = shlex.join([config.PYTHON_COMMANDS[config.PYTHON_LANG], str(source)])
    if not release:
        record_current(source)
    return command


def compile_cpp(problem, source, release):
    profile = 'release' if release else 'debug'
    flags = config.CXXFLAGS + (config.RELEASE_FLAGS if release else config.DEBUG_FLAGS)
    binary = BUILD / profile / problem.contest / problem.name
    binary.parent.mkdir(parents=True, exist_ok=True)
    command = [config.CXX, *flags, *precompiled_header(flags), '-o', str(binary), str(source), *config.LDLIBS]

    # ソースもフラグも変わっていなければ、ビルドし直さない（build & test のあとの stress など）
    stamp = binary.with_name(binary.name + '.cmd')
    if (binary.exists() and binary.stat().st_mtime >= source.stat().st_mtime
            and stamp.exists() and stamp.read_text() == shlex.join(command)):
        print('up to date ({}): {}'.format(profile, source.relative_to(WORKSPACE)))
    else:
        print('compile ({}): {}'.format(profile, source.relative_to(WORKSPACE)), flush=True)
        stamp.unlink(missing_ok=True)
        if subprocess.run(command).returncode != 0:
            sys.exit(1)
        stamp.write_text(shlex.join(command))

    if not release:
        # launch.json の "Debug C++" は build/debug/current を実行する
        CURRENT_BINARY.unlink(missing_ok=True)
        CURRENT_BINARY.symlink_to(binary)
    return binary


def precompiled_header(flags):
    """bits/stdc++.h をフラグごとに 1 度だけプリコンパイルし、それを使うための引数を返す

    GCC は #include のたびに、各インクルードディレクトリで <ヘッダ>.gch を先に探すため、
    build/pch/<フラグのハッシュ>/bits/stdc++.h.gch を置いたディレクトリを -I で渡すだけで使われる。
    フラグが少しでも違う .gch は使えないので、フラグごとに作る。作れなかったら普通にコンパイルする。
    """
    key = hashlib.sha1(shlex.join([config.CXX, *flags]).encode()).hexdigest()[:12]
    pch_dir = BUILD / 'pch' / key
    gch = pch_dir / 'bits' / 'stdc++.h.gch'
    if not gch.exists():
        header = find_system_header('bits/stdc++.h', flags)
        if header is None:
            return []
        gch.parent.mkdir(parents=True, exist_ok=True)
        print('precompile bits/stdc++.h（このフラグでは初回だけ。数十秒かかる）', flush=True)
        tmp = gch.with_name(gch.name + '.tmp')
        if subprocess.run([config.CXX, *flags, '-x', 'c++-header', header, '-o', str(tmp)]).returncode != 0:
            print('プリコンパイルに失敗したため、使わずにコンパイルします')
            return []
        tmp.replace(gch)
    return ['-I', str(pch_dir), '-Winvalid-pch']


def find_system_header(name, flags):
    # プリプロセッサの依存関係の出力（-M）から、実際に読まれるヘッダのパスを得る
    cp = subprocess.run([config.CXX, *flags, '-x', 'c++', '-M', '-'],
                        input='#include <{}>\n'.format(name), capture_output=True, text=True)
    for token in cp.stdout.split():
        if token.endswith(name):
            return token
    return None


def check_python(source):
    # Python はビルドが無いので、構文エラーだけ先に確かめる
    try:
        compile(source.read_text(encoding='utf-8'), str(source), 'exec')
    except SyntaxError as e:
        print('SyntaxError: {} ({}:{})'.format(e.msg, source, e.lineno))
        sys.exit(1)


def record_current(source):
    # デバッグ（scripts/debug_python.py）が、開いているファイルが .py でないときに使う
    BUILD.mkdir(exist_ok=True)
    CURRENT_JSON.write_text(json.dumps({'source': str(source)}))


# ---- サンプル ----

def download_samples(problem):
    cp = subprocess.run(['oj', 'download', problem.url, '-d', str(problem.tests_dir)])
    return cp.returncode == 0


def ensure_samples(problem):
    if any(problem.tests_dir.glob('*.in')):
        return
    print('サンプルが無いため取得します: ' + problem.url)
    if not download_samples(problem):
        sys.exit('サンプルを取得できませんでした。コンテストの開始前か、ログインが必要な可能性があります')


def oj_test(command, tests_dir):
    # テストケースを CPU のコア数だけ並列に実行する
    cp = subprocess.run(['oj', 'test', '-c', command, '-d', str(tests_dir), '-j', str(os.cpu_count())])
    return cp.returncode


def open_in_editor(path):
    if shutil.which('code'):
        subprocess.run(['code', str(path)])
