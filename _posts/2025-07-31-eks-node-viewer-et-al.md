---
layout: post
title: "TIL - eks-node-viewer and some other tools"
date: 2025-07-31 09:00:00-0000
categories: 
---

- `eks-node-viewer` allows you to visualize node usage within a Kubernetes cluster. Not just EKS. But for EKS it also shows the cost. Nice! `eks-node-viewer --resources cpu,memory` will be my go to command. More info here [https://github.com/awslabs/eks-node-viewer](https://github.com/awslabs/eks-node-viewer). This allowed me to confirm that actually Karpenter has an issue with scaling-in. There are a few issues open: [this](https://github.com/aws/karpenter-provider-aws/issues/7935), [this](https://github.com/aws/karpenter-provider-aws/issues/8211), and [this](https://github.com/kubernetes-sigs/karpenter/issues/2387).
- [https://github.com/locustio/locust](https://github.com/locustio/locust) for load testing using Python.
- [https://github.com/block/goose](https://github.com/block/goose) is an open-source and free AI agent framework. You can use many LLM providers, including the local ones (via Ollama or Docker Model Runner).
- [https://github.com/Aider-AI/aider](https://github.com/Aider-AI/aider) for AI pair programming in the terminal. It supports local models as well.