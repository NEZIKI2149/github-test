# 計算量・メモリ

制約と必要な容量を確認する。

[入口へ](../README.md)

使用言語：**C++23 (GCC 15.2.0)**。ローカルのコンパイル設定は `-std=gnu++23`。

## 計算量：制約から見る候補

<div class="table-wrap"><table><thead><tr><th>入力規模</th><th>候補になる計算量</th></tr></thead><tbody><tr><td>N ≲ 10</td><td>O(N × N!)</td></tr><tr><td>N ≲ 20</td><td>O(N × 2ᴺ)</td></tr><tr><td>N ≲ 3×10³</td><td>O(N²)</td></tr><tr><td>N ≲ 2×10⁵</td><td>O(N log N)、O(N)</td></tr><tr><td>値の範囲が10⁹〜10¹⁸</td><td>二分探索・数式など。値を1ずつ列挙しない</td></tr></tbody></table></div><p class="note">制限時間・処理内容・定数倍で変わる目安。秒数の保証ではない。</p>

## 計算量計算機

<div class="table-wrap"><table><thead><tr><th>N / O(N)</th><th>N log₂N</th><th>N²</th><th>N³</th></tr></thead><tbody><tr><td>10²</td><td>6.6×10²</td><td>10⁴</td><td>10⁶</td></tr><tr><td>10³</td><td>10×10³</td><td>10⁶</td><td>10⁹</td></tr><tr><td>3×10³</td><td>3.5×10⁴</td><td>9×10⁶</td><td>2.7×10¹⁰</td></tr><tr><td>10⁴</td><td>1.3×10⁵</td><td>10⁸</td><td>10¹²</td></tr><tr><td>2×10⁵</td><td>3.5×10⁶</td><td>4×10¹⁰</td><td>8×10¹⁵</td></tr><tr><td>10⁶</td><td>2×10⁷</td><td>10¹²</td><td>10¹⁸</td></tr></tbody></table></div><div class="table-wrap"><table><thead><tr><th>N</th><th>2ᴺ</th><th>N × 2ᴺ</th><th>N!</th></tr></thead><tbody><tr><td>10</td><td>1×10³</td><td>1×10⁴</td><td>3.6×10⁶</td></tr><tr><td>15</td><td>3.3×10⁴</td><td>4.9×10⁵</td><td>1.3×10¹²</td></tr><tr><td>20</td><td>1×10⁶</td><td>2.1×10⁷</td><td>2.4×10¹⁸</td></tr><tr><td>25</td><td>3.4×10⁷</td><td>8.4×10⁸</td><td>1.6×10²⁵</td></tr><tr><td>30</td><td>1.1×10⁹</td><td>3.2×10¹⁰</td><td>2.7×10³²</td></tr></tbody></table></div><p class="note">実際のCPU命令数ではなく、計算量の式の値。文字列コピーやmap操作などは単純な加算より重い。</p>

## メモリ計算機

<p>一次元／二次元と型を選んで配列容量を計算する。vector・set・multiset・map・unordered_set・unordered_mapにも対応し、管理領域込みの推定容量を選択式のメモリ制限と比較する。</p>

## 型と配列のメモリ

<div class="table-wrap"><table><thead><tr><th>型</th><th>1要素の目安</th><th>10⁵要素</th><th>10⁶要素</th><th>10⁷要素</th></tr></thead><tbody><tr><td>char</td><td>1 B</td><td>100 KB</td><td>1 MB</td><td>10 MB</td></tr><tr><td>int</td><td>4 B</td><td>400 KB</td><td>4 MB</td><td>40 MB</td></tr><tr><td>long long / double</td><td>8 B</td><td>800 KB</td><td>8 MB</td><td>80 MB</td></tr><tr><td>pair&lt;int,int&gt;</td><td>通常8 B</td><td>約800 KB</td><td>約8 MB</td><td>約80 MB</td></tr></tbody></table></div><p class="note">この表はint=4 B、long long=8 B、double=8 Bの一般的なGCC環境を想定。実際はsizeofで確認。1 KB=10³ B、1 MB=10⁶ B。1 KiB=2¹⁰ B、1 MiB=2²⁰ B。</p>

## 二次元配列のメモリ

