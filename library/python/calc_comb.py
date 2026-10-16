# 二項係数 nCr
# mod を取らないときは、標準の math.comb(n, r) を使う（Python 3.8 以降）
# mod を取るときは、階乗とその逆元を前計算しておき、1 回 O(1) で求める
MOD = 998244353
N = 2 * 10**5  # n の最大値

fact = [1] * (N + 1)  # fact[i] = i! % MOD
for i in range(1, N + 1):
    fact[i] = fact[i - 1] * i % MOD
inv_fact = [1] * (N + 1)  # inv_fact[i] = (i!)^-1 % MOD
inv_fact[N] = pow(fact[N], MOD - 2, MOD)
for i in range(N, 0, -1):
    inv_fact[i - 1] = inv_fact[i] * i % MOD


def cmb(n, r):
    if r < 0 or r > n:
        return 0
    return fact[n] * inv_fact[r] % MOD * inv_fact[n - r] % MOD
