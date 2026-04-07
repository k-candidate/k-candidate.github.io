---
layout: post
title: "SBOM Viewer - Using a GitHub App for Releases instead of a GITHUB_TOKEN"
date: 2026-06-01 00:00:00-0000
categories: 
---

After the work I have done in the SBOM Viewer repo, I found that `pyinstaller-release-publish.yaml` does not start automatically after `release.yaml`.

The reason was that `release.yaml` runs `semantic-release` with `GITHUB_TOKEN`. And the doc says that events created by `GITHUB_TOKEN` do **not** trigger new workflow runs, except `workflow_dispatch` and `repository_dispatch`. See [https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/trigger-a-workflow](https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/trigger-a-workflow) and [https://docs.github.com/en/actions/concepts/security/github_token](https://docs.github.com/en/actions/concepts/security/github_token).

So to fix this, I have to either use a PAT, or a Github App token, or trigger `pyinstaller release publish` from `workflow_run` of the `release` workflow instead.

I'm gonna go with the clean solution, the Github App, as it requires less long-term maintenance.

Useful doc:
- [https://docs.github.com/actions/writing-workflows/choosing-when-your-workflow-runs/triggering-a-workflow](https://docs.github.com/actions/writing-workflows/choosing-when-your-workflow-runs/triggering-a-workflow)
- [https://github.com/actions/create-github-app-token](https://github.com/actions/create-github-app-token)
- [https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)

## 1. Create the Github app

- Github settings for the account (my case) or org: Settings > Developer Settings > GitHub Apps
- New Github App
- give it a name (`sbom-viewer-release-bot`)
- homepage url can be the repo url
- uncheck the webhook

## 2. Give the app the minimum repo permissions

- Contents: Read and write
- Issues: Read and write
- Pull requests: Read and write
- Metadata: Read-only

This matches what semantic-release needs for:
- creating tags/releases
- posting release notes/comments

## 3. Install the app on the repo

- In the app settings, click Install App
- Install it on the account/org
- Limit access to just k-candidate/sbom-viewer

## 4. Generate a private key

- In the app page, click "Generate a privae key"
- Github downloads a pem file. Keep it safe

## 5. Add repo variables + secret

- In k-candidate/sbom-viewer, go to Settings > Secrets and variables > Actions
- Add repo variable: `APP_ID` = github app id
- Add repo secret: `APP_PRIVATE_KEY` = paste the full pem content

## 6. Update the release workflow

See [https://github.com/k-candidate/sbom-viewer/pull/4/changes](https://github.com/k-candidate/sbom-viewer/pull/4/changes).

I created the github app token in the workflow (using `actions/create-github-app-token`), and then used it for the semantic release action to replace the `GITHUB_TOKEN`.

I tightened the workflow-level permissions to just what checkout needs (contents: read).

There's nothing to change in `pyinstaller-release-publish.yaml` as the "release.types.published" is the right one.

## 7. Test

It failed: [https://github.com/k-candidate/sbom-viewer/actions/runs/24057681351/job/70167124722](https://github.com/k-candidate/sbom-viewer/actions/runs/24057681351/job/70167124722)

`semantic-release` was still trying to push with `github-actions[bot]`. The logs said: `Permission to k-candidate/sbom-viewer.git denied to github-actions[bot]`

why?
- `release.yaml` still does checkout first
- `actions/checkout` by default uses its own token and persists git credentials
- then `semantic-release` reads the repo remote and ends up pushing through those stored checkout credentials

So the fix is:
- Create the GitHub App token before checkout
- Use that token in `actions/checkout`

The fix is here: [https://github.com/k-candidate/sbom-viewer/pull/6/changes](https://github.com/k-candidate/sbom-viewer/pull/6/changes)

And now it works correctly: [https://github.com/k-candidate/sbom-viewer/actions/runs/24057889114](https://github.com/k-candidate/sbom-viewer/actions/runs/24057889114)