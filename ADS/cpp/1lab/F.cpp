#include <iostream>
#include <string>
using namespace std;

string process(string s){
    string res = "";

    for(char c:s){
        if(c=='#'){
            if(!res.empty()){
                res.pop_back();
            }
        } else {
            res.push_back(c);
        }
    }
    return res;
}


int main(){
    string s1,s2;
    cin >> s1 >> s2;
    if(process(s1)==process(s2)){
        cout << "Yes" << endl;
    } else {
        cout << "No" << endl;
    }
    return 0 ;
} 
