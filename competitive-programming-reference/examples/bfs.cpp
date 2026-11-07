#include <bits/stdc++.h>
using namespace std;

// 入力: N M、続いてM本の無向辺 a b (頂点は1始まり)。N >= 1
// 出力: 頂点1から各頂点への最短距離。到達不可は-1
int main(){
    int N, M;
    cin >> N >> M;
    vector<vector<int>> G(N);
    for(int i = 0;i < M;i++){
        int a, b;
        cin >> a >> b;
        a--; b--;
        G.at(a).push_back(b);
        G.at(b).push_back(a);
    }
    vector<int> dist(N, -1);
    queue<int> Q;
    dist.at(0) = 0;
    Q.push(0);
    while(!Q.empty()){
        int v = Q.front();
        Q.pop();
        for(int i = 0;i < (int)G.at(v).size();i++){
            int to = G.at(v).at(i);
            if(dist.at(to) != -1){
                continue;
            }
            dist.at(to) = dist.at(v)+1;
            Q.push(to);
        }
    }
    for(int i = 0;i < N;i++){
        cout << dist.at(i) << endl;
    }
}
