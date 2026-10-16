#include <bits/stdc++.h>
using namespace std;

// a を b で更新したら true を返す
// 型を 2 つに分けているので、chmin(ll の変数, 0) のように型が違っても使える
template <class T, class U>
bool chmin(T& a, const U& b) {
    if (b < a) {
        a = b;
        return true;
    }
    return false;
}

template <class T, class U>
bool chmax(T& a, const U& b) {
    if (a < b) {
        a = b;
        return true;
    }
    return false;
}
