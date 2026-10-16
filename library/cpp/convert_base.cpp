#include <bits/stdc++.h>
using namespace std;

// 0 以上の整数 x を、base 進数（2〜36）の文字列にする。10 以上の桁は A, B, ... で表す
// 逆に base 進数の文字列 s を整数にするときは、標準の stoll(s, nullptr, base)
// 2 進数の文字列をそのまま 10 進の数として扱いたいときは stoll(convert_base(x, 2))
string convert_base(long long x, int base) {
    if (x == 0) return "0";
    const string digits = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ";
    string s;
    while (x > 0) {
        s += digits[x % base];
        x /= base;
    }
    reverse(s.begin(), s.end());
    return s;
}
