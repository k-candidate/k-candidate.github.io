---
layout: post
title: "Jenkins - How to speed up node availability and lower cost at the same time"
date: 2025-04-08 00:00:00-0000
categories: 
---

It is possible to spin up ephemeral Jenkins nodes using a CSP’s VM plugin:
- [EC2 for AWS](https://plugins.jenkins.io/ec2/)
- [Azure VM Agents](https://plugins.jenkins.io/azure-vm-agents/)
- [Google Compute Engine](https://plugins.jenkins.io/google-compute-engine/) 

If this is the strategy you are using (as opposed to k8s pods for example), you can lower the cost and improve the node spin up speed by using the 5 tactics that we will discuss below. I will not cover the obvious ones like “use a VM of the size that you need”. I will mention only the corners that usually are overlooked (IMO).

But first, how do we get to these tactics? By looking at the sequence that Jenkins follows to get a node ready and speeding up every part that we can.

Here are the 5 tactics:
- Use newer generations of hardware. In AWS for example, m6i is newer (and therefore has better performance) than m4, but it is cheaper. This means quicker and cheaper builds. M7i is slightly more expensive than m6i, but it is quicker, so here one has to calculate if the shorter build time compensates for the price enough to make the total price cheaper. You can find a price and specs comparison here: [https://instances.vantage.sh/](https://instances.vantage.sh/).
- Use an OS that has a quick boot sequence. In AWS that would be AL2023. To test this, spin up 2 EC2 instances: AL2 and AL2023. The former will take more than a minute to be available for an SSH connection. The latter will take half a minute and sometimes considerably less.
- Disable host key checking in the Jenkins master. It’s practically useless in an environment where IPs are recycled.
- Use an SSH algorithm that is quicker: Ed25519 instead of RSA.
- Use a custom image that includes java. If not, the Jenkins master will connect to the node via SSH, then install multiple packages including Java. This takes time.

Now how does this lower cost?  
If nodes can be spun up and made available for jobs in less than a minute, then there’s no or little need for a “minimum number of instances” nor “spare instances”, meaning that the price for “idle” usage is $0.00.