# Rudin 第二章：定义、定理与公式清单（中英双语）

## 范围

- 教材：`papers/Rudin.md`
- 第二章标题：`FINITE, COUNTABLE, AND UNCOUNTABLE SETS`（有限集、可数集与不可数集）
- 第二章行范围：第 1309--2206 行（含 Exercises 部分，不含第 2207 行起的第三章）
- 本文件只列定义、定理、命题、公理、记号和正文中的关键公式；不附证明。
- 术语标注方式：每个术语在首次出现处给出英文原文；公式与记号本身为国际通用，不重复标注。

## 一、有限、可数与不可数集（Finite, Countable, and Uncountable Sets）

### 定义 2.1：函数（Functions）

函数（function，又称映射 mapping）$f$ 是从集合 $A$ 到集合 $B$ 的对应：对每个 $x\in A$ 关联一个 $f(x)\in B$。$A$ 称为 $f$ 的定义域（domain），$f(x)$ 称为 $f$ 的值（value），全体值组成的集合称为 $f$ 的值域（range）。

### 定义 2.2：像、原像、映上、一一映射（Images, Inverse Images, Onto, One-to-One）

- $E\subset A$ 在 $f$ 下的像（image）：
$$
f(E)=\{f(x):x\in E\}.
$$
- $f(A)$ 即 $f$ 的值域；若 $f(A)=B$，称 $f$ 将 $A$ 映上（onto）$B$。
- $E\subset B$ 在 $f$ 下的原像（inverse image）：
$$
f^{-1}(E)=\{x\in A:f(x)\in E\}.
$$
- 若对每个 $y\in B$，$f^{-1}(y)$ 至多含 $A$ 中一个元素，则称 $f$ 是 $A$ 到 $B$ 的一一（1-1, one-to-one）映射，即 $x_1\ne x_2\Longrightarrow f(x_1)\ne f(x_2)$。

### 定义 2.3：等价与基数（Equivalence and Cardinal Numbers）

若存在 $A$ 到 $B$ 的 1-1 映射（onto），则称 $A$ 与 $B$ 可建立 1-1 对应（1-1 correspondence），或 $A$ 与 $B$ 有相同的基数（cardinal number），或 $A$ 与 $B$ 等价（equivalent），记作

$$
A\sim B.
$$

该关系具有自反性（reflexive，$A\sim A$）、对称性（symmetric，$A\sim B\Longrightarrow B\sim A$）、传递性（transitive，$A\sim B,\ B\sim C\Longrightarrow A\sim C$）。具有这三个性质的关系称为等价关系（equivalence relation）。

### 定义 2.4：有限、可数、不可数（Finite, Countable, Uncountable）

对正整数 $n$，令

$$
J_n=\{1,2,\ldots,n\},
$$

令 $J$ 为全体正整数组成的集合。对任意集合 $A$：

- (a) $A$ 有限（finite）：$A\sim J_n$ 对某个 $n$ 成立（空集也视为有限）；
- (b) $A$ 无限（infinite）：$A$ 不是有限的；
- (c) $A$ 可数（countable）：$A\sim J$；
- (d) $A$ 不可数（uncountable）：$A$ 既非有限也非可数；
- (e) $A$ 至多可数（at most countable）：$A$ 有限或可数。

可数集又称可枚举（enumerable）或 denumerable。

### 例 2.5：整数集可数（The Set of Integers Is Countable）

整数集 $A$ 与 $J$ 的 1-1 对应由下式给出：

$$
A:\ 0,1,-1,2,-2,3,-3,\ldots
$$

$$
f(n)=\begin{cases}
\dfrac{n}{2},& n\text{ 为偶数（even）},\\[6pt]
-\dfrac{n-1}{2},& n\text{ 为奇数（odd）}.
\end{cases}
$$

### 评注 2.6：有限集与真子集

有限集不能与其真子集等价；无限集则可以（如 $J$ 是整数集 $A$ 的真子集，但 $A\sim J$）。

### 定义 2.7：序列（Sequences）

序列（sequence）是定义在 $J$ 上的函数 $f$。若 $f(n)=x_n$，则记作 $\{x_n\}$ 或 $x_1,x_2,x_3,\ldots$，$x_n$ 称为项（term）。若 $x_n\in A$ 对所有 $n$ 成立，称 $\{x_n\}$ 是 $A$ 中的序列。项不必互异。

### 定理 2.8：可数集的无限子集（Every Infinite Subset of a Countable Set Is Countable）

可数集 $A$ 的每个无限子集 $E$ 是可数的。

### 定义 2.9：集合族、并集与交集（Collections of Sets, Unions, Intersections）

