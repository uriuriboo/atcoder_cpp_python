// CI 用（.github/ci/check.bash）。a == b のときだけ間違える。ランダムテストで反例が見つかるかを確かめる
#include <bits/stdc++.h>
using namespace std;

int main() {
    int a, b;
    cin >> a >> b;
    cout << (a == b ? 0 : a + b) << '\n';
}
