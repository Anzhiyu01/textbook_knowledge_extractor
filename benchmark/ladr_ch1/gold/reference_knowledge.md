# 第一章 Vector Spaces（向量空间）· 知识清单

> **范围说明**：源为 Sheldon Axler《Linear Algebra Done Right》第 4 版第一章（`Linear Algebra Done Right.md`，源行 479–1662，切片 SHA-256 `A823686245B87B1717E63412210ADF5AF65180BF973280BBF9907BF25AA4620B`，共 1184 行）。第一章标题行在转换件中缺失（见 `audit.json.source_artifacts`），切片起点为该章正文起始段。本章含三节：1A $\mathbb{R}^{n}$ and $\mathbb{C}^{n}$、1B Definition of Vector Space、1C Subspaces。本清单仅收录定义、结论、公式、带标签的例与注（英文源，转写为中文，首次出现的术语以「中文（English）」标注）；证明、推导、习题（Exercises 1A/1B/1C）、图片/许可文字及第二章引言均不收入。转换损伤（如 `diferent`→different、`ofcomplex`→of complex、∎ 符号缺失等）按唯一判定修复并逐项登记。

## Chapter 1 Vector Spaces

### 1A $\mathbb{R}^{n}$ and $\mathbb{C}^{n}$（$\mathbb{R}^{n}$ 与 $\mathbb{C}^{n}$）

#### Complex Numbers（复数）

**K-505 定义 1.1：复数（complex number）、复数集 $\mathbb{C}$**

一个复数是一个有序对 $(a,b)$，其中 $a,b\in\mathbb{R}$，但把它写成 $a+bi$。复数全体记为 $\mathbb{C}$：

$$
\mathbb{C}=\{a+bi: a,b\in\mathbb{R}\}.
$$

$\mathbb{C}$ 上的加法与乘法定义为

$$
(a+bi)+(c+di)=(a+c)+(b+d)i,\qquad (a+bi)(c+di)=(ac-bd)+(ad+bc)i
$$

这里 $a,b,c,d\in\mathbb{R}$。

**K-522 注：$\mathbb{R}$ 视为 $\mathbb{C}$ 的子集**

若 $a\in\mathbb{R}$，将 $a+0i$ 与实数 $a$ 认同。于是把 $\mathbb{R}$ 看作 $\mathbb{C}$ 的子集。通常把 $0+bi$ 写成 $bi$，把 $0+1i$ 写成 $i$。

**K-536 例 1.2：复数算术**

乘积 $(2+3i)(4+5i)$ 可用 1.3 中的分配律与交换律求得：

$$
(2+3i)(4+5i)=-7+22i
$$

**K-546 性质 1.3：复数算术的性质**

- 交换律（commutativity）：$\alpha+\beta=\beta+\alpha$ 且 $\alpha\beta=\beta\alpha$，对所有 $\alpha,\beta\in\mathbb{C}$；
- 结合律（associativity）：$(\alpha+\beta)+\lambda=\alpha+(\beta+\lambda)$ 且 $(\alpha\beta)\lambda=\alpha(\beta\lambda)$，对所有 $\alpha,\beta,\lambda\in\mathbb{C}$；
- 单位元（identities）：$\lambda+0=\lambda$ 且 $\lambda1=\lambda$，对所有 $\lambda\in\mathbb{C}$；
- 加法逆元（additive inverse）：对每个 $\alpha\in\mathbb{C}$，存在唯一的 $\beta\in\mathbb{C}$ 使得 $\alpha+\beta=0$；
- 乘法逆元（multiplicative inverse）：对每个 $\alpha\in\mathbb{C}$ 且 $\alpha\neq0$，存在唯一的 $\beta\in\mathbb{C}$ 使得 $\alpha\beta=1$；
- 分配律（distributive property）：$\lambda(\alpha+\beta)=\lambda\alpha+\lambda\beta$，对所有 $\lambda,\alpha,\beta\in\mathbb{C}$。

**K-606 定义 1.5：$-\alpha$、减法、$1/\alpha$、除法**

设 $\alpha,\beta\in\mathbb{C}$。令 $-\alpha$ 表示 $\alpha$ 的加法逆元，即 $-\alpha$ 是唯一的复数使得