设 $A$、$\Omega$ 为集合，每个 $\alpha\in A$ 对应 $\Omega$ 的一个子集 $E_\alpha$，$\{E_\alpha\}$ 称为集合的族（collection，亦称 family）。并集（union）与交集（intersection）定义为

$$
S=\bigcup_{\alpha\in A}E_\alpha=\{x:x\in E_\alpha\text{ 对某个 }\alpha\in A\},
$$

$$
P=\bigcap_{\alpha\in A}E_\alpha=\{x:x\in E_\alpha\text{ 对每个 }\alpha\in A\}.
$$

有限与可数的记号变体：

$$
S=\bigcup_{m=1}^{n}E_m=E_1\cup E_2\cup\cdots\cup E_n,\qquad
S=\bigcup_{m=1}^{\infty}E_m,
$$

$$
P=\bigcap_{m=1}^{n}E_m=E_1\cap E_2\cap\cdots\cap E_n,\qquad
P=\bigcap_{m=1}^{\infty}E_m.
$$

若 $A\cap B$ 非空，称 $A$ 与 $B$ 相交（intersect）；否则称它们不相交（disjoint）。

### 例 2.10：并集与交集的例子（Examples of Unions and Intersections）

(a) $E_1=\{1,2,3\}$、$E_2=\{2,3,4\}$：$E_1\cup E_2=\{1,2,3,4\}$，$E_1\cap E_2=\{2,3\}$。

(b) 设 $A$ 为满足 $0<x\le1$ 的实数 $x$ 的集合，对每个 $x\in A$，令 $E_x$ 为满足 $0<y<x$ 的实数 $y$ 的集合，则

$$
E_x\subset E_z\ \text{当且仅当}\ 0<x\le z\le1,
$$

$$
\bigcup_{x\in A}E_x=E_1,
$$

$$
\bigcap_{x\in A}E_x=\varnothing.
$$

### 评注 2.11：并集与交集的运算律（Commutative, Associative, and Distributive Laws）

交换律（commutative law）与结合律（associative law）：

$$
A\cup B=B\cup A;\qquad A\cap B=B\cap A,
$$

$$
(A\cup B)\cup C=A\cup(B\cup C);\qquad (A\cap B)\cap C=A\cap(B\cap C).
$$

分配律（distributive law）：

$$
A\cap(B\cup C)=(A\cap B)\cup(A\cap C).
$$

其他关系：

$$
A\subset A\cup B,\qquad A\cap B\subset A,
$$

$$
A\cup\varnothing=A,\qquad A\cap\varnothing=\varnothing,
$$

$$
A\subset B\Longrightarrow A\cup B=B,\quad A\cap B=A.
$$

### 定理 2.12：可数个可数集的并（Countable Union of Countable Sets）

设 $\{E_n\}$（$n=1,2,3,\ldots$）为可数集序列，则

$$
S=\bigcup_{n=1}^{\infty}E_n
$$

是可数的。

**推论（Corollary）**：设 $A$ 至多可数，且对每个 $\alpha\in A$，$B_\alpha$ 至多可数，则

$$
T=\bigcup_{\alpha\in A}B_\alpha
$$

至多可数。

### 定理 2.13：$n$ 元组的集合（Sets of $n$-tuples）

设 $A$ 可数，$B_n$ 为所有 $n$ 元组（$n$-tuple）$(a_1,\ldots,a_n)$ 组成的集合（$a_k\in A$，元素不必互异），则 $B_n$ 可数。

**推论**：有理数集 $\mathbb Q$ 可数。

### 定理 2.14：$0$-$1$ 序列集不可数（The Set of 0-1 Sequences Is Uncountable）

设 $A$ 为所有以数字 $0$ 和 $1$ 为元素的序列组成的集合，则 $A$ 不可数。

（证明方法：Cantor 对角线过程（Cantor's diagonal process）。）

## 二、度量空间（Metric Spaces）

### 定义 2.15：度量空间（Metric Space）

集合 $X$（元素称为点，points）称为度量空间（metric space），若任意两点 $p,q\in X$ 关联一个实数 $d(p,q)$（从 $p$ 到 $q$ 的距离，distance），满足：

$$
\begin{aligned}
\text{(a)}&\quad d(p,q)>0\ (p\ne q);\qquad d(p,p)=0;\\
\text{(b)}&\quad d(p,q)=d(q,p);\\
\text{(c)}&\quad d(p,q)\le d(p,r)+d(r,q)\quad (\text{对任意 }r\in X).
\end{aligned}
$$

具有这三条性质的函数称为距离函数（distance function）或度量（metric）。

### 例 2.16：欧几里得空间（Euclidean Spaces）

