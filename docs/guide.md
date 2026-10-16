# 使い方ガイド

この環境で何ができるのか、コンテストで実際にどう使うのかをまとめたもの。タスクの内部の仕組みは [tasks.md](tasks.md) を参照。

## この環境でできること

| やりたいこと | 使う機能 |
| --- | --- |
| コンテストの問題とサンプルを取ってくる | タスク「new contest」 |
| 解いている問題をサンプルでテストする | タスク「build & test」 |
| 実行時間を確かめる | タスク「build & test release」 |
| 自分の入力で実行する | `input.txt` に入力を書いて、タスク「run (input.txt)」 |
| 提出する | タスク「submit」（テストして、ブラウザで提出ページを開く） |
| 自分の入力でステップ実行する | `input.txt` に入力を書いて F5 |
| サンプルは通るのに WA の原因を探す | タスク「stress: init / hack / test」 |
| グラフの入力を図で見る | タスク「visualize graph」 |
| よく書くコードをすぐ書く | スニペット（`tmplt` など）と `library/` |

## はじめかた

### 必要なもの

- Docker（Windows・Mac は Docker Desktop）
- VS Code と拡張機能「Dev Containers」
- AtCoder のアカウント（提出するときだけ。提出はブラウザで行うので、ブラウザでログインしておく）

### 初回のセットアップ

1. このリポジトリを clone する。フォルダ名は変えてもよい。
2. VS Code でフォルダを開き、右下に出る「コンテナーで再度開く」（Reopen in Container）を選ぶ。出ない場合は `Ctrl+Shift+P` →「Dev Containers: Reopen in Container」。
3. 初回はイメージのビルドに数分かかる。終わるとターミナルに、コンパイラなどのバージョンが表示される。

## タスクの実行のしかた

この環境の操作は、ほぼすべて VS Code のタスクで行う。実行のしかたは 3 通り。

- **ステータスバーのボタン**：画面の一番下に、よく使うタスクのボタンが並んでいる。クリックすると実行する。

  | ボタン | タスク |
  | --- | --- |
  | `new contest` | new contest |
  | `test` | build & test |
  | `release` | build & test release |
  | `run` | run (input.txt) |
  | `submit` | submit |

- **ショートカット**：`Ctrl+Shift+B` で「build & test」を実行する（既定のビルドタスク）。
- **コマンドパレット**：`Ctrl+Shift+P` →「タスク: タスクの実行」（Tasks: Run Task）→ タスクを選ぶ。ボタンの無いタスク（build、stress、visualize graph）はここから実行する。

