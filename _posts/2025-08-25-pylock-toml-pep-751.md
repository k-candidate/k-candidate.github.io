---
layout: post
title: "pylock.toml - PEP 751 - Automating Book Availability Checks"
date: 2025-08-25 00:00:00-0000
categories: 
---

PEP 751 introduces a standardized lock file format for Python dependency management, called `pylock.toml`, aiming to ensure reproducible installations, improve consistency, and enhance security across projects by recording exact package versions and file hashes in a human-readable TOML structure.

Key Python packaging tools are expected to adopt this new format, helping to unify installation workflows and reduce the complexity caused by multiple proprietary lock file formats (poetry, uv, pdm...).

We can see in the release notes that `pip` added support for this feature in version `25.1`: [https://pip.pypa.io/en/stable/news/#id33](https://pip.pypa.io/en/stable/news/#id33), via [https://github.com/pypa/pip/pull/13213](https://github.com/pypa/pip/pull/13213).

## Generate the lock file
Let’s make sure that our pip version is 25.2 (latest as of Aug 2025): `pip install --upgrade pip`

To generate the lock file: `pip lock .`  
This command resolves all the dependencies and versions and writes them into `pylock.toml`.

![Generate pylock.toml using pip]({{ site.baseurl }}/assets/images/pylock-toml-pep-751.png){:style="display:block; margin-left:auto; margin-right:auto; width:100.00%"}

Here's what the file looks like:

![Generate pylock.toml using pip]({{ site.baseurl }}/assets/images/pylock-toml-pep-751-head.png){:style="display:block; margin-left:auto; margin-right:auto; width:100.00%"}

## Install the dependencies from the lockfile
It’s not ready yet: [https://github.com/pypa/pip/issues/13334](https://github.com/pypa/pip/issues/13334).

So to use lockfiles today we’d have to use something else ([https://github.com/astral-sh/uv/issues/12584](https://github.com/astral-sh/uv/issues/12584)).  
This means changing the packaging tool that we’re using, which is bigger than just using a lockfile. I’ll make this change in another post, but for this one, I am making no changes to the repo.