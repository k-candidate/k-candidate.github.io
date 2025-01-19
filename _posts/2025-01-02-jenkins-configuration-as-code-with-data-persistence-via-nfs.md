---
layout: post
title: "Jenkins Configuration as Code with Data Persistence via NFS"
date: 2025-01-02 00:00:00-0000
categories: 
---
Today we will set up Jenkins with configuration as code (CasC) and data persistence via NFS.

![Jekins as Code]({{ site.baseurl }}/assets/images/JCasC.png){:style="display:block; margin-left:auto; margin-right:auto; width:33.33%"}

## 1. What is Jenkins?
Jenkins is an open source CI/CD server. Continuous Integration and Continuos Delivery (or Deployment) are an integral part of the backbone of any modern software company.  

## 2. Why Jenkins?
There are multiple CI/CD platforms out there. And the trend nowadays is moving towards the integrated solutions like Gitlab CI/CD or Gitea Actions or GitHub Actions. However, Jenkins still is the most used CI/CD tool ([here](https://www.cncf.io/blog/2020/11/17/cloud-native-survey-2020-containers-in-production-jump-300-from-our-first-survey/), and [here](https://devops.com/the-future-of-jenkins-in-2024/)).

Everything has pros and cons. What’s important is being aware of them, choosing the option that’s most convenient, and planning for the issues that may arise depending on those pros and cons, because the action plan should be different depending on what you’re using.

For example, having your CI/CD controller and your code repository in the same machine is like having your two most important eggs in the same basket. That’s a con. But that allows for seamless integration. That’s a pro.

My personal stance is that what matters at the end of the day is the principles. But, be familiar with both, and then get comfortable with and specialize in one of them. If later you have to move to another one, the transition should relatively be easy, because the principles do not change that much.

As you can see in my GitHub, I use both Jenkins and GitHub Actions.

## 3. Design
The repository we will be working with is : [https://github.com/k-candidate/tf-jenkins-as-code](https://github.com/k-candidate/tf-jenkins-as-code).  
We provision the Jenkins controller via Terraform. Terraform takes care of running the user data via cloud-init, and applies the configuration via Ansible, thanks to [our module](https://github.com/k-candidate/tf-module-kvm-vm).

We use [JCasC](https://www.jenkins.io/projects/jcasc/) for configuring Jenkins.

We achieve data persistence by storing all Jenkins data in [the NFS server](https://github.com/k-candidate/tf-nfs) we built in [the previous article](https://k-candidate.github.io/2024/12/27/creating-an-nfs-server-using-terraform-cloud-init-and-ansible.html).

### 3.1 Docker image
This part is done via GitHub Actions. See [https://github.com/k-candidate/tf-jenkins-as-code/blob/main/.github/workflows/docker-image.yaml](https://github.com/k-candidate/tf-jenkins-as-code/blob/main/.github/workflows/docker-image.yaml).

We start by using the [publicly available](https://hub.docker.com/r/jenkins/jenkins) `jenkins/jenkins:<LTS-tag>` for the base image, and we add the plugins to it. See [https://github.com/k-candidate/tf-jenkins-as-code/blob/main/jenkins_image/Dockerfile](https://github.com/k-candidate/tf-jenkins-as-code/blob/main/jenkins_image/Dockerfile)

We do not apply the CasC at this point for security and flexibility.

Our custom image gets automatically built when any file inside the `jenkins_image` directory is changed, and then pushed to [https://hub.docker.com/r/kcandidate/jenkins-casc](https://hub.docker.com/r/kcandidate/jenkins-casc).

The image is scanned via Trivy for vulnerabilities.

### 3.2 Running Jenkins
This part is decoupled from the previous Docker image build/push/scan part to keep flexibility, and to future-proof the ease of maintenance.

We are using the module [https://github.com/k-candidate/tf-module-kvm-vm](https://github.com/k-candidate/tf-module-kvm-vm) which we built in the ["On Terraform Modules" article](https://k-candidate.github.io/2024/12/22/on-terraform-modules.html). The flow is Terraform centric for ease of control, and to prescind from any scripts to glue the parts together.

- We use Terraform to provision the VM.
- Terraform triggers the user data part (cloud-init) and waits until it finishes. 
- Terraform launches Ansible. 
- Ansible maps the NFS server (where the Jenkins data is stored) to the VM using AutoFS, pulls the Docker image from [https://hub.docker.com/r/kcandidate/jenkins-casc](https://hub.docker.com/r/kcandidate/jenkins-casc), and launches it with the CasC and volume.

## 4. How to use
Assuming you already have Terraform, Ansible, libvirt etc, if you want to immediately use this component, you can clone the repo, supply the variable values, and run a `terraform apply`.

## 5. Maintenance and Upgrades
This setup has been designed to future-proof configuration changes, maintenances and upgrades.

### 5.1 Upgrade the Jenkins version
To upgrade the Jenkins version, we change [the tag in the Dockerfile for the base image](https://github.com/k-candidate/tf-jenkins-as-code/blob/b0d1f794ce7b9cc77a692630e58a37f2f1034205/jenkins_image/Dockerfile#L1).

That will trigger the GitHub Action that will build a newer version of our custom image and push it to Docker Hub.

Then we update [the tag of our custom image](https://github.com/k-candidate/tf-jenkins-as-code/blob/b0d1f794ce7b9cc77a692630e58a37f2f1034205/ansible/docker-compose.yml#L3) to his new one we created.

We do a `terraform apply` and we have ourselves an upgraded Jenkins with all the data.

### 5.2 Rollbacks
If for whatever reason, we need to rollback, we just have to change the tag and do a `terraform apply`.

### 5.3 Adding or removing plugins
It’s similar to upgrading the version of Jenkins Core. We modify the [plugins.txt file](https://github.com/k-candidate/tf-jenkins-as-code/blob/main/jenkins_image/plugins.txt), which will trigger the build of a newer version of our custom image.  
We use the new tag in [our Docker compose file](https://github.com/k-candidate/tf-jenkins-as-code/blob/5fa5556fe55d676d207d70fff0446ba826db4487/ansible/docker-compose.yml#L3).

### 5.4 Resilience
If any issues arise in the Jenkins VM, or the container, we do not care! Because we have the whole thing defined as code, and the data exists in a different machine (the NFS server).  
That being said, we should have a backup for our NFS server. Why? To have something to revert to quickly in case we’re doing a rollback after a bad Jenkins upgrade changes the `config.xml` file for example. Because, remember, Jenkins has `rw` access to its NFS share.  

I will delve into backups, and write an article about it when I get to setting up a BCDR (Business Continuity and Disaster Recovery) strategy.

## 6. Conclusion
We now have Jenkins, our CI/CD system, as code and with data persistence via NFS.  
What’s to come? We need to set up a deployment pipeline, and a backend for our Terraform.

That’s it for now, and I hope you learned something.