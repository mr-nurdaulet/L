#include <iostream> 
using namespace std;

int main(){
    long long  a , n , m , res=1 ; 
    cin >> a >> n >> m;
    a%=m;
    if (m==1){
        cout << 0 << endl;
        return 0;
    }
    while(n>0){

        if(n%2==1){
            res=(res*a)%m;
            n-=1;
        }
        else{
            a*=a;
            a%=m;
            n/=2;
        }
    }
    cout << res << endl;
    return 0;
}