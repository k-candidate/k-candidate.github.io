---
layout: post
title: "TIL - nektos/act - Running Github Actions locally"
date: 2025-09-02 00:00:00-0000
categories: 
---

- [https://github.com/nektos/act](https://github.com/nektos/act)
- I used the installation command from the doc (`curl --proto '=https' --tlsv1.2 -sSf https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash`) and it put the executable in `~/bin/act` which is not in my path. I removed it with a `sudo rm`
- And after looking at that bash script I then installed it via: `curl --proto '=https' --tlsv1.2 -sSf https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash -s -- -b /usr/local/bin`
- Usage example: `act -W .github/workflows/code_quality.yaml workflow_dispatch`
- I immediately encountered issues with basic steps, e.g. [https://github.com/nektos/act/issues/2768](https://github.com/nektos/act/issues/2768)
- I dont’t think I am going to be using it, at least for now. Because I'd be troubleshooting it, it looks like more of a hassle than doing a "commit + push + clicking on the 'Run workflow' button in the UI".