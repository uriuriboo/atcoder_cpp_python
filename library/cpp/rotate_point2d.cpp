#include <bits/stdc++.h>
using namespace std;

// 点 (x, y) を、点 (cx, cy) を中心に反時計回りに th ラジアン回転した点
// 度で回すときは th = deg * numbers::pi / 180
pair<double, double> rotate_point(double x, double y, double cx, double cy, double th) {
    double dx = x - cx, dy = y - cy;
    return {cx + dx * cos(th) - dy * sin(th), cy + dx * sin(th) + dy * cos(th)};
}
