#include <bits/stdc++.h>
using namespace std;

// 最長共通部分列（LCS）。O(|A||B|)
// dp[i][j] = A の先頭 i 文字と B の先頭 j 文字の LCS の長さ
vector<vector<int>> lcs_table(const string& A, const string& B) {
    int a = A.size(), b = B.size();
    vector dp(a + 1, vector<int>(b + 1, 0));
    for (int i = 0; i < a; i++) {
        for (int j = 0; j < b; j++) {
            dp[i + 1][j + 1] = A[i] == B[j] ? dp[i][j] + 1 : max(dp[i + 1][j], dp[i][j + 1]);
        }
    }
    return dp;
}

// LCS の長さ
int lcs(const string& A, const string& B) {
    return lcs_table(A, B)[A.size()][B.size()];
}

// LCS を 1 つ復元する
string lcsmake(const string& A, const string& B) {
    auto dp = lcs_table(A, B);
    string res;
    int i = A.size(), j = B.size();
    while (i > 0 && j > 0) {
        if (dp[i][j] == dp[i][j - 1]) {
            j--;
        } else if (dp[i][j] == dp[i - 1][j]) {
            i--;
        } else {
            res += A[i - 1];
            i--, j--;
        }
    }
    reverse(res.begin(), res.end());  // 後ろから集めたので反転する
    return res;
}
