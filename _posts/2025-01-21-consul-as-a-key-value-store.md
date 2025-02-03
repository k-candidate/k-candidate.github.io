---
layout: post
title: "Consul as a Key/Value Store"
date: 2025-01-21 00:00:00-0000
categories: 
---
Today we will set up a Key/Value Store.

![Consul Key/Value Store]({{ site.baseurl }}/assets/images/consul-kv-store.png){:style="display:block; margin-left:auto; margin-right:auto"}

## 1. What is a Key/Value Store?
>A key-value store, or key-value database is a simple database that uses an associative array as the fundamental data model where each key is associated with one and only one value in a collection. This relationship is referred to as a key-value pair.

## 2. Why a Key/Value Store?
We want to be able to store configuration data.  
For example: the values of Terraform variables for a component in a specific environment.

## 3. Choosing a Key/Value Store
Key/value stores usually are no-SQL databases like MongoDB. However, directly using that is too much overhead for our use case.

If we were on AWS, we would use SSM Parameter Store.  
But we are making a self-hosted environment. So we will go with Hashicorp’s Consul which includes a Key/Value Store.

## 4. Setting up Consul
I have created the component [https://github.com/k-candidate/tf-consul](https://github.com/k-candidate/tf-consul) using the Terraform module I had made previously ([https://github.com/k-candidate/tf-module-kvm-vm](https://github.com/k-candidate/tf-module-kvm-vm)). It does the following:
- Terraform provisions the VM.
- Terraform triggers the user data (cloud-init) to install Docker.
- Terraform launches Ansible.
- Ansible spins up Consul using Docker Compose with a volume for data persistence and another for the configuration.

For security, we set up the ACL policy to deny by default, and we create 2 tokens: one with read-only access to the KV store, and another with write access.

## 5. How to use
Deploying the component is straightforward: you simply need to supply the variables' values and the PostgreSQL connection string. See the previous article “[PostgreSQL as a Remote Terraform Backend with State Locking](https://k-candidate.github.io/2025/01/14/postgresql-as-a-remote-terraform-backend-with-state-locking.html)” for more information.

Once it is deployed, to create KV pairs, we can use the write-token in the web UI (port 8500) or the API.  

{% highlight bash %}
curl -X PUT -H "X-Consul-Token: <WRITE-TOKEN>" \
-d '<VALUE>' \
http://consul.domain.dom:8500/v1/kv/<KEY>

#Example
curl -X PUT -H "X-Consul-Token: aaaaa-bbbbb-ccccc" \
-d 'test-user' \
http://consul.domain.dom:8500/v1/kv/dev/tf-vm-test/vm_username
{% endhighlight %}

To read, we use the read-token.  
{% highlight bash %}
curl -s -X GET -H "X-Consul-Token: <READ-TOKEN>" \
http://consul.domain.dom:8500/v1/kv/<KEY> \
| jq -r '.[].Value' | base64 -d

#Example
curl -s -X GET -H "X-Consul-Token: ddddd-eeeee-fffff" \
http://consul.domain.dom:8500/v1/kv/dev/tf-vm-test/vm_username \
| jq -r '.[].Value' | base64 -d
{% endhighlight %}

More information in the [API documentation](https://developer.hashicorp.com/consul/api-docs/kv).

## 6. Conclusion
We now have a Key/Value Store for our configuration data: a necessary component to set up a deployment pipeline.

This is it for now, and I hope you learned something.