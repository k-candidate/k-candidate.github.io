---
layout: post
title: "Multi-threading - Automating Book Availability Checks"
date: 2025-12-08 00:00:00-0000
categories: 
---

I am looking for a way to speed up the GHA that checks for books in the local library's webpage.

Let's look at the different steps of the GHA:

![GHA without any changes]({{ site.baseurl }}/assets/images/multithreading01.png){:style="display:block; margin-left:auto; margin-right:auto; width:100.00%"}

We can see that the step that takes the most time is the actual book search script itself.

In this case, we are not doing any heavy computations, and therefore we should not be CPU bound. Meaning that multiprocessing should not be necessary.

However, we are waiting for the server to respond to our requests, so we are I/O bound. Meaning we should benefit from multithreading.

## Implementation

We could use the `threading` module. But I am going with the newer `concurrent.futures` which is a modern interface to `threading` (and also `multiprocessing`).

You can find the change in this PR: [https://github.com/k-candidate/selenium-book-search-slack-alerts/pull/10](https://github.com/k-candidate/selenium-book-search-slack-alerts/pull/10)

## Results

Here's the same GHA with multi-threading:

![GHA with multi-threading]({{ site.baseurl }}/assets/images/multithreading02.png){:style="display:block; margin-left:auto; margin-right:auto; width:100.00%"}

**We went from 2m22s to 57s.**  
**That's a 60% reduction!**