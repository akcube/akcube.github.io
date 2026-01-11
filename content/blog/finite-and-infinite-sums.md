---
author: Kishore Kumar
date: 2020-12-04 08:42:49+0530
doc: 2025-05-18 17:07:02+0530
tags:
- domain-math-analysis
title: Finite and Infinite Sums
---
# Finite and Infinite Sums

To understand the rearrangement theorem and it's many implications, we must first fully understand what a series is and what it means to find the sum of an **infinite** series. Let us begin by addressing the questions we raised in the introduction segment.

## Series

A series can be described as the sum of the terms of a given numerical sequence. Recall that a numerical sequence is simply an ordered list or collection of numbers where repetition is allowed. Consider the finite sequence of natural numbers from 1 to 10: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10.

The series corresponding to the terms of this sequence is:

$$\sum\limits_{k=1}^{10} k = 1 + 2 + 3 + \ldots + 10 = 55$$

This was an example of a finite sequence. Similarly, just like we can have finite and infinite sequences, we can have an infinite series. An infinite series is simply the sum of an infinite number of terms of a corresponding sequence. For example, if we extend the previous finite series to include the sum of all the natural numbers, we get:

$$\sum\limits_{k=1}^{\infty} k = 1 + 2 + 3 + \ldots$$

But what is the sum of an infinite series equal to? To answer this, let us begin by defining 2 different types of series. **Convergent** series and **divergent** series.

### Convergent series

We define a convergent series as a series who's sequence of partial sums tends to a limit.

Consider the following series,
$$S = \sum\limits_{k=1}^{\infty} \frac{1}{2^k} = \frac{1}{2} + \frac{1}{4} + \frac{1}{8} + \frac{1}{16} + \ldots$$
We now define a new term, **partial sums.** The $k^{th}$ partial sum of a series is defined as the sum of the first *k* terms of that series. The set of all the partial sums of an infinite series form an infinite sequence where the $n^{th}$ term of the sequence is equal to the $n^{th}$ partial sum of the series. Let $S_k$ denote the $k^{th}$ partial sum of our above defined series S. Then, the first few partial sums are as follows:
$$S_1 =  \sum\limits_{k=1}^{1} \frac{1}{2^k} = \frac{1}{2} = 1 - \frac{1}{2}$$
$$S_2 =  \sum\limits_{k=1}^{2} \frac{1}{2^k} = \frac{1}{2} + \frac{1}{4} = \frac{3}{4} = 1 - \frac{1}{4}$$
$$S_3 =  \sum\limits_{k=1}^{3} \frac{1}{2^k} = \frac{1}{2} + \frac{1}{4} + \frac{1}{8} = \frac{7}{8} = 1 - \frac{1}{8}$$
$$S_4 =  \sum\limits_{k=1}^{4} \frac{1}{2^k} = \frac{1}{2} + \frac{1}{4} + \frac{1}{8} + \frac{1}{16} = \frac{15}{16} = 1 - \frac{1}{16}$$
We can write down these partial sums as the beginning few terms of an infinite sequence,
$$\left\{ \ \frac{1}{2}, \  \frac{3}{4}, \  \frac{7}{8}, \  \frac{15}{16}, \ \ldots \  \right\}$$

Recall that the $n^{th}$ term of this sequence is the $n^{th}$ partial sum of the series. The $n^{th}$ partial sum of the series will also be the sum of our infinite series. We can now define the sum of an infinite series as the limit of the sequence of partial sums as *n* tends to infinity. If such a limit does not exist, we say that the series does not have a sum. Let us attempt to find the general term of this sequence, 
$$ 2s_{k}=\frac {2}{2}+\frac {2}{4}+\frac {2}{8}+\cdots +\frac {2}{2^{k}}=1+\left[\frac {1}{2}+\frac {1}{4}+\cdots +\frac {1}{2^{k-1}}\right]=1+\left[s_{k}-{\frac {1}{2^{k}}}\right]. $$
$$ s_k = 1 - \frac{1}{2^k}$$
$$2s_{k}=\frac {2}{2}+\frac {2}{4}+\frac {2}{8}+\cdots +\frac {2}{2^{k}}=1+\left[\frac {1}{2}+\frac {1}{4}+\cdots +\frac {1}{2^{k-1}}\right]=1+\left[s_{k}-{\frac {1}{2^{k}}}\right].$$
$$s_k = 1 - \frac{1}{2^k}$$

We can notice this occurrence in our listing of the first 4 partial sums of this series. As k tends to infinity, we have:

$$\lim_{k \to \infty} 1 - \frac{1}{2^k} = 1$$

