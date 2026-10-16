# 開いている問題だけを debug ビルドする（Python は構文チェックだけ）
# デバッグ（F5）の対象も、この問題に切り替わる
#
# 使い方: python3 build.py <開いているファイル>
import sys

from common import build, parse_path

problem, source = parse_path(sys.argv[1])
build(problem, source)
