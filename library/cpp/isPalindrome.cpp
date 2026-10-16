#include <bits/stdc++.h>
using namespace std;

// 回文か（前半と、後ろから読んだ前半が一致するか）。O(|s|)
bool ispal(const string& s) {
    return equal(s.begin(), s.begin() + s.size() / 2, s.rbegin());
}