<div class="table-wrap"><table><thead><tr><th>H × W</th><th>要素数</th><th>int</th><th>long long / double</th></tr></thead><tbody><tr><td>10² × 10²</td><td>10⁴</td><td>40 KB</td><td>80 KB</td></tr><tr><td>10³ × 10³</td><td>10⁶</td><td>4 MB</td><td>8 MB</td></tr><tr><td>2×10³ × 2×10³</td><td>4×10⁶</td><td>16 MB</td><td>32 MB</td></tr><tr><td>3×10³ × 3×10³</td><td>9×10⁶</td><td>36 MB</td><td>72 MB</td></tr><tr><td>5×10³ × 5×10³</td><td>2.5×10⁷</td><td>100 MB</td><td>200 MB</td></tr><tr><td>10⁴ × 10⁴</td><td>10⁸</td><td>400 MB</td><td>800 MB</td></tr></tbody></table></div><p class="note">要素本体の容量。vector&lt;vector&lt;T&gt;&gt;には行ごとのvector管理領域・確保処理も加わる。大きなローカル固定長配列はスタック上限にも注意し、vectorを使う。</p>

## メモリ上限との比較

<div class="table-wrap"><table><thead><tr><th>上限</th><th>intだけで使い切る理論要素数</th><th>正方形int配列の理論最大辺長</th></tr></thead><tbody><tr><td>256 MiB</td><td>約6.7×10⁷</td><td>8192</td></tr><tr><td>512 MiB</td><td>約1.3×10⁸</td><td>11585</td></tr><tr><td>1024 MiB</td><td>約2.7×10⁸</td><td>16384</td></tr></tbody></table></div><p class="note">上限の単位がMiBの場合の理論値であり、安全な確保量ではない。実行環境・他の変数・コピー・管理領域の分を差し引く。MB表記なら10⁶ Bで計算する。</p><p>合計容量 ≈ 配列ごとの「要素数 × sizeof(型)」の合計 + 管理領域。intのN×N配列をコピーすれば本体だけで8N² B。long longのN×N累積和なら約8(N+1)² B。</p>

## 容器・グラフ・コピーの注意

<div class="table-wrap"><table><thead><tr><th>対象</th><th>見積もり</th></tr></thead><tbody><tr><td>vector&lt;T&gt;</td><td>確保済みcapacity × sizeof(T) + 管理領域。sizeだけでは正確に見積もれない</td></tr><tr><td>vector&lt;vector&lt;T&gt;&gt;</td><td>各行のcapacity × sizeof(T) + H個のvector管理領域 + 各確保の管理領域</td></tr><tr><td>map / set / multiset</td><td>ノードごとのポインタ・色などで、値本体より大きくなる。要素数×sizeof(値)だけでは不足</td></tr><tr><td>unordered_map / unordered_set</td><td>要素ノードに加え、バケット配列も必要</td></tr><tr><td>無向グラフの隣接リスト</td><td>intの行き先を通常2M個持つ。本体約8M B + N個のvectorなど</td></tr><tr><td>vector&lt;bool&gt;</td><td>一般にbit圧縮。通常のbool配列とは扱いが異なる。分かりやすさ重視ならvector&lt;char&gt;</td></tr><tr><td>関数の引数</td><td>vector&lt;int&gt; Aはコピー。const vector&lt;int&gt;&amp; Aなら読むだけで参照</td></tr><tr><td>再帰DFS</td><td>呼び出しごとのスタックも消費。深いグラフではstackなどの反復実装を検討</td></tr></tbody></table></div>

## sizeof：実際の型のサイズを確認

<p>型のサイズをB単位で出力する。sizeof(vector&lt;int&gt;)は要素本体を含まない。</p><details class="code-only"><summary>全体コードを開く</summary><pre><code>#include &lt;bits/stdc++.h&gt;
using namespace std;

int main(){
    cout &lt;&lt; sizeof(int) &lt;&lt; endl;
    cout &lt;&lt; sizeof(long long) &lt;&lt; endl;
    cout &lt;&lt; sizeof(double) &lt;&lt; endl;
    cout &lt;&lt; sizeof(vector&lt;int&gt;) &lt;&lt; endl;
    return 0;
}
</code></pre></details>
