---
layout: post
title: "Distroless Docker Images for Python"
date: 2026-08-09 00:00:00-0000
categories: 
---

In [https://k-candidate.github.io/2025/10/09/sec-vuln-fatigue-build-troubleshoot-minimal-containers.html](https://k-candidate.github.io/2025/10/09/sec-vuln-fatigue-build-troubleshoot-minimal-containers.html) I explained how to minimize the attack surface and the vulnerability patching fatigue by using Google Distroless container images.

They're great. They're fit for use and fit for purpose.

However, they currently have one limitation. The Python variant offers just one version: `3.13`.

But there's great news: NVIDIA made a fork of Google's Distroless to build for Python `3.10`, `3.11`, `3.12`, `3.13`, and `3.14`. And NVIDIA is willing to contribute this feature out. See [https://github.com/GoogleContainerTools/distroless/issues/1703#issuecomment-3336186491](https://github.com/GoogleContainerTools/distroless/issues/1703#issuecomment-3336186491).

You can get these Distroless Python images from [https://catalog.ngc.nvidia.com/orgs/nvidia/distroless/containers/python/-](https://catalog.ngc.nvidia.com/orgs/nvidia/distroless/containers/python/-).

They're doing a great job to keep them vulnerability free as the cadence of release is frequent.

![NVIDIA Distoless Python docker image vulnerability scan via Trivy]({{ site.baseurl }}/assets/images/nvidia-distroless-python-trivy-scan.png){:style="display:block; margin-left:auto; margin-right:auto; width:100.00%"}

I migrated one of my Python containers to this Distroless variant to have an example of how the Dockerfile would look like.  
You can see it in this PR: [https://github.com/k-candidate/fastapi-app/pull/3](https://github.com/k-candidate/fastapi-app/pull/3).

![NVIDIA Distoless Python Dockerfile migration example]({{ site.baseurl }}/assets/images/nvidia-distroless-python-dockerfile.png){:style="display:block; margin-left:auto; margin-right:auto; width:100.00%"}

**<u>This reduced the image size by 35%</u>**: from 73.19MB to 47.33MB

![NVIDIA Distoless Python Docker image size reduction]({{ site.baseurl }}/assets/images/nvidia-distroless-python-size-reduction.png){:style="display:block; margin-left:auto; margin-right:auto; width:100.00%"}

**<u>Smaller attack surface, less vulnerabilities to patch, smaller disk size footprint, less storage cost, quicker startups as there's less to pull and therefore quicker scale-outs. What's not to like?</u>**

Great success :+1:
