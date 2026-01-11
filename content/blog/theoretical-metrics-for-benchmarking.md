---
author: Kishore Kumar
date: 2022-03-16 19:03:13+0530
doc: 2025-05-18 17:07:02+0530
tags:
- domain-cs-systems-high-performance-computing
title: Theoretical Metrics for Benchmarking
---
# Benchmarking a system

[Profiling a Program](/blog/profiling-a-program) tells us where hotpots in a programs execution are, what parts are the bottleneck and where we should focus our attention when trying to improve performance, but it’s just as important for us to know what the theoretical best performance is that we can get given some hardware. (More on this in [Brent's Theorem & Task Level Parallelism](/blog/brent-s-theorem-task-level-parallelism) as well).

## Why benchmark?

There is no point repeatedly trying to optimize some code just because it takes up the most time when that part of the code is already performing very close to it’s theoretical maximum. Some code can only execute so fast on some given hardware and there is no point trying to optimize it further.

[https://stackoverflow.com/questions/329174/what-is-flop-s-and-is-it-a-good-measure-of-performance](https://stackoverflow.com/questions/329174/what-is-flop-s-and-is-it-a-good-measure-of-performance)

> If you know the CPU's theoretical peak performance in FLOPS, you can work out how efficiently you use the CPU's floating point units, which are often one of the hard to utilize efficiently. A program which runs 30% of the FLOPS the CPU is capable of, has room for optimization. One which runs at 70% is probably not going to get much more efficient unless you change the basic algorithm. For math-heavy algorithms like yours, that is pretty much the standard way to measure performance. You could simply measure how long a program takes to run, but that varies wildly depending on CPU. But if your program has a 50% CPU utilization (relative to the peak FLOPS count), that is a somewhat more constant value (it'll still vary between radically different CPU architectures, but it's a lot more consistent than execution time). But knowing that "My CPU is capable of X GFLOPS, and I'm only actually achieving a throughput of, say, 20% of that" is very valuable information in high-performance software. It means that something other than the floating point ops is holding you back, and preventing the FP units from working efficiently. And since the FP units constitute the bulk of the work, that means your software has a problem. It's easy to measure "My program runs in X minutes", and if you feel that is unacceptable then sure, you can go "I wonder if I can chop 30% off that", but you don't know if that is possible unless you work out exactly how much work is being done, and exactly what the CPU is capable of at peak. How much time do you want to spend optimizing this, if you don't even know whether the CPU is fundamentally capable of running any more instructions per second?

## Defining some metrics to measure performance

Defining “how fast” a system performs is not an easy task. A specialized system might perform with varying speeds for different types of tasks. Plus, we don’t even have a unit to measure “performance.”

Again, performance of a system depends on the type of task it is computing. A graphics card will perform exceptionally well in highly parallelized workloads but might be terrible in serial workloads. When evaluating devices we must keep into account our use case and use a performance metric that is appropriate for our use case. Keeping this in mind, the world of computer science has several units on which we can measure the performance of a device. Perhaps the most famous of which, is the GFLOP.

1. **FLOPS -** FLOPS in CS mean “Floating point operations per second”, and as the name implies, this metric is quite useful when we are evaluating some system for performance in scientific computation involving workloads. A CPU capable of 2 GFLOPS is twice as fast as another CPU only capable of doing 1 GFLOP, _while doing floating point operations_.
    
    A natural question to ask here is, “Why FLOPS?”
    
    → The reason for this is that this method of computation is widely employed in scientific simulation work. Furthermore, when compared to integer operations, FLOPs are substantially more complex for a CPU to execute. Both of these are major factors why FLOPs have become a universal benchmark for HPC. Computers that perform online services or database queries, on the other hand, generally use integer arithmetic and for them we have MIPS. For single PC systems, we compute
    
    $$ FLOPS = cores \times \frac{cycles}{second} \times \frac{FLOPs}{cycle} $$
    
2. **MIPS -** MIPS stands for “Millions of instructions per second” and it is essentially a measure of the integer performance of a computer. However, in CISC machines different instructions take different time to execute hence the reported value depends heavily on the mix of the instructions used in the benchmark. MIPS tries to model the peak performance of a machine with few branches and no cache contention. It is a decent estimate of computer performance on commonly used apps which rely on integer arithmetic.
    
    $$ IPS = sockets \times \frac{cores}{socket}\times clock\times\frac{instructions}{cycle} $$
    
    Note: Instructions/cycle depends on the test instructions, data and many such test-specific factors.
    
    ## Benchmarking software
    
    There’s a bunch of programs out there written to stress-test your machine and record the max `insert-quantity-you're-measuring` that your machine is capable of. One such tool is the [Whetstone Benchmark](https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&ved=2ahUKEwj2mdK7vuX2AhVCR2wGHbtFAocQFnoECAcQAQ&url=https%3A%2F%2Fen.wikipedia.org%2Fwiki%2FWhetstone_(benchmark)&usg=AOvVaw0Letk1QFpBEe0FOy7rJpyU). I found code for it on [Netlib](https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&ved=2ahUKEwiPmKrKvuX2AhX4RmwGHfzNB_4QFnoECBAQAQ&url=https%3A%2F%2Fwww.netlib.org%2Fbenchmark%2Fwhetstone.c&usg=AOvVaw0axRP6mDSotBx0v1OCU_Ho). Although, looking at the code and results it produces, it looks like Netlib’s version measures MIPS, not FLOPS.
    
    ## Detour into compiler benchmarks and analysis
    
    I decided to try out different compilers and compiler flags and I’m glad I did, the results I got are pretty surprising
    
    ### ICC
    
    - `-O0` : 5882.4 MIPS
    - `-O3` : 100000.0 MIPS _(17x speedup!)_
    
    ### GCC
    
    - `-O0` : 6250.0 MIPS _(Faster than `icc -O0`!)_
    - `-O3` : 25000.0 MIPS MIPS _(4x slower than `icc -O3`)_
    
    This wasn’t what I expected at all. You’d expect the numbers to at least be close, perhaps some `avx` optimizations aren’t on?
    
    - `-O3 -mavx2 -mfma` : 25000.0 MIPS
    
    No change at all. This was quite disappointing, until...
    
    - `-Ofast` : 100000.0 MIPS
    
    What is going on? Why is there a sudden increase of **4x** performance from this flag? More on this later.
    
    ### Clang - LLVM
    
    - `-O0` : 5555.6 MIPS _(On par with `icc` and slightly slower than `gcc`)_
    - `-O3` : 16666.7 MIPS _(1.5x slower than `gcc`)_
    - `-Ofast` : 100000.0 MIPS
    - `-Ofast -mavx2` : 125000.0 MIPS _(Highest we’ve managed to record)_
    
    So what is going on here? How is `icc` so fast with just `O3` and why do the other two compilers need an extra flag to reach `icc`'s `O3` speeds? And no `icc` does not speed up more on `Ofast`, the above were the highest scores I managed to get out of each compiler by trying a lot of different flags.
    
    Upon investigating further, we discover that `-Ofast` turns on a flag called `-ffast-math` which is basically allowing the compiler to break some rules when doing floating point arithmetic for the sake of performance. [This blog](https://simonbyrne.github.io/notes/fastmath/) by Simon Byrne explains the risks of `-ffast-math` in detail but in brief, this allows it to rearrange and vectorize more code, hence the huge performance boost. Turns out, in floating point land, $a + (b+c) \neq (a+b) + c$. Associativity might lead to more floating point precision errors. Further, `ffast-math` considers all math that is computed is finite, so no `inf`, `nan`, etc. Subnormals (numbers _very_ close to zero) get considered as 0 via a hardware FPU control register, which may even affect _other code_ running on the same thread.
    
    To be fair, most of these optimizations won’t affect code in non-scientific environments much, but at the same time these are real risks. **The reason why `icc` gets such high performance on `O3` is because Intel has it’s version of `-ffast-math` on by default.** `-fp-model=fast` is the default in [ICC](https://www.intel.com/content/www/us/en/develop/documentation/cpp-compiler-developer-guide-and-reference/top/compiler-reference/compiler-options/compiler-option-details/floating-point-options/fp-model-fp.html).
    
    ### Reality of theoretical benchmarks
    
    In practice, while our theoretical estimates give us a _very loose_ upper bound on the performance we can hope to expect, it’s not very accurate. Consider FLOPS for example, most floating point operations do not take one cycle. FMA operations combine add and multiply and have their own throughput / latency to consider. SIMD vectorization affects the number of data units on which we apply the FLOP at the same time. Even SIMD instructions have their own throughput / latency. Add to this pipe-lining effects and most importantly, memory limits thanks to small cache sizes, memory bandwidth, etc. and there are a lot many factors which give us much lower peak practical performance vs peak theoretical performance. Hence while theoretical numbers are not a _terrible_ idea, it’s almost always good practice to run software benchmarks and get a good practical estimate as well.
    
    This site (translated from Russian) gives a pretty nice overview of why theoretical computation of GFLOPS/sec is a bad estimate and suggests an alternative which involves profiling a program to count the number of floating point operations it does and using this to measure GFLOPS/sec instead. [https://habr-com.translate.goog/ru/company/intel/blog/144388/?_x_tr_sl=auto&_x_tr_tl=en&_x_tr_hl=en-US&_x_tr_pto=wapp](https://habr-com.translate.goog/ru/company/intel/blog/144388/?_x_tr_sl=auto&_x_tr_tl=en&_x_tr_hl=en-US&_x_tr_pto=wapp)

# Operational Intensity and Achievable peak throughput

A slightly better estimate we can do involves using the max bandwidth our CPU can receive, Let’s say we’re running the `saxpy` program which computes $S = \alpha X +Y$. Here we’ll assume $\alpha$ is a scalar stored in memory and $X$ and $Y$ are floating point vector arrays. Now, we’ll disregard the load and store operations required to load the operands into register memory as this will mostly be pipelined. The floating point computations we are doing are $2$, One add and one multiply. We’ll ignore FMA for now.

So we’re doing $2$ FLOPs on $2 \times 4 = 8$ bytes of data. This gives us $operational \ intensity = \frac{2}{8} = 0.25$.
 
Operational intensity is essentially the number of FLOPs we’re doing per unit data. Multiplying this number by max bandwidth we get an idea of the peak throughput our program can hope to achieve. If my CPU had a max bandwidth of let’s say 50GB/s, I would have a peak throughput of around $12.5 \ GFLOPS / sec$