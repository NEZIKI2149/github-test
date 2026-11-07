#include <bits/stdc++.h>
using namespace std;

// 入力: K (1 <= K <= 10^18)
// 出力: x*x >= K となる最小の非負整数x
int main(){
    long long K;
    cin >> K;
    long long ng = 0;
    long long ok = K;
    while(ok-ng > 1){
        long long mid = ng + (ok-ng)/2;
        long long required = K/mid + (K % mid != 0);
        if(mid >= required){
            ok = mid;
        }
        else{
            ng = mid;
        }
    }
    cout << ok << endl;
}
