---
layout: post
title: "TIL - Python 3.14 and T-strings"
date: 2025-08-02 00:00:00-0000
categories: 
---

Python 3.14 will come with T-strings.  
Template strings are a new string interpolation feature that is a generalization of f-strings.

Unlike f-strings, which immediately return a fully evaluated string, t-strings return an instance of a new immutable `Template` type that represents the string with deferred interpolation.  
This allows more advanced manipulation of the template parts before final evaluation.

Let's take it for a test drive!

I tried installing it via pyenv but it failed for some reason that I do not want to troubleshoot. So let's do it via Docker:
```
docker run -it python:3.14-rc-alpine
```

We're in the Python REPL:
```
Python 3.14.0rc1 (main, Jul 23 2025, 22:06:57) [GCC 14.2.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> 
```

Now let's try it out:

{% highlight python %}
>>> name = "Alice"
>>> f_string = f"Hello, {name}!"
>>> t_string = t"Hello, {name}!"
>>> 
>>> print("f-string:", f_string)
f-string: Hello, Alice!
>>> print("t-string:", t_string)
t-string: Template(strings=('Hello, ', '!'), interpolations=(Interpolation('Alice', 'name', None, ''),))
>>> 
>>> login = "Alice"
>>> password = "mySecret123"
>>> 
>>>
>>> signup_template = t"Hi, {login}, your password is {password}."
>>> print(signup_template)
Template(strings=('Hi, ', ', your password is ', '.'), interpolations=(Interpolation('Alice', 'login', None, ''), Interpolation('mySecret123', 'password', None, '')))
>>> print(signup_template.interpolations)
(Interpolation('Alice', 'login', None, ''), Interpolation('mySecret123', 'password', None, ''))
>>> dir(signup_template.interpolations[0])
['__class__', '__class_getitem__', '__delattr__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getstate__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__match_args__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', 'conversion', 'expression', 'format_spec', 'value']
>>> print(signup_template.interpolations[0].expression)
login
>>> print(signup_template.interpolations[0].value)
Alice
>>> print(signup_template.interpolations[1].expression)
password
>>> print(signup_template.interpolations[1].value)
mySecret123
>>> 
>>> 
>>> 
>>> def secret_safe(template):
...     censored_parts = []
...     for part in template.interpolations:
...         expr = part.expression
...         val = part.value
...         if expr == "password":
...             if len(val) > 4:
...                 val = val[:3] + "*" * (len(val) - 5) + val[-2:]
...             else:
...                 val = "*" * len(val)
...         censored_parts.append(val)
...     result = ""
...     for i in range(len(template.strings)):
...         result += template.strings[i]
...         if i < len(censored_parts):
...             result += censored_parts[i]
...     return result
... 
>>> 
>>> print(secret_safe(signup_template))
Hi, Alice, your password is myS******23.
>>> 
{% endhighlight %}

```
>>> 
>>> type(f_string)
<class 'str'>
>>> type(t_string)
<class 'string.templatelib.Template'>
>>> type(signup_template)
<class 'string.templatelib.Template'>
>>> 
```

As we can see, the f-string immediately evaluated to `"Hello ,Alice!"`, but the t-string created a `Template` object containing the statuc strings and interpolation expressions separately.  
This means that we can iterate through and process these parts individually, which allows for safe substitution, censoring sensitive data, or just custom string transformation in general.