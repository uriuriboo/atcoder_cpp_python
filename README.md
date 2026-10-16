# AtCoder C++ / Python

VS Code で Dev Container として開くだけで、AtCoder の提出環境に合わせた C++ と Python の開発環境ができます。問題の取得からテスト・デバッグ・提出まで、タスクランナーから行います。

できること・便利な点・コンテストでの使い方は[使い方ガイド](docs/guide.md)にまとめています。

## 用意されるもの

AtCoder の 2025 年 10 月の言語環境に合わせています。

- C++23（GCC 15.2.0）と ac-library v1.6、gmp、boost
- Python（CPython 3.13.7）と、AtCoder と同じバージョンのライブラリ（numpy、scipy、networkx、sortedcontainers、ac-library-python など。`requirements.txt`）
- PyPy 3.11（v7.3.20）
- online-judge-tools（サンプルの取得・テスト・ランダムテスト）
- gdb（C++ のデバッグ）、Graphviz（グラフ可視化）

## タスクランナーでできること

解答ファイル（`contests/abc325/a.cpp` など）を開いた状態で実行すると、ファイルの場所から解いている問題を自動で判定します。C++ と Python は拡張子で判定します。よく使うタスク（new contest・test・release・run・submit）は、画面下のステータスバーのボタンから 1 クリックで実行できます。

| タスク | 内容 |
| --- | --- |
| new contest | コンテスト ID（`abc325` など）を入力すると、問題ごとの解答ファイルとサンプルを用意 |
| build | 開いている問題だけをビルド（Python は構文チェック） |
| build & test | 開いている問題をビルドして、サンプルでテスト |
| build & test release | AtCoder と同じ最適化でビルドしてテスト（実行時間の確認用） |
| run (input.txt) | `input.txt` を入力にして実行 |
| submit | サンプルでテストし、通ったら提出ページ（問題を選んだ状態）をブラウザで開く |
| stress: init / hack / test | ランダムな入力で愚直解と比べ、サンプル以外の反例を探す（[使い方](docs/stress_test.md)） |
| visualize graph | `input.txt` のグラフを画像（`graph.png`）にして表示。有向グラフ用の「visualize graph (directed)」もあります |

AtCoder の提出フォームには CAPTCHA（Cloudflare Turnstile）があり、コマンドラインからは提出できません。提出はブラウザで行います。

## 便利にしている点

- **バグを実行時エラーとして見つける**：debug ビルドでは、配列の範囲外アクセスや符号付き整数のオーバーフローを、その場で RE として止めます（AddressSanitizer・UndefinedBehaviorSanitizer・`_GLIBCXX_DEBUG`）
- **ビルドが速い**：`bits/stdc++.h` を初回にプリコンパイルし、2 回目以降のコンパイルを速くしています。ソースが変わっていなければビルドし直しません
- **サンプルテストを並列実行**：CPU のコア数だけ同時に実行します
- **すぐにデバッグできる**：最後にビルドした問題が F5 のデバッグ対象になります。`input.txt` に入力を書いて F5 を押すだけです
- **反例を自動で探せる**：サンプルは通るのに WA のとき、ランダムな入力で愚直解と比べ、見つけた反例を `input.txt` に入れます
- **エディタの補助**：C++ は保存時に clang-format で、Python は Ruff でフォーマットします。補完は AtCoder と同じライブラリが入った環境で効きます。スニペット（`tmplt` でテンプレートなど）も使えます
- **ライブラリ**：`library/cpp/`・`library/python/` にコピペ用のコードがあります

## フォルダ構成

```text
.
├── .devcontainer/   コンテナの設定（Dockerfile にツールをすべて入れる）
├── .vscode/         タスク・デバッグ・スニペットの設定
├── contests/        解答（gitignore 対象）。new contest で作られる
├── docs/            使い方ガイドなど
├── library/         コピペ用のライブラリ（cpp/・python/）
├── scripts/         タスクが呼ぶスクリプト。設定は scripts/config.py
├── templates/       解答ファイルの雛形（main.cpp・main.py）
└── requirements.txt CPython に入れるライブラリ
```

## はじめかた

1. Docker（Windows・Mac は Docker Desktop）と、VS Code の拡張機能「Dev Containers」を入れる。
2. このリポジトリを clone して VS Code で開き、「コンテナーで再度開く」（Reopen in Container）を選ぶ。初回はイメージのビルドに数分かかる。

詳しくは[使い方ガイド](docs/guide.md)を参照してください。
