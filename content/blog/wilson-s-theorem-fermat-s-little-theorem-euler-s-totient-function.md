---
author: Kishore Kumar
date: 2022-10-23 19:10:57+0530
doc: 2025-05-18 17:07:02+0530
tags:
- domain-math-number-theory
title: Wilson's Theorem, Fermat's Little Theorem & Euler's Totient Function
---
Last time, we covered the [Extended Euclidean Algorithm](/blog/extended-euclidean-algorithm). Now, we'll delve into some cooler number theory. 
# Wilson's Theorem
Wilson's Theorem states that for any number $p$, the following congruence holds $\iff p$ is prime:
$$(p-1)! \equiv -1 \pmod{p}$$
## Proof
### Proof for composite numbers
We can prove that this statement does not hold for any composite $p$ easily. Let $p$ be a composite number $\gt 2$. Then $p$ can be represented as the product of two numbers $a \cdot b = p$ for some $1 \leq a \leq b \lt p$. Note that this means that $a \mid (p-1)!$, hence $(p-1)! \equiv 0 \pmod{a}$. But if $a \mid p$ and $(p-1)! \equiv 0 \pmod{a}$, then $(p-1)! \equiv -1 \pmod{p}$ cannot be true. $(p-1)! \pmod{p}$ must be 0. This is a contradiction. 
Therefore, if $p$ is composite, $(p-1)! \not \equiv 0 \pmod{p}$. Similarly, if the equivalence is -1, then $p$ cannot be composite. 
### Proof for prime numbers
Let's prove the case for $p = 2$ first. $(2-1)! = 1! \equiv -1 \pmod{2}$ is seen trivially. Now we will prove for all odd primes $p$. 
Note that in $Z_{p+} = \{1, 2, 3, \ldots, p-1\}$, $\forall x \in Z_{p+}, \ \exists \ x' \mid x \cdot x' \equiv 1 \pmod{p}$. This is essentially the existence of an inverse. Also note that the inverse must always be unique for each $x \in Z_{p+}$. Now, there are two possible cases, $x = x'$ or $x \neq x'$. 

Let's assume $x = x'$.  Then, 
$$
\begin{aligned}
x \cdot x' \equiv 1 \pmod{p} \\
x^2 \equiv 1 \pmod{p} \\
\implies x \equiv \pm1 \pmod{p} \\ 
\implies x = 1 \ \lor \ x = p-1
\end{aligned}
$$
Therefore, the only two elements in this field with inverses equivalent to themselves are $1$ and $p-1$. Now, let's consider the entire product of $(p-1)!$. 
$$
\begin{aligned}
(p-1)! \pmod{p} \equiv (p-1)\cdot(p-2)\cdot(p-3)\cdots1 \pmod{p} \\
\text{Pairing off all the other elements with their unique inverses gives us} \\
(p-1)! \equiv 1\cdot (p-1) \pmod{p} \\
\implies (p-1)! \equiv -1 \pmod{p}
\end{aligned}
$$
Hence we have proved Wilson's theorem. 
# Fermat's Little Theorem

Fermat's little theorem states the following:

_If $p$ is a prime number, then for any integer $a$, the number $a^p -a$ is an integer multiple of $p$._

In other words,

$$ a^p\equiv a(mod \ p) $$

Further, if $a$ is not divisible by $p$, then

$$ a^{p-1} \equiv 1(mod \ p) $$

> Fun fact, this theorem is used to come up with a **very** accurate probabilistic [Randomization, Primality Testing Algorithms](/blog/randomization-primality-testing-algorithms)!
## Proof
The proof is as follows: Consider the set $Z_p = \{1, 2, 3, \ldots, p-1\}$, which contains all the non-zero integers modulo $p$. Let's construct the following equation and work on rearranging / substituting terms. 
$$
\begin{aligned} 
(a \cdot 1)(a \cdot 2)(a \cdot 3) \cdots (a \cdot (p-1)) &\equiv a^{p-1} \cdot (1 \cdot 2 \cdot 3 \cdots (p-1)) \pmod{p} \\ &\equiv a^{p-1} \cdot (p-1)! \pmod{p} 
\end{aligned}$$ By Wilson's Theorem, we know that $(p-1)! \equiv -1 \pmod{p}$ for any prime $p$. Substituting this, we get: $$a^{p-1} \cdot (p-1)! \equiv a^{p-1} \cdot (-1) \pmod{p}$$ Therefore, we have: $$a^{p-1} \cdot (-1) \equiv -a^{p-1} \pmod{p}$$ Rearranging the terms, we get: $$a^{p} - 1 \equiv 0 \pmod{p}$$ This can be rewritten as: $$a^{p} \equiv a \pmod{p}$$ Thus, we have proved Fermat's Little Theorem.
# Euler's Totient Function

Euler came along later and gave a more generalized version of Fermat's little theorem. He stated that for _any_ modulus $n$ and any integer $a$ co-prime to $n$, the following holds true.

$$ a^{\phi(n)} \equiv 1 (mod \ n) $$

Here, $\phi(n)$ is known as **Euler's Totient function.** It counts the number of integers between 1 and $n$ inclusive, which are co-prime to n. Or in simpler words, it is equivalent to the number of numbers less than $n$ that do not share any divisors with $n$.

**Some interesting properties:**

1. Notice that for any prime number $p$, $\phi (p) = p-1$. By virtue of being prime, $p$ does not share any factor with any number less than itself.
    
2. The totient function is a **multiplicative function**. This is not a trivial thing to see and follows from the Chinese remainder theorem. This [stack link](https://math.stackexchange.com/questions/192452/whats-the-proof-that-the-euler-totient-function-is-multiplicative) has a really nice write up of the proof. This property essentially means that for relatively prime $a$ and $b$,
    
    $$ \phi (ab) = \phi(a)\cdot\phi(b) $$
    

Notice that Fermat's is indeed a special case of this theorem. When $n$ is prime, we get Fermat's little theorem.

Further, just like factorization, computing the value of $\phi(n)$ is a **hard** problem. However, notice that if the factorization of $n$ is known, we can compute the value easily. We can simply write $n$ in terms of its prime products and write $\phi(n) = \phi(p_1) \cdot \phi(p_2)\cdots \phi(p_n)$. And it is easy to compute $\phi(p)$ where $p$ is prime.

# References
These notes are old and I did not rigorously horde references back then. If some part of this content is your's or you know where it's from then do reach out to me and I'll update it. 
1. Professor [Kannan Srinathan's](https://www.iiit.ac.in/people/faculty/srinathan/) course on Algorithm Analysis & Design in IIIT-H