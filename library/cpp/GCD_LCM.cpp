#include <bits/stdc++.h>
using namespace std;

// 2 つの数の最大公約数・最小公倍数は、標準の gcd(a, b)・lcm(a, b)（<numeric>、C++17 以降）で求められる
// lcm は a / gcd(a, b) * b の順に計算するが、結果が long long に収まらないとオーバーフローする

// 配列全体の最大公約数・最小公倍数
long long gcd_all(const vector<long long>& a) {
    long long g = 0;  // gcd(0, x) = x
    for (long long x : a) g = gcd(g, x);
    return g;
}

long long lcm_all(const vector<long long>& a) {
    long long l = 1;
    for (long long x : a) l = lcm(l, x);
    return l;
}
