#include <bits/stdc++.h>
using namespace std;

// 編集距離：s を t にするための、1 文字の挿入・削除・置換の最小回数。O(|s||t|)
int editdistance(const string& s, const string& t) {
    int n = s.size(), m = t.size();
    vector dp(n + 1, vector<int>(m + 1));  // dp[i][j] = s の先頭 i 文字と t の先頭 j 文字の編集距離
    for (int i = 0; i <= n; i++) dp[i][0] = i;
    for (int j = 0; j <= m; j++) dp[0][j] = j;
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < m; j++) {
            dp[i + 1][j + 1] = min({dp[i][j + 1] + 1, dp[i + 1][j] + 1, dp[i][j] + (s[i] != t[j])});
        }
    }
    return dp[n][m];
}
