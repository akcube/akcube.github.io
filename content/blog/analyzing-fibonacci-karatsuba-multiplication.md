---
author: Kishore Kumar
date: 2022-09-14 10:13:32+0530
doc: 2025-05-18 17:07:02+0530
tags:
- domain-cs-algorithms-analysis
title: Analyzing Fibonacci & Karatsuba Multiplication
---
# Fibonacci 
Let's try analyzing a few different algorithms for computing $F_n$, the $n^{th}$ Fibonacci number

**Note:** The number doubles rapidly and hence grows at an exponential rate. In fact, $F_n \approx 2^{0.694}$, which implies that we need around 0.694 bits to represent the $n^{th}$ Fibonacci number. This number can grow very large, very quickly. Not it is no longer accurate to consider the addition of 2 numbers as a constant time operation. For large values of n, the number of bits required to represent $F_n$ grows larger than any machine's word size and addition becomes a *linear-*time operation.

> 👾 **How do we know that $F_n \approx 2^{0.694}$?** We can solve the recurrence relation to get the following formula:
>$$ F_n = \frac{1}{\sqrt5}((\frac{1+\sqrt5}{2})^n-(\frac{1-\sqrt5}{2})^n) $$
>
> For large n, the second term is negative and hence tends to 0. So for large n, the equation simplifies to $F_n = \frac{\Phi^n}{\sqrt5}$, taking log here, we get $log_2(F_n) = n\times0.694 - \sqrt5$. Again, for larger n the change produced by $\sqrt5$ reduces and the dominant term is simply $0.694n$.
>
> From this, we can infer that the $n^{th}$ Fibonacci number, especially for larger and larger n will require about $0.694n$ bits to represent in binary
> 
> Bonus, running the below C++ program allows us to verify that the above relation even holds for smaller values of n. And with increasing n, the equation only grows more accurate and hence is a very good approximation of $F_n$
>```cpp
>int main(void){
>	long long n;
>	cin>>n;
>
>	long long p_2 = 0;
>	long long p_1 = 1;
>	for(int i=0; i<n; i++){
>		long long fib = p_2 + p_1;
>		cout<<fib<<" ";
>		swap(fib, p_2);
>		swap(p_1, fib);
>	}
>	cout<<endl;
>
>	long double phi = 1.61803398875;
>	for(int i=0; i<n; i++){
>		long long fib = round(pow(phi, i+1) / sqrt(5));
>		cout<<fib<<" ";
>	}
>	cout<<endl;
>}
>```

## Algorithm 1 for computing $F_n$

```bash
if n = 0: return 0
if n = 1: return 1
return fib1(n-1) + fib1(n-2)
```

Proving **correctness** for this particular algorithm is relatively straightforward as this algorithm is pretty much the exact definition of the Fibonacci function. This is one of the most powerful features that recursion is able to offer.

It is however important to keep track of space usage analysis as recursion stacks may grow very large and potentially overflow the stack.

>🛠 This is one of the reasons functional programming is a powerful idea. Functional languages have the inherent property that all code is expressed in a functional manner. This allows the code to pretty much express its own correctness proof.

### Recurrence relation

$T(n) = T(n - 1) + T(n - 2) + A\ for \ n > 2$ where $A$ is the complexity for addition of two numbers Therefore, the time complexity for adding two numbers via this algorithm is $O(2^nA)$. We can visualize the branching like a tree and every node branching into two child nodes at every step of the recursion. And at every node, we perform $A$ operations for addition. For large $F_n$, since addition is linear in the number of bits and since $F_n \approx 2^{0.694n}$, our final time complexity evaluates to $O(n2^n)$.

## Algorithm 2 for computing $F_n$

The key idea used here is converting the recursion to iteration. Just keeping track of $f_{i-1}$ and $f_{i-2}$ for computing $f_i$ is enough. This idea is a very basic application of the concept of **dynamic programming.**

Below is an algorithm that keeps track of the computed Fibonacci numbers for all $i \leq n$

```bash
if n = 0: return 0
create an array f[0..n]
f[0] = 0, f[1] = 1
for i = 2...n:
		f[i] = f[i-1] + f[i-2]
return f[n]
```

**Note** that this is however not a linear time algorithm

While the loop itself is linear, $F_n$ is about $0.694n$ bits long, and each addition is an $O(n)$ operation when we are dealing with arbitrarily large numbers. Therefore the overall complexity is $O(n^2)$ in the size of the input

