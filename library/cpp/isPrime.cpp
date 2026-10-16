#include <bits/stdc++.h>
using namespace std;

// n が素数か。O(√n)
bool isPrime(long long n) {
    if (n < 2) return false;
    for (long long i = 2; i * i <= n; i++) {
        if (n % i == 0) return false;
    }
    return true;
}
