# 開いている問題をビルドして、input.txt を標準入力にして実行する
# input.txt などを開いているときは、最後にビルドした問題を実行する（input.txt を編集してすぐ実行できるように）
#
# 使い方: python3 run.py <開いているファイル>
import subprocess
import sys

from common import INPUT, build, parse_path

problem, source = parse_path(sys.argv[1], use_current=True)
command = build(problem, source)
with open(INPUT) as stdin:
    sys.exit(subprocess.run(command, shell=True, stdin=stdin).returncode)
