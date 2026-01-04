---
author: Kishore Kumar
date: 2022-10-30 14:50:15+0530
doc: 2025-05-18 17:07:02+0530
tags:
- domain-cs-algorithms-analysis
- domain-math-number-theory
title: Randomization, Primality Testing Algorithms
---
# Randomized Algorithms
So far, we've discussed a lot of cool algorithms which we can use to solve many different problems. However, all these problems had a polynomial-time solution that we were able to come up with. This is not true for all problems. There are many **hard** problems for which there exists **no known** polynomial-time algorithm. A lot of these problems are quite important and an efficient way to solve them is a must. Without a polynomial-time solution to them, it is not feasible to compute their solutions for large inputs on any known computational device that man has access to.

In situations like these, we try to _probabilistic-ally_ solve the problem. We sacrifice being 100% accurate for an immense boost in speed. In some sense our algorithm is _wrong_. It does not pass the test of giving the correct answer to _every_ test case. But if it can do so with great accuracy, it might be the best "solution" we have.

## A more "mathematical" explanation

Let's suppose we're given a **hard** problem that has no known polynomial-time solution. However, what we do have is a set of $n$ _efficient_ but **not-correct** algorithms which output the correct answer for only $\frac{2k}{3}$ of all valid inputs. Let us denote the set of these "probabilistic" algorithms by

$A = \{ a_1, a_2, \dots,a_n\}$

Now, let's say I pick some random input $i$ and give it to my algorithm $a_1$. Since it gives me the correct answer for $\frac{2k}{3}$ of all possible inputs, my chances of getting a wrong answer are equal to $1-\frac{2}{3} = \frac{1}{3}$.

This is not terrible, but still not great. However, notice that I still have $n-1$ other algorithms that give me a probabilistic-ally correct answer. If we run some $m \leq n$ such algorithms on the same input, notice that the chances of getting a wrong answer diminish to $\frac{1}{3}^m$. After running just 5 such algorithms, our chances of getting a wrong answer are as low as 0.243%. This is a **very** good approximation and we can always do this since running 5 such efficient algorithms is _always_ much faster than running an exponential-time algorithm.

# Primality testing

A known computationally hard problem is primality testing. There is no easy way to test if a number is prime or not without iterating through at least all its factors $\leq \sqrt n$. Notice that here, the number is given as input in bits and for every added bit we have an exponential increase in complexity. The actual complexity is $\sqrt{2^n} = 2^{\frac{n}{2}}$. This is assuming that we are able to test divisibility in $O(1)$, which might not be true for large numbers.

Primality testing is also a very important algorithm. Algorithms like RSA are used worldwide to secure communication in web browsers, email, VPNs, etc. and it relies on us knowing very large prime numbers. Large prime numbers are difficult to find, especially if we don't have an algorithm that can test primality very quickly. But since it is a **hard** problem, we have come up with probabilistic algorithms to efficiently "almost" solve this problem.

## Fermat Primality Test

Just recently, we talked about Fermat's little theorem ([Wilson's Theorem, Fermat's Little Theorem & Euler's Totient Function](/blog/wilson-s-theorem-fermat-s-little-theorem-euler-s-totient-function)) which gives us the following equation. For any prime $p$ and _any_ integer $a$ co-prime to $p$,

$$ a^{p-1} \equiv 1 \ mod \ p $$

This equation always holds for primes and in general does _not_ hold for composite numbers. Notice that for different values of $a$, we essentially have an all-new algorithm to test the primality of $p$. If the equation does not hold for _any_ value $a$ co-prime to $p$, then we know for sure that the number is not prime. We can prove that by trying all values of $2 \leq a \leq p-2$ we can indeed guarantee that $p$ is prime. However, doing that would be worse than just iterating over all its factors and testing primality. Hence we can choose to just try the algorithm for many different values of $a$. This turns out to be a _very efficient_ probabilistic test for checking the primality of some number $p$.

Below is the implementation of such an algorithm that relies on randomness.

```cpp
bool fermatPrimalityTest(int p, int rep=10){
		if(p <= 3) return p == 2 || p == 3;
		
		for(int _=0; _<rep; _++){
				int a = rand()%(p-3) + 2;
				if(binpow(a, p-1, p) != 1) return false; // Fermat witness
		}
		return true;
}
```

This algorithm will return the right answer most of the time. Further, notice that we don't care if $a$ is co-prime to $p$ or not. The condition is imposed on this version of Fermat's because if $p$ divides $a$ then $a \equiv 0 \ mod \ p$. But this will not be an issue for the values of $a$ that we are picking.

While performing the check, if our equation fails for some base $a$, then we call $a$ the **Fermat witness** for the compositeness of $p$. If our number $p$ passes the test for some base $a$ but $p$ is actually composite, then we call base $a$ a **Fermat liar**.

