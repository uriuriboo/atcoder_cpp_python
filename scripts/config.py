# 環境に合わせて変える設定。タスクのスクリプトはすべてここを参照する
# AtCoder の言語環境（https://img.atcoder.jp/file/language-update/2025-10/language-list.html）が
# 更新されたら、ここと .devcontainer/Dockerfile・requirements.txt をまとめて更新する

# ---- C++ ----
CXX = 'g++'
# 共通のフラグ。AtCoder の C++23 (GCC 15.2.0) と同じ規格と、ac-library（Dockerfile で /opt/ac-library に置く）
CXXFLAGS = ['-std=gnu++23', '-Wall', '-Wextra', '-I/opt/ac-library']
# debug（build・build & test・submit 前のテスト・stress）：
# デバッガで追えるよう最適化せず、範囲外アクセス（_GLIBCXX_DEBUG・AddressSanitizer）と
# 未定義動作（符号付き整数のオーバーフローなど。UndefinedBehaviorSanitizer）を実行時エラー（RE）として検出する
DEBUG_FLAGS = [
    '-g', '-O0', '-DLOCAL', '-D_GLIBCXX_DEBUG',
    '-fsanitize=address,undefined', '-fno-sanitize-recover=all', '-fno-omit-frame-pointer',
]
# release（build & test release）：AtCoder のコンパイルオプションに合わせる。実行時間の確認用
RELEASE_FLAGS = [
    '-O2', '-DATCODER', '-DONLINE_JUDGE', '-DNOMINMAX', '-march=native', '-pthread', '-fopenmp',
    '-fconstexpr-depth=1024', '-fconstexpr-loop-limit=524288', '-fconstexpr-ops-limit=2097152',
    '-ftrivial-auto-var-init=zero',
]
LDLIBS = ['-lgmpxx', '-lgmp']

# ---- Python ----
# 解答の .py をテストするインタプリタと、提出する言語。'cpython' か 'pypy'
PYTHON_LANG = 'cpython'
PYTHON_COMMANDS = {
    'cpython': 'python3.13',  # Dockerfile の venv（~/.venv。AtCoder と同じライブラリ入り）
    'pypy': 'pypy3',          # apt の PyPy 7.3.20
}
# ランダムテストの gen.py・naive.py を動かす Python
PYTHON = 'python3.13'

# ---- 提出 ----
# 提出ページで選ぶ言語（submit がターミナルに表示する）
LANGUAGE_NAMES = {
    'cpp': 'C++23 (GCC 15.2.0)',
    'cpython': 'Python (CPython 3.13.7)',
    'pypy': 'Python (PyPy 3.11-v7.3.20)',
}

# ---- new contest ----
# 問題ごとに作る解答ファイル（templates/main.<拡張子> から作る）。使わない言語は消してよい
NEW_CONTEST_LANGUAGES = ['cpp', 'py']
