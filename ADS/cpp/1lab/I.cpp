#include <iostream>
#include <queue>
using namespace std;
int main(){
   queue<int> boris, nursik;
    int moves = 0 ;

    for(int i=0;i<5;i++){
        int x;
        cin >> x ;
        boris.push(x);
    }
    for(int i=0;i<5;i++){
        int x;
        cin >> x ;
        nursik.push(x);
    }
    while(!boris.empty() && !nursik.empty()){
        int b = boris.front();
        boris.pop();
        int n = nursik.front();
        nursik.pop();

        bool boris_wins = false;
        if(b == 9 && n ==0){
            boris_wins = false;}
        else if(b==0 && n == 9){
            boris_wins = true;
        }
        else if(b > n){
            boris_wins = true;
        }

        else {
            boris_wins = false;
        }

        if(boris_wins){
            boris.push(b);
            boris.push(n);
        } else {
            nursik.push(b);
            nursik.push(n);
        }
        moves++;
    }
    if(boris.empty()){
        cout << "Nursik " << moves << endl;
    } else {
        cout << "Boris " << moves << endl;
    }
    return 0;
}