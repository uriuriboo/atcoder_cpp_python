# CI 用（.github/ci/check.bash）。CPython ではライブラリが使えるかも確かめる（PyPy には入れていない）
import sys

if sys.implementation.name == "cpython":
    import numpy as np
    from sortedcontainers import SortedList

    assert SortedList([2, 1])[0] == 1 and np.int64(1) == 1

A, B = map(int, input().split())
print(A + B)
