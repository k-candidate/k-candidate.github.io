---
layout: post
title: "Renovate Bot Automerge - Automating Book Availability Checks"
date: 2026-03-22 00:00:00-0000
categories: 
---

I now have unit, integration, and e2e tests for [the book check repo](https://github.com/k-candidate/selenium-book-search-slack-alerts).

In a previous post I set up renovate updates.

It is time for more automation: have renovate merge its own PRs.

## Risk Management

To tame risk:
- I will start by allowing automerge for non-major version updates, then monitor before expanding.
- Increase the unit test coverage. It was around 80%, and [it is now almost at 100%](https://github.com/k-candidate/selenium-book-search-slack-alerts/pull/41).
- Set rules for the repo (branch protection).

## Branch Protection

Repo > Settings > Rules > Rulesets >   New branch ruleset >  
OR  
Repo > Settings > Branches > Add branch ruleset > 
- Ruleset Name = Protect main branch
- Enforcement status = Active
- Branch targeting criteria = Include default branch
- Branch rules = add
  - "Require a pull request before merging"
  - "Require status checks to pass" > check "Require branches to be up to date before merging", and add all the checks (code quality, unit, tox, integration, e2e).

## The Code

The PR for this work can be found here: [https://github.com/k-candidate/selenium-book-search-slack-alerts/pull/41](https://github.com/k-candidate/selenium-book-search-slack-alerts/pull/41).

How to validate the `renovate.json`:
```bash
nvm exec lts/* \
    npx --yes --package renovate \
    renovate-config-validator \
    renovate.json --strict
```

I have added that as a check in PRs, and also to the pre-commit hooks. See [https://github.com/k-candidate/selenium-book-search-slack-alerts/pull/42](https://github.com/k-candidate/selenium-book-search-slack-alerts/pull/42).

Keep an eye on [https://github.com/renovatebot/github-action/issues/548](https://github.com/renovatebot/github-action/issues/548).

Renovate has some quirks:
- `packageRules` apparently cannot control `lockFileMaintenance`. They're separate concepts:
  - `lockFileMaintenance` is file-level (`uv.lock`), not package-level
  - `packageRules` cannot override it. See [https://github.com/renovatebot/renovate/discussions/15899](https://github.com/renovatebot/renovate/discussions/15899).
- `pre-commit` updates should fall under `packageRules`

## Results

It's working as expected, e.g.:
- [https://github.com/k-candidate/selenium-book-search-slack-alerts/pull/35](https://github.com/k-candidate/selenium-book-search-slack-alerts/pull/35)
- [https://github.com/k-candidate/selenium-book-search-slack-alerts/pull/37](https://github.com/k-candidate/selenium-book-search-slack-alerts/pull/37)

Automerge disabled for major version:

![automerge disabled for major version]({{ site.baseurl }}/assets/images/automerge-01.png){:style="display:block; margin-left:auto; margin-right:auto; width:100.00%"}

Automerge enabled for non-major version:

![automerge enabled for non major version]({{ site.baseurl }}/assets/images/automerge-02.png){:style="display:block; margin-left:auto; margin-right:auto; width:100.00%"}

Less toil for me.

## References

- [https://docs.renovatebot.com/key-concepts/automerge/](https://docs.renovatebot.com/key-concepts/automerge/)
- [https://github.com/apps/renovate-approve](https://github.com/apps/renovate-approve)
- [https://github.com/apps/renovate-approve-2](https://github.com/apps/renovate-approve-2)
- [https://docs.renovatebot.com/configuration-options/#platformautomerge](https://docs.renovatebot.com/configuration-options/#platformautomerge)
- [https://docs.renovatebot.com/configuration-options/#automergetype](https://docs.renovatebot.com/configuration-options/#automergetype)
- [https://docs.renovatebot.com/configuration-options/#automergestrategy](https://docs.renovatebot.com/configuration-options/#automergestrategy)
- [https://docs.renovatebot.com/configuration-options/#automergeschedule](https://docs.renovatebot.com/configuration-options/#automergeschedule)
- [https://docs.renovatebot.com/configuration-options/#automergecomment](https://docs.renovatebot.com/configuration-options/#automergecomment)
- [https://docs.renovatebot.com/configuration-options/#automerge](https://docs.renovatebot.com/configuration-options/#automerge)
- [https://docs.renovatebot.com/configuration-options/#rebasewhen](https://docs.renovatebot.com/configuration-options/#rebasewhen)
- [https://docs.renovatebot.com/configuration-options/#matchupdatetypes](https://docs.renovatebot.com/configuration-options/#matchupdatetypes)