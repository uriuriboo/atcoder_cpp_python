#include <bits/stdc++.h>
using namespace std;
using ll = long long;

// G[v] = {(行き先, 重み), ...}。頂点は 0 始まり
using Graph = vector<vector<pair<int, ll>>>;
const ll INF = 1e18;

// ダイクストラ法：s から各頂点への最短距離。たどり着けない頂点は INF。O((V + E) log V)
// 重みが負の辺があると正しく求まらない
vector<ll> dijkstra(int s, const Graph& G) {
    vector<ll> dist(G.size(), INF);
    // (距離, 頂点) を距離の小さい順に取り出す
    priority_queue<pair<ll, int>, vector<pair<ll, int>>, greater<>> que;
    dist[s] = 0;
    que.emplace(0, s);
    while (!que.empty()) {
        auto [d, v] = que.top();
        que.pop();
        if (d > dist[v]) continue;  // 取り出す前に、もっと短い距離で更新済み
        for (auto [to, w] : G[v]) {
            if (dist[v] + w < dist[to]) {
                dist[to] = dist[v] + w;
                que.emplace(dist[to], to);
            }
        }
    }
    return dist;
}
