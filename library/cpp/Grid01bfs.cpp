#include <bits/stdc++.h>
using namespace std;

// グリッドの 0-1 BFS：'#' のマスに入るとコスト 1、それ以外のマスはコスト 0 で、上下左右に動く（壁を壊す回数など）
// s から g（どちらも (行, 列)）への最小コストを返す。O(HW)
int bfs01(pair<int, int> s, pair<int, int> g, const vector<string>& c) {
    int H = c.size(), W = c[0].size();
    const int dx[4] = {1, 0, -1, 0}, dy[4] = {0, 1, 0, -1};
    const int INF = 1e9;
    vector d(H, vector<int>(W, INF));
    deque<pair<int, int>> que;
    d[s.first][s.second] = 0;
    que.push_back(s);
    while (!que.empty()) {
        auto [x, y] = que.front();
        que.pop_front();
        for (int i = 0; i < 4; i++) {
            int nx = x + dx[i], ny = y + dy[i];
            if (nx < 0 || nx >= H || ny < 0 || ny >= W) continue;
            int cost = c[nx][ny] == '#' ? 1 : 0;
            // 先に見つけたときより小さいコストで行けたら、更新し直す（見つけた時点では確定しない）
            if (d[x][y] + cost < d[nx][ny]) {
                d[nx][ny] = d[x][y] + cost;
                // コスト 0 の移動は先頭、コスト 1 の移動は末尾に入れると、キューがコストの小さい順に並ぶ
                if (cost == 0) {
                    que.emplace_front(nx, ny);
                } else {
                    que.emplace_back(nx, ny);
                }
            }
        }
    }
    return d[g.first][g.second];
}