ボタンに出すタスクは、`.vscode/tasks.json` の各タスクの `options.statusbar` で変えられる（拡張機能 [Tasks](https://marketplace.visualstudio.com/items?itemName=actboy168.tasks) の設定。`"hide": true` で出さない）。

「new contest」「visualize graph」以外のタスクは、**解いている問題のファイルをエディタで開いてアクティブにした状態**で実行する。解答ファイルのほか、その問題のサンプル（`tests/a/`）やランダムテストのファイル（`stress/a/`）を開いていてもよい。「run」だけは、`input.txt` などを開いているときも、最後にビルドした問題を実行する。

## コンテストの流れ

ABC325 の A 問題を例にする。

### 1. コンテストを始める

コンテストが始まったら、タスク「new contest」を実行し、コンテスト ID（`abc325`）か URL を入力する。次のものが作られ、`a.cpp` がエディタで開く。

```text
contests/abc325/
├── a.cpp, a.py     解答ファイル（templates/ の雛形入り）
├── b.cpp, b.py
├── ...
├── tests/
│   ├── a/          サンプルの入出力（sample-1.in / sample-1.out ...）
│   └── ...
└── contest.json    問題の URL
```

- C++ と Python のどちらで解いてもよい。使わない方のファイルは消してよい。片方の言語しか使わないなら、`scripts/config.py` の `NEW_CONTEST_LANGUAGES` から外すと、作られなくなる。
- 既にあるファイルは上書きしない。途中で失敗したら、もう一度実行すればよい。
- 問題名は、問題一覧の「A」「B」… を小文字にしたもの（`a.cpp`）。

### 2. 解く

`contests/abc325/a.cpp`（または `a.py`）に書く。C++ ではスニペット `tmplt` を使うと、よく使うマクロや関数が入ったテンプレートに置き換えられる。

### 3. サンプルでテストする

解答ファイルを開いたまま、タスク「build & test」を実行する（`Ctrl+Shift+B`）。ターミナルに各サンプルの結果（AC / WA / RE など）が出る。

- C++ は debug ビルドで動かすので、配列の範囲外アクセスや符号付き整数のオーバーフローがあると、その場で **RE** になり、どの行で起きたかが表示される。AtCoder では WA や AC になってしまうバグも、手元で見つけられる。
- 実行時間を確かめたいときは「build & test release」を使う。AtCoder と同じ最適化（`-O2` など）でビルドする。
- コンパイルが通るかだけ確かめたいときは「build」。
- サンプルが無いとき（`new contest` を使わずにファイルを作ったときなど）は、テストの前に自動で取得する。

### 4. デバッグする

1. 「build」か「build & test」を実行する（デバッグの対象が今の問題に切り替わる）。
2. ルートの `input.txt` に、試したい入力を貼る。
3. 「実行とデバッグ」（`Ctrl+Shift+D`）の一覧で「Debug C++」か「Debug Python」を選び、ブレークポイントを置いて F5 を押す。

- 「Debug C++」は、最後にビルドした問題を実行する。`input.txt` を開いたままでも F5 を押せる。
- 「Debug Python」は、開いている `.py` を実行する。`.py` 以外（`input.txt` など）を開いているときは、最後にビルド・テストした `.py` の解答を実行する。
- デバッグせずに出力だけ見たいときは、タスク「run (input.txt)」（ボタン `run`）を使う。`input.txt` を開いたままでも、最後にビルドした問題を実行する。

### 5. 提出する

AtCoder の提出フォームには CAPTCHA（Cloudflare Turnstile）があり、コマンドラインからは提出できない（online-judge-tools などのツールも同じ）。そのため、提出はブラウザで行う。

1. 解答ファイルを開いたまま、タスク「submit」を実行する。サンプルテストが自動で走り、通らなければ止まる。
2. 通ると、問題を選んだ状態の提出ページがブラウザで開き、ターミナルに選ぶ言語が表示される。
3. エディタで `Ctrl+A` → `Ctrl+C` でコードをコピーし、提出ページに貼り付け、言語を選んで提出する。

- C++ は「C++23 (GCC 15.2.0)」を選ぶ。
- Python は、`scripts/config.py` の `PYTHON_LANG` に合わせて選ぶ。既定は `'cpython'`（「Python (CPython 3.13.7)」）。`'pypy'` にすると、テストも PyPy で行い、「Python (PyPy 3.11-v7.3.20)」と表示する。
- ブラウザが開かないときは、ターミナルに表示された URL を `Ctrl` を押しながらクリックする。

### 6. WA の原因が分からないとき

サンプルは通るのに WA になるときは、ランダムテストで反例を探す。

1. 「stress: init」で、入力生成の `gen.py` と愚直解の `naive.py` の雛形を作る（`contests/abc325/stress/a/` にできる）。
2. 2 つのファイルを問題に合わせて Python で書く。
3. 「stress: hack」で反例を探す。見つかると `input.txt` に入るので、F5 でデバッグする。
4. 直したら「stress: test」で、これまでに見つけた反例がすべて通るか確かめる。

詳しい書き方とコツは [stress_test.md](stress_test.md) を参照。

## そのほかの機能

### グラフの可視化

1. `input.txt` に問題の入力を貼る。
2. タスク「visualize graph」（有向グラフなら「visualize graph (directed)」）を実行する。
3. `graph.png` が作られ、エディタで開く。

| 1 行目 | 読み方 |
| --- | --- |
| `N` | 木として、続く N-1 行を辺として読む |
| `N M` | 続く M 行を辺として読む |

- 辺の行が `u v w` のように 3 列あれば、`w` を重みとして辺のラベルに表示する。
- 頂点番号は 1 始まりとして扱う。辺より後ろの行（クエリなど）は無視する。

### スニペット

| 言語 | キーワード | 展開される内容 |
| --- | --- | --- |
| C++ | `tmplt` / `ntemplt` / `nmtmplt` | マクロ・定数（`MOD = 998244353` など）・chmin/chmax を含むテンプレート全体 |
| C++ | `comb` / `combmod` | 二項係数（mod を取らない版 / mod 998244353 の版） |
| C++ | `pbit` / `binse` | bit 全探索 / めぐる式二分探索 |
| C++ | `fdijk` / `fgbsf` / `fisP` など | ダイクストラ・グリッドの BFS・素数判定などの関数 |
| C++ | `oans` / `oy` / `on` | `ans`・`Yes`・`No` の出力（改行は `endl` ではなく、速い `'\n'`） |
| Python | `input` | 入力の読み方（1 つの整数、整数のリスト、複数行など）を選んで展開 |

スニペットは `.vscode/cpp.code-snippets`・`.vscode/python.code-snippets` で追加・変更できる。

### ライブラリ

`library/cpp/`（ダイクストラ、Union-Find、LCS、ナップサック、mod を取る二項係数など）と `library/python/`（mod を取る二項係数、素因数分解、Union-Find など）に、コピーして使うためのコードがある。

- C++ のスニペット（`fdijk` など）は、`library/cpp/` と同じ中身を、テンプレート（`tmplt` など）の `ll`・`lINF`・`chmin` などを使う形にしたもの。
- 2 つの数の最大公約数・最小公倍数は、C++ も標準の `gcd`・`lcm`（C++17 以降）で求められる。

- C++ は ACL（ac-library）を `#include <atcoder/all>` でそのまま使える。Union-Find（`atcoder::dsu`）や modint などは ACL にもある。
- Python は ACL の移植（ac-library-python。`from atcoder.dsu import DSU` など）が入っている。最大公約数・最小公倍数・二項係数は、標準の `math.gcd`・`math.lcm`・`math.comb` で求められる。

### 設定を変える

設定は `scripts/config.py` にまとめてある。

| 設定 | 内容 |
| --- | --- |
| `PYTHON_LANG` | Python の解答をテスト・提出する言語（`'cpython'` / `'pypy'`） |
| `NEW_CONTEST_LANGUAGES` | new contest で作る解答ファイルの言語 |
| `DEBUG_FLAGS` / `RELEASE_FLAGS` | C++ のコンパイルオプション |
| `LANGUAGE_NAMES` | submit が表示する、提出ページで選ぶ言語の名前 |

解答ファイルの雛形は `templates/main.cpp`・`templates/main.py`。

### コマンドラインから使う

タスクはすべて `scripts/` の Python を呼んでいるので、コンテナ内のターミナルからも同じことができる。

```bash
python3 scripts/new_contest.py abc325
python3 scripts/test.py contests/abc325/a.cpp            # build & test
python3 scripts/test.py --release contests/abc325/a.cpp  # build & test release
python3 scripts/submit.py contests/abc325/a.cpp           # テストして提出ページを開く
python3 scripts/stress.py hack contests/abc325/a.cpp
```

## 困ったとき

### タスクが「解答ファイル（contests/...）を開いて…」で失敗する

解いている問題のファイルがアクティブになっているか確かめる。ターミナルや `input.txt` がアクティブなままだと、問題を判定できない。解答ファイルは `contests/<コンテスト>/<問題>.cpp`（または `.py`）に置く。

### 「Debug C++」で program が見つからない

まだ一度もビルドしていない。「build」か「build & test」を一度実行する。

### サンプルを取得できない

コンテストの開始前は取得できない。開始してから「new contest」をもう一度実行するか、「build & test」を実行する（サンプルが無ければ取得する）。

### ディスクの容量を空けたい

ビルド成果物（プリコンパイルヘッダを含む）は Docker ボリューム `atcoder-cpp-py-build` に置かれ、コンテナを作り直しても残る。コンテナを止めてから、ホストで `docker volume rm atcoder-cpp-py-build` を実行すると消せる。

## 制限

- 解答ファイルは `contests/<コンテスト>/<問題>.cpp` / `.py` に置く前提。ほかの場所のファイルではタスクを使えない。
- 同じ問題に `.cpp` と `.py` の両方があるとき、`gen.py` などから実行すると、更新が新しい方を解答として使う。
- AtCoder の言語環境が更新されたら、`scripts/config.py`・`.devcontainer/Dockerfile`・`requirements.txt` を合わせて更新する必要がある。
