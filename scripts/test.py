# 開いている問題をビルドして、サンプルでテストする
# サンプルが無ければ先に取得する（new contest を使わずに作ったファイルでも動く）
#
# 使い方: python3 test.py [--release] <開いているファイル>
#   --release: AtCoder と同じ最適化でビルドする（実行時間の確認用）。debug ビルドはしない
import argparse
import sys

from common import build, ensure_samples, oj_test, parse_path

parser = argparse.ArgumentParser()
parser.add_argument('file')
parser.add_argument('--release', action='store_true')
args = parser.parse_args()

problem, source = parse_path(args.file)
command = build(problem, source, release=args.release)
ensure_samples(problem)
sys.exit(oj_test(command, problem.tests_dir))
