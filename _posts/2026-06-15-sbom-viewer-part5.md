---
layout: post
title: "SBOM Viewer - Making installers for macOS (.dmg), Windows (.msi), and Ubuntu (.deb)"
date: 2026-06-15 00:00:00-0000
categories: 
---

I looked into a couple ways to offload this work onto a tool or framework, but I found multiple hassles, mainly because of incompatibilities with Tk and/or uv.

Not a problem, it's an opportunity to learn about how those frameworks or tools do it "under the water". Meaning, I am going to use what those wrappers or higher level tools rely on.

The important part is already done: I have the app bundled via Pyinstaller. See [https://k-candidate.github.io/2026/05/17/sbom-viewer-part3.html](https://k-candidate.github.io/2026/05/17/sbom-viewer-part3.html).

To make a `.dmg` for macOS, I used `hdiutil`. Doc here: [https://ss64.com/mac/hdiutil.html](https://ss64.com/mac/hdiutil.html).

To make a `.msi` for Windows, I used `wix`. See [https://docs.firegiant.com/quick-start/](https://docs.firegiant.com/quick-start/). This thing loves xml.

To make the `.deb` for Ubuntu, I used plain debian packaging tools to make some intermediate artifacts and then `ar` to combine them into the final deb file. See [https://manpages.ubuntu.com/manpages/noble/man1/ar.1.html](https://manpages.ubuntu.com/manpages/noble/man1/ar.1.html).

You can find the whole thing in these PRs:
- [https://github.com/k-candidate/sbom-viewer/pull/7](https://github.com/k-candidate/sbom-viewer/pull/7)
- [https://github.com/k-candidate/sbom-viewer/pull/8](https://github.com/k-candidate/sbom-viewer/pull/8)
- [https://github.com/k-candidate/sbom-viewer/pull/9](https://github.com/k-candidate/sbom-viewer/pull/9)
- [https://github.com/k-candidate/sbom-viewer/pull/10](https://github.com/k-candidate/sbom-viewer/pull/10)
- [https://github.com/k-candidate/sbom-viewer/pull/11](https://github.com/k-candidate/sbom-viewer/pull/11)

I am leaving here a bunch of pages I had to go through while working on this thing:
- [https://www.youtube.com/watch?v=KZz5Z8j1K-w](https://www.youtube.com/watch?v=KZz5Z8j1K-w)
- [https://www.youtube.com/watch?v=New2JLvWxiE](https://www.youtube.com/watch?v=New2JLvWxiE)
- [https://www.rfc-editor.org/rfc/rfc6761](https://www.rfc-editor.org/rfc/rfc6761)
- [https://briefcase.beeware.org/en/stable/how-to/building/ci/](https://briefcase.beeware.org/en/stable/how-to/building/ci/)
- [https://briefcase.beeware.org/en/stable/how-to/code-signing/macOS/](https://briefcase.beeware.org/en/stable/how-to/code-signing/macOS/)
- [https://briefcase.beeware.org/en/stable/how-to/publishing/macOS/](https://briefcase.beeware.org/en/stable/how-to/publishing/macOS/)
- [https://briefcase.beeware.org/en/stable/how-to/code-signing/windows/](https://briefcase.beeware.org/en/stable/how-to/code-signing/windows/)
- [https://briefcase.beeware.org/en/stable/reference/commands/create/](https://briefcase.beeware.org/en/stable/reference/commands/create/)
- [https://stackoverflow.com/questions/60332035/what-are-the-differences-between-dmg-and-app-file](https://stackoverflow.com/questions/60332035/what-are-the-differences-between-dmg-and-app-file)
- [https://github.com/beeware/briefcase/issues/318](https://github.com/beeware/briefcase/issues/318)
- [https://stackoverflow.com/questions/37710205/python-embeddable-zip-install-tkinter/44169516#44169516](https://stackoverflow.com/questions/37710205/python-embeddable-zip-install-tkinter/44169516#44169516)
- [https://github.com/beeware/briefcase/issues/383](https://github.com/beeware/briefcase/issues/383)
- [https://stackoverflow.com/questions/37710205/python-embeddable-zip-install-tkinter/73761645#73761645](https://stackoverflow.com/questions/37710205/python-embeddable-zip-install-tkinter/73761645#73761645)
- [https://github.com/astral-sh/uv/issues/6604](https://github.com/astral-sh/uv/issues/6604)
- [https://github.com/beeware/briefcase/issues/1367](https://github.com/beeware/briefcase/issues/1367)
- [https://github.com/beeware/briefcase/issues/2231](https://github.com/beeware/briefcase/issues/2231)
- [https://briefcase.beeware.org/en/stable/reference/platforms/windows/](https://briefcase.beeware.org/en/stable/reference/platforms/windows/)
- [https://www.wisecleaner.com/think-tank/762-How-to-Create-a-DMG-File-for-app-on-Mac.html](https://www.wisecleaner.com/think-tank/762-How-to-Create-a-DMG-File-for-app-on-Mac.html)
- [https://github.com/wixtoolset/wix/releases/](https://github.com/wixtoolset/wix/releases/)
- [https://man7.org/linux/man-pages/man1/dpkg-deb.1.html](https://man7.org/linux/man-pages/man1/dpkg-deb.1.html)

The most important takeaway, for me, from all of this is that there's still no simple and easy way to make cross OS and cross architecture installers. There isn't a single universal tool that you can use in one machine (one OS and one arch) to make installers for all OSes and all architectures. You still have to use different tools for each OS, and run them per OS and arch to get it all.  
Meaning, to have installers for x64 and arm64 for macOS, Windows, and Ubuntu, I have to use a matrix of 3 paths (1 per OS) and 6 machines (1 per OS and arch) in CI.

This is a lot of non value adding friction. Tools like Briefcase (Beeware) try to address that by being a wrapper. But it still has some limitations and still relies on OS specific tools. I do not know what is the answer in the long term. Maybe web assembly can alleviate part of the pain, but it won't solve it all.