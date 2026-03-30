---
layout: post
title: "SBOM Viewer - XVFB to Test a Desktop GUI"
date: 2026-05-10 00:00:00-0000
categories: 
---

![together]({{ site.baseurl }}/assets/images/sbom-viewer-post02-01.jpg){:style="display:block; margin-left:auto; margin-right:auto; width:33.33%"}

## How can one test a desktop GUI in a headless GHA runner?

Before we answer that, we have to answer another question: 

## Which display backend does Tkinter use?

Tkinter uses X11 as its display backend on Linux systems as per [https://docs.python.org/3/library/tkinter.html](https://docs.python.org/3/library/tkinter.html). For the curious: it uses Cocoa on macOS, and GDI on Windows.

Tkinter relies on Tk (a Tcl package), which is built around the X11 protocol for rendering windows and graphics.

## But, what about the new Wayland?

Well, for Tkinter to support Wayland, Tk (the Tcl package, remember) itself would have to support it. But it apparently ain't happening without some company providing monetary support. See [https://discuss.python.org/t/feature-request-wayland-support-for-tkinter/75198/2](https://discuss.python.org/t/feature-request-wayland-support-for-tkinter/75198/2) and [https://github.com/python/cpython/issues/128204](https://github.com/python/cpython/issues/128204) which has been closed as not planned.

So if you have a Wayland system and you want to use Tkinter, then use Xwayland as a bridge between X and Wayland. See [https://wiki.hypr.land/Configuring/XWayland/](https://wiki.hypr.land/Configuring/XWayland/).

Ok, so now we know that in our headless linux CI we would have to somehow use X11.

## How do we use X11 in headless mode?

Enter Xvfb. See [https://www.x.org/archive/X11R7.7/doc/man/man1/Xvfb.1.xhtml](https://www.x.org/archive/X11R7.7/doc/man/man1/Xvfb.1.xhtml) or [https://linux.die.net/man/1/xvfb](https://linux.die.net/man/1/xvfb).

Xvfb (X Virtual Framebuffer) is a display server that implements the X11 protocol entirely in virtual memory, without requiring physical display hardware or input devices. It enables graphical X11 applications to run on headless systems like servers by simulating a display environment.

## How to install it on Ubuntu?

```bash
sudo apt-get update && sudo apt-get install -y xvfb
```

## How does Tkinter detect this virtual display?

Tkinter detects the available display via the `DISPLAY` environment variable, defaulting to whatever X11 server (real or virtual like Xvfb) is present.

## How do I use xvfb to test my Tkinter software?

Via `xvfb-run`. See [https://manpages.ubuntu.com/manpages/jammy/man1/xvfb-run.1.html](https://manpages.ubuntu.com/manpages/jammy/man1/xvfb-run.1.html)

In my case I do `xvfb-run -a uv run pytest tests/integration -v`

See my tests in [https://github.com/k-candidate/sbom-viewer](https://github.com/k-candidate/sbom-viewer)