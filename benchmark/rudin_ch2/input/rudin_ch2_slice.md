## FINITE, COUNTABLE, AND UNCOUNTABLE SETS

We begin this section with a definition of the function concept.

2.1 Definition Consider two sets A and B, whose elements may be any objects whatsoever, and suppose that with each element x of A there is associated, in some manner, an element of B, which we denote by $f(x)$ . Then f is said to be a function from A to B (or a mapping of A into B). The set A is called the domain of f (we also say f is defined on A), and the elements $f(x)$ are called the values of f. The set of all values of f is called the range of f.

2.2 Definition Let $A$ and $B$ be two sets and let $f$ be a mapping of $A$ into $B$ . If $E \subset A, f(E)$ is defined to be the set of all elements $f(x)$ , for $x \in E$ . We call $f(E)$ the image of $E$ under $f$ . In this notation, $f(A)$ is the range of $f$ . It is clear that $f(A) \subset B$ . If $f(A) = B$ , we say that $f$ maps $A$ onto $B$ . (Note that, according to this usage, onto is more specific than into.)

If $E \subset B, f^{-1}(E)$ denotes the set of all $x \in A$ such that $f(x) \in E$ . We call $f^{-1}(E)$ the inverse image of $E$ under $f$ . If $y \in B, f^{-1}(y)$ is the set of all $x \in A$ such that $f(x) = y$ . If, for each $y \in B, f^{-1}(y)$ consists of at most one element of $A$ , then $f$ is said to be a 1-1 (one-to-one) mapping of $A$ into $B$ . This may also be expressed as follows: $f$ is a 1-1 mapping of $A$ into $B$ provided that $f(x_1) \neq f(x_2)$ whenever $x_1 \neq x_2, x_1 \in A, x_2 \in A$ .

(The notation $x_{1} \neq x_{2}$ means that $x_{1}$ and $x_{2}$ are distinct elements; otherwise we write $x_{1} = x_{2}$ .)

2.3 Definition If there exists a 1-1 mapping of A onto B, we say that A and B can be put in 1-1 correspondence, or that A and B have the same cardinal number, or, briefly, that A and B are equivalent, and we write $A \sim B$ . This relation clearly has the following properties:

It is reflexive: $A \sim A$ .

It is symmetric: If $A \sim B$ , then $B \sim A$ .

It is transitive: If $A \sim B$ and $B \sim C$ , then $A \sim C$ .

Any relation with these three properties is called an equivalence relation.

2.4 Definition For any positive integer n, let $J_{n}$ be the set whose elements are the integers 1, 2, ..., n; let J be the set consisting of all positive integers. For any set A, we say:

(a) $A$ is finite if $A \sim J_{n}$ for some $n$ (the empty set is also considered to be finite).

(b) $A$ is infinite if $A$ is not finite.

(c) $A$ is countable if $A \sim J$ .

(d) $A$ is uncountable if $A$ is neither finite nor countable.

(e) $A$ is at most countable if $A$ is finite or countable.

Countable sets are sometimes called enumerable, or denumerable.

For two finite sets A and B, we evidently have $A \sim B$ if and only if A and B contain the same number of elements. For infinite sets, however, the idea of “having the same number of elements” becomes quite vague, whereas the notion of 1-1 correspondence retains its clarity.

2.5 Example Let A be the set of all integers. Then A is countable. For, consider the following arrangement of the sets A and J:

$$
A: \quad 0, 1, - 1, 2, - 2, 3, - 3, \dots
$$

$$
J \colon \qquad 1, 2, 3, 4, 5, 6, 7, \ldots
$$

We can, in this example, even give an explicit formula for a function $f$ from $J$ to $A$ which sets up a 1-1 correspondence:

