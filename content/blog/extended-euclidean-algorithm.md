---
author: Kishore Kumar
date: 2022-10-22 07:51:22+0530
doc: 2025-05-18 17:07:02+0530
tags:
- domain-cs-algorithms-analysis
- domain-math-number-theory
title: Extended Euclidean Algorithm
---
# An efficient algorithm to find GCD

The problem we're attempting to solve is pretty simple. Given two numbers $a \text{ and } b$, find their GCD.

A naïve way to solve this problem is as follows, find all prime factors of the two numbers, and multiply all the common ones. However, even with fast prime finding algorithms like Eratosthenes sieve, it will work only for small numbers. It is not feasible to precompute the sieve for large numbers.

However, by combining the idea behind iterating over all roots of a number and the sieve logic we can actually come up with an algorithm that obtains the prime factors of a number in $O(\sqrt n . logn)$. How? Consider this approach, let us iterate from $i = 2 \to \sqrt n$ and **if $i$** divides $n$, then keep dividing $n$ by $i$. Each of these divisions implies that $i$ is each time, a prime factor of $n$.

The code looks something like this

```jsx
for(int i=2; i*i <= n; i++){
		while(n % i == 0){
				primefactors.insert(i);
				n /= i;
		}
}
if(n>2) primefactors.insert(n);
```

Consider let us try to **prove** why this works.

**Our claim:** _Every composite number has at least one prime factor less than or equal to the square root of itself._

**Proof:** Since our number is composite, it must have at least one-factor $a$. This implies that there exists some number $b$ such that $a \times b = n$. Now, we want to prove that either

$a \leq \sqrt n \text{ or } b \leq \sqrt n$

We prove this by contradiction. Assume that both $a \gt \sqrt n$ and $b \gt \sqrt n$.

This implies that $a\times b \gt \sqrt n \times \sqrt n \implies ab \gt n$. This is a contradiction. Hence either $a \leq \sqrt n$ or $b \leq \sqrt n$.

Now, W.L.O.G. assumes that $a \leq \sqrt n$. Either $a$ can be prime or by the fundamental theorem or arithmetic, $a$ must have a prime divisor $\lt a$. In both cases, our claim is true.

The inner while loop which removes every instance of the prime factor is pretty similar to the marking composite step in the sieve algorithm. Once they're removed we can move

However, notice that in the worst case, if $n$ itself happens to be prime our algorithm would have a worst-case runtime of $O(\sqrt n)$. Since the prime factors are obtained in sorted order, we can always run 2 pointers in linear time to get the common factors. But the worst case is still $O(\sqrt n)$,

The question is, _can we do better?_

## Euclid's Algorithm

The algorithm Euclid proposed to solve the GCD problem was extremely simple. According to him,

$$ gcd(a, b) = \begin{cases} a, & \text{ if } b =0 \\ gcd(b, a \ mod \ b) & \text{otherwise.} \end{cases} $$

### Proof

First, note that the second argument strictly decreases with each iteration of the Euclidean algorithm, implying that the method will always halt (because the arguments are never negative).

Now, to prove correctness, we must prove $gcd(a, b)= gcd(b, a \ mod \ b) \forall a \geq 0, b \gt 0$

First, notice that $a \ mod \ b = a-b.\lfloor \frac{a}{b} \rfloor$

With this reduction, let us try to prove a simpler identity. $gcd(a, b) = gcd(a-b, b)$.

Let $gcd(a, b) = d.$ This implies that $d|a \text{ and } d|b$. This also means that $d | (a-b)$ and $d|b$.

This is true for all common factors of $a$ and $b$. Therefore, $(a, b)$ and $(a-b, b)$ share the same set of common factors. Hence $gcd(a,b) = gcd(a-b, b)$.

Now notice that $a \ mod \ b$ is simply performing this operation $\lfloor \frac{a}{b} \rfloor$ times. Hence $gcd(a, b) = gcd(a \mod b, b)$. Hence proved.

Now that we have managed to prove correctness, let us try to put an upper bound on the running time of this algorithm.

### Time complexity

Notice that in every step of the recursion, one of the arguments get cut in at least half. Consider the operation $a \ mod \ b$.

**If $b \leq \frac{a}{2}$ :** Then by property of the mod, $a \ mod \ b \lt \frac{a}{2}$

**If $b \gt \frac{a}{2}$:** Then the operation $a \ mod \ b = a-b \lt \frac{a}{2}$

Therefore the number of recursive steps will be at max $log(min(a, b))$. And this is indeed the complexity of our algorithm.

Further note that for a $n$-bit number, since the operands get halved at every other step, we are removing one bit of the numbers per every 2 recursions. Hence the number of calls is linear in the number of bits of the number. The modulo operation is quadratic in the number of bits of the number. Hence final complexity $O(n^3)$.

> Lamé's theorem is used to estimate the method's running time, and it establishes an unexpected link between the Euclidean algorithm and the Fibonacci sequence: The Euclidean algorithm executes at most $n-2$ recursive calls if $a \gt b \geq 1$ and $b \lt F_n$ for some $n$. Furthermore, the upper bound of this theorem can be shown to be optimal. $gcd(a,b)$ will do exactly $n-2$ recursive calls when $a = F_n$ and $b = F_{n-1}$. In other words, the worst-case input for Euclid's algorithm is a series of Fibonacci numbers.

### Code

Below is the C++ implementation of the algorithm. Notice the conciseness that writing the algorithm recursively gives us.

```cpp
int gcd (int a, int b) {
    if (b == 0) return a;
    else return gcd (b, a % b);
}
```

However, we can also write it iteratively for more efficiency as follows