欧几里得空间（euclidean space）$R^k$（特别是 $R^1$ 实直线（real line）与 $R^2$ 复平面（complex plane））中的距离为

$$
d(\mathbf x,\mathbf y)=|\mathbf x-\mathbf y|\qquad(\mathbf x,\mathbf y\in R^k).
$$

度量空间的每个子集 $Y$ 以同一距离构成度量空间。

### 定义 2.17：线段、区间、$k$-胞腔、球、凸集（Segments, Intervals, $k$-cells, Balls, Convex Sets）

- 线段（segment）$(a,b)$：满足 $a<x<b$ 的实数 $x$ 的集合；
- 区间（interval）$[a,b]$：满足 $a\le x\le b$ 的实数 $x$ 的集合；
- 半开区间（half-open interval）$[a,b)$、$(a,b]$：分别为 $a\le x<b$、$a<x\le b$；
- $k$-胞腔（$k$-cell）：若 $a_i<b_i$（$i=1,\ldots,k$），所有坐标满足
$$
a_i\le x_i\le b_i\qquad(1\le i\le k)
$$
  的点 $\mathbf x=(x_1,\ldots,x_k)\in R^k$ 组成的集合。1-胞腔即区间，2-胞腔即矩形；
- 开球（open ball）（闭球（closed ball））：中心 $\mathbf x$、半径（radius）$r$ 的集合 $\{\mathbf y\in R^k:|\mathbf y-\mathbf x|<r\}$（$\le r$）；
- $E\subset R^k$ 凸（convex）：当 $\mathbf x,\mathbf y\in E$、$0<\lambda<1$ 时，
$$
\lambda\mathbf x+(1-\lambda)\mathbf y\in E.
$$

球与 $k$-胞腔都是凸的。

### 定义 2.18：邻域、极限点等（Neighborhoods, Limit Points, etc.；设 $X$ 为度量空间）

- (a) $p$ 的邻域（neighborhood）：对某个 $r>0$，
$$
N_r(p)=\{q:d(p,q)<r\},
$$
  $r$ 称为 $N_r(p)$ 的半径；
- (b) $p$ 是 $E$ 的极限点（limit point）：$p$ 的每个邻域含有 $E$ 中异于 $p$ 的点 $q$；
- (c) 孤立点（isolated point）：$p\in E$ 但不是 $E$ 的极限点；
- (d) $E$ 闭（closed）：$E$ 的每个极限点都属于 $E$；
- (e) 内点（interior point）：存在 $p$ 的邻域 $N\subset E$；
- (f) $E$ 开（open）：$E$ 的每个点都是 $E$ 的内点；
- (g) 补集（complement）：$E^c=\{p\in X:p\notin E\}$；
- (h) $E$ 完备（perfect）：$E$ 闭且 $E$ 的每个点都是 $E$ 的极限点；
- (i) $E$ 有界（bounded）：存在实数 $M$ 与点 $q\in X$，使对所有 $p\in E$ 有 $d(p,q)<M$；
- (j) $E$ 在 $X$ 中稠密（dense）：$X$ 的每个点是 $E$ 的极限点或是 $E$ 的点（或两者）。

### 定理 2.19：邻域是开集（Every Neighborhood Is an Open Set）

每个邻域都是开集。

### 定理 2.20：极限点的邻域（Limit Points and Neighborhoods）

若 $p$ 是集合 $E$ 的极限点，则 $p$ 的每个邻域含有 $E$ 的无穷多个点。

**推论**：有限点集没有极限点。

### 例 2.21：$R^2$ 中的子集（Examples of Subsets of $R^2$）

考虑以下 $R^2$ 子集：(a) $\{z:|z|<1\}$；(b) $\{z:|z|\le1\}$；(c) 非空有限集；(d) 整数集；(e) $\{1/n:n=1,2,3,\ldots\}$（有极限点 $z=0$，但 $E$ 中没有点是 $E$ 的极限点）；(f) 全体复数（即 $R^2$）；(g) 线段 $(a,b)$。其性质对照：

| 集合 | 闭（Closed） | 开（Open） | 完备（Perfect） | 有界（Bounded） |
|:---:|:---:|:---:|:---:|:---:|
| (a) | 否 | 是 | 否 | 是 |
| (b) | 是 | 否 | 是 | 是 |
| (c) | 是 | 否 | 否 | 是 |
| (d) | 是 | 否 | 否 | 否 |
| (e) | 否 | 否 | 否 | 是 |
| (f) | 是 | 是 | 是 | 否 |
| (g) | 否 | — | 否 | 是 |

