---
layout: post
title: "Creating an NFS server using Terraform, cloud-init, and Ansible"
date: 2024-12-27 00:00:00-0000
categories: 
---
Today we'll be creating an NFS server using the Terraform modules we built in the previous article.

We're starting from scratch, so there's no backend for Terraform, nor a deployment pipeline, at the moment.  
We're launching scripts from our laptop, for now. But we're building the machinery that will allow us to do that.

## Create the network
First, we create the network where this NFS server will live by using this component [https://github.com/k-candidate/tf-kvm-network-nat](https://github.com/k-candidate/tf-kvm-network-nat).

As per the README, we have to supply it with a subnet, a domain, and a name for our network. Make sure that the subnet range does not overlap with anything else in your setup.

We can just clone the repo, and supply the values as `TF_VAR_<var-name>` environment variables, or in a `terraform.tfvars` file, or simply by editing the `main.tf` file which is what I am showing below:

{% highlight terraform %}
module "tf-module-kvm-network" {
  source            = "git@github.com:k-candidate/tf-module-kvm-network.git?ref=v1.0.0"
  network_name      = "devops"
  network_mode      = "nat"
  network_domain    = "devops.dom"
  network_addresses = ["10.10.10.0/24"]
}
{% endhighlight %}

And then we run:
{% highlight bash %}
terraform init
terraform validate
terraform plan
terraform apply -auto-approve
{% endhighlight %}

## Create the NFS Server
Now that we have our network, we create the NFS server.

For this we use the component [https://github.com/k-candidate/tf-nfs](https://github.com/k-candidate/tf-nfs) which leverages the versatile module that we had created: [https://github.com/k-candidate/tf-nfs](https://github.com/k-candidate/tf-nfs)

As per the README, no variable is required because they all have a default.  
But in our case, we have to specify the `network_name` for example, because in the previous step we gave it the value `devops`. We tweak any other variables to suit our needs.

If we look inside this repo, and in the module it uses, we can see that it is Terraform centric, meaning, we have to deal only with Terraform. Terraform invokes cloud-init and Ansible, and passes variables to them.  
This saves us from having to deal with so many commands.

### Cloud-init 
Cloud-init expands the volume, sets up the account that will allow Ansible to SSH into the machine, applies the upgrades, installs the NFS server, and sets the hostname of the machine.

### Ansible
Ansible reboots the machine is its first start so that the cloud-init changes take effect, creates the exports to share, and configures the NFS server.  
If we make some change in the playbook, and we re-launch a `terraform apply`, it will apply the playbook thanks to [this trigger in the module](https://github.com/k-candidate/tf-module-kvm-vm/blob/9b0d1428f7bff415f1e6299207b27ec21d9c9fc4/main.tf#L95).  
We now are leveraging the power of idempotency to make the future maintenance of this server easier on ourselves. The objective is to keep everything as code.

## Conclusion
After applying this Terraform configuration, we got ourselves a working NFS server.

I hope you learned something, and next time we're going to use this NFS server.