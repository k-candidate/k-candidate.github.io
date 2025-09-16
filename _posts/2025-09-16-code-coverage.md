---
layout: post
title: "Code Coverage - Automating Book Availability Checks"
date: 2025-09-16 00:00:00-0000
categories: 
---

Code coverage measures the percentage of our code that runs when our unit test suite runs.

It helps see how much of our codebase is tested by our unit tests, makes it easier to spot untested code, and can improve code quality over time.

Coverage does not guarantee “good” tests. It simply means that every line ran, not that all scenarios were tested.

All the code changes are in [https://github.com/k-candidate/selenium-book-search-slack-alerts/pull/7](https://github.com/k-candidate/selenium-book-search-slack-alerts/pull/7).

I have it run in PRs with a minimum threshold so that in the future when I introduce changes to the code I have smaller odds of introducing bugs.

This is what it looks like when we are below the threshold: 

![code coverage below the threshold]({{ site.baseurl }}/assets/images/codecov01.png){:style="display:block; margin-left:auto; margin-right:auto; width:100.00%"}

And when above:

![code coverage above the threshold]({{ site.baseurl }}/assets/images/codecov02.png){:style="display:block; margin-left:auto; margin-right:auto; width:100.00%"}

I created a free account with [https://codecov.io](https://codecov.io) to visualize the change over time. It also shows us which code runs and which does not when running the unit tests: [https://app.codecov.io/github/k-candidate/selenium-book-search-slack-alerts/blob/code-coverage/main.py](https://app.codecov.io/github/k-candidate/selenium-book-search-slack-alerts/blob/code-coverage/main.py)

![codecov.io]({{ site.baseurl }}/assets/images/codecov03.png){:style="display:block; margin-left:auto; margin-right:auto; width:100.00%"}

To test locally we just use `pytest` without any arguments nor options and it will pick up the config we have in `pyproject.toml`:

![code coverage using pytest locally]({{ site.baseurl }}/assets/images/codecov04.png){:style="display:block; margin-left:auto; margin-right:auto; width:100.00%"}

I added a couple test functions to see the coverage go up:

![code coverage using pytest locally]({{ site.baseurl }}/assets/images/codecov05.png){:style="display:block; margin-left:auto; margin-right:auto; width:100.00%"}

In these 2 new functions I used fixtures ([https://www.geeksforgeeks.org/python/fixtures-in-pytest/](https://www.geeksforgeeks.org/python/fixtures-in-pytest/)) and the `yield` keyword ([https://www.w3schools.com/python/ref_keyword_yield.asp](https://www.w3schools.com/python/ref_keyword_yield.asp)).