$$
f (n) = \left\{ \begin{array}{l l} \frac {n}{2} & (n \text {   even }), \\ - \frac {n - 1}{2} & (n \text {   odd }). \end{array} \right.
$$

2.6 Remark A finite set cannot be equivalent to one of its proper subsets. That this is, however, possible for infinite sets, is shown by Example 2.5, in which J is a proper subset of A.

In fact, we could replace Definition 2.4(b) by the statement: A is infinite if A is equivalent to one of its proper subsets.

2.7 Definition By a sequence, we mean a function $f$ defined on the set $J$ of all positive integers. If $f(n) = x_n$ , for $n \in J$ , it is customary to denote the sequence $f$ by the symbol $\{x_n\}$ , or sometimes by $x_1, x_2, x_3, \ldots$ . The values of $f$ , that is, the elements $x_n$ , are called the terms of the sequence. If $A$ is a set and if $x_n \in A$ for all $n \in J$ , then $\{x_n\}$ is said to be a sequence in $A$ , or a sequence of elements of $A$ .

Note that the terms $x_{1}, x_{2}, x_{3}, \ldots$ of a sequence need not be distinct.

Since every countable set is the range of a 1-1 function defined on J, we may regard every countable set as the range of a sequence of distinct terms. Speaking more loosely, we may say that the elements of any countable set can be “arranged in a sequence.”

Sometimes it is convenient to replace J in this definition by the set of all nonnegative integers, i.e., to start with 0 rather than with 1.

## 2.8 Theorem Every infinite subset of a countable set $A$ is countable.

Proof Suppose $E \subset A$ , and $E$ is infinite. Arrange the elements $x$ of $A$ in a sequence $\{x_n\}$ of distinct elements. Construct a sequence $\{n_k\}$ as follows:

Let $n_1$ be the smallest positive integer such that $x_{n_1} \in E$ . Having chosen $n_1, \ldots, n_{k-1} (k = 2, 3, 4, \ldots)$ , let $n_k$ be the smallest integer greater than $n_{k-1}$ such that $x_{n_k} \in E$ .

Putting $f(k) = x_{n_k}$ ( $k = 1, 2, 3, \ldots$ ), we obtain a 1-1 correspondence between $E$ and $J$ .

The theorem shows that, roughly speaking, countable sets represent the “smallest” infinity: No uncountable set can be a subset of a countable set.

2.9 Definition Let $A$ and $\Omega$ be sets, and suppose that with each element $\alpha$ of $A$ there is associated a subset of $\Omega$ which we denote by $E_{\alpha}$ .

The set whose elements are the sets $E_{\alpha}$ will be denoted by $\{E_{\alpha}\}$ . Instead of speaking of sets of sets, we shall sometimes speak of a collection of sets, or a family of sets.

The union of the sets $E_{\alpha}$ is defined to be the set $S$ such that $x \in S$ if and only if $x \in E_{\alpha}$ for at least one $\alpha \in A$ . We use the notation

$$
S = \bigcup_ {\alpha \in A} E _ {\alpha}.\tag{1}
$$

If $A$ consists of the integers $1, 2, \ldots, n$ , one usually writes

$$
S = \bigcup_ {m = 1} ^ {n} E _ {m}\tag{2}
$$

or

$$
S = E _ {1} \cup E _ {2} \cup \dots \cup E _ {n}.\tag{3}
$$

If $A$ is the set of all positive integers, the usual notation is

$$
S = \bigcup_ {m = 1} ^ {\infty} E _ {m}.\tag{4}
$$

The symbol $\infty$ in (4) merely indicates that the union of a countable collection of sets is taken, and should not be confused with the symbols $+\infty$ , $-\infty$ , introduced in Definition 1.23.

The intersection of the sets $E_{\alpha}$ is defined to be the set P such that $x \in P$ if and only if $x \in E_{\alpha}$ for every $\alpha \in A$ . We use the notation

$$
P = \bigcap_ {\alpha \in A} E _ {\alpha},\tag{5}
$$

or

$$
P = \bigcap_ {m = 1} ^ {n} E _ {m} = E _ {1} \cap E _ {2} \cap \dots \cap E _ {n},\tag{6}
$$

or

$$
P = \bigcap_ {m = 1} ^ {\infty} E _ {m},\tag{7}
$$

as for unions. If $A \cap B$ is not empty, we say that $A$ and $B$ intersect; otherwise they are disjoint.

## 2.10 Examples

(a) Suppose $E_1$ consists of 1, 2, 3 and $E_2$ consists of 2, 3, 4. Then $E_1 \cup E_2$ consists of 1, 2, 3, 4, whereas $E_1 \cap E_2$ consists of 2, 3.

(b) Let $A$ be the set of real numbers $x$ such that $0 < x \leq 1$ . For every $x \in A$ , let $E_x$ be the set of real numbers $y$ such that $0 < y < x$ . Then

(i)

$$
E _ {x} \subset E _ {z} \text {   if   and   only   if   } 0 <   x \leq z \leq 1;\tag{ii}
$$

$$
\bigcup E _ {x} = E _ {1};\tag{iii}
$$

$$
\bigcap_ {x \in A} ^ {x \in A} E _ {x} \text {   is   empty; }
$$

(i) and (ii) are clear. To prove (iii), we note that for every $y > 0$ , $y \notin E_x$ if $x < y$ . Hence $y \notin \bigcap_{x \in A} E_x$ .

2.11 Remarks Many properties of unions and intersections are quite similar to those of sums and products; in fact, the words sum and product were sometimes used in this connection, and the symbols $\Sigma$ and $\Pi$ were written in place of $\bigcup$ and $\bigcap$ .

The commutative and associative laws are trivial:

(8)

$$
A \cup B = B \cup A; \quad A \cap B = B \cap A.\tag{9}
$$

$$
(A \cup B) \cup C = A \cup (B \cup C); \quad (A \cap B) \cap C = A \cap (B \cap C).
$$

Thus the omission of parentheses in (3) and (6) is justified.

The distributive law also holds:

$$
A \cap (B \cup C) = (A \cap B) \cup (A \cap C).\tag{10}
$$

To prove this, let the left and right members of (10) be denoted by $E$ and $F$ , respectively.

Suppose $x \in E$ . Then $x \in A$ and $x \in B \cup C$ , that is, $x \in B$ or $x \in C$ (possibly both). Hence $x \in A \cap B$ or $x \in A \cap C$ , so that $x \in F$ . Thus $E \subset F$ .

Next, suppose $x \in F$ . Then $x \in A \cap B$ or $x \in A \cap C$ . That is, $x \in A$ , and $x \in B \cup C$ . Hence $x \in A \cap (B \cup C)$ , so that $F \subset E$ .

It follows that E = F.

We list a few more relations which are easily verified:

(11)

$$
A \subset A \cup B,\tag{12}
$$

$$
A \cap B \subset A.
$$

If 0 denotes the empty set, then

$$
A \cup 0 = A, \quad A \cap 0 = 0.\tag{13}
$$

If $A \subset B$ , then

$$
A \cup B = B, \quad A \cap B = A.\tag{14}
$$

(17)

2.12 Theorem Let $\{E_n\}$ , $n = 1, 2, 3, \ldots$ , be a sequence of countable sets, and put

$$
S = \bigcup_ {n = 1} ^ {\infty} E _ {n}.\tag{15}
$$

Then $S$ is countable.

Proof Let every set $E_{n}$ be arranged in a sequence $\{x_{nk}\}, k=1,2,3,\ldots,$ and consider the infinite array

(16)

![](images/7c0871eb694273271fb0d6984d5b4c01a182f452cf914e947542c3e6db562e0e.jpg)

in which the elements of $E_{n}$ form the nth row. The array contains all elements of S. As indicated by the arrows, these elements can be arranged in a sequence

$$
x _ {1 1}; x _ {2 1}, x _ {1 2}; x _ {3 1}, x _ {2 2}, x _ {1 3}; x _ {4 1}, x _ {3 2}, x _ {2 3}, x _ {1 4}; \dots
$$

If any two of the sets $E_{n}$ have elements in common, these will appear more than once in (17). Hence there is a subset T of the set of all positive integers such that $S \sim T$ , which shows that S is at most countable (Theorem 2.8). Since $E_{1} \subset S$ , and $E_{1}$ is infinite, S is infinite, and thus countable.

Corollary Suppose A is at most countable, and, for every $\alpha \in A$ , $B_{\alpha}$ is at most countable. Put

$$
T = \bigcup_ {\alpha \in A} B _ {\alpha}.
$$

Then $T$ is at most countable.

For T is equivalent to a subset of (15).

2.13 Theorem Let A be a countable set, and let $B_{n}$ be the set of all n-tuples $(a_{1},\ldots,a_{n})$ , where $a_{k}\in A$ ( $k=1,\ldots,n$ ), and the elements $a_{1},\ldots,a_{n}$ need not be distinct. Then $B_{n}$ is countable.

Proof That $B_{1}$ is countable is evident, since $B_{1} = A$ . Suppose $B_{n-1}$ is countable ( $n = 2, 3, 4, \ldots$ ). The elements of $B_{n}$ are of the form

$$
(b, a) \quad (b \in B _ {n - 1}, a \in A).\tag{18}
$$

For every fixed b, the set of pairs $(b, a)$ is equivalent to A, and hence countable. Thus $B_{n}$ is the union of a countable set of countable sets. By Theorem 2.12, $B_{n}$ is countable.

The theorem follows by induction.

Corollary The set of all rational numbers is countable.

Proof We apply Theorem 2.13, with n = 2, noting that every rational r is of the form b/a, where a and b are integers. The set of pairs $(a, b)$ , and therefore the set of fractions b/a, is countable.

In fact, even the set of all algebraic numbers is countable (see Exercise 2).

That not all infinite sets are, however, countable, is shown by the next theorem.

2.14 Theorem Let $A$ be the set of all sequences whose elements are the digits 0 and 1. This set $A$ is uncountable.

The elements of $A$ are sequences like 1, 0, 0, 1, 0, 1, 1, 1, ....

Proof Let E be a countable subset of A, and let E consist of the sequences $s_{1}, s_{2}, s_{3}, \ldots$ . We construct a sequence s as follows. If the nth digit in $s_{n}$ is 1, we let the nth digit of s be 0, and vice versa. Then the sequence s differs from every member of E in at least one place; hence $s \notin E$ . But clearly $s \in A$ , so that E is a proper subset of A.

We have shown that every countable subset of A is a proper subset of A. It follows that A is uncountable (for otherwise A would be a proper subset of A, which is absurd).

The idea of the above proof was first used by Cantor, and is called Cantor's diagonal process; for, if the sequences $s_{1}, s_{2}, s_{3}, \ldots$ are placed in an array like (16), it is the elements on the diagonal which are involved in the construction of the new sequence.

Readers who are familiar with the binary representation of the real numbers (base 2 instead of 10) will notice that Theorem 2.14 implies that the set of all real numbers is uncountable. We shall give a second proof of this fact in Theorem 2.43.

## METRIC SPACES

2.15 Definition A set X, whose elements we shall call points, is said to be a metric space if with any two points p and q of X there is associated a real number $d(p, q)$ , called the distance from p to q, such that

(a) $d(p,q) > 0$ if $p\neq q$ ; $d(p,p) = 0$

(b) $d(p,q) = d(q,p);$

(c) $d(p,q)\leq d(p,r) + d(r,q)$ , for any $r\in X$

Any function with these three properties is called a distance function, or a metric.

2.16 Examples The most important examples of metric spaces, from our standpoint, are the euclidean spaces $R^{k}$ , especially $R^{1}$ (the real line) and $R^{2}$ (the complex plane); the distance in $R^{k}$ is defined by

$$
d (\mathbf {x}, \mathbf {y}) = | \mathbf {x} - \mathbf {y} | \quad (\mathbf {x}, \mathbf {y} \in R ^ {k}).\tag{19}
$$

By Theorem 1.37, the conditions of Definition 2.15 are satisfied by (19).

It is important to observe that every subset Y of a metric space X is a metric space in its own right, with the same distance function. For it is clear that if conditions (a) to (c) of Definition 2.15 hold for p, q, $r \in X$ , they also hold if we restrict p, q, r to lie in Y.

Thus every subset of a euclidean space is a metric space. Other examples are the spaces $\mathcal{C}(K)$ and $\mathcal{L}^{2}(\mu)$ , which are discussed in Chaps. 7 and 11, respectively.

2.17 Definition By the segment $(a, b)$ we mean the set of all real numbers $x$ such that $a < x < b$ .

By the interval $[a, b]$ we mean the set of all real numbers $x$ such that $a \leq x \leq b$ .

Occasionally we shall also encounter “half-open intervals” [a, b) and (a, b]; the first consists of all x such that $a \leq x < b$ , the second of all x such that $a < x \leq b$ .

If $a_i < b_i$ for $i = 1, \ldots, k$ , the set of all points $\mathbf{x} = (x_1, \ldots, x_k)$ in $R^k$ whose coordinates satisfy the inequalities $a_i \leq x_i \leq b_i$ ( $1 \leq i \leq k$ ) is called a $k$ -cell. Thus a 1-cell is an interval, a 2-cell is a rectangle, etc.

If $\mathbf{x} \in R^k$ and $r > 0$ , the open (or closed) ball $B$ with center at $\mathbf{x}$ and radius $r$ is defined to be the set of all $\mathbf{y} \in R^k$ such that $|\mathbf{y} - \mathbf{x}| < r$ (or $|\mathbf{y} - \mathbf{x}| \leq r$ ).

We call a set $E \subset R^k$ convex if

$$
\lambda \mathbf {x} + (1 - \lambda) \mathbf {y} \in E
$$

whenever $\mathbf{x} \in E, \mathbf{y} \in E$ , and $0 < \lambda < 1$ .

For example, balls are convex. For if $|\mathbf{y} - \mathbf{x}| < r$ , $|\mathbf{z} - \mathbf{x}| < r$ , and $0 < \lambda < 1$ , we have

$$
\begin{array}{r l} | \lambda \mathbf {y} + (1 - \lambda) \mathbf {z} - \mathbf {x} | & = | \lambda (\mathbf {y} - \mathbf {x}) + (1 - \lambda) (\mathbf {z} - \mathbf {x}) | \\ & \leq \lambda | \mathbf {y} - \mathbf {x} | + (1 - \lambda) | \mathbf {z} - \mathbf {x} | <   \lambda r + (1 - \lambda) r \\ & = r. \end{array}
$$

The same proof applies to closed balls. It is also easy to see that k-cells are convex.

2.18 Definition Let $X$ be a metric space. All points and sets mentioned below are understood to be elements and subsets of $X$ .

(a) A neighborhood of $p$ is a set $N_r(p)$ consisting of all $q$ such that $d(p, q) < r$ , for some $r > 0$ . The number $r$ is called the radius of $N_r(p)$ .

(b) A point $p$ is a limit point of the set $E$ if every neighborhood of $p$ contains a point $q \neq p$ such that $q \in E$ .

(c) If $p \in E$ and $p$ is not a limit point of $E$ , then $p$ is called an isolated point of $E$ .

(d) $E$ is closed if every limit point of $E$ is a point of $E$ .

(e) A point $p$ is an interior point of $E$ if there is a neighborhood $N$ of $p$ such that $N \subset E$ .

(f) $E$ is open if every point of $E$ is an interior point of $E$ .

(g) The complement of $E$ (denoted by $E^c$ ) is the set of all points $p \in X$ such that $p \notin E$ .

(h) $E$ is perfect if $E$ is closed and if every point of $E$ is a limit point of $E$ .

(i) $E$ is bounded if there is a real number $M$ and a point $q \in X$ such that $d(p, q) < M$ for all $p \in E$ .

(j) $E$ is dense in $X$ if every point of $X$ is a limit point of $E$ , or a point of $E$ (or both).

Let us note that in $R^{1}$ neighborhoods are segments, whereas in $R^{2}$ neighborhoods are interiors of circles.

## 2.19 Theorem Every neighborhood is an open set.

Proof Consider a neighborhood $E = N_{r}(p)$ , and let q be any point of E. Then there is a positive real number h such that

$$
d (p, q) = r - h.
$$

For all points $s$ such that $d(q, s) < h$ , we have then

$$
d (p, s) \leq d (p, q) + d (q, s) <   r - h + h = r,
$$

so that $s \in E$ . Thus $q$ is an interior point of $E$ .

2.20 Theorem If p is a limit point of a set E, then every neighborhood of p contains infinitely many points of E.

Proof Suppose there is a neighborhood N of p which contains only a finite number of points of E. Let $q_{1}, \ldots, q_{n}$ be those points of $N \cap E$ , which are distinct from p, and put

$$
r = \min _ {1 \leq m \leq n} d (p, q _ {m})
$$

[we use this notation to denote the smallest of the numbers $d(p, q_{1}), \ldots, d(p, q_{n})$ ]. The minimum of a finite set of positive numbers is clearly positive, so that r > 0.

The neighborhood $N_{r}(p)$ contains no point q of E such that $q \neq p$ , so that p is not a limit point of E. This contradiction establishes the theorem.

## Corollary A finite point set has no limit points.

2.21 Examples Let us consider the following subsets of $R^{2}$ :

(a) The set of all complex $z$ such that $|z| < 1$ .

(b) The set of all complex $z$ such that $|z| \leq 1$ .

(c) A nonempty finite set.

(d) The set of all integers.

(e) The set consisting of the numbers $1/n$ ( $n = 1, 2, 3, \ldots$ ). Let us note that this set $E$ has a limit point (namely, $z = 0$ ) but that no point of $E$ is a limit point of $E$ ; we wish to stress the difference between having a limit point and containing one.

(f) The set of all complex numbers (that is, $R^2$ ).

(g) The segment $(a, b)$ .

Let us note that $(d), (e), (g)$ can be regarded also as subsets of $R^1$ . Some properties of these sets are tabulated below:

<table><tr><td></td><td>Closed</td><td>Open</td><td>Perfect</td><td>Bounded</td></tr><tr><td>(a)</td><td>No</td><td>Yes</td><td>No</td><td>Yes</td></tr><tr><td>(b)</td><td>Yes</td><td>No</td><td>Yes</td><td>Yes</td></tr><tr><td>(c)</td><td>Yes</td><td>No</td><td>No</td><td>Yes</td></tr><tr><td>(d)</td><td>Yes</td><td>No</td><td>No</td><td>No</td></tr><tr><td>(e)</td><td>No</td><td>No</td><td>No</td><td>Yes</td></tr><tr><td>(f)</td><td>Yes</td><td>Yes</td><td>Yes</td><td>No</td></tr><tr><td>(g)</td><td>No</td><td></td><td>No</td><td>Yes</td></tr></table>

In $(g)$ , we left the second entry blank. The reason is that the segment $(a, b)$ is not open if we regard it as a subset of $R^2$ , but it is an open subset of $R^1$ .

## 2.22 Theorem Let $\{E_{\alpha}\}$ be a (finite or infinite) collection of sets $E_{\alpha}$ . Then

$$
\left(\bigcup_ {\alpha} E _ {\alpha}\right) ^ {c} = \bigcap_ {\alpha} (E _ {\alpha} ^ {c}).
$$

Proof Let $A$ and $B$ be the left and right members of (20). If $x \in A$ , then $x \notin \bigcup_{\alpha} E_{\alpha}$ , hence $x \notin E_{\alpha}$ for any $\alpha$ , hence $x \in E_{\alpha}^{c}$ for every $\alpha$ , so that $x \in \bigcap E_{\alpha}^{c}$ . Thus $A \subset B$ .

Conversely, if $x \in B$ , then $x \in E_{\alpha}^{c}$ for every $\alpha$ , hence $x \notin E_{\alpha}$ for any $\alpha$ , hence $x \notin \bigcup_{\alpha} E_{\alpha}$ , so that $x \in (\bigcup_{\alpha} E_{\alpha})^{c}$ . Thus $B \subset A$ .

It follows that A = B.

## 2.23 Theorem A set E is open if and only if its complement is closed.

Proof First, suppose $E^c$ is closed. Choose $x \in E$ . Then $x \notin E^c$ , and $x$ is not a limit point of $E^c$ . Hence there exists a neighborhood $N$ of $x$ such that $E^c \cap N$ is empty, that is, $N \subset E$ . Thus $x$ is an interior point of $E$ , and $E$ is open.

Next, suppose $E$ is open. Let $x$ be a limit point of $E^c$ . Then every neighborhood of $x$ contains a point of $E^c$ , so that $x$ is not an interior point of $E$ . Since $E$ is open, this means that $x \in E^c$ . It follows that $E^c$ is closed.

Corollary A set F is closed if and only if its complement is open.

## 2.24 Theorem

(a) For any collection $\{G_{\alpha}\}$ of open sets, $\bigcup_{\alpha} G_{\alpha}$ is open.

(b) For any collection $\{F_{\alpha}\}$ of closed sets, $\bigcap_{\alpha} F_{\alpha}$ is closed.

(c) For any finite collection $G_{1}, \ldots, G_{n}$ of open sets, $\bigcap_{i=1}^{n} G_{i}$ is open.

(d) For any finite collection $F_{1}, \ldots, F_{n}$ of closed sets, $\bigcup_{i=1}^{n} F_{i}$ is closed.

Proof Put $G = \bigcup_{\alpha} G_{\alpha}$ . If $x \in G$ , then $x \in G_{\alpha}$ for some $\alpha$ . Since $x$ is an interior point of $G_{\alpha}$ , $x$ is also an interior point of $G$ , and $G$ is open. This proves (a).

By Theorem 2.22,

$$
\left(\bigcap_ {\alpha} F _ {\alpha}\right) ^ {c} = \bigcup_ {\alpha} \left(F _ {\alpha} ^ {c}\right),\tag{21}
$$

and $F_{\alpha}^{c}$ is open, by Theorem 2.23. Hence (a) implies that (21) is open so that $\bigcap_{\alpha} F_{\alpha}$ is closed.

Next, put $H = \bigcap_{i=1}^{n} G_i$ . For any $x \in H$ , there exist neighborhoods $N_i$ of $x$ , with radii $r_i$ , such that $N_i \subset G_i (i = 1, \ldots, n)$ . Put

$$
r = \min (r _ {1}, \dots , r _ {n}),
$$

and let $N$ be the neighborhood of $x$ of radius $r$ . Then $N \subset G_i$ for $i = 1, \ldots, n$ , so that $N \subset H$ , and $H$ is open.

By taking complements, (d) follows from (c):

$$
\left(\bigcup_ {i = 1} ^ {n} F _ {i}\right) ^ {c} = \bigcap_ {i = 1} ^ {n} (F _ {i} ^ {c}).
$$

2.25 Examples In parts (c) and (d) of the preceding theorem, the finiteness of the collections is essential. For let $G_{n}$ be the segment $\left(-\frac{1}{n}, \frac{1}{n}\right) (n = 1, 2, 3, \ldots)$ . Then $G_{n}$ is an open subset of $R^{1}$ . Put $G = \bigcap_{n=1}^{\infty} G_{n}$ . Then $G$ consists of a single point (namely, $x = 0$ ) and is therefore not an open subset of $R^{1}$ .

Thus the intersection of an infinite collection of open sets need not be open. Similarly, the union of an infinite collection of closed sets need not be closed.

2.26 Definition If X is a metric space, if $E \subset X$ , and if $E'$ denotes the set of all limit points of E in X, then the closure of E is the set $\bar{E} = E \cup E'$ .

2.27 Theorem If $X$ is a metric space and $E \subset X$ , then

(a) $\bar{E}$ is closed,

(b) $E = \bar{E}$ if and only if $E$ is closed,

(c) $\bar{E} \subset F$ for every closed set $F \subset X$ such that $E \subset F$ .

By (a) and (c), $\bar{E}$ is the smallest closed subset of X that contains E.

Proof

(a) If $p \in X$ and $p \notin \bar{E}$ then $p$ is neither a point of $E$ nor a limit point of $E$ . Hence $p$ has a neighborhood which does not intersect $E$ . The complement of $\bar{E}$ is therefore open. Hence $\bar{E}$ is closed.

(b) If $E = \bar{E}$ , (a) implies that $E$ is closed. If $E$ is closed, then $E' \subset E$ [by Definitions 2.18(d) and 2.26], hence $\bar{E} = E$ .

(c) If $F$ is closed and $F \supset E$ , then $F \supset F'$ , hence $F \supset E'$ . Thus $F \supset \overline{E}$ .

2.28 Theorem Let $E$ be a nonempty set of real numbers which is bounded above. Let $y = \sup E$ . Then $y \in \overline{E}$ . Hence $y \in E$ if $E$ is closed.

Compare this with the examples in Sec. 1.9.

Proof If $y \in E$ then $y \in \bar{E}$ . Assume $y \notin E$ . For every h > 0 there exists then a point $x \in E$ such that y - h < x < y, for otherwise y - h would be an upper bound of E. Thus y is a limit point of E. Hence $y \in \bar{E}$ .

2.29 Remark Suppose $E \subset Y \subset X$ , where X is a metric space. To say that E is an open subset of X means that to each point $p \in E$ there is associated a positive number r such that the conditions $d(p, q) < r$ , $q \in X$ imply that $q \in E$ . But we have already observed (Sec. 2.16) that Y is also a metric space, so that our definitions may equally well be made within Y. To be quite explicit, let us say that E is open relative to Y if to each $p \in E$ there is associated an r > 0 such that $q \in E$ whenever $d(p, q) < r$ and $q \in Y$ . Example 2.21(g) showed that a set may be open relative to Y without being an open subset of X. However, there is a simple relation between these concepts, which we now state.

2.30 Theorem Suppose $Y \subset X$ . A subset $E$ of $Y$ is open relative to $Y$ if and only if $E = Y \cap G$ for some open subset $G$ of $X$ .

Proof Suppose E is open relative to Y. To each $p \in E$ there is a positive number $r_{p}$ such that the conditions $d(p, q) < r_{p}, q \in Y$ imply that $q \in E$ . Let $V_{p}$ be the set of all $q \in X$ such that $d(p, q) < r_{p}$ , and define

$$
G = \bigcup_ {p \in E} V _ {p}.
$$

Then $G$ is an open subset of $X$ , by Theorems 2.19 and 2.24.

Since $p \in V_p$ for all $p \in E$ , it is clear that $E \subset G \cap Y$ .

By our choice of $V_{p}$ , we have $V_{p} \cap Y \subset E$ for every $p \in E$ , so that $G \cap Y \subset E$ . Thus $E = G \cap Y$ , and one half of the theorem is proved.

Conversely, if $G$ is open in $X$ and $E = G \cap Y$ , every $p \in E$ has a neighborhood $V_{p} \subset G$ . Then $V_{p} \cap Y \subset E$ , so that $E$ is open relative to $Y$ .

## COMPACT SETS

2.31 Definition By an open cover of a set $E$ in a metric space $X$ we mean a collection $\{G_{\alpha}\}$ of open subsets of $X$ such that $E \subset \bigcup_{\alpha} G_{\alpha}$ .

2.32 Definition A subset $K$ of a metric space $X$ is said to be compact if every open cover of $K$ contains a finite subcover.

More explicitly, the requirement is that if $\{G_{\alpha}\}$ is an open cover of $K$ , then there are finitely many indices $\alpha_{1},\ldots ,\alpha_{n}$ such that

$$
K \subset G _ {\alpha_ {1}} \cup \dots \cup G _ {\alpha_ {n}}.
$$

The notion of compactness is of great importance in analysis, especially in connection with continuity (Chap. 4).

It is clear that every finite set is compact. The existence of a large class of infinite compact sets in $R^k$ will follow from Theorem 2.41.

We observed earlier (in Sec. 2.29) that if $E \subset Y \subset X$ , then $E$ may be open relative to $Y$ without being open relative to $X$ . The property of being open thus depends on the space in which $E$ is embedded. The same is true of the property of being closed.

Compactness, however, behaves better, as we shall now see. To formulate the next theorem, let us say, temporarily, that K is compact relative to X if the requirements of Definition 2.32 are met.

2.33 Theorem Suppose $K \subset Y \subset X$ . Then K is compact relative to X if and only if K is compact relative to Y.

By virtue of this theorem we are able, in many situations, to regard compact sets as metric spaces in their own right, without paying any attention to any embedding space. In particular, although it makes little sense to talk of open spaces, or of closed spaces (every metric space X is an open subset of itself, and is a closed subset of itself), it does make sense to talk of compact metric spaces.

Proof Suppose K is compact relative to X, and let $\{V_{\alpha}\}$ be a collection of sets, open relative to Y, such that $K \subset \bigcup_{\alpha} V_{\alpha}$ . By theorem 2.30, there are sets $G_{\alpha}$ , open relative to X, such that $V_{\alpha} = Y \cap G_{\alpha}$ , for all $\alpha$ ; and since K is compact relative to X, we have

$$
K \subset G _ {\alpha_ {1}} \cup \dots \cup G _ {\alpha_ {n}}\tag{22}
$$

for some choice of finitely many indices $\alpha_{1},\ldots ,\alpha_{n}$ . Since $K\subset Y$ , (22) implies

$$
K \subset V _ {\alpha_ {1}} \cup \dots \cup V _ {\alpha_ {n}}.\tag{23}
$$

This proves that $K$ is compact relative to $Y$ .

Conversely, suppose $K$ is compact relative to $Y$ , let $\{G_{\alpha}\}$ be a collection of open subsets of $X$ which covers $K$ , and put $V_{\alpha} = Y \cap G_{\alpha}$ . Then (23) will hold for some choice of $\alpha_{1}, \ldots, \alpha_{n}$ ; and since $V_{\alpha} \subset G_{\alpha}$ , (23) implies (22).

This completes the proof.

## 2.34 Theorem Compact subsets of metric spaces are closed.

Proof Let $K$ be a compact subset of a metric space $X$ . We shall prove that the complement of $K$ is an open subset of $X$ .

Suppose $p \in X, p \notin K$ . If $q \in K$ , let $V_q$ and $W_q$ be neighborhoods of $p$ and $q$ , respectively, of radius less than $\frac{1}{2} d(p, q)$ [see Definition 2.18(a)]. Since $K$ is compact, there are finitely many points $q_1, \ldots, q_n$ in $K$ such that

$$
K \subset W _ {q _ {1}} \cup \dots \cup W _ {q _ {n}} = W.
$$

If $V = V_{q_{1}} \cap \cdots \cap V_{q_{n}}$ , then V is a neighborhood of p which does not intersect W. Hence $V \subset K^{c}$ , so that p is an interior point of $K^{c}$ . The theorem follows.

## 2.35 Theorem Closed subsets of compact sets are compact.

Proof Suppose $F \subset K \subset X$ , F is closed (relative to X), and K is compact. Let $\{V_{\alpha}\}$ be an open cover of F. If $F^{c}$ is adjoined to $\{V_{\alpha}\}$ , we obtain an open cover $\Omega$ of $K$ . Since $K$ is compact, there is a finite subcollection $\Phi$ of $\Omega$ which covers $K$ , and hence $F$ . If $F^{c}$ is a member of $\Phi$ , we may remove it from $\Phi$ and still retain an open cover of $F$ . We have thus shown that a finite subcollection of $\{V_{\alpha}\}$ covers $F$ .

Corollary If $F$ is closed and $K$ is compact, then $F \cap K$ is compact.

Proof Theorems 2.24(b) and 2.34 show that $F \cap K$ is closed; since $F \cap K \subset K$ , Theorem 2.35 shows that $F \cap K$ is compact.

2.36 Theorem If $\{K_{\alpha}\}$ is a collection of compact subsets of a metric space $X$ such that the intersection of every finite subcollection of $\{K_{\alpha}\}$ is nonempty, then $\bigcap K_{\alpha}$ is nonempty.

Proof Fix a member $K_{1}$ of $\{K_{\alpha}\}$ and put $G_{\alpha}=K_{\alpha}^{c}$ . Assume that no point of $K_{1}$ belongs to every $K_{\alpha}$ . Then the sets $G_{\alpha}$ form an open cover of $K_{1}$ ; and since $K_{1}$ is compact, there are finitely many indices $\alpha_{1},\ldots,\alpha_{n}$ such that $K_{1}\subset G_{\alpha_{1}}\cup\cdots\cup G_{\alpha_{n}}$ . But this means that

$$
K _ {1} \cap K _ {\alpha_ {1}} \cap \dots \cap K _ {\alpha_ {n}}
$$

is empty, in contradiction to our hypothesis.

Corollary If $\{K_n\}$ is a sequence of nonempty compact sets such that $K_n \supset K_{n+1}$ ( $n = 1, 2, 3, \ldots$ ), then $\bigcap_{1}^{\infty} K_n$ is not empty.

2.37 Theorem If $E$ is an infinite subset of a compact set $K$ , then $E$ has a limit point in $K$ .

Proof If no point of $K$ were a limit point of $E$ , then each $q \in K$ would have a neighborhood $V_{q}$ which contains at most one point of $E$ (namely, $q$ , if $q \in E$ ). It is clear that no finite subcollection of $\{V_{q}\}$ can cover $E$ ; and the same is true of $K$ , since $E \subset K$ . This contradicts the compactness of $K$ .

2.38 Theorem If $\{I_n\}$ is a sequence of intervals in $R^1$ , such that $I_n \supset I_{n+1}$ ( $n = 1, 2, 3, \ldots$ ), then $\bigcap_1^\infty I_n$ is not empty.

Proof If $I_{n} = [a_{n}, b_{n}]$ , let E be the set of all $a_{n}$ . Then E is nonempty and bounded above (by $b_{1}$ ). Let x be the sup of E. If m and n are positive integers, then

$$
a _ {n} \leq a _ {m + n} \leq b _ {m + n} \leq b _ {m},
$$

so that $x \leq b_{m}$ for each $m$ . Since it is obvious that $a_{m} \leq x$ , we see that $x \in I_{m}$ for $m = 1, 2, 3, \ldots$ .

2.39 Theorem Let $k$ be a positive integer. If $\{I_n\}$ is a sequence of $k$ -cells such that $I_n \supset I_{n+1} (n = 1, 2, 3, \ldots)$ , then $\bigcap_1^\infty I_n$ is not empty.

Proof Let $I_{n}$ consist of all points $\mathbf{x} = (x_{1},\ldots ,x_{k})$ such that

$$
a _ {n, j} \leq x _ {j} \leq b _ {n, j} \quad (1 \leq j \leq k; n = 1, 2, 3, \dots),
$$

and put $I_{n,j} = [a_{n,j}, b_{n,j}]$ . For each $j$ , the sequence $\{I_{n,j}\}$ satisfies the hypotheses of Theorem 2.38. Hence there are real numbers $x_j^*(1 \leq j \leq k)$ such that

$$
a _ {n, j} \leq x _ {j} ^ {*} \leq b _ {n, j} \quad (1 \leq j \leq k; n = 1, 2, 3, \dots).
$$

Setting $\mathbf{x}^{*} = (x_{1}^{*},\ldots ,x_{k}^{*})$ , we see that $\mathbf{x}^{*}\in I_{n}$ for $n = 1,2,3,\ldots$ The theorem follows.

## 2.40 Theorem Every $k$ -cell is compact.

Proof Let $I$ be a $k$ -cell, consisting of all points $\mathbf{x} = (x_1, \ldots, x_k)$ such that $a_j \leq x_j \leq b_j$ ( $1 \leq j \leq k$ ). Put

$$
\delta = \left\{\sum_ {1} ^ {k} (b _ {j} - a _ {j}) ^ {2} \right\} ^ {1 / 2}.
$$

Then $|\mathbf{x} - \mathbf{y}| \leq \delta$ , if $\mathbf{x} \in I, \mathbf{y} \in I$ .

Suppose, to get a contradiction, that there exists an open cover $\{G_{\alpha}\}$ of I which contains no finite subcover of I. Put $c_{j} = (a_{j} + b_{j})/2$ . The intervals $[a_{j}, c_{j}]$ and $[c_{j}, b_{j}]$ then determine $2^{k} k$ -cells $Q_{i}$ whose union is I. At least one of these sets $Q_{i}$ , call it $I_{1}$ , cannot be covered by any finite subcollection of $\{G_{\alpha}\}$ (otherwise I could be so covered). We next subdivide $I_{1}$ and continue the process. We obtain a sequence $\{I_{n}\}$ with the following properties:

(a) $I \supset I_{1} \supset I_{2} \supset I_{3} \supset \cdots;$

(b) $I_{n}$ is not covered by any finite subcollection of $\{G_{\alpha}\}$ ;

(c) if $\mathbf{x} \in I_n$ and $\mathbf{y} \in I_n$ , then $|\mathbf{x} - \mathbf{y}| \leq 2^{-n}\delta$ .

By (a) and Theorem 2.39, there is a point $\mathbf{x}^*$ which lies in every $I_n$ . For some $\alpha, \mathbf{x}^* \in G_\alpha$ . Since $G_\alpha$ is open, there exists $r > 0$ such that $|\mathbf{y} - \mathbf{x}^*| < r$ implies that $\mathbf{y} \in G_\alpha$ . If $n$ is so large that $2^{-n}\delta < r$ (there is such an $n$ , for otherwise $2^n \leq \delta / r$ for all positive integers $n$ , which is absurd since $R$ is archimedean), then (c) implies that $I_n \subset G_\alpha$ , which contradicts (b).

This completes the proof.

The equivalence of (a) and (b) in the next theorem is known as the Heine-Borel theorem.

2.41 Theorem If a set $E$ in $R^k$ has one of the following three properties, then it has the other two:

(a) $E$ is closed and bounded.

(b) $E$ is compact.

(c) Every infinite subset of $E$ has a limit point in $E$ .

Proof If (a) holds, then $E \subset I$ for some k-cell I, and (b) follows from Theorems 2.40 and 2.35. Theorem 2.37 shows that (b) implies (c). It remains to be shown that (c) implies (a).

If E is not bounded, then E contains points $x_{n}$ with

$$
\left| \mathbf {x} _ {n} \right| > n \quad (n = 1, 2, 3, \dots).
$$

The set $S$ consisting of these points $\mathbf{x}_n$ is infinite and clearly has no limit point in $R^k$ , hence has none in $E$ . Thus (c) implies that $E$ is bounded.

If E is not closed, then there is a point $x_{0} \in R^{k}$ which is a limit point of E but not a point of E. For $n = 1, 2, 3, \ldots$ , there are points $x_{n} \in E$ such that $|x_{n} - x_{0}| < 1/n$ . Let S be the set of these points $x_{n}$ . Then S is infinite (otherwise $|x_{n} - x_{0}|$ would have a constant positive value, for infinitely many n), S has $x_{0}$ as a limit point, and S has no other limit point in $R^{k}$ . For if $y \in R^{k}, y \neq x_{0}$ , then

$$
\begin{array}{r l} & {| \mathbf {x} _ {n} - \mathbf {y} | \geq | \mathbf {x} _ {0} - \mathbf {y} | - | \mathbf {x} _ {n} - \mathbf {x} _ {0} |} \\ & {\qquad \geq | \mathbf {x} _ {0} - \mathbf {y} | - \frac {1}{n} \geq \frac {1}{2} | \mathbf {x} _ {0} - \mathbf {y} |} \end{array}
$$

for all but finitely many $n$ ; this shows that $\mathbf{y}$ is not a limit point of $S$ (Theorem 2.20).

Thus S has no limit point in E; hence E must be closed if (c) holds.

We should remark, at this point, that (b) and (c) are equivalent in any metric space (Exercise 26) but that (a) does not, in general, imply (b) and (c). Examples are furnished by Exercise 16 and by the space $L^{2}$ , which is discussed in Chap. 11.

## 2.42 Theorem (Weierstrass) Every bounded infinite subset of $R^{k}$ has a limit point in $R^{k}$ .

Proof Being bounded, the set E in question is a subset of a k-cell $I \subset R^{k}$ . By Theorem 2.40, I is compact, and so E has a limit point in I, by Theorem 2.37.

## PERFECT SETS

## 2.43 Theorem Let P be a nonempty perfect set in $R^{k}$ . Then P is uncountable.

Proof Since $P$ has limit points, $P$ must be infinite. Suppose $P$ is countable, and denote the points of $P$ by $\mathbf{x}_1, \mathbf{x}_2, \mathbf{x}_3, \ldots$ . We shall construct a sequence $\{V_n\}$ of neighborhoods, as follows.

Let $V_{1}$ be any neighborhood of $\mathbf{x}_{1}$ . If $V_{1}$ consists of all $\mathbf{y} \in R^{k}$ such that $|\mathbf{y} - \mathbf{x}_{1}| < r$ , the closure $\overline{V}_{1}$ of $V_{1}$ is the set of all $\mathbf{y} \in R^{k}$ such that $|\mathbf{y} - \mathbf{x}_{1}| \leq r$ .

Suppose $V_{n}$ has been constructed, so that $V_{n} \cap P$ is not empty. Since every point of $P$ is a limit point of $P$ , there is a neighborhood $V_{n+1}$ such that (i) $\overline{V}_{n+1} \subset V_{n}$ , (ii) $\mathbf{x}_n \notin \overline{V}_{n+1}$ , (iii) $V_{n+1} \cap P$ is not empty. By (iii), $V_{n+1}$ satisfies our induction hypothesis, and the construction can proceed.

Put $K_{n} = \overline{V}_{n} \cap P$ . Since $\overline{V}_{n}$ is closed and bounded, $\overline{V}_{n}$ is compact. Since $\mathbf{x}_n \notin K_{n+1}$ , no point of $P$ lies in $\bigcap_{1}^{\infty} K_{n}$ . Since $K_{n} \subset P$ , this implies that $\bigcap_{1}^{\infty} K_{n}$ is empty. But each $K_{n}$ is nonempty, by (iii), and $K_{n} \supset K_{n+1}$ , by (i); this contradicts the Corollary to Theorem 2.36.

Corollary Every interval $[a, b]$ ( $a < b$ ) is uncountable. In particular, the set of all real numbers is uncountable.

2.44 The Cantor set The set which we are now going to construct shows that there exist perfect sets in $R^1$ which contain no segment.

Let $E_0$ be the interval [0, 1]. Remove the segment $(\frac{1}{3}, \frac{2}{3})$ , and let $E_1$ be the union of the intervals

$$
[ 0, \frac {1}{3} ] [ \frac {2}{3}, 1 ].
$$

Remove the middle thirds of these intervals, and let $E_{2}$ be the union of the intervals

$$
[ 0, \frac {1}{9} ], [ \frac {2}{9}, \frac {3}{9} ], [ \frac {6}{9}, \frac {7}{9} ], [ \frac {8}{9}, 1 ].
$$

Continuing in this way, we obtain a sequence of compact sets $E_{n}$ , such that

(a) $E_{1} \supset E_{2} \supset E_{3} \supset \cdots;$

(b) $E_{n}$ is the union of $2^{n}$ intervals, each of length $3^{-n}$ .

The set

$$
P = \bigcap_ {n = 1} ^ {\infty} E _ {n}
$$

is called the Cantor set. $P$ is clearly compact, and Theorem 2.36 shows that $P$ is not empty.

No segment of the form

$$
\left(\frac {3 k + 1}{3 ^ {m}}, \frac {3 k + 2}{3 ^ {m}}\right),\tag{24}
$$

where k and m are positive integers, has a point in common with P. Since every segment $(\alpha, \beta)$ contains a segment of the form (24), if

$$
3 ^ {- m} <   \frac {\beta - \alpha}{6},
$$

$P$ contains no segment.

To show that P is perfect, it is enough to show that P contains no isolated point. Let $x \in P$ , and let S be any segment containing x. Let $I_{n}$ be that interval of $E_{n}$ which contains x. Choose n large enough, so that $I_{n} \subset S$ . Let $x_{n}$ be an endpoint of $I_{n}$ , such that $x_{n} \neq x$ .

It follows from the construction of $P$ that $x_{n} \in P$ . Hence $x$ is a limit point of $P$ , and $P$ is perfect.

One of the most interesting properties of the Cantor set is that it provides us with an example of an uncountable set of measure zero (the concept of measure will be discussed in Chap. 11).

## CONNECTED SETS

2.45 Definition Two subsets A and B of a metric space X are said to be separated if both $A \cap \overline{B}$ and $\overline{A} \cap B$ are empty, i.e., if no point of A lies in the closure of B and no point of B lies in the closure of A.

A set $E \subset X$ is said to be connected if E is not a union of two nonempty separated sets.

2.46 Remark Separated sets are of course disjoint, but disjoint sets need not be separated. For example, the interval [0, 1] and the segment (1, 2) are not separated, since 1 is a limit point of (1, 2). However, the segments (0, 1) and (1, 2) are separated.

The connected subsets of the line have a particularly simple structure:

2.47 Theorem A subset $E$ of the real line $R^1$ is connected if and only if it has the following property: If $x \in E$ , $y \in E$ , and $x < z < y$ , then $z \in E$ .

Proof If there exist $x \in E, y \in E$ , and some $z \in (x, y)$ such that $z \notin E$ , then $E = A_z \cup B_z$ where

$$
A _ {z} = E \cap (- \infty , z), \quad B _ {z} = E \cap (z, \infty).
$$

Since $x \in A_z$ and $y \in B_z$ , $A$ and $B$ are nonempty. Since $A_z \subset (-\infty, z)$ and $B_z \subset (z, \infty)$ , they are separated. Hence $E$ is not connected.

To prove the converse, suppose $E$ is not connected. Then there are nonempty separated sets $A$ and $B$ such that $A \cup B = E$ . Pick $x \in A, y \in B$ , and assume (without loss of generality) that $x < y$ . Define

$$
z = \sup (A \cap [ x, y ]).
$$

By Theorem 2.28, $z \in \overline{A}$ ; hence $z \notin B$ . In particular, $x \leq z < y$ .

If $z \notin A$ , it follows that $x < z < y$ and $z \notin E$ .

If $z \in A$ , then $z \notin \overline{B}$ , hence there exists $z_1$ such that $z < z_1 < y$ and $z_1 \notin B$ . Then $x < z_1 < y$ and $z_1 \notin E$ .

## EXERCISES

1. Prove that the empty set is a subset of every set.

2. A complex number $z$ is said to be algebraic if there are integers $a_0, \ldots, a_n$ , not all zero, such that

$$
a _ {0} z ^ {n} + a _ {1} z ^ {n - 1} + \dots + a _ {n - 1} z + a _ {n} = 0.
$$

Prove that the set of all algebraic numbers is countable. Hint: For every positive integer N there are only finitely many equations with

$$
n + \left| a _ {0} \right| + \left| a _ {1} \right| + \dots + \left| a _ {n} \right| = N.
$$

3. Prove that there exist real numbers which are not algebraic.

4. Is the set of all irrational real numbers countable?

5. Construct a bounded set of real numbers with exactly three limit points.

6. Let $E'$ be the set of all limit points of a set $E$ . Prove that $E'$ is closed. Prove that $E$ and $\bar{E}$ have the same limit points. (Recall that $\bar{E} = E \cup E'$ .) Do $E$ and $E'$ always have the same limit points?

7. Let $A_{1}, A_{2}, A_{3}, \ldots$ be subsets of a metric space.

(a) If $B_{n} = \bigcup_{i=1}^{n} A_{i}$ , prove that $\bar{B}_{n} = \bigcup_{i=1}^{n} \bar{A}_{i}$ , for $n = 1, 2, 3, \ldots$ .

(b) If $B = \bigcup_{i=1}^{\infty} A_i$ , prove that $\bar{B} \supset \bigcup_{i=1}^{\infty} \bar{A}_i$ .

Show, by an example, that this inclusion can be proper.

8. Is every point of every open set $E \subset R^2$ a limit point of $E$ ? Answer the same question for closed sets in $R^2$ .

9. Let $E^{\circ}$ denote the set of all interior points of a set $E$ . [See Definition 2.18(e); $E^{\circ}$ is called the interior of $E$ .]

(a) Prove that $E^{\circ}$ is always open.

(b) Prove that $E$ is open if and only if $E^{\circ} = E$ .

(c) If $G \subset E$ and $G$ is open, prove that $G \subset E^{\circ}$ .

(d) Prove that the complement of $E^{\circ}$ is the closure of the complement of $E$ .

(e) Do $E$ and $\bar{E}$ always have the same interiors?

(f) Do E and $E^{\circ}$ always have the same closures?

10. Let $X$ be an infinite set. For $p \in X$ and $q \in X$ , define

$$
d (p, q) = \left\{ \begin{array}{l l} 1 & \quad (\text { if } p \neq q) \\ 0 & \quad (\text { if } p = q). \end{array} \right.
$$

Prove that this is a metric. Which subsets of the resulting metric space are open? Which are closed? Which are compact?

11. For $x \in R^1$ and $y \in R^1$ , define

$$
d _ {1} (x, y) = (x - y) ^ {2},
$$

$$
d _ {2} (x, y) = \sqrt {| x - y |},
$$

$$
d _ {3} (x, y) = \left| x ^ {2} - y ^ {2} \right|,
$$

$$
d _ {4} (x, y) = | x - 2 y |,
$$

$$
d _ {5} (x, y) = \frac {| x - y |}{1 + | x - y |}.
$$

Determine, for each of these, whether it is a metric or not.

12. Let $K \subset R^1$ consist of 0 and the numbers $1/n$ , for $n = 1, 2, 3, \ldots$ . Prove that $K$ is compact directly from the definition (without using the Heine-Borel theorem).

13. Construct a compact set of real numbers whose limit points form a countable set.

14. Give an example of an open cover of the segment $(0, 1)$ which has no finite sub-cover.

15. Show that Theorem 2.36 and its Corollary become false (in $R^1$ , for example) if the word “compact” is replaced by “closed” or by “bounded.”

16. Regard $Q$ , the set of all rational numbers, as a metric space, with $d(p, q) = |p - q|$ . Let $E$ be the set of all $p \in Q$ such that $2 < p^2 < 3$ . Show that $E$ is closed and bounded in $Q$ , but that $E$ is not compact. Is $E$ open in $Q$ ?

17. Let $E$ be the set of all $x \in [0,1]$ whose decimal expansion contains only the digits 4 and 7. Is $E$ countable? Is $E$ dense in $[0,1]$ ? Is $E$ compact? Is $E$ perfect?

18. Is there a nonempty perfect set in $R^1$ which contains no rational number?

19. (a) If $A$ and $B$ are disjoint closed sets in some metric space $X$ , prove that they are separated.

(b) Prove the same for disjoint open sets.

(c) Fix $p \in X$ , $\delta > 0$ , define $A$ to be the set of all $q \in X$ for which $d(p, q) < \delta$ , define $B$ similarly, with $>$ in place of $<$ . Prove that $A$ and $B$ are separated.

(d) Prove that every connected metric space with at least two points is uncountable. Hint: Use (c).

20. Are closures and interiors of connected sets always connected? (Look at subsets of $R^2$ .)

21. Let $A$ and $B$ be separated subsets of some $R^k$ , suppose $\mathbf{a} \in A$ , $\mathbf{b} \in B$ , and define

$$
\mathbf {p} (t) = (1 - t) \mathbf {a} + t \mathbf {b}
$$

for $t \in R^1$ . Put $A_0 = \mathbf{p}^{-1}(A)$ , $B_0 = \mathbf{p}^{-1}(B)$ . [Thus $t \in A_0$ if and only if $\mathbf{p}(t) \in A$ .]

(a) Prove that $A_{0}$ and $B_{0}$ are separated subsets of $R^{1}$ .

(b) Prove that there exists $t_0 \in (0, 1)$ such that $\mathbf{p}(t_0) \notin A \cup B$ .

(c) Prove that every convex subset of $R^k$ is connected.

22. A metric space is called separable if it contains a countable dense subset. Show that $R^{k}$ is separable. Hint: Consider the set of points which have only rational coordinates.

23. A collection $\{V_{\alpha}\}$ of open subsets of $X$ is said to be a base for $X$ if the following is true: For every $x \in X$ and every open set $G \subset X$ such that $x \in G$ , we have $x \in V_{\alpha} \subset G$ for some $\alpha$ . In other words, every open set in $X$ is the union of a subcollection of $\{V_{\alpha}\}$ .

Prove that every separable metric space has a countable base. Hint: Take all neighborhoods with rational radius and center in some countable dense subset of X.

24. Let $X$ be a metric space in which every infinite subset has a limit point. Prove that $X$ is separable. Hint: Fix $\delta > 0$ , and pick $x_1 \in X$ . Having chosen $x_1, \ldots, x_j \in X$ , choose $x_{j+1} \in X$ , if possible, so that $d(x_i, x_{j+1}) \geq \delta$ for $i = 1, \ldots, j$ . Show that this process must stop after a finite number of steps, and that $X$ can therefore be covered by finitely many neighborhoods of radius $\delta$ . Take $\delta = 1/n (n = 1, 2, 3, \ldots)$ , and consider the centers of the corresponding neighborhoods.

25. Prove that every compact metric space $K$ has a countable base, and that $K$ is therefore separable. Hint: For every positive integer $n$ , there are finitely many neighborhoods of radius $1/n$ whose union covers $K$ .

26. Let X be a metric space in which every infinite subset has a limit point. Prove that X is compact. Hint: By Exercises 23 and 24, X has a countable base. It follows that every open cover of X has a countable subcover $\{G_{n}\}$ , $n = 1, 2, 3, \ldots$ . If no finite subcollection of $\{G_{n}\}$ covers X, then the complement $F_{n}$ of $G_{1} \cup \cdots \cup G_{n}$ is nonempty for each n, but $\bigcap F_{n}$ is empty. If E is a set which contains a point from each $F_{n}$ , consider a limit point of E, and obtain a contradiction.

27. Define a point $p$ in a metric space $X$ to be a condensation point of a set $E \subset X$ if every neighborhood of $p$ contains uncountably many points of $E$ .

Suppose $E \subset R^k$ , $E$ is uncountable, and let $P$ be the set of all condensation points of $E$ . Prove that $P$ is perfect and that at most countably many points of $E$ are not in $P$ . In other words, show that $P^c \cap E$ is at most countable. Hint: Let $\{V_n\}$ be a countable base of $R^k$ , let $W$ be the union of those $V_n$ for which $E \cap V_n$ is at most countable, and show that $P = W^c$ .

28. Prove that every closed set in a separable metric space is the union of a (possibly empty) perfect set and a set which is at most countable. (Corollary: Every countable closed set in $R^{k}$ has isolated points.) Hint: Use Exercise 27.

29. Prove that every open set in $R^1$ is the union of an at most countable collection of disjoint segments. Hint: Use Exercise 22.

30. Imitate the proof of Theorem 2.43 to obtain the following result:

If $R^k = \bigcup_{1}^{\infty} F_n$ , where each $F_n$ is a closed subset of $R^k$ , then at least one $F_n$ has a nonempty interior.

Equivalent statement: If $G_{n}$ is a dense open subset of $R^{k}$ , for $n = 1, 2, 3, \ldots$ , then $\bigcap_{1}^{\infty} G_{n}$ is not empty (in fact, it is dense in $R^{k}$ ).

(This is a special case of Baire's theorem; see Exercise 22, Chap. 3, for the general case.)

