---
author: Kishore Kumar
date: 2024-02-08 13:42:01+0530
doc: 2024-02-08 06:06:48+0530
tags:
- domain-cs-languages-cpp
title: '`New` and `Delete`'
---
# `new` & `delete`

Before we go ahead and figure out what smart pointers are, let's take a moment to look back to how we handle heap allocated memory in C++. Back in C, we had the `malloc` and `free` functions to handle heap memory. `new` and `delete` are C++ operators that try to do the same task, but cleaner. 

```cpp
int *b = (int*) malloc(sizeof(int)); // Old C-style heap allocation
int *c = new int; // New C++ heap allocation
```

`malloc` returns `void*`. You will notice that back in C, we did not have to explicitly cast a `void*` to `int*`, however in C++, implicit pointer type conversion is a compile error. `int *b = malloc(sizeof(int))` will throw:
> `error: invalid conversion from ‘void*’ to ‘int*’ [-fpermissive]`

In C++, `new` and `delete` are **operators.** They are **not** functions like their C counterparts. This means that just like any other operator, they can be overloaded to do pretty much anything. This means that the behaviour of `new` & `delete` are dependent on the C++ library and compiler that you are using. 

However, most implementations just implement calling `new` to call the underlying `malloc` function. And similarly `free` for `delete`. But one key additional task that `new` does is it **will** also **call the constructor** for the object it is creating. And `delete` the destructor.

We'll use the following `Entity` class as a toy-example when playing around with `new` / `delete`.

```cpp
class Entity{
public:
	Entity(){
 		std::cout << "Constructor!" << std::endl; }
	Entity(const std::string &name) : name(name) {
		std::cout << "P-Constructor!" << std::endl; }
	~Entity() {
 		std::cout << "Destructor!" << std::endl; }
private:
	std::string name;
};
```

Here are three ways to use `new` in C++.

```cpp
int main(void){
	Entity *obj = new Entity; // Output: Constructor!
	Entity *same_thing = new Entity(); // Output: Constructor!
	Entity *pobj = new Entity("abcd"); // Output: P-Constructor!, name: abcd
	Entity *obj_arr = new Entity[5];
	/**
	 * Output:
	 * Constructor!
	 * Constructor!
	 * Constructor!
	 * Constructor!
	 * Constructor!
	 */
	// This is called "placement new"
	std::cout << sizeof(Entity) << std::endl; // Output: 32
	int *space = new int[10];
	Entity *placement_new = new(space) Entity[2];
	/*
	 * Output:
	 * Constructor!
	 * Constructor!
	 */
}
```
 
So the first 4 examples are the basic ones. You'll notice that `new` always makes it a point to call the constructor of the class we're allocating memory for. This is an attempt to work around the uninitialized memory problem we have with `malloc`. Links back to [RAII - Resource Acquisition Is Initialization](/blog/raii-resource-acquisition-is-initialization) principles as well. We **don't** want uninitialized memory. We can use `new` to also initialize an object with it's parameterized constructor instead of the default one. However we can't parameter initialize an array of them :) 

Getting a pointer to an array of `Entity` objects is also quite simple. `obj_arr` is a pointer to a contiguous chunk of memory that points to an array of 5 `Entity` objects.

The interesting `new` use-case here is the "placement new". Here, `new` isn't actually allocating a block of memory. It simply uses the previously allocated memory for `space` and just initializes `Entity` in that memory by calling it's constructor. 

For `delete`, it's pretty similar. 

```cpp
delete obj; // Output: Destructor!
delete[] obj_arr;
/**
 * Output:
 * Destructor!
 * Destructor!
 * Destructor!
 * Destructor!
 * Destructor!
*/
// Note! It's also possible to compile
delete obj_arr; // Output: Destructor!
```

You'll notice the last way to call `delete` actually just calls the destructor once. So when de-allocating a pointer to an array of elements in memory it's important to always remember to use `delete[]` instead of `delete` to properly clean this memory. 

### Why `new` & `delete`?

One, it's a lot cleaner than the C-style way. Two, it is a paradigm that avoids the uninitialized memory issue we can have when using the C-style `malloc` and `free` functions. `new` and `delete` prevent this from ever happening by **always** calling the constructor and destructor. 

However, a problem they still don't solve is the problem of memory leaks and dangling pointers. To solve this, we have the idea of [Smart Pointers](/blog/smart-pointers).
