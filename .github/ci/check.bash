#!/bin/bash
# CI（.github/workflows/check_environment.yml）で、devcontainer の中で実行する確認
# AtCoder に接続しない確認だけを失敗扱いにする（new contest はネットワークとコンテストの状態に左右されるため警告だけ）
set -eux

dir=contests/ci
mkdir -p "$dir/tests/a"
cp .github/ci/a.cpp .github/ci/a.py .github/ci/b.cpp "$dir/"
printf '3 5\n' > "$dir/tests/a/sample-1.in"
printf '8\n' > "$dir/tests/a/sample-1.out"
printf '1000000000 1000000000\n' > "$dir/tests/a/sample-2.in"
printf '2000000000\n' > "$dir/tests/a/sample-2.out"

# C++：debug（サニタイザ・プリコンパイルヘッダ）と release でビルドしてテストする
python3 scripts/test.py "$dir/a.cpp"
python3 scripts/test.py "$dir/a.cpp"  # 2 回目はビルドしない
python3 scripts/test.py --release "$dir/a.cpp"
test -x build/debug/current

# Python：CPython（ライブラリ入り）と PyPy
python3 scripts/test.py "$dir/a.py"
pypy3 "$dir/a.py" < "$dir/tests/a/sample-1.in"

# submit：テストが通ると、提出ページの URL をブラウザ（ここでは echo）に渡す
BROWSER=echo python3 scripts/submit.py "$dir/a.cpp" | grep -F 'https://atcoder.jp/contests/ci/submit?taskScreenName=ci_a'

# デバッグ実行の入力と run
cp "$dir/tests/a/sample-1.in" input.txt
python3 scripts/run.py "$dir/a.cpp"

# ランダムテスト：a == b のときだけ間違える b.cpp の反例が見つかるか
python3 scripts/stress.py init "$dir/b.cpp"
cat > "$dir/stress/b/gen.py" << 'EOF'
import random

print(random.randint(1, 3), random.randint(1, 3))
EOF
cat > "$dir/stress/b/naive.py" << 'EOF'
A, B = map(int, input().split())
print(A + B)
EOF
timeout 300 python3 scripts/stress.py hack "$dir/stress/b/gen.py"
test -s input.txt
# 見つけた反例で、stress: test が失敗すること（set -e は ! を付けたコマンドで止まらないため if で確かめる）
if python3 scripts/stress.py test "$dir/b.cpp"; then exit 1; fi

# グラフの可視化
printf '3\n1 2\n2 3\n' > input.txt
python3 scripts/visualize.py input.txt
test -s graph.png

# new contest（AtCoder に接続する）
python3 scripts/new_contest.py abc325 || echo "::warning::new contest failed"