Since the sequence of its partial sums tends to a limit, this is a convergent series who's sum is equal to the $n^{th}$ term of the sequence as n tends to infinity. Here,
$$S = \sum\limits_{k=1}^{\infty} \frac{1}{2^k} = \frac{1}{2} + \frac{1}{4} + \frac{1}{8} + \frac{1}{16} + \ldots = 1$$

### Divergent Series

A divergent series can be simply defined as a series which does not converge, i.e., a series is divergent if the infinite sequence of its partial sums does not have a finite limit. This is true if either the limit does not exist or it is equal to.

Consider the simple harmonic series,
$$S = \sum\limits_{k=1}^{\infty} \frac{1}{k} = 1 + \textcolor{red}{\frac{1}{2} + \frac{1}{3}}   + \textcolor{orange}{\frac{1}{4} + \frac{1}{5} + \frac{1}{6} + \frac{1}{7}} + \textcolor{purple}{\frac{1}{8} +\frac{1}{9} +\frac{1}{10} +\frac{1}{11} +\frac{1}{12} + \frac{1}{13} + \frac{1}{14} + \frac{1}{15}} + \textcolor{blue}{\frac{1}{16} \ldots}$$

Let $S_k$ represent the sum of the terms between the terms indexed $2^k$ (excluded) and $2^{k-1}$ (included) We make the following observations:
$$S_1 = 1 > \frac{1}{2}$$
$$S_2 = \textcolor{red}{\frac{1}{2} + \frac{1}{3}} > \frac{1}{2}$$
$$S_3 = \textcolor{orange}{\frac{1}{4} + \frac{1}{5} + \frac{1}{6} + \frac{1}{7}} > \frac{4}{8} = \frac{1}{2}$$
$$S_4 = \textcolor{purple}{\frac{1}{8} + \frac{1}{9} + \frac{1}{10} + \frac{1}{11} + \frac{1}{12} + \frac{1}{13} + \frac{1}{14} + \frac{1}{15}} > \frac{8}{16} = \frac{1}{2}$$
$$\vdots$$

We can write the series S as the sum of these segments $S_1$, $S_2$, $S_3$\... etc. Now, since each segment individually sums to a number greater than $\frac{1}{2}$, we can make the following relation:

$$S = S_1 + \textcolor{red}{S_2} + \textcolor{orange}{S_3} + \textcolor{purple}{S_4} + \textcolor{blue}{\ldots} > \frac{1}{2} + \textcolor{red}{\frac{1}{2}} + \textcolor{orange}{\frac{1}{2}} + \textcolor{purple}{\frac{1}{2}} + \textcolor{blue}{\ldots}$$

The sequence of partial sums of the series on the right $\left( \frac{1}{2} + \frac{1}{2} + \frac{1}{2} + \ldots \right)$ tends to $\infty$. Hence, we can say that, our simple harmonic series S diverges to $\infty$.

## Commutativity of Absolute Convergence

**If $\displaystyle \sum_{i=n}^m a_n$ is a series of complex numbers which converges absolutely, then every rearrangement of $\displaystyle \sum_{i=n}^m a_n$ converges to the same sum.**

Now we know that since $a_n$ is absolutely convergent,

$$\displaystyle \sum_{i=n}^m |a_i|\leq \epsilon$$

if $m\geq n\geq N$ for an integer N , given an $\epsilon$ \> 0 .

We choose p such that the integers 1,2,3..N are all present i the set $k_1,k_2,k_3...k_p$, which is the rearranged sequence . So if n\>p, the numbers, $a_1,a_2,a_3...a_n$ cancel out in the difference $s_n-S_n$, where $S_n$ is the sum of the rearranged sequence . Thus we get that, $s_n-S_n \leq \epsilon$ .Hence $S_n$ converges to the same value as $s_n$ .

**Commutative law for addition: a+b= b+a**

That is, the commutative law says rearranging the summands in a finite sum does not change the total.

But, that's not true for conditionally convergent series

Ex:(Alternating harmonic series)

$$1-\frac{1}{2}+\frac{1}{3}-\frac{1}{4}+\frac{1}{5}-\frac{1}{6}+\frac{1}{7}-\frac{1}{8}+\frac{1}{9}-\frac{1}{10}+...= ln2$$

Consider:

$$1-\frac{1}{2}-\frac{1}{4}+\frac{1}{3}-\frac{1}{6}-\frac{1}{8}+\frac{1}{5}-\frac{1}{10}-\frac{1}{12}+...$$

$$=(1-\frac{1}{2})-\frac{1}{4}+(\frac{1}{3}-\frac{1}{6})-\frac{1}{8}+(\frac{1}{5}-\frac{1}{10})-\frac{1}{12}+...$$

