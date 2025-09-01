---
layout: post
title: "Rustification of Python - uv, ruff, ty - Automating Book Availability Checks"
date: 2025-09-01 00:00:00-0000
categories: 
---

The changes that correspond to this post are in these PRs: 
- [https://github.com/k-candidate/selenium-book-search-slack-alerts/pull/4](https://github.com/k-candidate/selenium-book-search-slack-alerts/pull/4)
- [https://github.com/k-candidate/selenium-book-search-slack-alerts/pull/5](https://github.com/k-candidate/selenium-book-search-slack-alerts/pull/5)

## Switch from pyenv and pip to uv
In `~/.bashrc` and `~/.profile` comment out the lines:
```
export PYENV_ROOT="$HOME/.pyenv"
command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"
```

If we run `which pyenv`, we see that it is in our homefolder (`~/.pyenv/bin/pyenv`). Let’s get rid of it:
```
rm -rf ~/.pyenv
```

Now let’s install uv:
```
curl -LsSf https://astral.sh/uv/install.sh | sh
```

- How uv chooses the Python version:
  - python-version file: If the project directory includes a `.python-version` file, UV uses the version indicated in that file.
  - Command-line specification: We can override the Python version per command using flags like `uv run --python 3.12 ...`
  - System and managed installations: UV can discover Python installations already present on the system, or manage versions it has installed itself. Managed versions are those UV installed, while system versions include those installed by other means (OS, pyenv, manual install).
  - Multiple versions support: UV supports having multiple Python versions on the system, and packages will be installed under the interpreter we specify for the operation.

- A few useful commands:
  - To list all python interpreters: `uv python list` (similar to `pyenv versions`)
  - There’s no equivalent for `pyenv version`. You’d have to check `.python-version` or use `uv run python --version`
  - To pin a version locally: `uv python pin 3.13` (similar to `pyenv local 3.13`)
  - There’s no equivalent for `pyenv shell 3.13`. You’d have to use `uv run --python 3.13 CMD` to temporarily use that python version for a command.
  - `ls -al $(uv python dir)` shows what python versions are installed via uv and where
  - `uv python uninstall 3.11.13`

Here’s the ref: [https://docs.astral.sh/uv/reference/cli/#uv-python-install](https://docs.astral.sh/uv/reference/cli/#uv-python-install) 

There are still some things to work out, like [https://github.com/astral-sh/uv/issues/12989](https://github.com/astral-sh/uv/issues/12989) 

Here’s how my workflow looks like now for a new project:
```
mkdir some_project
cd some_project
uv python pin 3.13 # Creates the .python-version file and installs the interpreter if needed
uv init # creates pyproject.toml, README.md, .gitignore, and main.py
# uv add some_package # adds some_package to pyproject.toml
uv sync # creates the .venv directory, and installs the dependencies to that venv. But the venv is not activated! Creates the uv.lock file
source .venv/bin/activate
# write code
uv run main.py
uv lock # lock dependencies to uv.lock file
```

Here’s the workflow when working on an existing project:
```
# clone repo
# cd repo
uv venv
source .venv/bin/activate
# uv pip install -r requirements.txt # if requirements.txt
# uv lock
uv sync # if the repo has a pyproject.toml but no uv.lock
# uv sync --extra dev # to install also the optional dependencies “dev”
# uv sync --locked # if the repo has a uv.lock with or without pyproject.toml
# uv sync --locked --all-extras # install all optional dependencies
# uv sync --locked --extra dev # install dev optional dependencies
```

## Ruff
From [https://astral.sh/blog/the-ruff-formatter](https://astral.sh/blog/the-ruff-formatter):
> TL;DR: The Ruff formatter is an extremely fast Python formatter, written in Rust. It’s over 30x faster than Black and 100x faster than YAPF, formatting large-scale Python projects in milliseconds - all while achieving >99.9% Black compatibility.

If using `ruff` from the CLI:
- `ruff check .`
- `ruff check --fix . #you’d want this first`
- `ruff format --check .` 
- `ruff format . # you’d want this second`  
From [https://docs.astral.sh/ruff/formatter/#sorting-imports](https://docs.astral.sh/ruff/formatter/#sorting-imports) (just a reminder that this is still not mature):
> Currently, the Ruff formatter does not sort imports. In order to both sort imports and format, call the Ruff linter and then the formatter…
A unified command for both linting and formatting is [planned](https://github.com/astral-sh/ruff/issues/8232).

From [https://marketplace.visualstudio.com/items?itemName=charliermarsh.ruff](https://marketplace.visualstudio.com/items?itemName=charliermarsh.ruff):
> A Visual Studio Code extension for Ruff, an extremely fast Python linter and code formatter, written in Rust. Available on the Visual Studio Marketplace.
Ruff can be used to replace Flake8 (plus dozens of plugins), Black, isort, pyupgrade, and more, all while executing tens or hundreds of times faster than any individual tool.
Ruff's automatic fixes are labeled as "safe" and "unsafe". By default, the "Fix all" action will not apply unsafe fixes. However, unsafe fixes can be applied manually with the "Quick fix" action. Application of unsafe fixes when using "Fix all" can be enabled by setting unsafe-fixes = true in your Ruff configuration file or adding --unsafe-fixes flag to the "Lint args" setting.

Configuration:
- [https://github.com/astral-sh/ruff-vscode/issues/425](https://github.com/astral-sh/ruff-vscode/issues/425)
- [https://docs.astral.sh/ruff/configuration/#shell-autocompletion](https://docs.astral.sh/ruff/configuration/#shell-autocompletion)

![Ruff extension for VSCode]({{ site.baseurl }}/assets/images/ruff-extension.png){:style="display:block; margin-left:auto; margin-right:auto; width:100.00%"}

Extension commands:
- command palette > Organize imports (just like with Isort)
- command palette > Format document (just like with Black)
- command palette > Ruff: fix all auto-fixable problems


There are still some things to work out, like [https://github.com/astral-sh/ruff/issues/9926](https://github.com/astral-sh/ruff/issues/9926)

## Ty
This would be a replacement for mypy.
But, their repo [https://github.com/astral-sh/ty](https://github.com/astral-sh/ty) says:
> ty is in preview and is not ready for production use.
We're working hard to make ty stable and feature-complete, but until then, expect to encounter bugs, missing features, and fatal errors.

So for now (August 2025), I will abstain from using it.

## Conclusion
The speed is noticeable. But there are still some needed improvements.  
However, I'll be using these tools for now. My changes can be seen in the PRs I mentioned at the top of the post.