---
author: Kishore Kumar
date: 2022-08-03 10:02:06+0530
doc: 2025-05-18 17:07:02+0530
tags:
- domain-cs-algorithms-analysis
- domain-cs-algorithms-complexity
title: Defining Computational Problems
---
# Introduction
To study & analyze algorithms, we must have a solid foundational theory for what algorithms are. We often define algorithms as a series of steps that must be followed to solve a problem. This raises a few basic questions that we must answer concretely.

- What are **computational** problems?
- Once _a_ solution is obtained, how do we know that it is indeed correct?
- Say we have 2 solutions `a` & `b`. How can we compare these 2 solutions? On what basis can we say one solution is better than the other?
- Once we can do the above, how can we find the lower bound, i.e., the most optimal solution to a problem? and more importantly, can we prove that it is indeed optimal?

# What are computational problems?

There are many kinds of problems in the world. Math problems, world peace & hunger problems, problems arising from eating a bat, etc. to name a few. We wish to concern ourselves with problems of a particular class, **computational** problems. However, there are many difficulties associated with defining such a class. Consider the following challenges:

- **There may be infinite ways of posing the same problem**
    
    Consider the following problems.
    
    1. _What is the smallest prime number?_
    2. _What is the smallest even positive integer?_
    3. _What is the GCD of the set of even positive integers?_
    
    Notice that the output (solution) for all the above problems is two. From a computational standpoint, the above problems are all the same. But there are infinite ways to pose the same problem.
      
- **How do we pose a question without solving it?**
    
    Consider the age-old problem of sorting. The problem is usually phrased as follows,
    
    > _Given a sequence of `n` integers, among all possible permutations of this sequence, output such a sequence that it is in ascending order. That is, $a_i < a_{i+1} \ \ \forall \ \ 1 \leq i \lt n$_
    
    Notice that in the above statement, we provide the solution to the question itself. Phrased differently, the problem is essentially telling us to iterate over all possible $n!$ permutations and pick the permutation such that the sequence is in ascending order. While granted, this isn't a _good_ solution, it is a solution. We must come up with a way to pose problems that we do not have a solution to yet. Or maybe even problems for which there does _not_ exist any solution.
    
- **What kind of tools can we allow to be used to solve the problem?**
    
    Notice that depending on the solutions that are allowed to a problem, the meaning of "solving" the problem changes. Consider the following _mythological_ sort algorithm.
    
    1. Meditate until god appears
    2. Provide input to god
    3. Obtain sorted output from god
    
    This is not a _computational_ solution to the sorting problem. Hence it is necessary to enforce a _computational_ constraint on problems.
    
    ## Defining a computational problem
    
    When defining a computational problem, we make the following assumption about the world we live in.
    
    >🧭 The input is digitized. We live in a noisy environment. Whenever there is noise, if 2 symbols are closer than some threshold, we say they are in the same equivalence class and are one and the same. This ensures that the total number of symbols we must deal with becomes finite in a finite space. This ensures that we're able to digitize the input and output.
    
    Further, assume that the output has multiple but a finite number of bits. We can then model each bit as a separate problem. This enables us to model all problems with finite output as decision problems. A decision problem is simply a problem with **1-bit** output. "_Is this true or false?"_
    
    **This allows us to pose problems as membership queries in _"languages."_**
    
    ### Defining a "Language"
    
    We can reduce the question _"X is my input and I am looking for the output Y"_ to "_Does my input X belong to the set of all inputs which give output one?"_
    
    >💬 **Languages** Each decision problem is characterized by a subset of the set of all possible inputs. (,i.e., subset of say, {0, 1}*)
    >
    > $L = \{x \ | \ s\in \{0,1 \}^* \}$
    >
    > For example: Consider the problem of checking if a sequence is sorted or not.
    > 
    > Let us encode our strings as numbers in binary separated by some terminator which splits each number in the sequence. Our question now reduces to, _"Given a string encoded this form, does it belong to the language $L_{sorted}$?"_ The string that encodes the sequence {1, 2, 3} would belong to this set. But the string which encodes the sequence {3, 2, 5} would not. Our encoding must be able to represent all different inputs in a unique manner. Notice that this has allowed us to reduce the problem to a simple decision problem of querying membership in our language $L_{sorted}$
    
    This is essentially how all problems in complexity theory are formalized.
    
    This formalization allows us to deal with most of the challenges aforementioned. Multiple ways to pose the same question no longer matter as the problems are characterized by the language. If the set of all possible inputs for which the output is 1 is the same for 2 different problems, then they are one and the same. Further, we can now pose problems without providing a solution as it is possible for us to define sets without having to enumerate them.
    
    We will discuss the problem of what tools can the solver be allowed to use when discussing how we define a _solution_ to a computational problem.
    
    # What are solutions in the world of computing?
    
    While there is no such thing called "axioms of computation" in standard literature, Prof. Kannan calls the following the base "axioms" or assumptions we make when defining what counts as a solution.
    
    - **It takes non-zero time to retrieve data from far-off locations**
        
        This essentially implies that the flow of information is not instantaneous. Consider memory so large that it spans the distance from Earth to Mars. If information transfer from the 2 ends of this memory was instantaneous then it would imply information traveling faster than light speed. This shouldn't be possible. Hence it is not feasible to allow our computational solutions to be able to have **random** access to huge chunks of memory.
        
    - **Only finite information can be stored/retrieved from finite volume**
        
        We cannot store infinite information in finite memory. Note that this assumption/axiom essentially invalidates solutions that allow time travel. If time travel were possible, we could go back in time to change the contents of memory/access infinite different states of some finite volume, and hence, allow infinite information access from finite memory. This is now ruled out.
        
    - **A finite-length code only exerts a finite amount of control**
        
        Any finite-length program cannot be omnipotent. That is, because the number of instructions is finite, there can only be a finite number of states the machine can exist in. Both the symbols making the instruction set and the instructions are finite, hence limiting the states it can be into a finite amount.
        
    
    > ⚠️ Note that these assumptions are made because we are limited by the technology of our time. If we are able to construct technology that can, indeed, violate any of the above "axioms", then we will in fact be able to come up with a model of computation where we will be able to solve problems much harder than the ones we are able to do today.