$$
\alpha+(-\alpha)=0.
$$

$\mathbb{C}$ 上的减法定义为

$$
\beta-\alpha=\beta+(-\alpha).
$$

对 $\alpha\neq0$，令 $1/\alpha$ 和 $\frac{1}{\alpha}$ 表示 $\alpha$ 的乘法逆元，即 $1/\alpha$ 是唯一的复数使得

$$
\alpha(1/\alpha)=1.
$$

对 $\alpha\neq0$，除以 $\alpha$ 定义为

$$
\beta/\alpha=\beta(1/\alpha).
$$

**K-636 记号 1.6：$\mathbb{F}$ 表示 $\mathbb{R}$ 或 $\mathbb{C}$**

整本书中，$\mathbb{F}$ 表示 $\mathbb{R}$（实数）或 $\mathbb{C}$（复数）两者之一。若证明一个关于 $\mathbb{F}$ 的定理，就知道把 $\mathbb{F}$ 换成 $\mathbb{R}$ 时成立，换成 $\mathbb{C}$ 时也成立。字母 $\mathbb{F}$ 的选用是因为 $\mathbb{R}$ 和 $\mathbb{C}$ 是所谓域（field）的例子。

**K-644 定义：标量（scalar）**

$\mathbb{F}$ 的元素称为标量（scalar）。「标量」即「数」的别称，常用来强调对象是一个数而非向量。

**K-646 定义：$\alpha^{m}$ 及其性质**

对 $\alpha\in\mathbb{F}$ 和正整数 $m$，定义 $\alpha^{m}$ 为 $\alpha$ 自乘 $m$ 次：

$$
\alpha^{m}=\underbrace{\alpha\cdots\alpha}_{m\ \text{times}}.
$$

这个定义蕴含

$$
(\alpha^{m})^{n}=\alpha^{mn}\quad\text{且}\quad (\alpha\beta)^{m}=\alpha^{m}\beta^{m}
$$

对所有 $\alpha,\beta\in\mathbb{F}$ 及所有正整数 $m,n$。

#### Lists（列表）

**K-664 例 1.7：$\mathbb{R}^{2}$ 与 $\mathbb{R}^{3}$**

集合 $\mathbb{R}^{2}$（可看作平面）是全体实数有序对：

$$
\mathbb{R}^{2}=\{(x,y): x,y\in\mathbb{R}\}.
$$

集合 $\mathbb{R}^{3}$（可看作通常的空间）是全体实数有序三元组：

$$
\mathbb{R}^{3}=\{(x,y,z): x,y,z\in\mathbb{R}\}.
$$

**K-680 定义 1.8：列表（list）与长度（length）**

设 $n$ 是非负整数。长度为 $n$ 的列表是 $n$ 个元素的有序集（元素可以是数、其他列表或更抽象的对象）。两个列表相等当且仅当它们长度相同、元素相同且顺序相同。列表中元素用逗号分隔、外面加圆括号；长度 $n$ 的列表可写成

$$
(z_{1},\dots,z_{n}).
$$

许多数学家把长度为 $n$ 的列表称为 $n$ 元组（$n$-tuple）。每个列表都有有限的、非负整数的长度；形如 $(x_{1},x_{2},\dots)$ 的对象不是列表。长度为 0 的列表写作 `( )`，也视为列表。列表与集合有两方面区别：列表讲究顺序、重复有意义；集合中顺序与重复都无关。

**K-701 例 1.9：列表与集合的区别**

列表 $(3,5)$ 与 $(5,3)$ 不相等，而集合 $\{3,5\}$ 与 $\{5,3\}$ 相等。列表 $(4,4)$ 与 $(4,4,4)$ 不相等（长度不同），虽然集合 $\{4,4\}$ 与 $\{4,4,4\}$ 都等于集合 $\{4\}$。

#### $\mathbb{F}^{n}$（$\mathbb{F}^{n}$）

**K-710 记号 1.10：$n$**

本章剩下部分固定一个正整数 $n$。

**K-714 定义 1.11：$\mathbb{F}^{n}$ 与坐标（coordinate）**

$\mathbb{F}^{n}$ 是长度为 $n$、元素取自 $\mathbb{F}$ 的全体列表：

