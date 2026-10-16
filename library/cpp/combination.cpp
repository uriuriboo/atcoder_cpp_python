#include <bits/stdc++.h>
#include <atcoder/modint>
using namespace std;
using mint = atcoder::modint998244353;

// nCr を mod 998244353 で求める。階乗とその逆元を O(n) で前計算し、1 回 O(1)
// 使い方: Combination C(200000); C(5, 2).val() == 10
struct Combination {
    vector<mint> fact, inv_fact;

    Combination(int n) : fact(n + 1), inv_fact(n + 1) {
        fact[0] = 1;
        for (int i = 1; i <= n; i++) fact[i] = fact[i - 1] * i;
        inv_fact[n] = fact[n].inv();
        for (int i = n; i > 0; i--) inv_fact[i - 1] = inv_fact[i] * i;
    }

    mint operator()(int n, int r) const {
        if (r < 0 || r > n) return 0;
        return fact[n] * inv_fact[r] * inv_fact[n - r];
    }
};

// mod を取らない nCr。r が小さいとき用。O(r)
// res は常に nC(i+1) なので、割り算は割り切れる。結果が long long に収まらないとオーバーフローする
long long nCr_naive(long long n, int r) {
    long long res = 1;
    for (int i = 0; i < r; i++) res = res * (n - i) / (i + 1);
    return res;
}
