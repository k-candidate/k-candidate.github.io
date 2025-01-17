---
layout: post
title: "On Terraform Modules"
date: 2024-12-22 00:00:00-0000
categories: 
---
I want to make my whole homelab setup as code.  

I use kvm (hypervisor) qemu (hardware emulator) and libvirt (wrapper, provides APIs) for virtualization, so what do I need? First a network, and then VMs in it. But later I will need more networks and more VMs.

Enter Terraform modules.

## How do I need these modules to be?

### Improve iteratively in an Agile way
I’ll start with a MVP (Minimum Viable Product) and improve things as the need arises or as I see potential future limitations.  

This applies to the networking module I have made: [https://github.com/k-candidate/tf-module-kvm-network](https://github.com/k-candidate/tf-module-kvm-network).  
It is very simple, but for now it is enough for my use case, which is to create a NAT network component: [https://github.com/k-candidate/tf-kvm-network-nat](https://github.com/k-candidate/tf-kvm-network-nat).

### Easy to use
I must have default values to cover the “vanilla case” which is the majority of cases. And I have to either include an examples directory, or point to another repo as an example in the readme.  

I want to avoid having to figure out how it works or how it’s set up after a month or two of not touching any of this material.  
Ever wrote some code and then a year later you have to revisit it and you start asking yourself “How does it work? I don’t remember where this was supposed to go…”. I want to prevent this.  

Another thing to do to reduce the probabilities of future regrets is pinning the Terraform and provider versions.

### Versioned
I use semantic versioning ([https://semver.org/](https://semver.org/)) and conventional commits ([https://www.conventionalcommits.org](https://www.conventionalcommits.org)), and have a GitHub action take care of that.

### Deep
I mentioned this in [https://k-candidate.github.io/2024/12/15/a-philophy-of-software-design-book-takeaways.html](https://k-candidate.github.io/2024/12/15/a-philophy-of-software-design-book-takeaways.html).

In the case of the VM module for example, I might need just a VM with the base image, but sometimes I might want it with some software installed via cloud-init (user data) and configured via Ansible. 

I do not want to do any heavy lifting when provisioning VMs. So all the logic has to go in the module to support my different use cases.  
And that’s what I did here: [https://github.com/k-candidate/tf-module-kvm-vm ](https://github.com/k-candidate/tf-module-kvm-vm)


This is it for now. If you want more information on building modules you can check the official documentation: [https://developer.hashicorp.com/terraform/tutorials/modules/pattern-module-creation](https://developer.hashicorp.com/terraform/tutorials/modules/pattern-module-creation).  
Now let's build our environment!