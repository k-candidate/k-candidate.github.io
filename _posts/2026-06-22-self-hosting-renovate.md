---
layout: post
title: "Self-Hosting Renovate Bot on Kubernetes"
date: 2026-06-22 00:00:00-0000
categories: 
---

I have posted previously about renovate. I am not going to repeat information I already shared. I invite you to have a look in the previous posts.

There are multiple ways to self-host renovate. See [https://docs.renovatebot.com/examples/self-hosting/](https://docs.renovatebot.com/examples/self-hosting/).

## Which one to use?

- Docker: ok, but how to orchestrate it?!
- cli: running where?! Too low level, I do not want to manage that much stuff.
- GitHub Action: I do not want to depend on GitHub. What if I migrate to another platform? What if I have some repos that are hosted on a different platform? I do not want to migrate them, I want them to be able to benefit from the self hosted renovate bot immediately.
- Gitlab runner: same argument as the previous one.
- CircleCI: same story.
- CE (Community Edition): closed source. No, thank you.
- Kubernetes: Yes

With Kubernetes, it is just a cronjob.

## Design

There's one key limitation to be aware of: Renovate OSS and CE operate as a monolith. They cannot scale horizontally. See [https://github.com/mend/renovate-ce-ee/blob/11a8dbb4c8567caaf4977961328210e3af5098ea/docs/advanced.md#horizontal-scaling](https://github.com/mend/renovate-ce-ee/blob/11a8dbb4c8567caaf4977961328210e3af5098ea/docs/advanced.md#horizontal-scaling).

Another factor to take into account: if you self host your Git repositories and have many orgs and repos, you do not want to hammer your platform.

So how to work around these 2?

By "sharding" your renovate: make a k8s cronjob per org (or per list of repos), and have the k8s cronjobs run at different times.

The next point is onboarding. I recommend to start with an opt-in model to reduce the blast radius: you want a repo to have a config file in it (`renovate-json`) for renovate to act on it. You can achieve this with `requireConfig=required` and `onboarding=false`. See [https://docs.renovatebot.com/self-hosted-configuration/#requireconfig](https://docs.renovatebot.com/self-hosted-configuration/#requireconfig). When your automated updates initiative becomes more mature, you can switch models.

Another thing I recommend is having an inherited global config ("global" in the sense of per org or per list of repos) with cautious sensible defaults. See [https://docs.renovatebot.com/config-overview/#inherited-config](https://docs.renovatebot.com/config-overview/#inherited-config).  
For example: you can have the repo `myorg1/renovate-config` with a `default.json` that contains something like this:

```json
{
  "description": "myorg1 shared Renovate defaults",
  "extends": [
    "config:best-practices",
    "group:allNoMajor"
  ],
  "automerge": false,
  "dependencyDashboard": true,
  "semanticCommits": "enabled"
}
```

And then when you want to enroll the repo `myorg1/someComponent` you add to it the file `renovate.json` with:

```json
{
  "schema": "https://docs.renovate.com/renovate-schema.json",
  "extends": ["local>myorg1/renovate-config"]
}
```

The `myorg1/someComponent` repo maintainers can override the defaults (inherited from `myorg1/renovate-config`) via their `renovate.json` at the repo level.

## Implementation details

The manifests in [https://docs.renovatebot.com/examples/self-hosting/#kubernetes](https://docs.renovatebot.com/examples/self-hosting/#kubernetes) already cover the skeleton.

But if for example you are using Github to host your repos, I recommend to make a GitHub App (just better security with short lived tokens). And that means that you will have to write a little bit of Javascript for an init container to get the token and share it with the main renovate pod. This would be your `RENOVATE_TOKEN`.  
You can put the secrets (gh app id, gh app installation id, gh app private key) in whatever secrets management service you prefer. Just get them securely to the init container with whatever you use (like the External Secrets Operator: [https://github.com/external-secrets/external-secrets](https://github.com/external-secrets/external-secrets)).

The Github App in question will need these permissions:
- Read access to Dependabot and metadata
- Read and Write access to code, issues, pull requests, workflows, and commit statuses.

Another thing you will need is a read-only token for `github.com`. But why? Because renovate needs authenticated access to public `github.com` metadata to avoid unauthenticated API rate limits.

Another thing you might need is a service account for your renovate pod. This can be necessary for certain datasources like the AWS AMI one. See [https://docs.renovatebot.com/modules/datasource/aws-machine-image/](https://docs.renovatebot.com/modules/datasource/aws-machine-image/). You can use IRSA if you're doing all of this in EKS. See [https://docs.aws.amazon.com/eks/latest/userguide/iam-roles-for-service-accounts.html](https://docs.aws.amazon.com/eks/latest/userguide/iam-roles-for-service-accounts.html).

With this you should get it working.  
You now might ask, _what about performance?_

I already mentioned the "sharding" in the design.

Another thing you can do is use `optimizeForDisabled`. See [https://docs.renovatebot.com/self-hosted-configuration/#optimizefordisabled](https://docs.renovatebot.com/self-hosted-configuration/#optimizefordisabled).

One other thing is using caching. See [https://docs.renovatebot.com/self-hosted-configuration/#cachedir](https://docs.renovatebot.com/self-hosted-configuration/#cachedir). In the k8s cron job case, a `ReadWriteOnce` PVC mapped to `tmp/renovate` is what we need.

## User Guide and Miscellanea

The first thing, is you want the users of this tool to understand why they would want to use it.

The main objective is to reduce the toil of manual updates, whether you do this to prevent software rot, or to get new features, or for vulnerability patching or ...

I will make the case for the last motive: make dependency and vulnerability management proactive, instead of reacting only after vulnerabilities are reported. Renovate continuously detects new upstream releases, opens PRs, lets the existing tests and checks run, and the repo owners retain full control over review and merge decisions (which can be automated too with renovate. See one of my previous posts).

But we have here a big open question: is it always safe to update to the latest version? As per the report from [https://blackkite.com/reports/third-party-breach-report-2026](https://blackkite.com/reports/third-party-breach-report-2026), "_most vendors identify a compromise within a relatively swift 10-day window._", and "_it now takes an average of nearly four months for a breach to be publicly disclosed after discovery._"

I started writing about this point and realized that it's a separate conversation. So I am putting it in a separate blog post about supply chain security and trust.

What I can tell you here is that I cannot define your risk appetite for you. There's no easy universal answer. 

But I can offer you `minimumReleaseAge` to have dependency cooldowns. See [https://docs.renovatebot.com/key-concepts/minimum-release-age/](https://docs.renovatebot.com/key-concepts/minimum-release-age/)

Moving on.

There's this nice cheat sheet: [https://www.augmentedmind.de/2023/07/30/renovate-bot-cheat-sheet/](https://www.augmentedmind.de/2023/07/30/renovate-bot-cheat-sheet/)

Test your renovate configs. This is a rabbit whole on its own. At least validate them. Here's how: [https://github.com/k-candidate/selenium-book-search-slack-alerts/blob/8fb423622e2bca7b2c59aadd3b1b92a1279b125e/.github/workflows/validate-renovate-config.yaml](https://github.com/k-candidate/selenium-book-search-slack-alerts/blob/8fb423622e2bca7b2c59aadd3b1b92a1279b125e/.github/workflows/validate-renovate-config.yaml).

You might benefit from Github's merge queues. I posted about it in the past.

Very important:
- Have a fertile soil for your seeds: use CODEOWNERS, branch protection rules, required checks...
- Have reliable tests. This should empower you to later use automerge.

I already spoke about those 2 in previous posts...

And last but not least, follow up with the different teams using your self-hosted renovate. You want to understand how they are using it, and make sure that you document and share the learned lessons between the different teams so that the internal knowledge about the tool improves and matures with time.