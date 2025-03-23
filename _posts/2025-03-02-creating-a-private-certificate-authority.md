---
layout: post
title: "Creating a Private Certificate Authority to issue Private TLS certificates"
date: 2025-03-02 00:00:00-0000
categories: 
---

Today we're creating a private Certificate Authority.

## 1. Why?
Why not just use use self-signed certificates?
- because anyone can issue one.
- because they can’t be revoked.

Why not use a public CA like Let’s Encrypt?
- because public CAs need a domain to be publicly accessible to issue a cert. All of my infrastructure is internal.

## 2. Design and Architecture
If we were on AWS, we would use Certificate Manager (ACM) for public certificates, and Private Certificate Authority (PCA) for internal usage.  
But we’re building a self-hosted environment here. We’re making the invisible lower parts of what AWS offers as ready to use services.

### 2.1 Software
There are a few options to choose from (see [https://en.wikipedia.org/wiki/Comparison_of_cryptography_libraries](https://en.wikipedia.org/wiki/Comparison_of_cryptography_libraries)). We are going to use the de facto standard: OpenSSL.  
As I said in the previous post [https://k-candidate.github.io/2024/11/23/real-world-cryptography-book-takeaways.html](https://k-candidate.github.io/2024/11/23/real-world-cryptography-book-takeaways.html): be conservative, and use tried and tested cryptography.

### 2.2 Hardware
We have to remember that security should be at the service of the business, not an  impediment. Why am I saying that? Well, because like with any project, how far and deep do we want to go? Meaning, how much do we want to spend on this? My answer is zero, because this is for my personal use, not for a business nor an enterprise that is subject to HIPAA or PCI DSS.  
But, if you have have a Hardware Security Module (HSM), or locked cages etc., this is a good opportunity to use them.

### 2.3 Process
Again, how deep do you want to go? How much do you want to spend on this? In my case, this is a personal internal environment.  
But if that is not your situation, and you are operating an environment that is subject to regulations, then to be compliant you will need to set up a formal process with segregation of duties.  
Studying ICANN’s IANA key signing ceremony can be helpful to see how far this can go. See [https://www.icann.org/en/blogs/details/the-key-to-the-internet-and-key-ceremonies-an-explainer-11-07-2023-en](https://www.icann.org/en/blogs/details/the-key-to-the-internet-and-key-ceremonies-an-explainer-11-07-2023-en) and [https://www.youtube.com/watch?v=K590t6szNLI](https://www.youtube.com/watch?v=K590t6szNLI). 

### 2.4 System
The system architecture should use a multi-tiered hierarchy:
- Root CA
  - Offline: once the intermediate CA is created, take the root and its private key offline.
  - Ultimate trust anchor.
  - To issue and renew intermediate CA certificates.
  - The root certificate will be distributed to internal systems.
- Intermediate CA
  - Online.
  - For day-to-day operations of end-entity certificate issuance.
  - The intermediate certificate will be included in the chain sent by the web servers during TLS handshakes

In my case, I will put both in the same machine simply to save on resources.  
Also, I will be making a wildcard certficate because I have no need for the overhead of making a cert per service (Jenkins, Vault, Consul, Minio …). It adds no value for my use case.

### 2.5 Revocation
At least for now, in my case I will not be using CRL nor OCSP as this is just a personal environment that is not exposed to the Internet.

## 3. Implementation
While working on this, I have tried EJBCA. But it is too much overhead: too many buttons and knobs for my use case. However, I might add it in the future to have OCSP. Here's the code I made in case someone finds it useful: [https://github.com/k-candidate/tf-ejbca](https://github.com/k-candidate/tf-ejbca).

We have the usual setup: Terraform for the infrastructure, and Ansible for the configuration including issuing the keys and certificates.  
We store the artifacts in a Minio S3 bucket, so that it is easy to retrieve them later from the different machines.  
This allows us to turn off the machine once the artifacts are in the S3 bucket.  
Here's the code: [https://github.com/k-candidate/tf-ca](https://github.com/k-candidate/tf-ca).

I tried using Ed25519 but in vain, because the web browsers do not support it. This is confirmed by the CA/B Forum Baseline Requirements: [https://cabforum.org/working-groups/server/baseline-requirements/documents/](https://cabforum.org/working-groups/server/baseline-requirements/documents/). Current version (as of Mar 2025) here: [https://cabforum.org/working-groups/server/baseline-requirements/documents/CA-Browser-Forum-TLS-BR-2.1.4.pdf](https://cabforum.org/working-groups/server/baseline-requirements/documents/CA-Browser-Forum-TLS-BR-2.1.4.pdf). Search for the keyword “curve” in the pdf.

## 4. Testing
To test the created certificates, we will spin up a `nginx` container:

`Dockerfile`:
```
FROM nginx:alpine
COPY chain.pem /etc/nginx/ssl/chain.pem
COPY end-entity-key.pem /etc/nginx/ssl/end-entity-key.pem
COPY index.html /usr/share/nginx/html/index.html
COPY nginx.conf /etc/nginx/nginx.conf

RUN chmod 600 /etc/nginx/ssl/end-entity-key.pem
```
`nginx.conf`:
```
events {
    worker_connections 1024;
}

http {
    server {
        listen 80;
        listen 443 ssl;
        server_name www.test.dom;

        ssl_certificate /etc/nginx/ssl/chain.pem;
        ssl_certificate_key /etc/nginx/ssl/end-entity-key.pem;

        location / {
            root /usr/share/nginx/html;
            index index.html;
        }
    }
}
```
`index.html`:
```
<h1>Hello from www.test.dom</h1>
```
Build the image via: `docker build -t test-domain-https .`

Append `127.0.0.1	www.test.dom` to `/etc/hosts`

Start the container: `docker run -d -p 80:80 -p 443:443 --name fake-domain-container fake-domain-https`

If we run `curl https://www.test.dom`, we get the error `curl failed to verify the legitimacy of the server and therefore could not establish a secure connection to it.`.  

But if we run `curl --cacert root-ca-cert.pem https://www.test.dom` it works correctly.

To make this change permanent, we can add the root cert to the trust store of the OS. In Ubuntu: 
```
$ sudo cp root-ca-cert.pem /usr/local/share/ca-certificates/root-ca-cert.crt
$ sudo update-ca-certificates
```
Notice the file extension change. More details here: [https://documentation.ubuntu.com/server/how-to/security/install-a-root-ca-certificate-in-the-trust-store/index.html](https://documentation.ubuntu.com/server/how-to/security/install-a-root-ca-certificate-in-the-trust-store/index.html)

We go to that url in Firefox, and we get this warning: 
![Firefox TLS error]({{ site.baseurl }}/assets/images/firefox-tls-error.png){:style="display:block; margin-left:auto; margin-right:auto"}

This is because Firefox does not have access to the OS's trust store. You can try adding the `preference` mentioned in [https://support.mozilla.org/en-US/kb/setting-certificate-authorities-firefox](https://support.mozilla.org/en-US/kb/setting-certificate-authorities-firefox).  
But that won't work in modern versions of Ubuntu, because of the `snap` confinement.  
We go to Firefox's settings > Privacy & Security > View Certificates > Authorities > Import > we add the root cert.  
Now if we refresh the page we will be able to see it using TLS.  
And if we view the certificate we will see the chain of trust: 
![Firefox TLS chain of trust]({{ site.baseurl }}/assets/images/firefox-tls-chain-of-trust.png){:style="display:block; margin-left:auto; margin-right:auto"}

This means that it is working as expected.