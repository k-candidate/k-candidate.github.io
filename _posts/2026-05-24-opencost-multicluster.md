---
layout: post
title: "K8s Cost Control - OpenCost - Multi-Cluster Setup"
date: 2026-05-24 00:00:00-0000
categories: 
---

As of April 2026, there is no documentation for multi-cluster setup of OpenCost. And I was unable to find any blogs explaining it. So here it is.

![opencost logo]({{ site.baseurl }}/assets/images/opencost-logo.png){:style="display:block; margin-left:auto; margin-right:auto; width:50.00%"}

You have to deploy OpenCost per cluster even if you have a centralized datasource (e.g. Thanos). Why? Why not one centralized OpenCost in the cluster where you have the centralized datasource (e.g. Thanos)? Because it is not supported by OpenCost. See [https://github.com/opencost/opencost/issues/2673](https://github.com/opencost/opencost/issues/2673):
> OpenCost currently does not support multiple clusters, you must install 1 Prometheus and 1 OpenCost per cluster.

So let's make it clear: even though all your OpenCost deployments in the different clusters will query the same Thanos endpoint (variable `PROMETHEUS_SERVER_ENDPOINT`), you still have to deploy opencost per cluster.

You need a consistent cluster label present in your metric source data. A common setup is Prometheus `externalLabels` with a key like `cluster`.  
Remember that the implicit assumption here is that you already have Prometheus per cluster, and Thanos in one central cluster.

Wht are `externalLabels`? They're key-value pairs added to all metrics only when data is sent to external systems, such as Thanos. They act as globally unique identifiers for a specific Prometheus, commonly specifying cluster, region, or replica to enable data aggregation and deduplication.  
Here's where you set them when using the helm chart [https://github.com/prometheus-community/helm-charts/blob/97de013b787ae602d8c24e12f6a82c9bb716927e/charts/kube-prometheus-stack/values.yaml#L4184-L4186](https://github.com/prometheus-community/helm-charts/blob/97de013b787ae602d8c24e12f6a82c9bb716927e/charts/kube-prometheus-stack/values.yaml#L4184-L4186)

And you need to set these environment variables in each OpenCost deployment:
```yaml
opencost:
  exporter:
    extraEnv:
      CURRENT_CLUSTER_ID_FILTER_ENABLED: "true"
      PROM_CLUSTER_ID_LABEL: "cluster"
      CLUSTER_ID: "<this-cluster-label-value>"
```

What does that stuff mean?
- `CURRENT_CLUSTER_ID_FILTER_ENABLED=true` enables cluster-scoped filtering on OpenCost Prometheus (or Thanos) queries.
- `PROM_CLUSTER_ID_LABEL` is the metric label key OpenCost should use for cluster matching (for example, `cluster` or `cluster_id`).
- `CLUSTER_ID` is the label value for the current cluster. It should match the value used in the backend metrics.

For example, if one of your Prometheus instances writes to Thanos and uses:

```yaml
externalLabels:
  cluster: qa
```

Then, the OpenCost instance running in that cluster should use:

```yaml
opencost:
  exporter:
    extraEnv:
      CURRENT_CLUSTER_ID_FILTER_ENABLED: "true"
      PROM_CLUSTER_ID_LABEL: "cluster"
      CLUSTER_ID: "qa"
```

Happy kubernetes cost monitoring and saving!

Adding here some issues I read while looking into this. Just breadcrumbs to find the trail ...
- [https://github.com/opencost/opencost/issues/3227](https://github.com/opencost/opencost/issues/3227)
- [https://github.com/opencost/opencost/pull/3253](https://github.com/opencost/opencost/pull/3253)
- [https://github.com/opencost/opencost/issues/2638](https://github.com/opencost/opencost/issues/2638)
- [https://github.com/opencost/opencost/issues/268](https://github.com/opencost/opencost/issues/268)
- [https://github.com/opencost/opencost-website/issues/194](https://github.com/opencost/opencost-website/issues/194)
- [https://github.com/opencost/opencost/issues/2673](https://github.com/opencost/opencost/issues/2673)

## Update
The public documentation has been updated to include this information via [https://github.com/opencost/opencost-website/pull/488](https://github.com/opencost/opencost-website/pull/488).