---
author: Kishore Kumar
date: 2022-08-07 10:02:06+0530
doc: 2025-05-18 17:07:02+0530
tags:
- domain-cs-algorithms-analysis
- domain-cs-algorithms-complexity
title: Church-Turing Hypothesis
---
# Church-Turing Hypothesis

The church turning hypothesis is essentially a hypothesis that answers the question, _"What are algorithms?"_ The hypothesis states that algorithms are nothing but Turing machines. Any mechanical computation can be performed by a Turing machine. If there is no Turing machine that can decide a problem P, then there is no algorithm that can solve P.

Note that while the Church-Turing Hypothesis is just a hypothesis and **not** proof. However, it is widely accepted as it is founded on very logical arguments that are based on the "axioms" of computing we stated while defining what constitutes a computational solution.

## The Turing Machine

We have an infinite length tape that has been split into an infinite number of finite length cells. We have a "read/write" head that can move along the tape (to the left or right cells). This read-write head operates on the current cell it is on top of. Note that this is in line with the fact that it is not possible to read/write to an infinite amount of memory. Hence it must operate on finite-sized cells.

The Turing machine is defined as a 7-tuple $(Q, \Sigma, \Gamma, \delta, q_0, q_{accept}, q_{reject})$.

1. $Q$ - **The finite set of states**
    
    The TM must at all times be in one of the finitely many _control_ states defined by the set $Q$. This is similar to the state diagram of circuits. When in a particular state the TM decides and responds to some input based on the control state it is in.
    
2. $\Sigma$ - **The finite alphabet set (not containing blank)**
    
    $\Sigma$ is the finite input alphabet. This is the _alphabet_ we encode our input in. Since input can be of any size, we also require a _blank_ alphabet to represent the end of some particular input. This is analogous to the C implementation of strings. Strings can be thought of as the input with ASCII constituting its input alphabet. The blank character here would be the `\\0` null terminator which signifies the end of the string. Note that the blank alphabet is **not** a part of this set.
    
3. $\Gamma$ - **The finite tape alphabet (includes blank)**
    
    $\Gamma$ is the finite _working_ alphabet + the _input_ alphabet. It is hence, a superset of the finite alphabet set $\Sigma$. The tape alphabet but contain at least _one_ more symbol than the input alphabet. Namely, the blank alphabet. However, apart from the blank alphabet, we can have many more _work_ alphabets which signify something of meaning to the TM read-write head. This is analogous to the "instruction encoding" of the ISAs used by modern computers.
    
4. $\delta:(Q\times \Gamma) \to(Q\times\Gamma\times\{L, R\})$ - **The transition function**
    
    When we are in some control state $Q$ and we read some tape symbol $\Gamma$, then we can move to some other state $Q'$, overwrite the contents of the current cell with some tape symbol $\Gamma'$ and move either to the left or to the right. Note that $\Gamma'$ and $Q'$ may be the same states. The transition function essentially just tells the Turing machine what to do when it reads some tape alphabet when it is in some control state $Q$.
    
    Note that it is also possible to remain in the same state. We can simply encode a move right and the right cell can be a move right. This would take 2 steps but the result is the same. The goal here is to define an abstract construct in a **simple** manner that allows us to represent any algorithm. _NOT_ defining the most efficient such construct.
    
5. $q_0$ - **The start state**
    
    Whenever the machine begins to work on a decision problem it must begin in some pre-defined control state. This is the _start_ state of the machine.
    
6. $q_{accept}$ - **The accept state**
    
    If the machine ever reaches this state, then the machine can decide that the input does indeed belong to the language and output `1` and stop.
    
7. $q_{reject}$ - **The reject state**
    
    If the machine ever reaches this state, then it can decide that the input does not belong to the language and output `0` and stop.
# References
These notes are old and I did not rigorously horde references back then. If some part of this content is your's or you know where it's from then do reach out to me and I'll update it. 
1. Professor [Kannan Srinathan's](https://www.iiit.ac.in/people/faculty/srinathan/) course on Algorithm Analysis & Design in IIIT-H