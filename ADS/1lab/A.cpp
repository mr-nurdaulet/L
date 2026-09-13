#include <iostream>
#include <numeric>
using namespace std;

long long fGCD(long long a, long long b) {
    while (b != 0) {
        long long c = b;
        b = a % b;
        a = c;
    }
    return a;
}

int main(){
        long long a,b;
        cin >> a >> b;
        long long ans = gcd(a,b);
        cout << ans << endl;

    return 0;
}