---
layout: post
title: "pyproject.toml - Automating Book Availability Checks"
date: 2025-08-23 00:00:00-0000
categories: 
---

A `pyproject.toml` file is not just for code destined to be distributed or packaged and published (PyPI). It has a much wider scope. It is a central config file. It can store settings for tools like formatters and linters, it can list dependencies instead of `requirements.txt` (or pointing to it), it can store metadata…

Here’s the official guide: [https://packaging.python.org/en/latest/guides/writing-pyproject-toml/](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/)

And here are my changes: [https://github.com/k-candidate/selenium-book-search-slack-alerts/pull/2](https://github.com/k-candidate/selenium-book-search-slack-alerts/pull/2)

Now once I clone the repo, here’s what I have to do:
```
# The .python-version file takes care of the Python version
python -m venv .venv
source .venv/bin/activate
pip install .
```

I used a `pip install .` because I am not touching the source code this time.  
But usually I’d use `pip install -e .` to have an editable install so that I am able to modify the source code and have changes visible immediately without reinstalling. However, changes to project metadata or dependencies would still require rerunning `pip install -e .` to update packages or scripts.

One thing we notice in the `pyproject.toml` is:
```
[project.scripts]
book-search = "main:main"
```
The syntax is `command-name = "module:function"`

It allows me to use `book-search` from the command line without explicitly calling `python main.py`:

![pyproject.scripts in action]({{ site.baseurl }}/assets/images/pyproject-toml-01.png){:style="display:block; margin-left:auto; margin-right:auto; width:100.00%"}

That obviously is available only in the venv. But let’s look into how it works:

![pyproject.scripts in action]({{ site.baseurl }}/assets/images/pyproject-toml-02.png){:style="display:block; margin-left:auto; margin-right:auto; width:100.00%"}

We can see that `book-search` is just a tiny executable wrapper script placed in the `.venv/bin/`.