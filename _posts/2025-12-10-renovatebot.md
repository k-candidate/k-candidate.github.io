---
layout: post
title: "Renovate bot - Automating Book Availability Checks"
date: 2025-12-10 00:00:00-0000
categories: 
---

I want to keep all the dependencies in the repo up to date.

AFAIK, I have two options: Dependabot and Renovatebot.

The package manager I’m using is uv, so the first step is to check whether both tools support it.

As per [https://docs.astral.sh/uv/guides/integration/dependency-bots/](https://docs.astral.sh/uv/guides/integration/dependency-bots/), as of 2025/12/10:
>uv is supported by Renovate.

>Dependabot has announced support for uv, but there are some use cases that are not yet working.

These issues of dependabot with uv remain open: 
- [https://github.com/astral-sh/uv/issues/2512](https://github.com/astral-sh/uv/issues/2512)
- [https://github.com/dependabot/dependabot-core/issues/11913](https://github.com/dependabot/dependabot-core/issues/11913)
- [https://github.com/dependabot/dependabot-core/issues/13912](https://github.com/dependabot/dependabot-core/issues/13912)

Based on that, Renovate is the better choice for now.

Another advantage of Renovate is its flexibility: Dependabot is GitHub specific, while Renovate supports Github, Gitlab, and Bitbucket, and can also be self-hosted.

I installed [the app](https://github.com/apps/renovate) just for the repo in question.

Since I'm using uv, I had to enable lock file maintenance by adding a commit in [the Onboarding PR](https://github.com/k-candidate/selenium-book-search-slack-alerts/pull/12).

Afterward, Renovate started creating PRs like [this one](https://github.com/k-candidate/selenium-book-search-slack-alerts/pull/14).

I also wanted to observe how Renovate reacts when I push commits to one of its PRs, so I used [this PR](https://github.com/k-candidate/selenium-book-search-slack-alerts/pull/13) to test that behavior.

Given that I already had tests that run in the PRs, it was easy and quick to verify that the changes were correct and working.

## Resources

- [https://developer.mend.io/](https://developer.mend.io/)
- [https://docs.astral.sh/uv/guides/integration/dependency-bots/](https://docs.astral.sh/uv/guides/integration/dependency-bots/)
- [https://www.youtube.com/watch?v=vKRuQkMMkOM](https://www.youtube.com/watch?v=vKRuQkMMkOM)
- [https://www.youtube.com/watch?v=5CkCr9U_Q1Y](https://www.youtube.com/watch?v=5CkCr9U_Q1Y)
- [https://www.youtube.com/watch?v=q43LmW1b2O0](https://www.youtube.com/watch?v=q43LmW1b2O0)
- [https://github.com/renovatebot/renovate](https://github.com/renovatebot/renovate)
- [https://docs.renovatebot.com/reading-list/](https://docs.renovatebot.com/reading-list/)
- [https://docs.renovatebot.com/configuration-options/#lockfilemaintenance](https://docs.renovatebot.com/configuration-options/#lockfilemaintenance)
- [https://github.com/renovatebot/tutorial](https://github.com/renovatebot/tutorial)
- [https://github.blog/changelog/2022-10-24-dependabot-updates-support-for-the-python-pep-621-standard/](https://github.blog/changelog/2022-10-24-dependabot-updates-support-for-the-python-pep-621-standard/)
- [https://docs.github.com/en/code-security/dependabot/dependabot-version-updates/about-dependabot-version-updates#supported-repositories-and-ecosystems](https://docs.github.com/en/code-security/dependabot/dependabot-version-updates/about-dependabot-version-updates#supported-repositories-and-ecosystems)
- [https://docs.github.com/en/code-security/dependabot/ecosystems-supported-by-dependabot/supported-ecosystems-and-repositories](https://docs.github.com/en/code-security/dependabot/ecosystems-supported-by-dependabot/supported-ecosystems-and-repositories)