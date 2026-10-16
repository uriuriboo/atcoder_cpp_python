# タスクの仕組み

`.vscode/tasks.json` のタスクが何をしているか、環境の各設定がなぜそうなっているかをまとめたもの。

## タスク一覧

| タスク名 | 呼び出すもの | 開いているファイルを使うか |
| --- | --- | --- |
| new contest | `scripts/new_contest.py <contest>` | 使わない（コンテスト ID を入力する） |
| build | `scripts/build.py ${file}` | 使う |
| build & test | `scripts/test.py ${file}` | 使う |
| build & test release | `scripts/test.py --release ${file}` | 使う |
| run (input.txt) | `scripts/run.py ${file}` | 使う |
| submit | `scripts/submit.py ${file}` | 使う |
| stress: init / hack / test | `scripts/stress.py <mode> ${file}` | 使う |
| visualize graph (directed) | `scripts/visualize.py input.txt [--directed]` | 使わない |

設定（コンパイルオプション・Python の言語など）は `scripts/config.py`、共通の処理は `scripts/common.py` にある。

## 共通処理（`scripts/common.py`）

### パスの解析（`parse_path`）

開いているファイルを `contests/` からの相対パスにして判定する。リポジトリの場所は `common.py` 自身の場所から求めるので、フォルダ名やコンテナ内のパスに依存しない。

| 開いているファイル | 問題 | 解答ファイル |
| --- | --- | --- |
| `contests/abc325/a.cpp` | `abc325` の `a` | そのファイル |
| `contests/abc325/stress/a/gen.py` など | `abc325` の `a` | `a.cpp`・`a.py` のうち更新が新しい方 |
| `contests/abc325/tests/a/sample-1.in` など | 同上 | 同上 |

問題の URL は、new contest が保存した `contests/<contest>/contest.json` から読む。無ければ `https://atcoder.jp/contests/<contest>/tasks/<contest>_<problem>` とみなす。

### ビルド（`build`）

- **C++**：`g++` でコンパイルし、`build/<debug|release>/<contest>/<problem>` に置く。フラグは `config.py` の `CXXFLAGS` に、`DEBUG_FLAGS` か `RELEASE_FLAGS` を足したもの。
  - debug：`-g -O0`、`_GLIBCXX_DEBUG`（STL の範囲外アクセスの検出）、AddressSanitizer・UndefinedBehaviorSanitizer（`-fno-sanitize-recover=all` で検出したら止める）。`-DLOCAL` も付くので、`#ifdef LOCAL` でデバッグ出力を切り替えられる。
  - release：AtCoder のコンパイルオプション（`-O2 -march=native` など）に合わせる。
  - コマンドを `<バイナリ>.cmd` に保存し、ソースより新しいバイナリがあってコマンドも同じなら、ビルドし直さない。
  - debug のときは `build/debug/current` をそのバイナリへのシンボリックリンクにする（「Debug C++」が実行する）。
- **Python**：ビルドは無いので、`compile()` で構文エラーだけ確かめる。実行コマンドは `config.PYTHON_COMMANDS[config.PYTHON_LANG]`（既定は `python3.13`）。
- debug のときは、解答ファイルのパスを `build/current.json` に書く（「Debug Python」が、`.py` 以外を開いているときに使う）。

### プリコンパイルヘッダ（`precompiled_header`）

`bits/stdc++.h` の解析がコンパイル時間の大半を占めるため、フラグごとに 1 度だけプリコンパイルする。

- GCC は `#include <x>` のたびに、各インクルードディレクトリで `x.gch` を先に探す。そこで `build/pch/<フラグのハッシュ>/bits/stdc++.h.gch` を作り、そのディレクトリを `-I` で渡す。解答のソースは変えなくてよい。
- `.gch` は作ったときとフラグが違うと使えないので、フラグのハッシュごとにディレクトリを分ける。
- `#include <bits/stdc++.h>` がファイルの最初の `#include` でないと使われない（普通にコンパイルされ、遅いだけ）。
- 作れなかったときは、使わずに普通にコンパイルする。

### サンプル（`ensure_samples`・`oj_test`）

- `contests/<contest>/tests/<problem>/` に `*.in` が無ければ、`oj download` で取得する。
- `oj test -c <実行コマンド> -d <dir> -j <CPU のコア数>` で並列にテストする。

## 各タスクの詳細

### new contest

1. `https://atcoder.jp/contests/<contest>/tasks` から問題の一覧を読む。表の各行の最初のリンクの文字（「A」）を小文字にして問題名にする。online-judge-tools の `oj-api get-contest` は AtCoder の表の変更で動かなくなっているため、自前で読んでいる。
2. `contest.json` に問題の URL を保存する。
3. 問題ごとに、`config.NEW_CONTEST_LANGUAGES` の言語の解答ファイルを `templates/main.*` から作り（既にあれば作らない）、サンプルを `oj download` で取得する（既にあれば取得しない）。
4. 最初の問題をエディタで開く。

### build / build & test / build & test release / run

共通処理のビルドのあと、それぞれ何もしない／サンプルでテスト／release でビルドしてテスト／`input.txt` を標準入力にして実行する。release は debug ビルドをせず、デバッグの対象（`build/debug/current`）も変えない。run は、開いているファイルが解答・サンプル・stress のどれでもないとき（`input.txt` を編集中など）、`build/current.json` の解答（最後に debug ビルドしたもの）を実行する（`parse_path(..., use_current=True)`）。

### submit

