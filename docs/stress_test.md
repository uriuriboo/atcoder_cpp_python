# ランダムテスト（stress）の使い方

サンプルは通るのに WA になるときに、ランダムな入力で自分の解答と愚直解を比べて、答えが食い違う入力（反例）を探す。online-judge-tools（`oj`）の `generate-input` を使う。

## 用意するもの

問題ごとに、次の 2 つを Python で書く。解答が C++ でも Python でも、この 2 つは Python で書く。

| ファイル | 役割 |
| --- | --- |
| `gen.py` | 入力を 1 ケース分作り、標準出力に書き出す |
| `naive.py` | 愚直解。遅くてよいので、確実に正しい方法で解く |

置き場所は `contests/<contest>/stress/<problem>/`。

```text
contests/abc325/
├── a.cpp               解答
└── stress/a/
    ├── gen.py
    ├── naive.py
    └── test/           見つけた反例がたまる
        ├── hack-000.in
        └── hack-000.out
```

## 手順

stress のタスクは、ほかのタスク（build & test など）と同じように、解きたい問題のファイルを開いた状態で実行する。`a.cpp`・`a.py`・`gen.py`・`naive.py` のどれを開いていても、同じ問題として扱われる。

### 1. 雛形を作る（stress: init）

`a.cpp` を開いて「stress: init」を実行すると、`stress/a/gen.py` と `stress/a/naive.py` の雛形ができる。既にあるファイルは上書きしない。

### 2. gen.py と naive.py を書く

例：「N 個の整数 A から異なる 2 つを選んだときの和の最大値」を求める問題。

`gen.py`

```python
import random

N = random.randint(2, 5)
A = [random.randint(-10, 10) for _ in range(N)]
print(N)
print(*A)
```

`naive.py`

```python
N = int(input())
A = list(map(int, input().split()))
print(max(A[i] + A[j] for i in range(N) for j in range(i + 1, N)))
```

### 3. 反例を探す（stress: hack）

「stress: hack」を実行すると、次のことを行う。

1. 解答を debug ビルドする（C++。デバッグの対象もこの問題に切り替わる）。
2. `gen.py` で入力を作り、解答と `naive.py` に与えて出力を比べる。食い違うか、解答が実行時エラーになるまで、CPU のコア数だけ並列に繰り返す。
3. 反例を `test/hack-XXX.in` に、`naive.py` の出力を `test/hack-XXX.out` に保存する。
4. 反例を `input.txt` にコピーし、正しい出力をターミナルに表示する。

C++ の debug ビルドは範囲外アクセスなどを実行時エラーにするので、出力が合っていても、そうしたバグのある入力も反例として見つかる。反例がなかなか見つからないときは、Ctrl+C で止める。

### 4. デバッグする

反例は `input.txt` に入っているので、そのまま F5 でデバッグできる（「Debug C++」か「Debug Python」）。直したら、もう一度「stress: hack」を実行して、ほかの反例がないか確かめる。

`gen.py` や `naive.py` もデバッグできる。開いてアクティブにし、「Debug Python」を選んで F5 を押す。標準入力は `input.txt` から読む。

### 5. これまでの反例で確認する（stress: test）

「stress: test」は、`test/` にたまった反例をすべて解答に流す。修正で前の反例が再び壊れていないかを確かめるのに使う。

## うまく使うコツ

- **値は小さくする**：N は 1〜10 程度、値も 10 程度にすると、反例を手で追える。小さい範囲でもたいていのバグは見つかる。
- **端のケースを出やすくする**：N の最小値、すべて同じ値、負の数や 0 など、制約の端が出るように範囲を決める。
- **gen.py が制約を守っているか確かめる**：制約外の入力を作ると、正しい解答でも食い違うことがある。「異なる値」「連結なグラフ」などの条件に注意する。
- **反例をやり直したいとき**：`stress/<problem>/test/` を消す。消さなければ番号が `hack-001`、`hack-002` … と増えていく。

## 使えない場面

- **答えが複数ある問題**・**小数の答え**：出力をそのまま比べるので、別の正解や誤差を食い違いとして扱う。
- **実行時間（TLE）の確認**：debug ビルドで、時間制限なしで動かしている。速さは「build & test release」で確かめる。
