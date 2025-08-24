---
layout: post
title: "Black, Isort, Mypy - Code Quality Checks - Automating Book Availability Checks"
date: 2025-08-24 00:00:00-0000
categories: 
---

![Black, Isort, and Mypy logos]({{ site.baseurl }}/assets/images/black-isort-mypy.png){:style="display:block; margin-left:auto; margin-right:auto; width:50.00%"}

## Black
- Black is a Python code formatter that automatically formats Python code to follow a consistent style based on the [PEP 8 style guide](https://peps.python.org/pep-0008/).  
- It can be included in CI pipelines for checking: `black --check .`  
- Here’s their repo: [https://github.com/psf/black](https://github.com/psf/black)
- I am using it via this extension: [https://marketplace.visualstudio.com/items?itemName=ms-python.black-formatter](https://marketplace.visualstudio.com/items?itemName=ms-python.black-formatter). The extension ships with a `black` binary which can be used from the cli.
- To see the changes that would be made to a file (or directory) without making the changes (dry-run): `black --diff .`
- To use the extension: command palette > Format Document.

## Isort
- Isort specializes in sorting and organizing import statements in Python files. It sorts imports alphabetically, groups them into sections (e.g., standard library, third-party, local imports), and formats multi-line imports for readability. Isort can also add or remove imports automatically as configured.
- Like Black, it can be integrated into workflows: `isort --check-only .`
- Here’s their repo: [https://github.com/pycqa/isort/](https://github.com/pycqa/isort/)
- I am using the extension [https://marketplace.visualstudio.com/items?itemName=ms-python.isort](https://marketplace.visualstudio.com/items?itemName=ms-python.isort).
- Once installed: command palette > Organize imports.

## Mypy
- Mypy is a static type checker for Python. It analyzes Python code to check type correctness based on type annotations, helping to catch bugs and improve code quality by enforcing type consistency before runtime.
- Here’s their repo: [https://github.com/python/mypy](https://github.com/python/mypy)
- To set in VSCode: [https://code.visualstudio.com/docs/python/linting#_choose-a-linter](https://code.visualstudio.com/docs/python/linting#_choose-a-linter) > [https://marketplace.visualstudio.com/items?itemName=ms-python.mypy-type-checker](https://marketplace.visualstudio.com/items?itemName=ms-python.mypy-type-checker). The extension ships with `mypy`.
- Here’s an example of what this tool can do for us: it warns us as we’re writing code that a `None` cannot be added to a `dict`: 

![Mypy in action]({{ site.baseurl }}/assets/images/mypy-01.png){:style="display:block; margin-left:auto; margin-right:auto; width:100.00%"}

- But what if I did not specify the type? Then I’d have to run mypy in strict mode to catch the errors. That can be specified in the `pyproject.toml`, which takes us to my next point where I answer this.

## Configuring dev tools in the pyproject.toml
- In my PR, [https://github.com/k-candidate/selenium-book-search-slack-alerts/pull/3](https://github.com/k-candidate/selenium-book-search-slack-alerts/pull/3), we can see that strict mode is set to true for mypy in the pyproject.toml.
- Here’s what mypy in strict mode gives us when we do not specify the type:

![Mypy in action]({{ site.baseurl }}/assets/images/mypy-02.png){:style="display:block; margin-left:auto; margin-right:auto; width:100.00%"}

- To fix it, we’d have do something like this:

![Mypy in action]({{ site.baseurl }}/assets/images/mypy-03.png){:style="display:block; margin-left:auto; margin-right:auto; width:100.00%"}

- To install our dependencies the command stays the same. But to install the optional dependencies:
```
pip install .[dev]
```
This installs the main dependencies and the dev tools.

- VSCode reads the `[tool.*]` configs in our `pyproject.toml` automatically. So we’re set in our local development environment. But what about the CI?

## GHA for Code Quality Checks in CI
- I made a GHA that runs the 3 tools to check code quality in Pull Requests. We can see it as well in [https://github.com/k-candidate/selenium-book-search-slack-alerts/pull/3](https://github.com/k-candidate/selenium-book-search-slack-alerts/pull/3).