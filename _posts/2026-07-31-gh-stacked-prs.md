---
layout: post
title: "GitHub Stacked Pull Requests"
date: 2026-07-31 00:00:00-0000
categories: 
---

GH Stacked Pull Requests are currently in preview: [https://github.blog/changelog/2026-07-30-stacked-pull-requests-are-now-in-public-preview/](https://github.blog/changelog/2026-07-30-stacked-pull-requests-are-now-in-public-preview/)

## What are Stacked PRs?

Stacked PRs are a Git workflow where a large feature is broken down into a chain of smaller, sequential PRs that build on top of each other.

Instead of opening one massive 10K line PR (which I have seen since LLM Agents came into existence), you create a sequence:
- PR 1: Targets the main trunk branch (main or master).
- PR 2: Targets the branch of PR 1.
- PR 3: Targets the branch of PR 2.

This creates an ordered review structure where each "layer" only shows the narrow diff of its own specific changes. It allows you to keep writing downstream code without waiting for upstream PRs to be approved and merged, keeping you unblocked.

## Why a Stacked PR and not just multiple commits in your 10K PR?

- Layers can be merged incrementally VS Everything merges at once. If one commit has an issue, the whole thing is kaput.
- Reverting is atomic: you can roll back a single problematic layer without touching the rest. VS Reverting a broken part means reverting the whole PR or surgically picking it out via git acrobatics.

## How Stacked PRs Relate to Merge Queues

See my previous post [https://k-candidate.github.io/2026/03/15/til-gh-merge-queue.html](https://k-candidate.github.io/2026/03/15/til-gh-merge-queue.html).

Refresher: a merge queue is an automated system that sequences PRs to ensure they don't break main when merged concurrently.

Stacked PRs and merge queues are highly complementary
- Ordered Queuing: When you ready a stack for production, the merge queue respects the hierarchy. It adds all PRs to the queue in their strict dependency order (PR 1, then PR 2, then PR 3).
- Atomic Ejection: If a check fails for a PR in the middle of the stack, the merge queue will automatically eject that PR and all subsequent downstream PRs that depend on it. This prevents broken dependency code from entering the main branch.
