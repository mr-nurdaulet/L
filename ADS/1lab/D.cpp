#include <iostream>
#include <vector>
using namespace std;

bool isPrime(long long a){
    if(a<2){
        return false;
    }
    for(int i=2; i*i <= a; i++){
        if(a%i==0){
            return false;
        }
    }
    return true;
}
int main(){
    long long n;
    vector<long long> a;
    cin >> n;
    long long current = 2;
    while (a.size() < n) {
        if (isPrime(current)) {
            a.push_back(current);
        }
        current++;
    }
     cout << a[n-1] << endl;
    
    return 0;
}