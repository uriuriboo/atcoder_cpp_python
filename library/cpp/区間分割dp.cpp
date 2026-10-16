#include <bits/stdc++.h>
using namespace std;

// 区間分割 DP：長さ n の列をいくつかの区間に分けるとき、区間のコストの合計の最小値。O(n^2)
// c[i][j] = 区間 [j, i) を 1 つの区間にするコスト（0 <= j < i <= n）。c は (n+1)×(n+1)
long long split_dp(const vector<vector<long long>>& c) {
    int n = c.size() - 1;
    const long long INF = 1e18;
    vector<long long> dp(n + 1, INF);  // dp[i] = 先頭 i 個を分けたときの最小コスト
    dp[0] = 0;
    for (int i = 1; i <= n; i++) {
        for (int j = 0; j < i; j++) dp[i] = min(dp[i], dp[j] + c[i][j]);  // 最後の区間が [j, i)
    }
    return dp[n];
}