>📈 We can also observe that the space complexity for the above algorithm is also evaluated to about $O(n^2)$. Arbitrarily large numbers can occupy $0.694n$ bits in memory, and we are storing all values of $F_n$ from $i \dots n$.
>
>However, a simple optimization will help us reduce the space complexity to simply $O(n)$. We only ever need the previous two values of $F_i$ to compute it. That is, we only need to keep track of $F_{i-1}$ and $F_{i-2}$ to compute $F_i$. The rest of the values of $F_{j \lt i-2}$ are not required. Keeping track of just the 3 values allows us to reduce space complexity by simply storing the number of bits in $F_n, F_{n-1}$ and $F_{n-2}$, which is linear in the input size. Space complexity: $O(n)$
>
>The **key** realization here is just observing that our algorithm calculates all values of $F_i$ for **all $0\leq i\leq n$.** This is a redundancy. We only require to calculate the $n^{th}$ Fibonacci number. This realization will help us reduce the time complexity even further, as we will see below.

## Algorithm 3 for computing $F_n$

Motivated by our realization to eliminate the redundancy, we can attempt to make our computation even faster.

Let us assume that we know $F_{i-1}$ and $F_{i-2}$ and we are attempting to compute $F_i$. Notice that to compute $F_i$, our equation looks like $F_i=1\times F_{i-1} + 1\times F_{i-2}$. This gives us $F_i$. Now from $F_i$, to get $F_{i+1}$, we need the term $F_{i-1}$ as well.

We get the following equations

$$ F_i = F_{i-1}+F_{i-2} \\ F_{i-1} = 0\times F_{i-2} + 1\times F_{i-1} $$

Notice that these set of equations can be represented nicely in a matrix form which lets us write

$$ \begin{pmatrix} F_{i-1} \\ F_{i} \\ \end{pmatrix} =\begin{pmatrix} 0 & 1 \\ 1 & 1 \end{pmatrix} \begin{pmatrix} F_{i-2} \\ F_{i-1} \end{pmatrix} $$

Notice that by simply left-multiplying the RHS with our constant matrix, we calculate any $F_n$ that we desire. This allows us to come up with the following beautiful equation.

$$ \begin{pmatrix} F_n \\ F_{n+1} \\ \end{pmatrix} =\begin{pmatrix} 0 & 1 \\ 1 & 1 \end{pmatrix}^n \begin{pmatrix} F_0 \\ F_1 \end{pmatrix} $$

To calculate any $F_n$, we only need to know the values of $F_0, F_1$ , and a constant matrix exponentiated to some $n$. Exponentiation of a constant to some power $n$, can be solved via _binary exponentiation._ Therefore the time complexity of this Algorithm comes out to be $O(M(n)log(n))$ where $M(n)$ is the time complexity for multiplying two n-bit integers

## Algorithm 4 for computing $F_n$ (Direct formula)

$F_n = \frac{1}{\sqrt{5}}(\frac{1 + \sqrt{5}}{2})^{n} - \frac{1}{\sqrt{5}}(\frac{1 - \sqrt{5}}{2})^{n}$t

We can also attempt to compute $F_n$ using the direct formula we obtain by solving the recurrence relation. However, notice that there are irrational and divisions involved. This might give us accuracy issues depending on machine type and whatnot. This makes it very difficult to prove accuracy of the algorithm on machines.

Further, we can note that we still need to compute some value to the power n. This requires $log_2(n)$ operations for the exponentiation and $M(n)$ operations for multiplication. This algorithm is essentially equivalent to our previous algorithm in terms of time complexity.

We also see that the eigenvalues of the matrix we use in Algorithm #3 appear in the direct formula. Therefore, it's better if we just use Algorithm #3 as we don't have to deal with irrational numbers, hence no accuracy issues arise. They are essentially 2 forms of the same algorithm.

>In fact, if we calculate the eigenvalues of the matrix obtained in our 3rd algorithm, we get $\lambda_1 = \frac{1+\sqrt5}{2} \\ \lambda_2 = \frac{1-\sqrt5}{2}$
>
>This further solidifies our suspicion that both algorithms 4 and 3 are essentially two different ways of expressing the same idea. One is a more mathematical method to compute $F_n$ and the other, a matrix represented technique that will be easier to implement on computers. They both have equal time complexity. But the matrix method is preferred as we do not have to deal with accuracy issues.

Note that in all the above algorithms, the derived complexity involved the function $M(n)$. This is the number of operations required for multiplying 2 n-bit numbers.

Notice that the naive algorithm for implementing n-bit multiplication is of the order of $n^2$. This makes our algorithms 3 and 4 worse than 1 and 2 as they become $n^2logn$ in the order of input size. However, if we are able to reduce the complexity of the multiplication operation, we will be able to do better than algorithms 1 and 2.

# Karatsuba Multiplication

_Can we do better than the order of $n^2$ operations per multiplication?_

This problem is an **open** question. We know an algorithm that can do better than $n^2$, but we have not been able to prove the optimality of this algorithm.

**Intuition**:

Multiplying two complex numbers.

