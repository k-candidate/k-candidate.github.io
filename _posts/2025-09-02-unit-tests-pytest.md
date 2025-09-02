---
layout: post
title: "Unit Tests - Pytest - Automating Book Availability Checks"
date: 2025-09-02 05:00:00-0000
categories: 
---

Unit tests are automated tests focusing on the smallest functional parts of code (e.g. functions or methods) to verify they behave correctly in isolation, usually without dependencies like databases. They are fast, isolated, and check a single logical concept.

[Pytest](https://github.com/pytest-dev/pytest) is a popular and powerful Python testing framework that makes it easy to write, organize, and run tests for Python code. It is known for its simple syntax, rich features, and excellent error reporting, making tests easier to read and maintain.

## How Pytest works
- Files must be named either with the `test_` prefix (e.g. `test_example.py`) or the `_test` suffix (e.g. `example_test.py`). These are the standard patterns pytest searches for in directories.
- Tests are usually written in functions or classes whose names start with `test_`. Only functions starting with `test_` will be recognized and executed as tests by pytest.
- For classes used to group tests, class names should start with `Test` (e.g. class TestMath:), and the methods inside should also begin with `test_`.
- Each test uses Python’s built-in `assert` statement. Pytest outputs detailed error messages when assertions fail, which helps diagnose problems quickly. 
- When run, pytest automatically discovers and executes all tests matching its pattern (e.g. files named `test_*.py` or ending with `_test.py`). Meaning, we do not have to give it the tests script file as an argument, and we can just use `uv run pytest`.
- Example:

{% highlight python %}
def func(x):
    return x + 1

def test_answer():
    assert func(3) == 5

def test_answer2():
    assert func(6) == 7

def test_answer3():
    assert fun(4) == 8
{% endhighlight %}

We run  it using the command `pytest` (after installing the package)

![Pytest example]({{ site.baseurl }}/assets/images/pytest-example.png){:style="display:block; margin-left:auto; margin-right:auto; width:100.00%"}

- For easier debugging in GitHub UI: [https://github.com/pytest-dev/pytest-github-actions-annotate-failures](https://github.com/pytest-dev/pytest-github-actions-annotate-failures). We just install it and use pytest as we were going to do.

## Notes on my Code Changes
- The changes can be seen in this PR: [https://github.com/k-candidate/selenium-book-search-slack-alerts/pull/6](https://github.com/k-candidate/selenium-book-search-slack-alerts/pull/6).
- A mock is a fake object used in testing to simulate the behavior of real objects. It allows us to check if our code interacts correctly with things like web elements, browser drivers, or web requests without needing to actually run a browser or send real HTTP requests.
- Combo of pytest and mocking:
  - pytest runs the tests, checks assertions, and reports failures.
  - unittest.mock makes fake objects to check that our code calls them in the way we expect.
  - This lets us test our logic quickly, without slow or unreliable external systems.
- [https://docs.python.org/3/library/unittest.mock.html](https://docs.python.org/3/library/unittest.mock.html)
- We Use side_effect (also in the python doc I just mentioned) to simulate an element throwing an exception.
- In general, the monkeypatch fixture helps us to safely set/delete an attribute, dictionary item or environment variable, or to modify sys.path for importing. In our case, monkeypatch replaces the network call inside send_slack_message so that no actual HTTP requests happen. It simulates all possible results (success, failure, exception).
- The "http://dummy-url.com" is just a placeholder. The mock intercepts and prevents real network calls.
- The tests purposely use Mock() and monkeypatch. When running tests, these take the place of real selenium or urllib objects so we aren't expected to set up a browser/webserver/Slack for testing.
- On purpose, I introduced a mistake to verify if the unit tests would catch it, and also so see how the Pytest plugin looks in action: 

![Pytest plugin]({{ site.baseurl }}/assets/images/pytest-plugin.png){:style="display:block; margin-left:auto; margin-right:auto; width:100.00%"}