$$
\mathbb{F}^{n}=\{(x_{1},\dots,x_{n}): x_{k}\in\mathbb{F}\ \text{对}\ k=1,\dots,n\}.
$$

对 $(x_{1},\dots,x_{n})\in\mathbb{F}^{n}$ 且 $k\in\{1,\dots,n\}$，称 $x_{k}$ 是 $(x_{1},\dots,x_{n})$ 的第 $k$ 个坐标。

**K-726 例 1.12：$\mathbb{C}^{4}$**

$\mathbb{C}^{4}$ 是长度为 4、元素取自 $\mathbb{C}$ 的全体列表：

$$
\mathbb{C}^{4}=\{(z_{1},z_{2},z_{3},z_{4}): z_{1},z_{2},z_{3},z_{4}\in\mathbb{C}\}.
$$

**K-738 定义 1.13：$\mathbb{F}^{n}$ 中的加法**

$\mathbb{F}^{n}$ 中的加法通过逐坐标相加定义：

$$
(x_{1},\dots,x_{n})+(y_{1},\dots,y_{n})=(x_{1}+y_{1},\dots,x_{n}+y_{n}).
$$

**K-748 性质 1.14：$\mathbb{F}^{n}$ 中加法的交换律**

若 $x,y\in\mathbb{F}^{n}$，则 $x+y=y+x$。

**K-766 记号 1.15：$0$**

令 $0$ 表示坐标全为 0 的长度 $n$ 的列表：

$$
0=(0,\dots,0).
$$

此式左边的 0 表示 $\mathbb{F}^{n}$ 中的列表，右边的每个 0 表示数；这种混淆做法实际无害，因为上下文总指明是哪个 0。

**K-776 例 1.16：语境决定哪个 $0$**

考虑「$0$ 是 $\mathbb{F}^{n}$ 的一个加法单位元」这一陈述：

$$
x+0=x\quad\text{对一切}\ x\in\mathbb{F}^{n}.
$$

其中的 0 是 1.15 定义的列表，不是数 0，因为尚未定义 $\mathbb{F}^{n}$ 的元素 $x$ 与数 0 的和。

**K-840 定义 1.17：$\mathbb{F}^{n}$ 中的加法逆元 $-x$**

对 $x\in\mathbb{F}^{n}$，$x$ 的加法逆元记为 $-x$，是 $\mathbb{F}^{n}$ 中使

$$
x+(-x)=0
$$

的向量。若 $x=(x_{1},\dots,x_{n})$，则 $-x=(-x_{1},\dots,-x_{n})$。

**K-865 定义 1.18：$\mathbb{F}^{n}$ 中的数乘（scalar multiplication）**

数 $\lambda$ 与 $\mathbb{F}^{n}$ 中向量的乘积通过把向量的每个坐标乘以 $\lambda$ 来计：

$$
\lambda(x_{1},\dots,x_{n})=(\lambda x_{1},\dots,\lambda x_{n});
$$

这里 $\lambda\in\mathbb{F}$ 且 $(x_{1},\dots,x_{n})\in\mathbb{F}^{n}$。

#### Digression on Fields（域的补充说明）

**K-893 定义：域（field）**

域是含至少两个不同元素（记为 0 和 1）的集合，连同满足 1.3 中全部性质的加法与乘法运算。于是 $\mathbb{R}$ 和 $\mathbb{C}$ 都是域，有理数集按通常的加法与乘法也是域。另一个例子是 $\{0,1\}$，按通常加法与乘法，但规定 $1+1=0$。

**K-897 注：对任意域的推广**

本书只用 $\mathbb{R}$ 和 $\mathbb{C}$ 两域。但线性代数中许多对 $\mathbb{R}$、$\mathbb{C}$ 成立的定义、定理与证明可以不加修改地用于任意域。除第 6、7 章（内积空间）外，可以把 $\mathbb{F}$ 理解为任意域；凡以「$\mathbb{F}$ 为 $\mathbb{C}$」为假设的结果（内积章节除外），可以把该假设替换为「$\mathbb{F}$ 为代数闭域」（即每个非常系数数多项式都有零点）。少数结果（例如 1C 节习题 13）需要 $\mathbb{F}$ 满足 $1+1\neq0$。

