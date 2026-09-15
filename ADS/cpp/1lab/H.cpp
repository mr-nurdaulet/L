#include <iostream>
#include <vector>
#include <stack>
using namespace std;

int main(){
    int n,x;
    cin >> n;
    stack<int> s;
    for(int i=0;i<n;i++){
        cin >> x ;
        while(!s.empty() && s.top()>=x){
            s.pop();
        }
        if(s.empty()){
            cout << -1 << " ";
        } else {
            cout << s.top() << " ";
        }
        s.push(x);
    }
    return 0 ;
}