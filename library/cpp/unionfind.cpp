#include <bits/stdc++.h>
using namespace std;

// Union-Find（素集合データ構造）。ほぼ O(1)
// 機能を足す必要がなければ、ACL の atcoder::dsu（merge・same・leader・size・groups）でもよい
struct UnionFind {
    vector<int> d;  // 根なら -(集合の大きさ)、根でなければ親の番号

    UnionFind(int n = 0) : d(n, -1) {}

    int find(int x) { return d[x] < 0 ? x : d[x] = find(d[x]); }

    // x と y の集合をまとめる。もともと同じ集合なら false
    bool unite(int x, int y) {
        x = find(x), y = find(y);
        if (x == y) return false;
        if (d[x] > d[y]) swap(x, y);  // 大きい集合（x）に小さい集合（y）をつなぐ
        d[x] += d[y];
        d[y] = x;
        return true;
    }

    bool same(int x, int y) { return find(x) == find(y); }

    int size(int x) { return -d[find(x)]; }
};
