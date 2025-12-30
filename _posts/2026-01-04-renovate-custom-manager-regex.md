---
layout: post
title: "Renovate bot - Custom Manager using Regex"
date: 2026-01-04 00:00:00-0000
categories: 
---

I wanted to automate the build of curl statically whenever a new version of curl is released without having to trigger the build manually. See this post for context: [https://k-candidate.github.io/2025/10/09/sec-vuln-fatigue-build-troubleshoot-minimal-containers.html](https://k-candidate.github.io/2025/10/09/sec-vuln-fatigue-build-troubleshoot-minimal-containers.html).

I did a quick search to do this via Dependabot, but it turns out that it's impossible or at least I did not find a straightforward way of doing it.

So I went with Renovate: [https://github.com/k-candidate/docker-static-curl/blob/40e2dfe5a34bb731d13c84d932dbc3abf2ed2fc4/renovate.json](https://github.com/k-candidate/docker-static-curl/blob/40e2dfe5a34bb731d13c84d932dbc3abf2ed2fc4/renovate.json)

The tricky part was the regex. If you go to [https://github.com/curl/curl/releases](https://github.com/curl/curl/releases), you'll see that the "titles" have the format `Major.Minor.Patch` (e.g. `8.15.0`), but the "tags" have the format `curl-<Major>_<Minor>_<Patch>` (e.g. [curl-8_15_0](https://github.com/curl/curl/releases/tag/curl-8_15_0)).

What Renovate's `versioningTemplate` relies on is the "tag" (not the "title") even if the `datasourceTemplate` is `github-releases` ([https://docs.renovatebot.com/modules/datasource/github-releases/](https://docs.renovatebot.com/modules/datasource/github-releases/)) and not `github-tags` ([https://docs.renovatebot.com/modules/datasource/github-tags/](https://docs.renovatebot.com/modules/datasource/github-tags/)).

And it is working fine: [https://github.com/k-candidate/docker-static-curl/pull/16](https://github.com/k-candidate/docker-static-curl/pull/16). Less toil for me!