A natural question to ask here is, how many such composite numbers pass this test very frequently. Are there any composite numbers that pass this test for **all** $a$ co-prime to $n$ maybe?

### Carmichael numbers

Sadly, there are such composite numbers for which this test returns true for **all** $a$ co-prime to $p$. They are the ****[Carmichael numbers](https://en.wikipedia.org/wiki/Carmichael_number). We can identify these false positives only if try bases that are not co-prime to $p$. This makes Fermat's primality test a weak prime test. However, it is not very bad and Carmichael numbers are fairly rare. There exist only 646 such numbers $\leq 10^9$ and only 1401644 such numbers $\leq 10^{18}$. This is still reasonable for such a fast and efficient algorithm.

## Miller-Rabin Primality Test

The idea behind this primality test is somewhat an extension of Fermat's. Let's say we are testing the primality of some integer $p$. If $p$ is even, it is obviously not prime for all values of $p \neq 2$.

Let us eliminate all even numbers (excluding the trivial case of 2). Now, given that $p$ is a odd number who's primality we're testing, $p$ being odd $\implies p-1$ is even. This means that it has _at least_ one factor of two.

Let us write $p-1 = 2^k\cdot q$, we are essentially factorizing all the $2$ factors from the number $p$. From this construction, it must be true that $q$ is odd. Substituting this back in Fermat's test we can write it as

$$ a^{p-1} \equiv 1 \ mod \ p \iff a^{2^k \cdot q}-1 \equiv 0 \ mod \ p $$

Notice that we can factorize this expression further. Any term of the form $x^2-1=(x+1)(x-1)$. So we can write the above term as

$$ a^{2^k \cdot q}-1 \equiv 0 \ mod \ p \iff (a^{2^{k-1}\cdot q}+1)(a^{2^{k-1}\cdot q}-1) \equiv 0 \ mod \ p $$

Notice that the 2nd term on the RHS can be factorized further until we run out of powers of 2. That is, we can factorize it $k-1$ times to get the following expression.

$$ 
\begin{aligned}
(a^{2^{k-1}\cdot q}+1)(a^{2^{k-1}\cdot q}-1) \equiv 0 \ mod \ p \\ \iff (a^{2^{k-1}\cdot q}+1)(a^{2^{k-2}\cdot q}+1)\cdots(a^q+1)(a^q-1)\equiv 0 \ mod \ p 
\end{aligned}
$$

This equation must be true for $p$ to be prime. This means that _at least_ one of these terms must be divisible by $p$. That is, either

$$ a^q - 1 \equiv 0 \ mod \ p \iff a^q \equiv 1 \ mod \ p $$

holds or for some $0 \leq r \leq k-1$ we check if

$$ a^{2^rq}+1 \equiv 0 \ mod \ p \iff a^{2^rq} \equiv -1 \ mod \ p $$

holds.

If none of these statements hold (for all values of $r$) then we know that $p$ **must** be composite. We call the base $a$ a _witness_ for the compositeness of $p$. However, recall that this test is only probabilistic. It is possible for certain bases to pass this test even for composite $p$. We call such bases a _strong liar._

## Why Miller-Rabin over Fermat?

The nice part about this test is that unlike with Fermat, there are _no_ numbers like the Carmichael numbers where all non-trivial bases lie.

We give the name [Strong pseudoprime](https://en.wikipedia.org/wiki/Strong_pseudoprime) to composite numbers which pass the Miller-Rabin test. From the Wiki,

> A composite number $n$ is a strong pseudoprime to at most one quarter of all bases below $n$. Of the first 25,000,000,000 positive integers, there are 1,091,987,405 integers that are probable primes to **base 2**, but only 21,853 of them are pseudoprimes, and even fewer of them are strong pseudoprimes

The proof for the bound that for any composite $p$, the probability that a random integer $a \in [1, N-1]$ is a witness for the compositeness of $p$ is at least $\frac{3}{4}$ can be found here: [Primality Proving - Lecture Notes 12 from MIT](https://math.mit.edu/classes/18.783/2017/LectureNotes12.pdf)

We can take this even further!

The Miller-Rabin primality test can be made **deterministic** by _only_ testing all bases $a \leq 2ln(p)^2$. The proof for this claim relies on the [Generalized Riemann Hypothesis](https://en.wikipedia.org/wiki/Generalized_Riemann_hypothesis) being true. However, if it does hold true, then we have a polynomial time deterministic test for the primality of some number $p$!

# References
These notes are old and I did not rigorously horde references back then. If some part of this content is your's or you know where it's from then do reach out to me and I'll update it. 
1. Professor [Kannan Srinathan's](https://www.iiit.ac.in/people/faculty/srinathan/) course on Algorithm Analysis & Design in IIIT-H