```cpp
int gcd (int a, int b) {
    while (b) {
        a %= b;
        swap(a, b);
    }
    return a;
}
```

# The Extended Euclidean Algorithm

While the Euclidean algorithm calculates only the greatest common divisor (GCD) of two integers $a$ and $b$, the extended version also finds a way to represent GCD in terms of $a$ and $b$, i.e. coefficients $x$ and $y$ for which:

$a \cdot x + b \cdot y = \gcd(a, b)$

## The algorithm

Let the GCD of $a$ and $b$ be $g$.

We can find this representation by simply extending the previously explained algorithm. Notice that the previous algorithm terminates when $b=0$ and $a = g$. At this step, we can easily find the coefficients $g = g \cdot 1 + 0 \cdot 0$ .

From here, the main idea is to **backtrack** through our recursive calls. The only transition we need to describe is the transition of $<x, y>$ from $(b, a \ mod \ b) \to (a,b)$ ,

Let's suppose that we have the coefficients $<x_1, y_1>$ for $(b, a\ mod \ b)$, This implies that the following equation holds true always.

$$ b \cdot x_1 + (a \bmod b) \cdot y_1 = g $$

Now, we want to find the transition of $<x_1, y_1> \to <x_2, y_2>$ for the pair $(a, b)$. That is,

$$ a \cdot x + b \cdot y = g $$

Recall that we can write $a \bmod b = a - \left\lfloor \frac{a}{b} \right\rfloor \cdot b$. Now, substituting this in the previous equation, we get,

$$ g = b \cdot x_1 + (a \bmod b) \cdot y_1 = b \cdot x_1 + \left(a - \left\lfloor \frac{a}{b} \right\rfloor \cdot b \right) \cdot y_1 $$

We can now solve this equation to get,

$$ g = a \cdot y_1 + b \cdot \left( x_1 - y_1 \cdot \left\lfloor \frac{a}{b} \right\rfloor \right) $$

And that's it! We have found our transition.

$$ \begin{cases} x_2 = y_1 \\ y_2 = x_1 - y_1 \cdot \left\lfloor \frac{a}{b} \right\rfloor \end{cases} $$

## Proof

**Lemma:** If $d$ divides both $a$ and $b$, and $d = ax + by$ for some integers $x$ and $y$, then necessarily $d = gcd(a, b)$.

**Proof:**

1. Since it is given that $d|a$ and $d|b$, then $d$ is a common divisor of $a$ and $b$. This implies that $d \leq gcd(a, b)$ by definition of $gcd$.
2. Since $gcd(a, b)|a$ and $gcd(a, b)|b$, it implies that $gcd(a,b)|(ax+by) \implies gcd(a,b)|d$. Therefore $gcd(a,b) \leq d$.

We have $gcd(a,b) \leq d$ and $d \leq gcd(a,b)$. Therefore it must be true that $d = gcd(a,b)$

## Code

As before, we can implement this both recursively and iteratively. The recursive version is quite concise. Below is the C++ implementation of the recursive code.

```cpp
int gcd(int a, int b, int &x, int &y) {
    if (b == 0) {
        x = 1;
        y = 0;
        return a;
    }
    int x1, y1;
    int d = gcd(b, a % b, x1, y1);
    x = y1;
    y = x1 - y1 * (a / b);
    return d;
}
```

# Modular Division (Multiplicative Inverse)

When doing operations in the modular field, we perform operations between two numbers $a, b$ belonging to the field like $(a+b)mod \ k$. Here $+$ is the binary operation and $Z_k$ is the modular field.

Notice that while this is fine for integer addition, subtraction, and multiplication, it is not so easy to define division.

In the world of modular arithmetic, we define the modular multiplicative inverse of an integer $a$ as an integer $x$ such that $a \cdot x \equiv 1 \mod k$. Further, in terms of defining notation, we write such an integer $x = a^{-1}$.

Further, notice that the modular inverse of an element belonging to the modular field of $Z_k$ does not always exist. For example, consider $3 \in Z_6$. $Z_6 = \{0, 1, 2, 3, 4, 5\}$. By trying all possible elements we can confirm that there exists no integer $\in Z_6$ such that $3 \cdot x \equiv 1 \ mod \ 6$. It can be proven that the modular inverse for an integer $a$ exists in the modular field $Z_k$ **if and only if $gcd(a, k) = 1$.** That is, $a$ and $k$ are relatively prime.

## Finding the modular inverse using the Extended Euclidean Algorithm

Let's take the following equation,

$$ a \cdot x + k \cdot y = 1 $$

Remember that the modular inverse of $a$ exists, if and only if $gcd(a, k) = 1$. Further, notice that the above equation can be solved by the extended euclidean algorithm.

Once the **EED** algorithm gives us the values of $x$ and $y$, we can mod the entire expression with $k$ to get

$$ a \cdot x + 0 \equiv 1 \ mod \ k $$

Then $x = a^{-1}$

### Code

The code for it is pretty simple. Below is C++ implementation of the same

```cpp
int a, k, x, y;
int g = EED(a, k, x, y);
if(g!=1) // No solution
else // (x % m + m) % m is our solution 
```

Note that we do the addition %m + m step to make sure $x$ is positive.

# References
These notes are old and I did not rigorously horde references back then. If some part of this content is your's or you know where it's from then do reach out to me and I'll update it. 
1. Professor [Kannan Srinathan's](https://www.iiit.ac.in/people/faculty/srinathan/) course on Algorithm Analysis & Design in IIIT-H
2. [Extended Euclidean Algorithm - cpalgorithms](https://cp-algorithms.com/algebra/extended-euclid-algorithm.html)