### 1B Definition of Vector Space（向量空间的定义）

**K-946 定义 1.19：加法与数乘**

集合 $V$ 上的一个加法（addition）是给每对元素 $u,v\in V$ 指派一个元素 $u+v\in V$ 的函数。集合 $V$ 上的一个数乘（scalar multiplication）是给每个 $\lambda\in\mathbb{F}$ 和每个 $v\in V$ 指派一个元素 $\lambda v\in V$ 的函数。

**K-953 定义 1.20：向量空间（vector space）**

向量空间是一个集合 $V$，连同 $V$ 上的一个加法与 $V$ 上的一个数乘，满足如下性质：

- 交换律（commutativity）：$u+v=v+u$，对所有 $u,v\in V$；
- 结合律（associativity）：$(u+v)+w=u+(v+w)$ 且 $(ab)v=a(bv)$，对所有 $u,v,w\in V$ 及所有 $a,b\in\mathbb{F}$；
- 加法单位元（additive identity）：存在元素 $0\in V$ 使得 $v+0=v$ 对所有 $v\in V$；
- 加法逆元（additive inverse）：对每个 $v\in V$，存在 $w\in V$ 使得 $v+w=0$；
- 乘法单位元（multiplicative identity）：$1v=v$ 对所有 $v\in V$；
- 分配律（distributive properties）：$a(u+v)=au+av$ 且 $(a+b)v=av+bv$，对所有 $a,b\in\mathbb{F}$ 及所有 $u,v\in V$。

**K-991 定义 1.21：向量（vector）与点（point）**

向量空间的元素称为向量或点。

**K-995 注：「over $\mathbb{F}$」的表述**

数乘依赖于 $\mathbb{F}$，因此需要精确时，说 $V$ 是 $\mathbb{F}$ 上的向量空间（vector space over $\mathbb{F}$）而不只是向量空间。例如 $\mathbb{R}^{n}$ 是 $\mathbb{R}$ 上的向量空间，$\mathbb{C}^{n}$ 是 $\mathbb{C}$ 上的向量空间。

**K-997 定义 1.22：实向量空间、复向量空间**

$\mathbb{R}$ 上的向量空间称为实向量空间（real vector space）；$\mathbb{C}$ 上的向量空间称为复向量空间（complex vector space）。通常 $\mathbb{F}$ 的选择由上下文决定或无关紧要，因而常常省略不写。

**K-1004 注：$\mathbb{F}^{n}$ 是向量空间**

按通常的加法与数乘，$\mathbb{F}^{n}$ 是 $\mathbb{F}$ 上的向量空间。

**K-1006 注：最简向量空间**

最简单的向量空间是 $\{0\}$，只包含一个点。

**K-1010 例 1.23：$\mathbb{F}^{\infty}$**

$\mathbb{F}^{\infty}$ 定义为 $\mathbb{F}$ 中元素的一切序列：

$$
\mathbb{F}^{\infty}=\{(x_{1},x_{2},\dots): x_{k}\in\mathbb{F}\ \text{对}\ k=1,2,\dots\}.
$$

$\mathbb{F}^{\infty}$ 上的加法与数乘按自然方式定义：

$$
(x_{1},x_{2},\dots)+(y_{1},y_{2},\dots)=(x_{1}+y_{1},x_{2}+y_{2},\dots),
$$

$$
\lambda(x_{1},x_{2},\dots)=(\lambda x_{1},\lambda x_{2},\dots).
$$

按这些定义，$\mathbb{F}^{\infty}$ 成为 $\mathbb{F}$ 上的向量空间；其加法单位元是全为 0 的序列。

**K-1032 记号 1.24：$\mathbb{F}^{S}$**

若 $S$ 是集合，则 $\mathbb{F}^{S}$ 表示从 $S$ 到 $\mathbb{F}$ 的函数全体。对 $f,g\in\mathbb{F}^{S}$，和 $f+g\in\mathbb{F}^{S}$ 定义为

$$
(f+g)(x)=f(x)+g(x)\quad\text{对所有}\ x\in S.
$$

对 $\lambda\in\mathbb{F}$ 与 $f\in\mathbb{F}^{S}$，乘积 $\lambda f\in\mathbb{F}^{S}$ 定义为

