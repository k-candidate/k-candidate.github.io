---
layout: post
title: "SBOM Viewer - Pyinstaller to Bundle the App into a Single Package"
date: 2026-05-17 00:00:00-0000
categories: 
---

I do not have much time, so I am just dumping here my notes for [https://github.com/k-candidate/sbom-viewer/pull/2](https://github.com/k-candidate/sbom-viewer/pull/2).

The software is working. Now how do we get it into the hands of people?

If someone is comfortable with cloning the repo and setting up the environment etc, then this tool is not really of much use to them. They can just use the existing CLIs and TUIs.

However, this tool is for people who do not want to or do not know how to mess around with development tools. So I have to package it and make it easily downloadable for them. This post is about the packaging part. i want them to be able to use the app without having to install a Python interpreter or any modules or even know how any of this stuff works under the hood.

![Looking under the hood]({{ site.baseurl }}/assets/images/sbom-viewer-post03-01.png){:style="display:block; margin-left:auto; margin-right:auto; width:33.33%"}

There are many options to do this. Some of them are mentioned here: [https://sparxeng.com/blog/software/python-standalone-executable-generators-pyinstaller-nuitka-cx-freeze](https://sparxeng.com/blog/software/python-standalone-executable-generators-pyinstaller-nuitka-cx-freeze).

I have used cx_freeze a very long time ago.  
I have played around with nuitka when learning about web assembly: [https://k-candidate.github.io/2024/12/11/what-is-web-assembly.html](https://k-candidate.github.io/2024/12/11/what-is-web-assembly.html).  
But I haven't used Pyinstaller.

So I am going with Pyinstaller.

First question: how does it support cross-platform? This is ok: [https://coderslegacy.com/python/cross-compilation-in-pyinstaller/](https://coderslegacy.com/python/cross-compilation-in-pyinstaller/).

Start here [https://github.com/pyinstaller/pyinstaller](https://github.com/pyinstaller/pyinstaller), here [https://pyinstaller.org/en/stable/index.html](https://pyinstaller.org/en/stable/index.html), and here [https://pyinstaller.org/en/latest/usage.html](https://pyinstaller.org/en/latest/usage.html).

Then you'll find out that you need spec files: [https://pyinstaller.org/en/stable/spec-files.html](https://pyinstaller.org/en/stable/spec-files.html)

But how do I make that spec file? Do I really have to make it manually?!  
Then you find `pyi-makespec` (it gets installed automatically when you install `pyinstaller`): [https://pyinstaller.org/en/stable/man/pyi-makespec.html](https://pyinstaller.org/en/stable/man/pyi-makespec.html).

I'm gonna be using pyinstaller in CI/CD, should I use the spec file or should I generate every time via pyi-makespec just in case the syntax changes if pyinstaller gets upgraded? Well, I'll defer to one of the maintainers: [https://github.com/orgs/pyinstaller/discussions/8349](https://github.com/orgs/pyinstaller/discussions/8349).

I'll just use the pyi-makespec to generate a skeleton which I'll tweak manually (lots of trial and error) and then I'll use that spec file and forget about pyi-makespec. The command to make the skeleton: 
```bash
uv run pyi-makespec \
  --name sbom-viewer \
  --windowed \
  --hidden-import tkinter \
  --hidden-import tkinter.ttk \
  --hidden-import tkinter.filedialog \
  --hidden-import tkinter.messagebox \
  main.py
```

On your journey you'll find out about `--onedir` vs `--onefile`. Which should I choose? I'll defer to a pyinstaller maintainer again: [https://discuss.python.org/t/opinion-pyinstaller-onefile-or-onedir-for-program-distribution/106137](https://discuss.python.org/t/opinion-pyinstaller-onefile-or-onedir-for-program-distribution/106137).

So `--onedir` it is.

Playing around with pyinstaller, I see `_MEIPASS`. What on earth is it? Pyinstaller's `_MEIPASS` is a runtime attribute in the sys module. It holds the absolute path to the temporary directory where PyInstaller unpacks bundled files when running an executable. The bootloader sets sys._MEIPASS (alongside sys.frozen) during startup to help your code locate resources like data files, images, or modules inside the bundle. If in one-folder mode, it points to the `_internal` folder with the executable and files. But if in one-file mode, it points to a temp folder created on launch, and it's cleaned up after exit.

I got it to work, but how can I customize the icon? Well, Linux can use a `png`, macOS needs a `icns`, and Windows needs an `ico`.

For icns, you can `sudo apt install icnsutils`. See [https://launchpad.net/ubuntu/noble/+package/icnsutils](https://launchpad.net/ubuntu/noble/+package/icnsutils).

I tried the same in CI (a GHA in a PR) but it failed. After hitting walls for a while and looking at these issues (which were not very useful, but writing them down just in case I need in the future to hunt down the breadcrumbs):
- [https://github.com/astral-sh/uv/issues/6893](https://github.com/astral-sh/uv/issues/6893)
- [https://github.com/python/cpython/issues/124111](https://github.com/python/cpython/issues/124111)
- [https://github.com/astral-sh/uv/issues/7036](https://github.com/astral-sh/uv/issues/7036)
- [https://github.com/astral-sh/rye/pull/233](https://github.com/astral-sh/rye/pull/233)

Then I found this which was related to what was happening in my case and helped me understand the issue: [https://github.com/pyinstaller/pyinstaller/issues/9204](https://github.com/pyinstaller/pyinstaller/issues/9204).

Here's what was happening:
- the Linux runner has Tcl/Tk 8.6 packages
- uv’s CPython 3.14.2 build expects Tcl/Tk 9.0. That Python’s `_tkinter` extension expects Tcl/Tk 9.0:
  - `libtcl9.0.so`
  - `libtcl9tk9.0.so`

But why was it working on my laptop?!?! I was using a cached version of python (built months ago) that was linked against Tcl/Tk 8.6 which is what's on my OS. I removed python (via uv) and installed it again and now I was facing the same issue as the runner. Well it's a step back, but it allowed me to confirm the issue.

So the solution here is to explicitly bundle the Tcl/Tk shared libraries in the PyInstaller spec. More fighting with the spec file, but I Won't have to depend on nor wait for upstream fixes. So now the packages made by pyinstaller will be using the Tcl/Tk 9 runtime family (`_tkinter` is linked against `libtcl9.0.so` and `libtcl9tk9.0.so`).

CI was able to do all the packaging. I tested Linux x64 and Windows x64 and they both worked. For macOS I still have to set up some infra to be able to test it.

So what's in [https://github.com/k-candidate/sbom-viewer/pull/2](https://github.com/k-candidate/sbom-viewer/pull/2)?
- `sbom-viewer.spec`
  - single cross-platform pyinstaller spec for Linux, Windows, and macOS.
  - `onedir` packaging
  - platform specific icons
- helper scripts:
  - `scripts/get_project_version.py`: read version from `pyproject.toml`. Not very important.
  - `scripts/package_pyinstaller_dist.py`: create versioned release archive
  - `scripts/smoke_test_pyinstaller.py`: smoke-test the built app
- Pyinstaller GitHub workflows:
  - `.github/workflows/pyinstaller-build-test.yaml`: PR workflows that builds all targets and uploads artifacts for inspection
  - `.github/workflows/pyinstaller-release-publish.yaml`: release workflow rebuilds from the released tag and uploads assets to the GitHub release.
- icons in `assets/`
- Wired runtime icon handling into the app in `app/view.py` and added tests for it in `tests/integration/test_view.py`
- I updated the readme to document how to create a package via Pyinstaller.