# ランダムテスト（oj generate-input）で、サンプル以外のテストケースを作る
#
# 使い方: python3 stress.py <init|hack|test> <開いているファイル>
#   init: contests/<contest>/stress/<problem>/ に gen.py（入力の生成）と naive.py（愚直解）の雛形を作る
#   hack: gen.py の入力で、解答と naive.py の出力が食い違うケース（反例）を探す
#         見つかったら stress/<problem>/test/hack-XXX.{in,out} に保存し、input.txt にもコピーする
#   test: stress/<problem>/test/ に保存したケースで、解答をテストする
# 解答の a.cpp・a.py のほか、gen.py・naive.py を開いた状態でも実行できる
import os
import shlex
import shutil
import subprocess
import sys

import config
from common import INPUT, build, oj_test, parse_path

GEN_TEMPLATE = '''\
# 入力を 1 ケース分、標準出力に書き出す
# 値を小さくしておくと、反例が見つかったときに手で追いやすい
import random

N = random.randint(1, 10)
A = [random.randint(1, 10) for _ in range(N)]
print(N)
print(*A)
'''

NAIVE_TEMPLATE = '''\
# 愚直解。計算量は気にせず、確実に正しい方法で書く
N = int(input())
A = list(map(int, input().split()))
print(sum(A))
'''

GEN = shlex.join([config.PYTHON, 'gen.py'])
NAIVE = shlex.join([config.PYTHON, 'naive.py'])


def write_if_absent(path, content):
    if path.exists():
        print('skip (already exists): {}'.format(path))
        return
    path.write_text(content)
    print('created: {}'.format(path))


def init(stress_dir):
    stress_dir.mkdir(parents=True, exist_ok=True)
    write_if_absent(stress_dir / 'gen.py', GEN_TEMPLATE)
    write_if_absent(stress_dir / 'naive.py', NAIVE_TEMPLATE)


def prepare(problem, source):
    if not (problem.stress_dir / 'gen.py').exists():
        sys.exit('gen.py がありません。先に "stress: init" を実行してください: {}'.format(problem.stress_dir))
    command = build(problem, source)
    os.chdir(problem.stress_dir)
    return command


def hack(stress_dir, command):
    if not os.path.exists('naive.py'):
        sys.exit('naive.py がありません: {}'.format(stress_dir))
    # 反例が見つかるまで生成を繰り返す。止めるときは Ctrl+C
    try:
        cp = subprocess.run(['oj', 'generate-input', '-d', 'test', '-j', str(os.cpu_count()),
                             '--hack-actual', command, '--hack-expected', NAIVE, GEN])
    except KeyboardInterrupt:
        sys.exit('interrupted')
    if cp.returncode != 0:
        sys.exit(cp.returncode)
    # 見つけた反例を input.txt にコピーし、F5 のデバッグ実行でそのまま追えるようにする
    found = max((stress_dir / 'test').glob('hack-*.in'), key=os.path.getmtime)
    shutil.copyfile(found, INPUT)
    print('copied {} to input.txt'.format(found))
    print('expected output:')
    print(found.with_suffix('.out').read_text(), end='')


def test(stress_dir, command):
    if not any((stress_dir / 'test').glob('*.in')):
        sys.exit('テストケースがありません。先に "stress: hack" を実行してください: {}'.format(stress_dir))
    sys.exit(oj_test(command, stress_dir / 'test'))


mode = sys.argv[1]
problem, source = parse_path(sys.argv[2])
if mode == 'init':
    init(problem.stress_dir)
elif mode == 'hack':
    hack(problem.stress_dir, prepare(problem, source))
elif mode == 'test':
    test(problem.stress_dir, prepare(problem, source))
else:
    sys.exit('unknown mode: ' + mode)
