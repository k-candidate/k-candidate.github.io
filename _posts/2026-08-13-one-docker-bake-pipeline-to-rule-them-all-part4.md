---
layout: post
title: "One Docker Bake Pipeline to Rule Them All - Part IV: Docker Secrets"
date: 2026-08-13 00:00:00-0000
categories: 
---

This universal Docker bake pipeline must support Docker secrets.

## References

- [https://docs.docker.com/build/bake/reference/#targetsecret](https://docs.docker.com/build/bake/reference/#targetsecret)
- [https://docs.docker.com/build/building/secrets/](https://docs.docker.com/build/building/secrets/)

## Why Use Docker Build Secrets?

To prevent credentials from being permanenetly baked into the final container image layers or image history.

Using something like `ENV` or `ARG` instructions stores those values directly in the image metadata and intermediate layers. Meaning, anyone who pulls the image or runs commands like `docker image history` can easily extract and read those plain-text secrets long after the build completes.

## Choosing a Design

I see 4 ways of doing this:
- Have the reusable pipeline explicitly expect specific secrets.
  - Not a good idea, as it is not future proof and limits the calling repo.
  - Pass.
- Have the reusable pipeline expect one GHA secret, and the caller repo would have one GHA secret that contains the different secrets needed by Docker in a JSON.
  - OK actually, but it makes secret management uncomfortable for the calling repo. Anytime the user (calling repo) has to change the value of a secret, they have to make the whole JSON, meaning they have to find and fill the values of all the secrets of the JSON. Bad user experience.
  - Pass.
- Use an external secrets manager
  - This is what's supposedly a good practice, but from a threat modeling perspective, it provides no real value because there's no added security: once a malicious actor has access to the calling repo they can retrieve the secret whether it is stored in a GHA secret or in an external secrets manager.
  - And there's definitely added complexity, which means more maintenance overhead.
  - Pass.
- Have each Docker build secret in a GHA secret, and have the calling workflow use `secrets:inherit`
  - This fits all the requirements: best user experience, and security is not traded off from a threat modeling perspective. Passing all the secrets to the reusable pipeline is ok, because the premise is that the reusable pipeline's repo is more secured than the calling repo, and because the owner of the calling repo is already outsourcing the building of the image to the reusable repo.
  - Go!

## Implementation

See this PR for the change in the reusable pipeline: [https://github.com/k-candidate/gha-workflows/pull/5](https://github.com/k-candidate/gha-workflows/pull/5).  
And see this PR for an example in the consuming repo: [https://github.com/k-candidate/gha-test/pull/2](https://github.com/k-candidate/gha-test/pull/2)