To compute $(a+ib) \times (c+id)$, we require 4 steps naively. $(ac-bd)+i(ad+bc)$

It is, however, possible to compute this in just 3 steps.

- Compute $a \times c$
- Compute $b\times c$
- Compute $(a+b)\times(c+d)$

Notice that $(ad+bc) = (a+b)\times(c+d)-ac-bd$

Let us try to realize this same concept while multiplying 2 n-bit integers.

Say we have some n-bit integer $X$. This implies that there are n-bits in its binary representation. This also means that we can divide every n-bit integer into 2 sets of $\frac{n}{2}$ bits each (+-1).

$X = 01001011 \implies x_1 = 0100, x_0 = 1011$

That is, we can write $X = 2^{\frac{n}{2}}x_1+x_0$. Notice that multiplying by $2^x$ is the same as shifting the binary by $x$ steps to the left. Hence shifting can be considered a constant operation.

**Note** that this is true for any base. Multiplying by $k$ for any number in base $k$ is equivalent to shifting.

This is essentially all we need to know for coming up with the Karatsuba algorithm ourselves.

## The algorithm

To multiply any two n-bit integers,

1. Add two $\frac{1}{2}n$ bit integers
2. Multiply three $\frac{1}{2}n$ bit integers
3. Add, subtract, and shift $\frac{1}{2}n$ bit integers to obtain the answer

$$ X = 2^{\frac{n}{2}}.x_1 + x_0 \\ Y = 2^{\frac{n}{2}}.y_1 + y_0 \\ X.Y = (2^{\frac{n}{2}}.x_1 + x_0)\times(2^{\frac{n}{2}}.y_1 + y_0) \\ = 2^n.x_1.y_1 + 2^{\frac{n}{2}}((x_0+x_1)(y_0+y_1)-x_1.y_1-x_0.y_0) + x_0.y_0 $$

Notice that the last step of the expansion is essentially the same as the constructive change we put forward in the multiplication of complex numbers idea to reduce multiplications required from 4 to **3**. This allows us to multiply 2 n-bit integers with an algorithm that recursively divides its input into $\frac{n}{2}$ bit chunks and requires only 3 multiplications per $\frac{n}{2}$ bit chunk.

Let's suppose that our algorithm takes $T(n)$ steps to compute. At every step, we need to calculate the following terms.

1. $x_1.y_1$ which can be done in $T(\frac{n}{2})$
2. $x_0.y_0$ which can be done in $T(\frac{n}{2})$
3. $(x_0+x_1)(y_0+y_1)$. Notice that the addition of two $\frac{n}{2}$ bit numbers _can_ be a $1+\frac{n}{2}$ bit number. Hence this will take us $T(\frac{n}{2}+1)$ steps.
4. Finally, once the shifts are done, we have a few $O(n)$ additions to be done.

This gives us the following result,

**[Karatsuba-Ofman, 1962]** Can multiply two n-digit integers in $O(n^{1.585})$ bit operations.

$$ T(n) \leq T(\frac{n}{2})+T(\frac{n}{2})+T(\frac{n}{2}+1) +\Theta(n) \\ T(n) = O(n^{log_2(3)})=O(n^{1.585}) $$

## Can we do _better_?

We shall cover the algorithm in detail later, but there does indeed exist an algorithm that can do it better.

- The [The Fast Fourier Transform (FFT)](/blog/the-fast-fourier-transform-fft) based algorithms are able to compute this operation in $O(n\ log(n)\ log(log(n)))$
- In 2007, we discovered a new method that computes it in $O(n\ logn\ 2^{log*n})$
- The **best** (with proof of optimality) algorithm is still... an **open** problem

The fastest known algorithm till now is of the order of $O(nlogn)$ [by Harvey and van der Hoeven, 2019]. This is the [relevant paper](https://hal.archives-ouvertes.fr/hal-02070778v2/document). It begins by introducing the previously known algorithms and then deep dives into the math behind proving its upper bound. We were able to prove a lower bound on sorting as seen in [How to analyze algorithms? Proving a lower bound for comparison based sorting](/blog/how-to-analyze-algorithms-proving-a-lower-bound-for-comparison-based-sorting), can we do the same for this problem?

No, we do **not know** if this algorithm is the best at the time of writing this note. The theoretical lower bound we know of is $\Omega(n)$ as the very least we require to do is process every bit of the input. There may or may not exist an algorithm better than $nlog(n)$, but we do not know of any such algorithms.
# References
These notes are old and I did not rigorously horde references back then. If some part of this content is your's or you know where it's from then do reach out to me and I'll update it. 
1. Professor [Kannan Srinathan's](https://www.iiit.ac.in/people/faculty/srinathan/) course on Algorithm Analysis & Design in IIIT-H
