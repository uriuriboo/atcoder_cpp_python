#include <bits/stdc++.h>
using namespace std;

// ナップサック問題：重さ w[i]・価値 v[i] の品物を、重さの合計が W 以下になるように選び、価値の合計を最大にする。O(NW)
// dp[j] = 重さの合計 j 以下での価値の合計の最大値

// 各品物を 1 個まで使う（0-1 ナップサック）
long long knapsack01(int W, const vector<int>& w, const vector<long long>& v) {
    vector<long long> dp(W + 1, 0);
    for (int i = 0; i < (int)w.size(); i++) {
        // 重さの大きい方から更新すると、同じ品物を 2 回使わない
        for (int j = W; j >= w[i]; j--) dp[j] = max(dp[j], dp[j - w[i]] + v[i]);
    }
    return dp[W];
}

// 各品物を何個でも使える（個数制限なし）
long long knapsack_unbounded(int W, const vector<int>& w, const vector<long long>& v) {
    vector<long long> dp(W + 1, 0);
    for (int i = 0; i < (int)w.size(); i++) {
        // 重さの小さい方から更新すると、同じ品物を何回でも使える
        for (int j = w[i]; j <= W; j++) dp[j] = max(dp[j], dp[j - w[i]] + v[i]);
    }
    return dp[W];
}
