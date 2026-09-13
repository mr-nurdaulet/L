#include <iostream>
#include <string>
#include <queue>
using namespace std;

void procces(){
    int n;
    cin >> n ;

    int freq[26] = {0};
    queue<char> q;
    for(int i = 0 ; i < n ; i++){
        char c;
        cin >> c;
        freq[c - 'a']++;
        q.push(c);

        while(!q.empty() && freq[q.front() - 'a'] > 1){
            q.pop();
        }

        if(q.empty()){
            cout << -1 << endl;
        }else{
            cout << q.front() << endl;
        }
        if(i < n - 1){
            cout << " ";
        }
        cout<< endl;
    }
}

int main() {
    int T;
    cin >> T;
    while(T--){
        procces();
    }
    return 0;
}