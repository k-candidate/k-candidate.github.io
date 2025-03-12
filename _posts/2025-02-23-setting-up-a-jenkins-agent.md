---
layout: post
title: "Setting up a Jenkins agent"
date: 2025-02-23 00:00:00-0000
categories: 
---

Today we will set up a Jenkins agent. This is a quick one to knock out.

We create the node itself using Terraform: [https://github.com/k-candidate/tf-jenkins-slave](https://github.com/k-candidate/tf-jenkins-slave).  

We are not interested in customizing it via Ansible, because we intend to run the Jenkins jobs in containers running in the node. Meaning, the node is just a means to run the containers where the jobs will be executed. Here’s the doc for more information: [https://www.jenkins.io/doc/book/pipeline/docker/](https://www.jenkins.io/doc/book/pipeline/docker/)

We want to be able to turn on and off the node on demand.  
To achieve that, we will use this plugin: [https://plugins.jenkins.io/libvirt-slave/](https://plugins.jenkins.io/libvirt-slave/)  
So that’s something to add to our Jenkins master image. See these 2 PRs:
- [https://github.com/k-candidate/tf-jenkins-as-code/pull/9](https://github.com/k-candidate/tf-jenkins-as-code/pull/9)
- [https://github.com/k-candidate/tf-jenkins-as-code/pull/10](https://github.com/k-candidate/tf-jenkins-as-code/pull/10)


Unfortunately, the libvirt-slave plugin does not allow using SSH keys, and therefore we have no other choice but to rely on the username/password. So, remember to enable password authentication in the `sshd_config` of the server where you have your hypervisor.

The documentation of the plugin is simple and clear, so there’s no need to repeat that in here.  
After setting up the cloud and the agent node itself, we’re ready to build pipelines!