$$\frac{1}{2}(1-\frac{1}{2}+\frac{1}{3}-\frac{1}{4}+\frac{1}{5}-\frac{1}{6}+\frac{1}{7}-\frac{1}{8}+\frac{1}{9}-...)=\frac{1}{2}ln2$$

We explained earlier that sum of a series is a limit of partial sums as $n\to\infty$

SO, Rearranging terms of a series changes the partial sums and a result this changes limit of the partial sums.

### Conditionally Convergent Series

A series $\sum\limits_{n=1}^\infty a_n$ is conditionally convergent if and only if the sequence of its partial sums, i.e., $\lim_{m \to \infty} \sum\limits_{n=1}^m a_n$ exists and evaluates to some finite number while $\lim_{m \to \infty} \sum\limits_{n=1}^m |a_n|$ diverges to $\infty$.

## Rearrangement:

### Definition: 
Let ${k_n}, n = 1,2,3,...,$ be an integer valued positive sequence in which every positive integer appears once and only once (that is, $k_n= k_{n'}$ and only if $n=n'$). Given a series $\sum a_n$, Put

$$a'_n = a_{k_n} \ \ \ \ \ \ \ \ \ \ \ \ (n=1,2,3...)$$

we say that $\sum a'_n$ is a rearrangement of $\sum a_n$.

# Sum of Alternating Harmonic Series

A power series (centered at 0) is a function of the form

$\displaystyle\sum_{n=0}^{\infty}a_nx^n = a_0 + a_1x + a_2x^2 + a_3x^3 + . ..$

If the series converges for non-zero $x$, there is an $R>0$ so that the series converges in the open interval $-R<x<R.$ In this interval, the series can be differentiated and integrated term by term and the resulting series also converge in this open interval.

## Abel's Theorem

If $\displaystyle\sum a_n$ converges , and if $f(x) = \sum a_nx^n$, then

$$\sum a_n = \displaystyle\lim_{x\to1^-}f(x)$$

Abel's theorem and results on integration and differentiation of series allow us to find sums of series like the AHS.

To sum

$$1-\frac{1}{2}+\frac{1}{3}-\frac{1}{4}+\frac{1}{5}-\frac{1}{6}+\frac{1}{7}-\frac{1}{8}+\frac{1}{9}-\frac{1}{10}+...$$

let,

$$f(x) = x-\frac{1}{2}x^2+\frac{1}{3}x^3-\frac{1}{4}x^4+\frac{1}{5}x^5-\frac{1}{6}x^6+\frac{1}{7}x^7-...$$

This power series converges in the open interval $-1<x<1$.

let $F(x)=f'(x)$ so that

$$F(x)=f'(x) = 1-\frac{1}{2}2x+\frac{1}{3}3x^2-\frac{1}{4}4x^3+\frac{1}{5}5x^4-...$$

$$=1-x+x^2-x^3+x^4-x^5+x^6+....$$

$$=\frac{1}{1+x}$$

Since $f'(x)=\frac{1}{1+x}$ we can see $f(x) = ln(1+x)$

Now Abel's theorem says

$$1-\frac{1}{2}+\frac{1}{3}-\frac{1}{4}+\frac{1}{5}-\frac{1}{6}+\frac{1}{7}-...=\displaystyle\lim_{x\to1} ln(1+x)=ln2$$

Next, we'll take a look at [Riemann Series Rearrangement](/blog/riemann-series-rearrangement).

# References
- [The classical theory of rearrangements, Agana, M. J.](https://scholarworks.boisestate.edu/cgi/viewcontent.cgi?article=2052&amp)
- [Riemann series theorem, Wikipedia](https://en.wikipedia.org/wiki/Riemann_series_theorem)
- [Riemann's paradox: pi = infinity minus infinity, Mathologer](https://www.youtube.com/watch?v=-EtHF5ND3_s)
- [Infinite Series - Numberphile](https://www.youtube.com/watch?v=Jwtn5_d2YCs)
- [Riemann - Wikipedia](https://en.wikipedia.org/wiki/Bernhard_Riemann)
- Principles of Mathematical Analysis, Walter Rudin
- [On Conditionally Convergent Series, Werner Horn and Madjiguene Ndiaye](http://www.csun.edu/~hcmth017/riemann1/riemann1.pdf)
- [Calculus Notes, Grinshpan](https://www.math.drexel.edu/~tolya/123_harmonic.pdf)
- [Rearranging the Alternating Harmonic Series, Carl C. Cowen](https://www.math.iupui.edu/~ccowen/ButlerAHslides.pdf)
