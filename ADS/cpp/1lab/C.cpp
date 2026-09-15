#include <iostream> 
#include <cmath>
using namespace std;

int main(){
    long long  a ;
    cin >> a;
    if(a<2){
        cout << "NO" << endl;
        return 0;
    }
    for(int i=2; i*i <= a; i++){
        if(a%i==0){
            cout << "NO" << endl;
            return 0;
        }
    }
    cout << "YES" << endl;
    return 0;
}