$$
(\lambda f)(x)=\lambda f(x)\quad\text{对所有}\ x\in S.
$$

例如 $S=[0,1]$ 且 $\mathbb{F}=\mathbb{R}$ 时，$\mathbb{R}^{[0,1]}$ 是 $[0,1]$ 上实值函数的集合。

**K-1055 例 1.25：$\mathbb{F}^{S}$ 是向量空间**

若 $S$ 是非空集合，则 $\mathbb{F}^{S}$（按上述加法与数乘）是 $\mathbb{F}$ 上的向量空间。$\mathbb{F}^{S}$ 的加法单位元是函数 $0:S\to\mathbb{F}$，定义为

$$
0(x)=0\quad\text{对所有}\ x\in S.
$$

对 $f\in\mathbb{F}^{S}$，$f$ 的加法逆元是函数 $-f:S\to\mathbb{F}$，定义为

$$
(-f)(x)=-f(x)\quad\text{对所有}\ x\in S.
$$

**K-1074 注：$\mathbb{F}^{n}$ 是 $\mathbb{F}^{S}$ 的特例**

向量空间 $\mathbb{F}^{n}$ 是向量空间 $\mathbb{F}^{S}$ 的特例：每个 $(x_{1},\dots,x_{n})\in\mathbb{F}^{n}$ 可以看作从集合 $\{1,2,\dots,n\}$ 到 $\mathbb{F}$ 的函数 $x$，只须把第 $k$ 个坐标 $x_{k}$ 写成 $x(k)$。换言之，可以把 $\mathbb{F}^{n}$ 看作 $\mathbb{F}^{\{1,2,\dots,n\}}$；类似地可把 $\mathbb{F}^{\infty}$ 看作 $\mathbb{F}^{\{1,2,\dots\}}$。

**K-1084 结论 1.26：加法单位元唯一**

向量空间有唯一的加法单位元。

**K-1098 结论 1.27：加法逆元唯一**

向量空间中每个元素有唯一的加法逆元。

**K-1112 记号 1.28：$-v$、$w-v$**

设 $v,w\in V$，则 $-v$ 表示 $v$ 的加法逆元；$w-v$ 定义为 $w+(-v)$。

**K-1121 记号 1.29：$V$ 表示 $\mathbb{F}$ 上的向量空间**

全书其余部分，$V$ 表示 $\mathbb{F}$ 上的一个向量空间。

**K-1127 结论 1.30：数 0 乘向量**

$$
0v=0\quad\text{对每个}\ v\in V.
$$

（左端的 0 是标量，右端的 0 是 $V$ 的加法单位元。）

**K-1147 结论 1.31：数乘向量 0**

$$
a0=0\quad\text{对每个}\ a\in\mathbb{F}.
$$

（此处的 0 是 $V$ 的加法单位元。）

**K-1163 结论 1.32：数 $-1$ 乘向量**

$$
(-1)v=-v\quad\text{对每个}\ v\in V.
$$

### 1C Subspaces（子空间）

**K-1245 定义 1.33：子空间（subspace）**

$V$ 的子集 $U$ 称为 $V$ 的子空间，若 $U$ 与 $V$ 使用相同的加法单位元、加法与数乘时也是一个向量空间。

**K-1251 注：术语「线性子空间」**

有人使用术语「线性子空间（linear subspace）」，它与「子空间」意思相同。

**K-1253 判定 1.34：子空间的充要条件**

$V$ 的子集 $U$ 是 $V$ 的子空间当且仅当 $U$ 满足下列三个条件：

- 加法单位元（additive identity）：$0\in U$；
- 对加法封闭（closed under addition）：$u,w\in U$ 蕴含 $u+w\in U$；
- 对数乘封闭（closed under scalar multiplication）：$a\in\mathbb{F}$ 且 $u\in U$ 蕴含 $au\in U$。

**K-1279 注：条件可替换为「非空」**

上述加法单位元条件可以替换为「$U$ 非空」（因为取 $u\in U$ 乘以 0 就能得到 $0\in U$）。不过若 $U$ 确是子空间，通常最快说明 $U$ 非空的办法就是证明 $0\in U$。

