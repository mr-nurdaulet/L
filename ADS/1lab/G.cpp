#include <iostream>
#include <string>
using namespace std;

int main(){
    string st , s = ""; 
    cin >> st ;
    for(char c:st){
        if(!s.empty() &&  s.back()==c){
            s.pop_back();
        } else {
            s.push_back(c);
        }
    }
    if(s.empty()){
        cout << "Yes" << endl;
    } else {
        cout << "No" << endl;
    }   


    return 0 ;
}