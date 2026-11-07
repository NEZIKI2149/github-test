#include <bits/stdc++.h>
#include <atcoder/dsu>
using namespace std;

// 入力: N Q、続いてQ個の t a b (頂点は0始まり)
// t=0: aとbを結合。t=1: 同じグループなら1、違えば0を出力
int main(){
    int N, Q;
    cin >> N >> Q;
    atcoder::dsu D(N);
    for(int i = 0;i < Q;i++){
        int t, a, b;
        cin >> t >> a >> b;
        if(t == 0){
            D.merge(a, b);
        }
        else{
            cout << D.same(a, b) << endl;
        }
    }
}
