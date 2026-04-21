---
layout: post
title: "K8s Cost Control - Right-Sizing - VPA, Goldilocks, KRR"
date: 2026-06-08 00:00:00-0000
categories: 
---

In [https://k-candidate.github.io/2026/05/24/opencost-multicluster.html](https://k-candidate.github.io/2026/05/24/opencost-multicluster.html), I talked about OpenCost, which allows to see how much one spends on K8s in a granular way.

Once we have that information, what to do about it? Well, we have to reduce the cost by right-sizing the resources, and reducing the waste on idle capacity.

This post is about right-sizing. Let's get one thing clear right now: you, the owner or stakeholder, are responsible for testing the recommendations of these tools. "_Trust, but verify_".

I am going to mention 2 tools: Goldilocks and KRR.

Goldilocks requires 2 things:
- The recommender of VPA (Vertical Pod Autoscaler).
- Kubernetes metrics server.

It is worth it to do a deeper dive in VPA especially now that it improved a lot with the in-place resizing: no need to restart a container to change its cpu or memory requests and limits. But I will not go into all of this and repeat information that is already well documented given that this is about right-sizing. I will instead leave some sources at the end of the post, and now just mention that there are 3 components in VPA: recommender, updater, and admission-controller. For Goldilocks, we need just the recommender.

The VPA can be used in checkpoint mode (with metrics server) or Prometheus mode (with Prometheus or Thanos or ...).

So there are basically 2 ways to operate VPA. Or so I thought until I found a third option that I saw documented nowhere. Here are the 3 options:
- Option A: Prometheus history mode (Prometheus/Thanos).
- Option B: Checkpoint mode + metrics-server.
- Option C: checkpoint mode + Prometheus via prometheus-adapter, where metrics.k8s.io is served by adapter: Prometheus -> prometheus-adapter -> metrics.k8s.io -> VPA (checkpoint mode) -> checkpoints.

So if Prometheus history mode is eventually deprecated/removed (which is the intention as per a VPA maintainer), users can still rely on Prometheus with VPA checkpoint mode by exposing `metrics.k8s.io` through prometheus-adapter.

What are those VPA checkpoints? `VerticalPodAutoscalerCheckpoint` are k8s objects where the recommender stores cpu/mem usage history that it accumulates from the live (short window) metrics of `metrics.k8s.io`. Checkpoints use decaying weights: newer samples count more that older ones. It is exponential decay (half life is 24h), meaning each day older data has about half the influence of the previous day.

This is pretty much it for Goldilocks. One little trick for Goldilocks that is not documented: once you get its dashboard running, you will notice a banner asking for your email. If you want to get rid of it you need to set in the values of their helm chart `dashboard.enable-cost` to `false`.

Now let's move onto the other tool: KRR. 

Goldilocks gave us a dashboard (web ui), I like to use KRR (Kubernetes Resource Recommender) as a CLI.

You can use use this CLI from your local laptop, or from the CI if you want to get creative.

KRR requires 3 things:
- a Prometheus compatible endpoint
- cAdvisor (usually this comes with your kubelet in the nodes)
- kube state metrics (not to be confused with the k8s metrics server) which you might already have from the helm chart of prometheus operator.

Once you install krr, you can run it like so:

```bash
krr simple \
  --prometheus-url $PROM_URL \
  --prometheus-label $PROM_LABEL_FOR_CLUSTERS \ # i.e. "cluster" or "cluster_id" if this is a centralized source like Thanos
  -l $CLUSTER \ # e.g. "qa"
  -c $CONTEXT # if you have multiple clusters in different contexts
```

I left a little PR to update krr for homebrew: [https://github.com/robusta-dev/homebrew-krr/pull/8](https://github.com/robusta-dev/homebrew-krr/pull/8).

If you do not want to or cannot install it, then the good news is that it's all python:

```bash
git clone https://github.com/robusta-dev/krr
cd krr
uv python install 3.11
uv venv --python 3.11 .venv
source .venv/bin/activate
uv pip install -r requirements.txt
python krr.py --help
```

Append `--allow-hpa` when you want krr to produce recommendations for HPA managed resources.

So, to conclude, if you already have a multi-cluster environment with centralized Thanos (or similar) with prom-operator (with kube-state-metrics enabled) and prom-adapter (serving metrics.k8s.io) per cluster, you can start using krr cli immediately, and for Goldilocks you'll need to deploy VPA recommender (and Goldilocks of course).

## Resources

- [https://github.com/kubernetes/kube-state-metrics](https://github.com/kubernetes/kube-state-metrics)
- [https://github.com/kubernetes/autoscaler/blob/249d8feadcbe7514abd3db7869e440411946ede5/vertical-pod-autoscaler/docs/flags.md](https://github.com/kubernetes/autoscaler/blob/249d8feadcbe7514abd3db7869e440411946ede5/vertical-pod-autoscaler/docs/flags.md)
- [https://github.com/kubernetes/autoscaler/blob/249d8feadcbe7514abd3db7869e440411946ede5/vertical-pod-autoscaler/docs/installation.md](https://github.com/kubernetes/autoscaler/blob/249d8feadcbe7514abd3db7869e440411946ede5/vertical-pod-autoscaler/docs/installation.md)
- [https://github.com/kubernetes/autoscaler/blob/249d8feadcbe7514abd3db7869e440411946ede5/vertical-pod-autoscaler/docs/quickstart.md](https://github.com/kubernetes/autoscaler/blob/249d8feadcbe7514abd3db7869e440411946ede5/vertical-pod-autoscaler/docs/quickstart.md)
- [https://github.com/kubernetes/autoscaler/blob/249d8feadcbe7514abd3db7869e440411946ede5/vertical-pod-autoscaler/docs/components.md](https://github.com/kubernetes/autoscaler/blob/249d8feadcbe7514abd3db7869e440411946ede5/vertical-pod-autoscaler/docs/components.md)
- [https://github.com/kubernetes/autoscaler/blob/249d8feadcbe7514abd3db7869e440411946ede5/vertical-pod-autoscaler/docs/features.md](https://github.com/kubernetes/autoscaler/blob/249d8feadcbe7514abd3db7869e440411946ede5/vertical-pod-autoscaler/docs/features.md)
- [https://github.com/kubernetes/autoscaler/blob/249d8feadcbe7514abd3db7869e440411946ede5/vertical-pod-autoscaler/docs/known-limitations.md](https://github.com/kubernetes/autoscaler/blob/249d8feadcbe7514abd3db7869e440411946ede5/vertical-pod-autoscaler/docs/known-limitations.md)
- [https://github.com/kubernetes/autoscaler/issues/9491](https://github.com/kubernetes/autoscaler/issues/9491)
- [https://github.com/FairwindsOps/goldilocks](https://github.com/FairwindsOps/goldilocks)
- [https://docs.aws.amazon.com/eks/latest/userguide/vertical-pod-autoscaler.html](https://docs.aws.amazon.com/eks/latest/userguide/vertical-pod-autoscaler.html)
- [https://docs.aws.amazon.com/eks/latest/userguide/metrics-server.html](https://docs.aws.amazon.com/eks/latest/userguide/metrics-server.html)
- [https://medium.com/@ozlemtanrikulu/achieve-cost-efficient-scaling-leveraging-vpa-and-prometheus-for-smarter-resource-allocation-in-1dc26a32c4ba](https://medium.com/@ozlemtanrikulu/achieve-cost-efficient-scaling-leveraging-vpa-and-prometheus-for-smarter-resource-allocation-in-1dc26a32c4ba)
- [https://kubernetes.io/blog/2025/05/16/kubernetes-v1-33-in-place-pod-resize-beta/](https://kubernetes.io/blog/2025/05/16/kubernetes-v1-33-in-place-pod-resize-beta/)
- [https://kubernetes.io/docs/tasks/configure-pod-container/resize-container-resources/](https://kubernetes.io/docs/tasks/configure-pod-container/resize-container-resources/)
- [https://kubernetes.io/docs/tasks/configure-pod-container/resize-pod-resources/](https://kubernetes.io/docs/tasks/configure-pod-container/resize-pod-resources/)
- [https://kubernetes.io/docs/concepts/workloads/autoscaling/vertical-pod-autoscale/](https://kubernetes.io/docs/concepts/workloads/autoscaling/vertical-pod-autoscale/)
- [https://www.fairwinds.com/blog/introducing-goldilocks-a-tool-for-recommending-resource-requests](https://www.fairwinds.com/blog/introducing-goldilocks-a-tool-for-recommending-resource-requests)
- [https://github.com/FairwindsOps/charts/blob/b160b22b7171d0da247079d9dc0d2659174cda27/stable/goldilocks/README.md](https://github.com/FairwindsOps/charts/blob/b160b22b7171d0da247079d9dc0d2659174cda27/stable/goldilocks/README.md)
- [https://github.com/FairwindsOps/charts/blob/b160b22b7171d0da247079d9dc0d2659174cda27/stable/goldilocks/values.yaml](https://github.com/FairwindsOps/charts/blob/b160b22b7171d0da247079d9dc0d2659174cda27/stable/goldilocks/values.yaml)
- [https://aws.amazon.com/blogs/opensource/right-size-your-kubernetes-applications-using-open-source-goldilocks-for-cost-optimization/](https://aws.amazon.com/blogs/opensource/right-size-your-kubernetes-applications-using-open-source-goldilocks-for-cost-optimization/)
- [https://medium.com/better-programming/goldilocks-vs-krr-c986dfd7484d](https://medium.com/better-programming/goldilocks-vs-krr-c986dfd7484d)
- [https://github.com/robusta-dev/krr](https://github.com/robusta-dev/krr)
- [https://github.com/prometheus-operator/prometheus-operator](https://github.com/prometheus-operator/prometheus-operator)
- [https://github.com/kubernetes-sigs/prometheus-adapter](https://github.com/kubernetes-sigs/prometheus-adapter)