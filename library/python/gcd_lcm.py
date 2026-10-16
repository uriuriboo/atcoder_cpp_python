# 最大公約数・最小公倍数は、標準の math で求められる（Python 3.9 以降。引数はいくつ渡してもよい）
from math import gcd, lcm

A = [12, 18, 30]
print(gcd(*A), lcm(*A))  # 6 180
