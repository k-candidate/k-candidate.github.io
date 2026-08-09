---
layout: post
title: "Laptop GPU passthrough"
date: 2026-08-02 00:00:00-0000
categories: 
---

Not every story is a success story. This is one of those. It took me a couple of days of fighting with my laptop to realize that there's no way to get the GPU to be passed through to a VM. This is the case for the majority of laptops.

The silver lining is that I found some good sources (e.g. [https://github.com/bryansteiner/gpu-passthrough-tutorial](https://github.com/bryansteiner/gpu-passthrough-tutorial)) and picked up some new tricks.

Now I am just using the GPU directly on the host (laptop), and whenever I need to test something without affecting the system I just do it inside a container via nvidia-container-toolkit. See my previous post [https://k-candidate.github.io/2025/10/22/nvidia-container-toolkit-cdi.html](https://k-candidate.github.io/2025/10/22/nvidia-container-toolkit-cdi.html) and my PR to get it working in the AWS ECS AMI [https://github.com/aws/amazon-ecs-ami/pull/541](https://github.com/aws/amazon-ecs-ami/pull/541).