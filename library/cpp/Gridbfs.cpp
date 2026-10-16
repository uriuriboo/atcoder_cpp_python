#include <bits/stdc++.h>
using namespace std;

// グリッドの BFS：'#' のマスは通れない。上下左右に動く
// s から g（どちらも (行, 列)）への最短距離を返す。たどり着けなければ -1。O(HW)
int bfs(pair<int, int> s, pair<int, int> g, const vector<string>& c) {
    int H = c.size(), W = c[0].size();
    const int dx[4] = {1, 0, -1, 0}, dy[4] = {0, 1, 0, -1};
    vector d(H, vector<int>(W, -1));  // まだ来ていないマスは -1
    queue<pair<int, int>> que;
    d[s.first][s.second] = 0;
    que.push(s);
    while (!que.empty()) {
        auto [x, y] = que.front();
        que.pop();
        for (int i = 0; i < 4; i++) {
            int nx = x + dx[i], ny = y + dy[i];
            if (nx < 0 || nx >= H || ny < 0 || ny >= W) continue;
            if (c[nx][ny] == '#' || d[nx][ny] != -1) continue;
            d[nx][ny] = d[x][y] + 1;
            que.emplace(nx, ny);
        }
    }
    return d[g.first][g.second];
}
