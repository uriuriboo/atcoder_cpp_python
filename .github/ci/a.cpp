// CI 用（.github/ci/check.bash）。ac-library と gmp が使えるかも確かめる
#include <bits/stdc++.h>
#include <atcoder/dsu>
#include <gmpxx.h>
using namespace std;

int main() {
    long long a, b;
    cin >> a >> b;
    atcoder::dsu d(2);
    d.merge(0, 1);
    mpz_class sum = mpz_class(to_string(a)) + mpz_class(to_string(b));
    cout << (d.same(0, 1) ? sum.get_str() : "-1") << '\n';
}
