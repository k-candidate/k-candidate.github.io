---
layout: post
title: "TIL - Big O notation; enum module"
date: 2025-07-30 00:00:00-0000
categories: 
---

- Big-O doesn’t measure speed, it measures how performance degrades as n increases. It is about rate of decay.
- "Python is slow" is not always true, because a lot of Python operations do not stay in Python: they're in optimized C.
- Python's `in` operator is faster in `sets` that in `lists`.
  - `Lists` use dynamic arrays. Python performs a linear search: it iterates through each element of the list until it finds a match or the end of the list. Time complexity: `O(n)`.
  - `Sets` use hash tables which allow looking up key-value pairs quickly. Average-case time complexity: `O(1)`, but in the worst case `O(n)`.
- The [enum](https://docs.python.org/3/library/enum.html) module is part of the standard library and allows creating enumerations (constant values grouped together under a common type). It allows for better readability and easier maintenance.