**K-1287 例 1.35：子空间的例子**

(a) 若 $b\in\mathbb{F}$，则

$$
\{(x_{1},x_{2},x_{3},x_{4})\in\mathbb{F}^{4}: x_{3}=5x_{4}+b\}
$$

是 $\mathbb{F}^{4}$ 的子空间当且仅当 $b=0$。

(b) $[0,1]$ 上连续实值函数的集合是 $\mathbb{R}^{[0,1]}$ 的子空间。

(c) $\mathbb{R}$ 上可微实值函数的集合是 $\mathbb{R}^{\mathbb{R}}$ 的子空间。

(d) 区间 $(0,3)$ 上满足 $f'(2)=b$ 的可微实值函数 $f$ 的集合是 $\mathbb{R}^{(0,3)}$ 的子空间当且仅当 $b=0$。

(e) 极限为 0 的复数序列全体是 $\mathbb{C}^{\infty}$ 的子空间。

**K-1304 注：最小与最大子空间；空集不是子空间**

$\{0\}$ 是 $V$ 的最小子空间，$V$ 本身是 $V$ 的最大子空间。空集不是 $V$ 的子空间，因为子空间必须是向量空间，从而必须至少含一个元素（一个加法单位元）。

**K-1306 注：$\mathbb{R}^{2}$、$\mathbb{R}^{3}$ 的子空间分类**

$\mathbb{R}^{2}$ 的子空间恰好是 $\{0\}$、$\mathbb{R}^{2}$ 中过原点的所有直线，以及 $\mathbb{R}^{2}$。$\mathbb{R}^{3}$ 的子空间恰好是 $\{0\}$、$\mathbb{R}^{3}$ 中过原点的所有直线、$\mathbb{R}^{3}$ 中过原点的所有平面，以及 $\mathbb{R}^{3}$。

#### Sums of Subspaces（子空间的和）

**K-1312 注：子空间的并很少是子空间**

子空间的并很少是子空间（见习题 12），这正是通常用和而非并的原因。

**K-1314 定义 1.36：子空间的和（sum of subspaces）**

设 $V_{1},\dots,V_{m}$ 是 $V$ 的子空间。$V_{1},\dots,V_{m}$ 的和记为 $V_{1}+\cdots+V_{m}$，是 $V_{1},\dots,V_{m}$ 中元素的一切可能之和的集合。更确切地，

$$
V_{1}+\dots+V_{m}=\{v_{1}+\dots+v_{m}: v_{1}\in V_{1},\dots,v_{m}\in V_{m}\}.
$$

**K-1324 例 1.37：$\mathbb{F}^{3}$ 中子空间之和**

设 $U$ 是 $\mathbb{F}^{3}$ 中第二、三坐标等于 0 的元素全体，$W$ 是第一、三坐标等于 0 的元素全体：

$$
U=\{(x,0,0)\in\mathbb{F}^{3}: x\in\mathbb{F}\}\quad\text{且}\quad W=\{(0,y,0)\in\mathbb{F}^{3}: y\in\mathbb{F}\}.
$$

则

$$
U+W=\{(x,y,0)\in\mathbb{F}^{3}: x,y\in\mathbb{F}\}.
$$

**K-1340 例 1.38：$\mathbb{F}^{4}$ 中子空间之和**

设

$$
U=\{(x,x,y,y)\in\mathbb{F}^{4}: x,y\in\mathbb{F}\}\quad\text{且}\quad W=\{(x,x,x,y)\in\mathbb{F}^{4}: x,y\in\mathbb{F}\}.
$$

用语言描述：$U$ 是 $\mathbb{F}^{4}$ 中前两个坐标相等、后两个坐标也相等的元素全体；$W$ 是前三个坐标相等的元素全体。则

$$
U+W=\{(x,x,y,z)\in\mathbb{F}^{4}: x,y,z\in\mathbb{F}\},
$$

即：$U+W$ 是前两个坐标相等的元素全体。

**K-1378 结论 1.40：子空间之和是包含各加项的最小子空间**

设 $V_{1},\dots,V_{m}$ 是 $V$ 的子空间，则 $V_{1}+\cdots+V_{m}$ 是 $V$ 中包含 $V_{1},\dots,V_{m}$ 的最小子空间（即每个包含所有加项的子空间都包含这个和）。

