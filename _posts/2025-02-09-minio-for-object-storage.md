---
layout: post
title: "MinIO for Object Storage"
date: 2025-02-09 00:00:00-0000
categories: 
---
Today we will set up an object storage system.

![Minio UI]({{ site.baseurl }}/assets/images/minio-object-storage.png){:style="display:block; margin-left:auto; margin-right:auto"}

## 1. Why?
We want to be able to store and retrieve files for CICD pipelines and other random tasks for which NFS or SMB are not suitable.

## 2. Choosing a solution
There are multiple options.  
We want an on-prem self-hosted system that offers the same features as AWS S3.

We will go with MinIO. It is API compatible with the Amazon S3 cloud storage service.

## 3. Setup
Although MinIO can be used for many scenarios including HPC, we want the most basic functions (for now): creating a bucket and putting/getting objects.

We are using the usual IaC and CaC setup with Terraform, cloud-init, and Ansible.  
All the code can be found here: [https://github.com/k-candidate/tf-minio](https://github.com/k-candidate/tf-minio).

## 4. Usage
Once deployed, we have multiple options to interface with a bucket in MinIO:
- UI: port 9001.
- MinIO cli (`mc`): [https://github.com/minio/mc](https://github.com/minio/mc). We can see it used in the Ansible playbook of the repo we made above.
- MinIO SDK: [https://min.io/docs/minio/linux/developers/minio-drivers.html](https://min.io/docs/minio/linux/developers/minio-drivers.html).