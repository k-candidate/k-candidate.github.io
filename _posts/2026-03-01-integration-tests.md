---
layout: post
title: "Integration Tests - Automating Book Availability Checks"
date: 2026-03-01 00:00:00-0000
categories: 
---

![questions answers integration tests]({{ site.baseurl }}/assets/images/questions_answers_integration_tests.jpg){:style="display:block; margin-left:auto; margin-right:auto; width:50.00%"}

My code changes can be found here: [https://github.com/k-candidate/selenium-book-search-slack-alerts/pull/39](https://github.com/k-candidate/selenium-book-search-slack-alerts/pull/39).

## What are Integration Tests?

**Integration tests** verify that different components of an application work together correctly as a system. Unlike **unit tests**, which isolate and test individual functions in isolation (using mocks for external dependencies), integration tests exercise the wiring and orchestration of multiple components. 

**Unit tests** are fast and focused: they test single functions (`parse_args`, `safe_send_keys`, `send_slack_message`, etc.) with mocks to verify behavior in isolation.

**Integration tests** exercise the program entrypoint (`main.main()`) end-to-end, verifying that the isolated pieces wire together correctly. The integration test uses monkeypatches to avoid real Selenium browser launches and Slack calls, but it verifies that the orchestration logic (concurrency, sorting, output formatting) works correctly.

**End-to-end (E2E) tests** would go further by launching real browsers and calling real external services to simulate actual user flows through the complete system.

## What integration test was added and where is it?
A lightweight integration test is located at `tests/integration/test_integration.py`.  
It exercises `main.main()` end-to-end wiring (argument parsing, creating tasks, submitting to ThreadPoolExecutor, collecting futures, sorting results, and printing the aggregated output). The test monkeypatches `main.check_single_book` and `main.send_slack_message` so it does not launch browsers or call Slack.

## Should integration tests count toward coverage?
Maybe. I do not see the benefit here for me, and therefore chose not to: this repo measures coverage from unit tests only and runs the integration test separately without coverage.

## How is pytest configured so unit tests are measured for coverage only?
`pyproject.toml` contains `[tool.pytest.ini_options]` with
`addopts = "--cov=. --cov-report=xml"` and `testpaths = ["tests/unit"]`.  
Because `testpaths` limits collection to `tests/unit`, running `pytest` with default settings runs unit tests only and measures coverage from them.

## Do pre-commit hooks run integration tests?
No. The local pre-commit hook uses an entry that invokes `.venv/bin/pytest` (see `.pre-commit-config.yaml`). `pytest` reads `pyproject.toml` and therefore only collects `tests/unit` because of `testpaths`. The pre-commit pytest hook therefore runs the unit suite only.

## What changes were made to `tox.ini` and why?
`tox.ini` is configured to follow best practice:
- The default `[testenv]` now runs unit tests with coverage: `pytest tests/unit -v --cov=.--cov-report=xml`.
- A separate `[testenv:integration]` was added for on-demand integration runs: `pytest -o addopts= tests/integration -v` (you can run it locally with `uvx tox -e integration`).  
Why? To allow integration tests to be run on-demand or in a dedicated CI job.

## Why does the integration tox env use `pytest -o addopts= tests/integration`?
`pyproject.toml` sets `addopts = "--cov=. --cov-report=xml"` which injects coverage flags into all pytest invocations. However, the integration env only installs `pytest` (not `pytest-cov`), so `pytest` in that env does not understand coverage flags and would error if they were applied.  
The `-o addopts=` override clears the ini-file `addopts` for that invocation, preventing coverage flags from being injected into integration runs.  
This keeps the config simple: coverage is measured in the unit env (which has `pytest-cov` installed) and not in the integration env.

## Why do unit tests run across 4 Python versions but integration runs only on one?
To save CI time.  
There's no benefit in it for my case.

## How to run tests locally?
- Run unit tests (with coverage):
```bash
uv sync --locked --all-extras
source .venv/bin/activate
pytest -v
```
Or, without activating the venv, just `uv run pytest -v`
- Run integration tests directly:
```bash
uv run pytest tests/integration/ --no-cov -v
```
- Run integration via tox (on-demand):
```bash
uv tool install tox --with tox-uv # already documented in the post about tox
uv sync --locked --all-extras
uvx tox -e integration
```
- Run the full tox matrix (unit tests across Python versions):
```bash
uvx tox
```

## CI behavior
`.github/workflows/integration-tests.yaml` runs integration tests once (Python 3.14) with `pytest --no-cov tests/integration -v`. Integration tests are executed in CI separately from the tox matrix.

## Notes for future me
- Keep integration tests in `tests/integration` and mark them with `@pytest.mark.integration` if you want explicit markers in the future.
- Keep `pyproject.toml`'s `testpaths` pointing at `tests/unit` so quick `pytest` runs remain fast and consistent with the coverage gate.