(g) 的第二格留空：线段 $(a,b)$ 作为 $R^2$ 的子集不开，但作为 $R^1$ 的子集是开的。

### 定理 2.22：De Morgan 律（De Morgan's Laws）

设 $\{E_\alpha\}$ 为（有限或无限）集合族，则

$$
\left(\bigcup_{\alpha}E_\alpha\right)^{c}=\bigcap_{\alpha}(E_\alpha^{c}).
$$

### 定理 2.23：开集与闭集的对偶（Open iff Complement Is Closed）

集合 $E$ 开当且仅当其补集 $E^c$ 闭。

**推论**：集合 $F$ 闭当且仅当其补集开。

### 定理 2.24：开集与闭集的运算（Unions and Intersections of Open and Closed Sets）

- (a) 任意一族开集的并是开集；
- (b) 任意一族闭集的交是闭集；
- (c) 有限个开集的交是开集；
- (d) 有限个闭集的并是闭集。

### 例 2.25：有限性的本质（Finiteness Is Essential）

$G_n=(-\frac1n,\frac1n)$ 都是 $R^1$ 的开集，但

$$
\bigcap_{n=1}^{\infty}G_n=\{0\}
$$

不是开集：无限个开集的交不必是开集；同理无限个闭集的并不必是闭集。

### 定义 2.26：闭包（The Closure of a Set）

若 $E'\subset X$ 记 $E$ 的全体极限点组成的集合，则 $E$ 的闭包（closure）为

$$
\bar E=E\cup E'.
$$

### 定理 2.27：闭包的性质（Properties of the Closure）

设 $X$ 为度量空间，$E\subset X$，则

- (a) $\bar E$ 是闭集；
- (b) $E=\bar E$ 当且仅当 $E$ 是闭集；
- (c) 对每个满足 $E\subset F$ 的闭集 $F$，有 $\bar E\subset F$。

由 (a)(c)，$\bar E$ 是包含 $E$ 的最小闭集（smallest closed set）。

### 定理 2.28：上确界属于闭包（The Supremum Belongs to the Closure）

设 $E$ 为非空上有界实数集，$y=\sup E$，则 $y\in\bar E$。因此若 $E$ 闭，则 $y\in E$。

### 评注 2.29：相对开集（Open Relative to a Subset）

设 $E\subset Y\subset X$。称 $E$ 相对 $Y$ 开（open relative to $Y$），若对每个 $p\in E$ 存在 $r>0$，使 $d(p,q)<r$ 且 $q\in Y$ 蕴含 $q\in E$。集合可以相对 $Y$ 开而不相对 $X$ 开（例 2.21(g)）。

### 定理 2.30：相对开集的刻画（Characterization of Relative Openness）

设 $Y\subset X$。$E\subset Y$ 相对 $Y$ 开，当且仅当存在 $X$ 的开子集 $G$，使

$$
E=Y\cap G.
$$

## 三、紧集（Compact Sets）

### 定义 2.31：开覆盖（Open Covers）

度量空间 $X$ 中集合 $E$ 的开覆盖（open cover）是满足

$$
E\subset\bigcup_{\alpha}G_\alpha
$$

的一族 $X$ 的开子集 $\{G_\alpha\}$。

### 定义 2.32：紧集（Compact Sets）

度量空间 $X$ 的子集 $K$ 称为紧的（compact），若 $K$ 的每个开覆盖都含有有限子覆盖（finite subcover），即存在有限多个指标 $\alpha_1,\ldots,\alpha_n$，使

$$
K\subset G_{\alpha_1}\cup\cdots\cup G_{\alpha_n}.
$$

每个有限集都是紧的。

### 定理 2.33：紧性不依赖嵌入空间（Compactness Does Not Depend on the Embedding Space）

设 $K\subset Y\subset X$，则 $K$ 相对 $X$ 紧当且仅当 $K$ 相对 $Y$ 紧。

### 定理 2.34：紧子集闭（Compact Subsets Are Closed）

度量空间的紧子集是闭集。

### 定理 2.35：紧集的闭子集（Closed Subsets of Compact Sets Are Compact）

紧集的闭子集是紧的。

**推论**：若 $F$ 闭、$K$ 紧，则 $F\cap K$ 紧。

### 定理 2.36：紧集的有限交性质（Finite Intersection Property）

设 $\{K_\alpha\}$ 为度量空间 $X$ 中一族紧集，若 $\{K_\alpha\}$ 的每个有限子族的交都非空，则

$$
\bigcap_{\alpha}K_\alpha
$$

非空。

**推论**：若 $\{K_n\}$ 是非空紧集序列，且 $K_n\supset K_{n+1}$（$n=1,2,3,\ldots$），则

