#include <iostream>
#include <deque>

using namespace std;
void solve(){
    int n ;
    cin >> n ;


    deque<int> dq;

    for(int i = n ; i >= 1 ; i--){
        dq.push_front(i);

            for(int j = 0 ; j < i ; j++){
                int x = dq.back();
                dq.pop_back();
                dq.push_front(x);
            }
            
        } 
        for(int i : dq){
            cout << i << " ";
        }
    
        cout << endl;

}

int main(){
    int n ;
    cin >> n ;

    while(n--){
        solve();
    }



    return 0;
}