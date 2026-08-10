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
