# 第一章 数列（Sequences）：知识清单

- 源文件：sample_translation_textbook.md
- 范围：第 5--70 行，即“Chapter 1 Sequences”至“Chapter 2 Continuous Functions”之前。
- 以下按源文档顺序忠实翻译知识块；证明、教学解释和课后习题不列入本清单。

## K-009 1.1 定义：收敛数列（convergent sequence）

实数数列 $\{a_n\}$ 收敛到 $L$，是指：对每个 $\varepsilon>0$，存在正整数 $N$，使得当 $n\ge N$ 时，

$$
|a_n-L|<\varepsilon.
$$

记作 $a_n\to L$。

## K-019 1.2 定理：极限唯一性（uniqueness of limits）

若实数数列 $\{a_n\}$ 收敛，则它的极限唯一。

## K-027 1.3 例：倒数数列（reciprocal sequence）

数列 $a_n=1/n$ 收敛到 $0$。

## K-031 1.4 反例：有界数列（bounded sequence）不保证收敛

数列 $a_n=(-1)^n$ 有界但不收敛。因此，“每个有界数列都收敛”这一断言是错误的。

## K-035 1.5 备注：有限项修改（finite modification）不影响极限

改变一个收敛数列的有限多个项，不改变其极限。

## K-039 1.6 性质：极限的线性运算（linearity of limits）

若 $a_n\to A$、$b_n\to B$，且 $c$ 为常数，则

$$
a_n+b_n\to A+B,\qquad ca_n\to cA.
$$

## K-049 上尾集合（tail set）构造

对数列 $\{a_n\}$ 和正整数 $N$，它的第 $N$ 个上尾集合为

$$
T_N=\{a_n:n\ge N\}.
$$
