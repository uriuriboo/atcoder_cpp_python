# コンテストを始める：問題の一覧を取得し、問題ごとに解答ファイルの雛形とサンプルを用意する
#
# 使い方: python3 new_contest.py <abc325 か https://atcoder.jp/contests/abc325>
#
# contests/<contest>/
# ├── a.cpp, a.py      解答ファイル（templates/main.* から作る。config.NEW_CONTEST_LANGUAGES の言語だけ）
# ├── tests/a/         サンプルの入出力（sample-1.in / sample-1.out ...）
# └── contest.json     問題の URL（テストと提出で使う）
#
# 既にあるファイルは上書きしないので、途中で失敗しても、もう一度実行すればよい
import json
import re
import shutil
import sys
from urllib.error import URLError
from urllib.request import urlopen

import config
from common import CONTESTS, WORKSPACE, Problem, download_samples, open_in_editor

# 問題一覧の表の各行には、問題へのリンクが「A」（問題の記号）と問題名の 2 つある。最初のリンクの文字を問題名にする
# online-judge-tools の oj-api get-contest は、AtCoder の表の変更で動かなくなっているため自前で読む
TASK_LINK = re.compile(r'<a href="(/contests/[^/"]+/tasks/([^/"]+))">([^<]*)</a>')


def contest_id(arg):
    match = re.search(r'atcoder\.jp/contests/([^/?#]+)', arg)
    return match.group(1) if match else arg.strip().lower()


def fetch_problems(contest):
    url = 'https://atcoder.jp/contests/{}/tasks'.format(contest)
    try:
        html = urlopen(url, timeout=30).read().decode('utf-8')
    except (URLError, TimeoutError) as e:
        sys.exit('問題の一覧を取得できませんでした（{}）: {}'.format(e, url))

    problems = {}
    seen = set()
    for path, task_id, text in TASK_LINK.findall(html):
        if path in seen:
            continue
        seen.add(path)
        name = text.strip().lower()
        if not re.fullmatch(r'[0-9a-z_-]+', name):
            name = task_id.rsplit('_', 1)[-1]
        problems[name] = 'https://atcoder.jp' + path
    if not problems:
        sys.exit('問題が見つかりません。コンテストの開始前か、コンテスト ID が違う可能性があります: ' + url)
    return problems


def main():
    contest = contest_id(sys.argv[1])
    contest_dir = CONTESTS / contest
    problems = fetch_problems(contest)
    contest_dir.mkdir(parents=True, exist_ok=True)
    with open(contest_dir / 'contest.json', 'w', encoding='utf-8') as f:
        json.dump({'contest': contest, 'problems': problems}, f, indent=2)
    print('{}: {}'.format(contest, ' '.join(problems)))

    failed = []
    for name in problems:
        for language in config.NEW_CONTEST_LANGUAGES:
            source = contest_dir / '{}.{}'.format(name, language)
            if not source.exists():
                shutil.copyfile(WORKSPACE / 'templates' / 'main.{}'.format(language), source)
        problem = Problem(contest, name)
        if not any(problem.tests_dir.glob('*.in')) and not download_samples(problem):
            failed.append(name)

    if failed:
        print('サンプルを取得できなかった問題: {}（build & test のときにもう一度取得します）'.format(' '.join(failed)))
    # 最初の問題をエディタで開く
    first = next(iter(problems))
    open_in_editor(contest_dir / '{}.{}'.format(first, config.NEW_CONTEST_LANGUAGES[0]))


if __name__ == '__main__':
    main()
