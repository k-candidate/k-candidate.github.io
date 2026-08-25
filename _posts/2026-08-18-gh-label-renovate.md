---
layout: post
title: "Renovate and GitHub Labels"
date: 2026-08-18 00:00:00-0000
categories: 
---

## What Is The Issue We Are Trying To Solve?

You have hundreds or thousands of GitHub repositories, and you do not have Renovate's automerge enabled in the majority of them (because your tests are flaky or absent, and your CI/CD is deficient), but you still have to patch dependencies (one might argue that this is less impotant than the utomated tests and the automated CI/CD, but we are not here to discuss that).

This means that you will have many PRs opened.

How can you discover the opened PRs? How can you know if they are for chores or fixes or feats or breaking changes? How can you know what type of dependency they are for (Python, Terraform, Dockerfile etc.)?

If this is your current situation, then this is for you, and GitHub labels are your solution.

## What Is A GitHub Label?

A GitHub label is a customizable, color-coded tag used to categorize and organize Issues, Pull Requests (PRs), and Discussions within a repository. They serve as the primary tool for sorting work, defining development workflows, and filtering items in your project.

In this case, we want them just for PRs.

## How It Works And What It Does

Labels act like visual metadata attached to your work items. When you assign a label to an issue or pull request, it instantly applies a colored badge to that item.

To search and filter by a label, you can click it, or you can type in the search field `label:<labelname>`.

## How And Where To Create It

### At The Org Level For New Repos

You can create a label at the org level. That will apply only to repositories created after the creation of the label.

You need to do this from the UI. There's no `gh` cli for it, and there's no REST API for it. ¯\\\_(ツ)_/¯

Procedure here: [https://docs.github.com/en/organizations/managing-organization-settings/managing-default-labels-for-repositories-in-your-organization](https://docs.github.com/en/organizations/managing-organization-settings/managing-default-labels-for-repositories-in-your-organization).

### Per Repo For Existing Repos

For the existing repos, you have to create the labels in each repo. You can do this via the UI (if you have a couple repos) or via the CLI (make a script) if you have hundreds or thousands of repos.

Procedure for the UI: [https://docs.github.com/en/issues/using-labels-and-milestones-to-track-work/managing-labels](https://docs.github.com/en/issues/using-labels-and-milestones-to-track-work/managing-labels)

Doc for CLI: [https://cli.github.com/manual/gh_label](https://cli.github.com/manual/gh_label).

## Renovate And GitHub Labels

Renovate can apply labels to the PRs after the labels have been created. So, create the labels first, then add the labels config to Renovate.

You need a centralized shared preset. See this previous post in which I explained that: [https://k-candidate.github.io/2026/06/22/self-hosting-renovate.html](https://k-candidate.github.io/2026/06/22/self-hosting-renovate.html).

And in that centralized shared preset you want to use Renovate's `addLabels` and not `labels` because you want to add to what's already in use and not disrupt it.

See the doc here: [https://docs.renovatebot.com/configuration-options/#addlabels](https://docs.renovatebot.com/configuration-options/#addlabels).

The centralized shared preset will end up looking something like this:

```json
{
  "$schema": "https://renovatebot.com",
  "extends": [
    "config:recommended"
  ],
  "labels": ["dependencies", "renovate"],
  "packageRules": [
    {
      "matchUpdateTypes": ["patch", "minor"],
      "addLabels": ["minor"]
    },
    {
      "matchUpdateTypes": ["major"],
      "addLabels": ["major", "breaking-change"]
    },
    {
      "matchManagers": ["terraform"],
      "addLabels": ["lang:terraform"]
    },
    {
      "matchManagers": ["pip_requirements", "pipenv", "poetry", "setup-cfg"],
      "addLabels": ["lang:python"]
    },
    {
      "matchManagers": ["npm", "yarn", "pnpm"],
      "addLabels": ["lang:javascript"]
    },
    {
      "matchManagers": ["dockerfile", "docker-compose"],
      "addLabels": ["lang:dockerfile"]
    },
    {
      "matchManagers": ["gomod"],
      "addLabels": ["lang:golang"]
    }
  ]
}
```
