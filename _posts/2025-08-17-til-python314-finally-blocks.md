---
layout: post
title: "TIL - Python 3.14 and 'finally' blocks - PEP 765"
date: 2025-08-17 00:00:00-0000
categories: 
---

In Python versions prior to 3.14 the `finally` block is used as part of exception handling to guarantee that certain cleanup code runs, regardless of whether an exception was raised or not in the `try` block.  
This is especially useful for releasing resources such as files or network connections.

## Basic behaviour
- The code inside `finally` will always execute, whether or not an exception occurs in the try or except blocks.
- We don’t have to use except for `finally` to work. A `try`/`finally` combination is valid and common.

One example is closing a file no matter what (even if there's an error while reading it)

{% highlight python %}
try:
  file = open("example.txt", "r")
  # Some code that may raise an exception
finally:
  file.close()  # Always runs, even if there was an error above
{% endhighlight %}

One quirky thing in older Python versions, is that we can use `return`, `break`, or `continue` statements inside `finally`. These statements would override `return` values and exceptions from the try or except block, which can lead to confusing or buggy code. This is not intuitive.
Here's an example:

{% highlight python %}
def func():
  try:
    return "try"
  finally:
    return "finally"  # This overrides the previous return

print(func())  # Outputs: "finally"
{% endhighlight %}

![unintuitive finally block in old python]({{ site.baseurl }}/assets/images/py314-finally-01.png){:style="display:block; margin-left:auto; margin-right:auto; width:100.00%"}

The problem is that if an exception is raised in `try`, a `return` or `break` in `finally` will suppress that exception.  
Here's an example:

{% highlight python %}
def func():
  try:
    raise Exception("error")
  finally:
    return "suppressed"  # Exception is swallowed!

print(func())  # Outputs: "suppressed"
{% endhighlight %}

![finally block suppressing exception in old python]({{ site.baseurl }}/assets/images/py314-finally-02.png){:style="display:block; margin-left:auto; margin-right:auto; width:100.00%"}

## What changed?
In Python 3.14, there is a significant change regarding the use of control flow statements (specifically `return`, `break`, and `continue`) in `finally` blocks. As per PEP 765, Python 3.14 now disallows these statements if they would cause the flow to exit from a `finally` block. This means that attempting to use `return`, `break`, or `continue` to break out of a `finally` block will raise a SyntaxError in Python 3.14.

Here's an example of code that would work in older Python but raise a Syntax Error in Python 3.14:

{% highlight python %}
def test():
  try:
    raise Exception("Oops")
  finally:
    return "Finally Return"  # In Python 3.14, this now causes SyntaxError
{% endhighlight %}

![comparison between py314 and older]({{ site.baseurl }}/assets/images/py314-finally-03.png){:style="display:block; margin-left:auto; margin-right:auto; width:100.00%"}

## What is still allowed?
Using `return`, `break`, or `continue` inside control structures (like a loop) that are themselves inside a `finally` block is allowed, as long as they don’t exit the `finally` block itself. For example, breaking out of a loop within a `finally` block (but not out of the finally block) is permitted.  
Here's an example:

{% highlight python %}
def demo():
  try:
    print("In try")
  finally:
    for i in range(3):
      print("Loop", i)
      if i == 1:
        break  # This is allowed: breaks out of loop, not the finally block
    print("After loop in finally")  # This will run after the loop

demo()
{% endhighlight %}

![what is still allowed in python314]({{ site.baseurl }}/assets/images/py314-finally-04.png){:style="display:block; margin-left:auto; margin-right:auto; width:100.00%"}

## Conclusion
It's more intuitive. But if we have code that uses `return`, `break`, or `continue` statements in `finally` blocks that exit the block, then we should refactor it for Python 3.14 compatibility.