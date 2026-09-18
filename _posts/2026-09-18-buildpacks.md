---
layout: post
title: "What On Earth Are Buildpacks?"
date: 2026-09-18 00:00:00-0000
categories: 
---

Last month, Buildpacks [graduated from the CNCF](https://www.cncf.io/announcements/2026/08/11/cncf-announces-graduation-of-cloud-native-buildpacks-advancing-the-standard-for-container-builds/). What's a [Buildpack](https://buildpacks.io/)?

## What is a Buildpack?

A Buildpack is an open-source tool that transforms your raw source code into a container image without requiring a Dockerfile.

Instead of you writing low-level infrastructure instructions, Buildpacks abstract the entire packaging process away. You simply run a CLI tool like pack build against your application folder. The framework automatically detects what language your app is written in, fetches the required dependencies, compiles the code, and configures the container automatically.

The resulting artifact is a standard, fully OCI-compliant container image that runs seamlessly on any modern container platform (docker, aws ecs, k8s ...).

## How Does It Work?

Under the hood, it does 2 things:
1. Detect: it looks for "signals" to determine the tech stack (`package.json` for Node, `requirements.txt` for Python, `pom.xml` for Java etc.)
2. Build: Once the language is identified, the buildpack sets up a secure user environment (non-root by default), installs the language runtime, downloads dependencies, compiles the binaries, and sets the final container entrypoint command.

## Main Difference of Buildack vs Docker

The core difference boils down to Procedural (Dockerfile) vs Declarative (Buildpack).

## Rebasing

In a traditional Dockerfile, your image layers are baked together sequentially like a stack of pancakes. If a security vulnerability (CVE) is discovered in your base Ubuntu layer, you can't just fix the bottom layer. You have to rebuild the image.

Buildpacks solve this by strictly decoupling the underlying operating system from your application code via unique layer metadata.

Because these layers are separated, Buildpacks can perform what is called Image Rebasing. If a core OS library gets hit with a CVE, you can run a single command directly against your container registry: `pack image rebase my-app-image --run-image patched-base-os-image --publish`

Because this process only edits the metadata pointers rather than compiling code, it patches your containers in milliseconds. I repeat: no code compiling. That's the magic of this thing. That's what these tools mention in their homepages: [https://paketo.io/](https://paketo.io/).

How to do the rebasing:

```bash
pack image rebase ://amazonaws.com \
  --run-image ://amazonaws.com \
  --publish
```

In the case of Kubernetes, rebasing can be handled via an open-source Kubernetes controller called Kpack. Kpack runs inside your cluster and constantly watches for base OS updates. More info in their repo [https://github.com/buildpacks-community/kpack](https://github.com/buildpacks-community/kpack) and their doc [https://buildpacks.io/docs/for-platform-operators/how-to/integrate-ci/kpack/](https://buildpacks.io/docs/for-platform-operators/how-to/integrate-ci/kpack/).

## Security: Distroless and Scratch Docker Images vs Buildpack

In a static binary using `gcr.io/distroless/static` or a `FROM scratch` scenario, there's zero security benefit from using Buildpack.  
There's actually more work with Buildpack because you have to do the rebasing. In Distroless (or scratch) there's no OS layer so that work does not exist.

## Supported Languages

- Java
- Node.js
- Python
- Go
- .Net

## Unsupported Languages and Use Cases

- C
- C++
- Rust
- Elixir/Erlang
- R, Perl, Fortran
- System level binaries and custom binaries. For example if you need to install `ffmpeg` in your image
- AI, ML, and Data Science stacks with NVIDIA CUDA drivers and specialized GPU libraries
- multi-process containers

## My Verdict

I think it comes down to who's the user and how they want to build and manage their pipelines.

For example, if it's a small team of developers using just Java and without the resources to maintain pipelines, I can see this being used.

But, I do not know what's stopping Docker from adding an abstraction layer that does what Buildpacks does. Meaning, you have your app code and you run just one `docker <new_magical_subcommand>` and on its own, under the hood, it handles creating an invisible Dockerfile that gets built into an image.

Also, with generative AI tools becoming common, I do not see making a good Dockerfile being a hassle.

So I don't see where Buildpacks would fit in any of the things I am doing right now. But I'll be on the lookout. It's an interesting project.