#### Direct Sums（直和）

**K-1398 定义 1.41：直和（direct sum）与记号 $\oplus$**

设 $V_{1},\dots,V_{m}$ 是 $V$ 的子空间。和 $V_{1}+\cdots+V_{m}$ 称为直和，若 $V_{1}+\cdots+V_{m}$ 中每个元素都只能以一种方式写成和 $v_{1}+\cdots+v_{m}$（其中每个 $v_{k}\in V_{k}$）。若 $V_{1}+\cdots+V_{m}$ 是直和，则记 $V_{1}\oplus\cdots\oplus V_{m}$，$\oplus$ 记号表示这是直和。

**K-1405 例 1.42：两个子空间的直和**

设 $U$ 是 $\mathbb{F}^{3}$ 中末坐标等于 0 的向量构成的子空间，$W$ 是前两个坐标等于 0 的向量构成的子空间：

$$
U=\{(x,y,0)\in\mathbb{F}^{3}: x,y\in\mathbb{F}\}\quad\text{且}\quad W=\{(0,0,z)\in\mathbb{F}^{3}: z\in\mathbb{F}\}.
$$

则 $\mathbb{F}^{3}=U\oplus W$。

**K-1415 例 1.43：多个子空间的直和**

设 $V_{k}$ 是 $\mathbb{F}^{n}$ 中除第 $k$ 个位置外坐标全为 0 的向量构成的子空间；例如 $V_{2}=\{(0,x,0,\dots,0)\in\mathbb{F}^{n}: x\in\mathbb{F}\}$。则

$$
\mathbb{F}^{n}=V_{1}\oplus\dots\oplus V_{n}.
$$

**K-1431 反例 1.44：不是直和的子空间之和**

设

$$
V_{1}=\{(x,y,0)\in\mathbb{F}^{3}: x,y\in\mathbb{F}\},\qquad V_{2}=\{(0,0,z)\in\mathbb{F}^{3}: z\in\mathbb{F}\},\qquad V_{3}=\{(0,y,y)\in\mathbb{F}^{3}: y\in\mathbb{F}\}.
$$

则 $\mathbb{F}^{3}=V_{1}+V_{2}+V_{3}$。但 $\mathbb{F}^{3}$ 不等于 $V_{1},V_{2},V_{3}$ 的直和，因为 $(0,0,0)$ 可以以多种方式写成和 $v_{1}+v_{2}+v_{3}$（各 $v_{k}\in V_{k}$）。具体地，

$$
(0,0,0)=(0,1,0)+(0,0,1)+(0,-1,-1)
$$

且当然

$$
(0,0,0)=(0,0,0)+(0,0,0)+(0,0,0),
$$

其中每个等式右边第一个向量在 $V_{1}$ 中、第二个在 $V_{2}$ 中、第三个在 $V_{3}$ 中。因此和 $V_{1}+V_{2}+V_{3}$ 不是直和。

**K-1473 判定 1.45：直和的充要条件**

设 $V_{1},\dots,V_{m}$ 是 $V$ 的子空间，则 $V_{1}+\cdots+V_{m}$ 是直和当且仅当把 0 写成和 $v_{1}+\cdots+v_{m}$（每个 $v_{k}\in V_{k}$）的唯一方式是每个 $v_{k}=0$。

**K-1503 判定 1.46：两个子空间的直和**

设 $U$ 和 $W$ 是 $V$ 的子空间，则

$$
U+W\ \text{是直和}\iff U\cap W=\{0\}.
$$

**K-1521 注：多于两个子空间的情形**

上述结论只处理两个子空间。询问多于两个子空间是否构成直和时，只检验每对子空间的交为 $\{0\}$ 是不够的（见例 1.44：其中 $V_{1}\cap V_{2}=V_{1}\cap V_{3}=V_{2}\cap V_{3}=\{0\}$，但和不是直和）。

**K-1523 注：与并/不交并的类比**

子空间的和类似于集合的并；子空间的直和类似于集合的不交并（disjoint union）。向量空间的两个子空间不可能不相交（都含 0），所以在两个子空间的情形，「不相交」被「交等于 $\{0\}$」取代。
