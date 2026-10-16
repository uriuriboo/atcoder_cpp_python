#include <bits/stdc++.h>
using namespace std;

// 素因数分解：(素因数, 個数) の組を、素因数の小さい順に返す。O(√n)
// 例: prime_fac(12) = {(2, 2), (3, 1)}
vector<pair<long long, int>> prime_fac(long long n) {
    vector<pair<long long, int>> res;
    for (long long p = 2; p * p <= n; p++) {
        if (n % p != 0) continue;
        int cnt = 0;
        while (n % p == 0) {
            n /= p;
            cnt++;
        }
        res.emplace_back(p, cnt);
    }
    if (n != 1) res.emplace_back(n, 1);  // 残りは √n より大きい素数
    return res;
}
