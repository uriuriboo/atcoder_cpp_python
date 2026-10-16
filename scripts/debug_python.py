# Python のデバッグ実行用（.vscode/launch.json の "Debug Python"）。標準入力を input.txt に向けてから、指定したファイルを実行する
# debugpy の launch.json には標準入力を切り替える設定が無いため、このスクリプトを経由する
#
# 使い方: python3 debug_python.py <実行する .py>
# 開いているファイルが .py でないとき（input.txt を編集中など）は、最後にビルド・テストした .py の解答を実行する
import json
import os
import runpy
import sys

from common import CURRENT_JSON, INPUT

target = os.path.abspath(sys.argv[1])
if not target.endswith('.py'):
    try:
        target = json.loads(CURRENT_JSON.read_text())['source']
    except (OSError, KeyError, ValueError):
        target = ''
    if not target.endswith('.py'):
        sys.exit('デバッグする .py を開いてアクティブにしてから、F5 を押してください')
print('debug: ' + target)
# input()・sys.stdin・open(0) のどれで読んでも input.txt から読めるよう、ファイル記述子 0 を差し替える
fd = os.open(INPUT, os.O_RDONLY)
os.dup2(fd, 0)
os.close(fd)
# 対象のファイルを直接実行したときと同じ sys.argv・sys.path にする
sys.argv = [target]
sys.path[0] = os.path.dirname(target)
runpy.run_path(target, run_name='__main__')