debug ビルドしてサンプルでテストし、すべて通ったときだけ、提出ページ `https://atcoder.jp/contests/<contest>/submit?taskScreenName=<task>`（問題を選んだ状態）をブラウザで開き、選ぶ言語（`config.LANGUAGE_NAMES`）を表示する。

- 提出そのものはブラウザで行う。AtCoder の提出フォームには Cloudflare Turnstile があり、ブラウザが作るトークン（`cf-turnstile-response`）が無いと提出できないため。online-judge-tools の `oj submit` も、これに加えて問題ページのメモリ制限（`1024 MiB`）を読めずに失敗する（[oj#939](https://github.com/online-judge-tools/oj/issues/939)）。
- ブラウザは Python の `webbrowser` で開く。Dev Container では VS Code が環境変数 `BROWSER` を設定しているので、ホストのブラウザで開く。
- 同じ理由でログインも不要になったため、ログインのタスクは無い（ブラウザでログインしておけばよい）。

### stress: init / hack / test

[stress_test.md](stress_test.md) を参照。

- init：`stress/<problem>/` に `gen.py`・`naive.py` の雛形を作る（上書きしない）。
- hack：解答を debug ビルドしたあと、`stress/<problem>/` で `oj generate-input -d test -j <コア数> --hack-actual <解答> --hack-expected "python3.13 naive.py" "python3.13 gen.py"` を実行する。見つけた反例（一番新しい `test/hack-*.in`）を `input.txt` にコピーし、正しい出力を表示する。
- test：`test/` のケースで `oj test` を実行する。

### visualize graph

`input.txt` を読み、Graphviz で `graph.png` を出力して開く。1 行目が `N` なら木、`N M` なら M 本の辺のグラフとして読み、辺の行の 3 列目は重みとして表示する。

## デバッグ（`.vscode/launch.json`）

`launch.json` はタスクで書き換えず、固定のまま使う。

- **Debug C++**：`build/debug/current`（最後に debug ビルドした問題）を gdb で実行し、`input.txt` を標準入力にする。
- **Debug Python**：`scripts/debug_python.py` が、ファイル記述子 0 を `input.txt` に付け替えてから、開いている `.py` を実行する（debugpy には標準入力を切り替える設定が無いため）。`.py` 以外を開いているときは、`build/current.json` の解答を実行する。

## 環境（`.devcontainer/`）

| 要件 | 実現している場所 |
| --- | --- |
| AtCoder と同じ GCC 15.2.0・CPython 3.13.7・PyPy 3.11・ac-library v1.6 | `Dockerfile` |
| ツールを、コンテナを作るたびに入れ直さない | `Dockerfile`（イメージのレイヤーにキャッシュ） |
| ビルド成果物を Windows ホストの bind mount に置かない | `devcontainer.json` の `mounts`（`build/` を名前付きボリューム `atcoder-cpp-py-build` に） |
| gdb と AddressSanitizer が動く | `devcontainer.json` の `runArgs`（`SYS_PTRACE`・`seccomp=unconfined`） |
| メモリリークを RE にしない | `Dockerfile` の `ASAN_OPTIONS=detect_leaks=0` |

- ベースは Ubuntu 26.04。apt の `g++` が GCC 15.2、`pypy3` が PyPy 7.3.20（Python 3.11）で、AtCoder と同じなので、apt からそのまま入れる。boost は apt の 1.90（AtCoder は 1.88）。
- CPython は uv で入れ、`~/.venv`（venv）に `requirements.txt` のライブラリを入れて PATH の先頭に置く（`VIRTUAL_ENV` も設定するので、`uv pip install` でライブラリを足せる）。そのため、コンテナ内の `python3` は AtCoder と同じ CPython 3.13 になる（スクリプトもこれで動く）。
- uv で入れるものは、`vscode` ユーザーで既定の場所（`~/.local`）に入れる。root で入れると、置き場所の指定や所有者の変更が必要になるため。
- online-judge-tools は `uv tool` で入れる（`~/.local/bin/oj`）。`distutils` を使うため、Python 3.12 以降では `setuptools` を一緒に入れないと起動しない。
- `postCreateCommand.bash` は、`input.txt`・`contests/` の作成と、ボリュームの所有者の変更だけを行う。

## online-judge-tools について

online-judge-tools（`oj`）は 2022 年を最後に更新が止まっていて、AtCoder の変更に追いついていない。この環境では、動く機能だけを使っている。

| 機能 | 状態 | この環境での扱い |
| --- | --- | --- |
| `oj download`（サンプルの取得） | 動く | 使う |
| `oj test`（テスト） | 動く（手元で実行するだけ） | 使う |
| `oj generate-input`（ランダムテスト） | 動く（手元で実行するだけ） | 使う |
| `oj-api get-contest`（問題の一覧） | メモリ制限の `MiB` 表記を読めず失敗する | `new_contest.py` で自前で読む |
| `oj submit`（提出） | 同上。加えて提出フォームの Turnstile で提出できない | ブラウザで提出する（submit タスクがページを開く） |
| `oj login`（ログイン） | ログイン画面の Turnstile で失敗する | 不要（提出をブラウザで行うため） |

`oj download` も AtCoder のページの変更で動かなくなったら、サンプルの取得も `new_contest.py` と同じように自前で読む形に置き換える。

## CI（`.github/workflows/check_environment.yml`）

`devcontainers/ci` で devcontainer と同じイメージをビルドし、その中で `.github/ci/check.bash` を実行する。C++（debug・release・2 回目にビルドしないこと）と Python のテスト、PyPy、run、ランダムテスト（わざと間違える `b.cpp` の反例が見つかるか）、グラフの可視化を確かめる。AtCoder に接続する new contest は、失敗しても警告だけにする。
