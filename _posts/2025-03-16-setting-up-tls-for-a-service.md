---
layout: post
title: "Setting up TLS for a service"
date: 2025-03-16 00:00:00-0000
categories: 
---

In [a previous post](https://k-candidate.github.io/2025/03/02/creating-a-private-certificate-authority.html), we created our private CA, and we generated our certificates.  
Today we will show how to set up TLS for a service, e.g. Jenkins.

There basically are 2 approaches:
- TLS termination using a reverse proxy like `nginx`. This is similar to what we already did for testing in [https://k-candidate.github.io/2025/03/02/creating-a-private-certificate-authority.html#4-testing](https://k-candidate.github.io/2025/03/02/creating-a-private-certificate-authority.html#4-testing). This is like having TLS termination in an AWS LoadBalancer.
- Terminating TLS directly on the service. This is what we will do because we already showed the other case, and because there's no need to have another piece to maintain.

The necessary changes to make this work are in this PR: [https://github.com/k-candidate/tf-jenkins-as-code/pull/13](https://github.com/k-candidate/tf-jenkins-as-code/pull/13).

In the ["Convert PEM to PKCS12" task](https://github.com/k-candidate/tf-jenkins-as-code/pull/13/files#diff-f5b0294ee7c07af1b2c6802c443dbd18a6c861061bb590a28e0f5b22d856c456R77), we are using a command instead of the module [ansible.crypto.openssl_pkcs12](https://docs.ansible.com/ansible/latest/collections/community/crypto/openssl_pkcs12_module.html) because the latter does not keep the intermediate and the end-entity in the resulting `p12`, but instead puts the end-entity only. We need both in the file.

We re-deploy (re-apply) the Terraform configuation/component for [tf-jenkins-as-code](https://github.com/k-candidate/tf-jenkins-as-code) and we're set!

![Jenkins TLS]({{ site.baseurl }}/assets/images/jenkins-tls.png){:style="display:block; margin-left:auto; margin-right:auto; width:100.00%"}

For fun let's look at that TLS termination using `nmap`:
{% highlight bash %}
$ nmap --script ssl-cert -p 443 $JENKINS_FQDN
Starting Nmap 7.80 ( https://nmap.org ) at 2025-03-16 00:00 UTC
Nmap scan report for jenkins.devops.dom (10.10.10.10)
Host is up (0.00033s latency).

PORT    STATE SERVICE
443/tcp open  https
| ssl-cert: Subject: commonName=*.devops.dom
| Subject Alternative Name: DNS:*.devops.dom, DNS:devops.dom
| Issuer: commonName=DevOps Private Intermediate CA
| Public Key type: ec
| Public Key bits: 256
| Signature Algorithm: ecdsa-with-SHA256
| Not valid before: 2025-03-01T00:00:00
| Not valid after:  2026-03-01T00:00:00
| MD5:   xxxx xxxx xxxx xxxx xxxx xxxx xxxx xxxx
|_SHA-1: xxxx xxxx xxxx xxxx xxxx xxxx xxxx xxxx xxxx xxxx

Nmap done: 1 IP address (1 host up) scanned in 0.22 seconds
{% endhighlight %}

{% highlight bash %}
$ nmap --script ssl-enum-ciphers -p 443 $JENKINS_FQDN
Starting Nmap 7.80 ( https://nmap.org ) at 2025-03-16 00:00 UTC
Nmap scan report for jenkins.devops.dom (10.10.10.10)
Host is up (0.00033s latency).

PORT    STATE SERVICE
443/tcp open  https
| ssl-enum-ciphers: 
|   TLSv1.2: 
|     ciphers: 
|       TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384 (secp256r1) - A
|       TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256 (secp256r1) - A
|       TLS_ECDHE_ECDSA_WITH_CHACHA20_POLY1305_SHA256 (secp256r1) - A
|       TLS_ECDHE_ECDSA_WITH_AES_256_CBC_SHA384 (secp256r1) - A
|       TLS_ECDHE_ECDSA_WITH_AES_128_CBC_SHA256 (secp256r1) - A
|     compressors: 
|       NULL
|     cipher preference: server
|_  least strength: A

Nmap done: 1 IP address (1 host up) scanned in 0.31 second
{% endhighlight %}