$$
\bigcap_{n=1}^{\infty}K_n
$$

非空。

### 定理 2.37：紧集中的极限点（Limit Points of Infinite Subsets of Compact Sets）

若 $E$ 是紧集 $K$ 的无限子集，则 $E$ 在 $K$ 中有极限点。

### 定理 2.38：$R^1$ 中区间套（Nested Intervals in $R^1$）

若 $\{I_n\}$ 是 $R^1$ 中的区间序列，且 $I_n\supset I_{n+1}$（$n=1,2,3,\ldots$），则

$$
\bigcap_{n=1}^{\infty}I_n
$$

非空。

### 定理 2.39：$k$-胞腔套（Nested $k$-cells）

设 $k$ 为正整数。若 $\{I_n\}$ 是 $k$-胞腔序列，且 $I_n\supset I_{n+1}$（$n=1,2,3,\ldots$），则

$$
\bigcap_{n=1}^{\infty}I_n
$$

非空。

### 定理 2.40：$k$-胞腔紧（Every $k$-cell Is Compact）

每个 $k$-胞腔都是紧的。

### 定理 2.41：Heine-Borel 定理（The Heine-Borel Theorem）

设 $E\subset R^k$，则下列三个性质两两等价：

- (a) $E$ 闭且有界；
- (b) $E$ 紧；
- (c) $E$ 的每个无限子集在 $E$ 中有极限点。

（(a) 与 (b) 的等价性即 Heine-Borel 定理。在一般度量空间中 (b) 与 (c) 等价，但 (a) 一般不蕴含 (b)(c)。）

### 定理 2.42（Weierstrass）：有界无限集有极限点（Weierstrass' Theorem）

$R^k$ 的每个有界无限子集在 $R^k$ 中有极限点。

## 四、完备集与 Cantor 集（Perfect Sets and the Cantor Set）

### 定理 2.43：完备集不可数（Perfect Sets Are Uncountable）

设 $P$ 为 $R^k$ 中的非空完备集，则 $P$ 不可数。

**推论**：每个区间 $[a,b]$（$a<b$）不可数；特别地，全体实数组成的集合不可数。

### 2.44 Cantor 集（The Cantor Set）

构造：令 $E_0=[0,1]$，去掉线段 $(\frac13,\frac23)$，令 $E_1$ 为区间

$$
[0,\tfrac13],\quad[\tfrac23,1]
$$

之并；再去掉这两区间的中间三分之一，令 $E_2$ 为区间

$$
[0,\tfrac19],\ [\tfrac29,\tfrac39],\ [\tfrac69,\tfrac79],\ [\tfrac89,1]
$$

之并；如此继续，得到紧集序列 $E_n$，满足

- (a) $E_1\supset E_2\supset E_3\supset\cdots$；
- (b) $E_n$ 是 $2^n$ 个长度为 $3^{-n}$ 的区间之并。

Cantor 集（Cantor set）定义为

$$
P=\bigcap_{n=1}^{\infty}E_n.
$$

性质：$P$ 紧且非空；不含任何线段——每个线段 $(\alpha,\beta)$ 都含有形如

$$
\left(\frac{3k+1}{3^{m}},\frac{3k+2}{3^{m}}\right)
$$

（$k,m$ 为正整数）的线段，只要 $3^{-m}<\frac{\beta-\alpha}{6}$；$P$ 完备（无孤立点）；$P$ 不可数；且 $P$ 是测度（measure）为零的不可数集（测度概念见第 11 章）。

## 五、连通集（Connected Sets）

### 定义 2.45：分离集与连通集（Separated Sets and Connected Sets）

度量空间 $X$ 的两个子集 $A,B$ 称为分离的（separated），若

$$
A\cap\bar B=\varnothing,\qquad \bar A\cap B=\varnothing,
$$

即 $A$ 中没有点落在 $B$ 的闭包中，$B$ 中没有点落在 $A$ 的闭包中。

集合 $E\subset X$ 称为连通的（connected），若 $E$ 不是两个非空分离集之并。

### 评注 2.46：分离与不相交

分离集当然不相交，但不相交集不必分离。例如区间 $[0,1]$ 与线段 $(1,2)$ 不相交但不分离（$1$ 是 $(1,2)$ 的极限点）；而线段 $(0,1)$ 与 $(1,2)$ 是分离的。

### 定理 2.47：$R^1$ 中连通集的刻画（Connected Sets on the Real Line）

实数直线 $R^1$ 的子集 $E$ 连通，当且仅当它具有如下性质：若 $x\in E$、$y\in E$ 且 $x<z<y$，则 $z\in E$。

