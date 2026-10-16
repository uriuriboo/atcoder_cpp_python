# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## このリポジトリについて

AtCoder の問題を C++ と Python で解くための VS Code devcontainer 環境。アプリケーションではなくテンプレート兼作業場所であり、解答（`contests/`）、ビルド成果物（`build/`）、`input.txt`、`graph.png` は gitignore 対象でローカルで生成される。姉妹リポジトリの atcoder_rust（cargo-compete 版）と同じ機能を、online-judge-tools（`oj`）と自前のスクリプトで実現している。

すべて devcontainer 内で動かす前提（g++ 15・`/opt/ac-library`・`python3.13`・`pypy3`・`oj` が必要）。スクリプトはリポジトリの場所を `scripts/common.py` の位置から求めるので、パスはハードコードしていない。

## よく使うコマンド

```bash
python3 scripts/new_contest.py abc325                    # 問題一覧を取得し、解答ファイルとサンプルを用意
python3 scripts/build.py contests/abc325/a.cpp           # debug ビルド（.py は構文チェック）
python3 scripts/test.py contests/abc325/a.cpp            # debug ビルド + サンプルテスト
python3 scripts/test.py --release contests/abc325/a.cpp  # AtCoder と同じフラグでビルド + テスト
python3 scripts/run.py contests/abc325/a.cpp             # input.txt を標準入力にして実行
python3 scripts/submit.py contests/abc325/a.cpp          # テストが通れば提出ページをブラウザで開く
python3 scripts/stress.py <init|hack|test> contests/abc325/a.cpp
bash .github/ci/check.bash                               # CI と同じ確認（devcontainer 内で）
```

普段の操作は `.vscode/tasks.json` のタスクで行う前提で、タスクは開いているファイル（`${file}`）を引数にこれらのスクリプトを呼ぶ。よく使うタスクは拡張機能 actboy168.tasks でステータスバーのボタンにしている（各タスクの `options.statusbar`。`hide: true` は出さない）。run だけは、解答以外のファイルを開いているとき `build/current.json`（最後に debug ビルドした解答）を使う。

## 主な構成

- `scripts/config.py`：コンパイルオプション（debug はサニタイザ付き、release は AtCoder と同じ）、Python のテスト・提出言語（`PYTHON_LANG`）、提出ページで選ぶ言語名、new contest で作る言語。AtCoder の言語環境が更新されたら、ここと `.devcontainer/Dockerfile`・`requirements.txt` をまとめて更新する。
- `scripts/common.py`：パスの解析（`contests/<contest>/<problem>.{cpp,py}`、`stress/<problem>/`・`tests/<problem>/` 配下も可）、C++ のコンパイル（`build/<profile>/<contest>/<problem>`、`.cmd` による再ビルドの省略、`bits/stdc++.h` のプリコンパイルヘッダ）、サンプルの取得と `oj test`。
- `scripts/new_contest.py`：`oj-api get-contest` は AtCoder の HTML 変更で壊れているため、タスク一覧ページを自前で正規表現で読む。問題の URL は `contests/<contest>/contest.json` に保存し、テスト・提出で使う。
- online-judge-tools は更新が止まっていて（2022 年が最後）、`oj submit`・`oj login`・`oj-api` は AtCoder で動かない。使うのは `oj download`・`oj test`・`oj generate-input` だけ。AtCoder の提出フォームには Cloudflare Turnstile があり CLI から提出できないので、`scripts/submit.py` はテスト後に提出ページをブラウザで開くだけ（ログインの仕組みも持たない）。詳細は `docs/tasks.md` の「online-judge-tools について」。
- デバッグ：`.vscode/launch.json` は固定。"Debug C++" は `build/debug/current`（debug ビルドのたびに張り替えるシンボリックリンク）を実行し、"Debug Python" は `scripts/debug_python.py` 経由で `${file}`（.py 以外なら `build/current.json` の解答）を実行する。どちらも `input.txt` が標準入力。
- `.devcontainer/Dockerfile`：Ubuntu 26.04（apt の g++ が GCC 15.2、pypy3 が 7.3.20 で AtCoder と同じ）、ac-library v1.6、uv の CPython 3.13.7 venv（`~/.venv`、PATH の先頭）、`uv tool` の online-judge-tools（setuptools 同梱。無いと distutils が無く起動しない）。uv は `vscode` ユーザーで既定の場所に入れる。`build/` は名前付きボリューム（`devcontainer.json` の `mounts`）。
- `library/cpp/`・`library/python/` はコピペ用のスニペット集、`.vscode/*.code-snippets` はエディタ用スニペット、`templates/main.*` は new contest が作る解答の雛形。
- `docs/guide.md`（利用者向けの使い方）、`docs/tasks.md`（タスクと環境の仕組み）、`docs/stress_test.md`（ランダムテスト）。タスクや機能を変えたら合わせて更新する。

## CI

`.github/workflows/check_environment.yml` は `devcontainers/ci` で devcontainer のイメージをビルドし、その中で `.github/ci/check.bash` を実行する。ドキュメント（`*.md`・`docs/`）だけの変更では動かない。