# How to compare computational solutions?

Now that we have defined computational problems and solutions, we need a way to compare two different solutions to a problem and say deterministically which solution is _"better"._

However, we again run into multiple challenges. It is difficult to come up with a deterministic answer to a somewhat subject question, _"Which solution is better?"_

In the field of complexity theory, we usually focus on worst-case analysis/asymptotic analysis. We measure the performance of a solution in terms of its input size. However, note that this is not necessarily the best method to compare two solutions. Let's say some solution 'a' takes (a heavy) constant amount of time to run and another solution 'b' runs in logarithmic time. For larger inputs, we should see algorithm `a` perform better than `b`. But it may be true that our machine is never provided large inputs. In this case, it might be better to compare the best case.

To judge which algorithm is "better", we can say that the solution which uses lesser resources to compute is better. However, we run into another challenge. Computing a solution does not usually just depend on _one_ resource. One very precious resource is time. But there are other resources that matter too. Space & power are two other important resources.

In general, we put **time** at a pedestal compared to all other resources. In general, every other resource can be reused or generated in some manner. We can reuse memory & generate power, but time once lost can never be gained back. Hence unless specified explicitly, when we compare 2 solutions, we often implicitly assume that we are comparing 2 solutions based on the most precious resource **time.**

> ☄️ Note that, _technically,_ according to relativity: space and time are the same constructs and we can effectively interchange them. It is possible to say that I can start a program that would take 50 million years to compute, load it into a spaceship, let it go on a trip across the universe close to the speed of light and then when it returns to earth after a month, collect the output. However, as we lack the resources to be able to do anything even remotely close to this in the near (or distant) future, we ignore these technicalities when deciding on the quantity we'd primarily wish to compare algorithms with.

Now that we've defined how to define a problem, let's try to construct useful arguments using this definition. [Are there computational problems that computers cannot solve?](/blog/are-there-computational-problems-that-computers-cannot-solve). How do we define a "solution" to a computation problem in an "algorithmic" sense. Note that this theory dates to before when computers were invented. How do we formalize a notion of a machine that can carry out these tasks? This is what the [Church-Turing Hypothesis](/blog/church-turing-hypothesis) aims to answer. 
# References
These notes are old and I did not rigorously horde references back then. If some part of this content is your's or you know where it's from then do reach out to me and I'll update it. 
1. Professor [Kannan Srinathan's](https://www.iiit.ac.in/people/faculty/srinathan/) course on Algorithm Analysis & Design in IIIT-H