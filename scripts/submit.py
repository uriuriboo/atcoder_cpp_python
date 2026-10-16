# 開いている問題をサンプルでテストし、通ったら AtCoder の提出ページ（問題を選んだ状態）をブラウザで開く
# AtCoder の提出フォームには Cloudflare Turnstile（CAPTCHA）があり、コマンドラインからは提出できないため、提出はブラウザで行う
# （online-judge-tools の oj submit も、同じ理由と AtCoder のページの変更で動かない）
#
# 使い方: python3 submit.py <開いているファイル>
import re
import sys
import webbrowser

import config
from common import build, ensure_samples, oj_test, parse_path

problem, source = parse_path(sys.argv[1])
command = build(problem, source)
ensure_samples(problem)
if oj_test(command, problem.tests_dir) != 0:
    sys.exit('サンプルが通らないため、提出ページを開きません')

match = re.search(r'/contests/([^/]+)/tasks/([^/?#]+)', problem.url)
if not match:
    sys.exit('問題の URL から提出ページが分かりません: ' + problem.url)
url = 'https://atcoder.jp/contests/{}/submit?taskScreenName={}'.format(*match.groups())
language = config.LANGUAGE_NAMES['cpp' if source.suffix == '.cpp' else config.PYTHON_LANG]
print()
print('提出ページ: ' + url)
print('言語「{}」を選び、コード（エディタで Ctrl+A → Ctrl+C）を貼り付けて提出してください'.format(language), flush=True)
# Dev Container では、VS Code が設定する環境変数 BROWSER によって、ホストのブラウザで開く
webbrowser.open(url)
