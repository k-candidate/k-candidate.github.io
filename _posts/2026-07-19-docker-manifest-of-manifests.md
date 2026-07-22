---
layout: post
title: "Docker Image Annotations - Manifest of Manifests: Docker Manifest List vs OCI Index"
date: 2026-07-19 00:00:00-0000
categories: 
---

In [One Docker Bake Pipeline to Rule Them All - Part I: The Baking](https://k-candidate.github.io/2026/02/16/one-docker-bake-pipeline-to-rule-them-all-part1.html) and [One Docker Bake Pipeline to Rule Them All - Part II: Understanding Container Image Signing, Attestations, and K8s Admission Control](https://k-candidate.github.io/2026/04/06/one-docker-bake-pipeline-to-rule-them-all-part2.html), I am using multi-arch images.

Those multi-arch images have a manifest of manifests.

A manifest of manifests uses descriptors that point to the image manifests. There's one descriptor per arch, and one image manifest per arch.

If this stuff sounds like spaghetti to you, let me say it another way:
- Manifest of manifests: this is the top level JSON file referenced by the multi-arch image tag. It contains an array of entries mapping out supported platforms.
- Descriptors: small JSON objects inside the manifest of manifests. Each descriptor specifies a child object's `mediaType`, unique content hash (`digest`), `size`, and target `platform` (arch and OS).
- Image Manifests: specific JSON files for each individual arch. Each points to its own unique config blob and ordered list of filesystem layers.

```bash
docker manifest inspect kcandidate/gha-test:v11 | jq

{
  "schemaVersion": 2,
  "mediaType": "application/vnd.oci.image.index.v1+json", 
  
  // ─── MANIFEST OF MANIFESTS  ─────────────────────────────────────────────
  // The entire JSON object represents the OCI Image Index.
  // It groups multiple image manifests together under one tag.
  
  "manifests": [
    
    // ─── DESCRIPTOR 1 (amd64 / linux) ─────────────────────────────────────
    // Descriptors point to specific content using mediaType, size, and digest.
    {
      "mediaType": "application/vnd.oci.image.manifest.v1+json",
      "size": 668,
      "digest": "sha256:3f932cb48e4df3b457de86d272a467b85680a901eb2a7b27388880cbbb3c9dc4",
      "platform": {
        "architecture": "amd64",
        "os": "linux"
      }
    },
    
    // ─── DESCRIPTOR 2 (arm64 / linux) ─────────────────────────────────────
    {
      "mediaType": "application/vnd.oci.image.manifest.v1+json",
      "size": 668,
      "digest": "sha256:dabb9f966973f987011928dc88c177391b32254c2970e61965d4e0e60a879320",
      "platform": {
        "architecture": "arm64",
        "os": "linux"
      }
    }
  ]
}
```

```bash
regctl manifest get kcandidate/gha-test:v11 \
  --platform=linux/amd64 --format raw-body | jq

// Note: This output is an Image Manifest. 
// The 'regctl' command used '--platform=linux/amd64' to drill down 
// from the main Image Index to extract this specific platform's manifest.
{
  "schemaVersion": 2,
  "mediaType": "application/vnd.oci.image.manifest.v1+json",
  "config": {
    "mediaType": "application/vnd.oci.image.config.v1+json",
    "digest": "sha256:db2a4467bf38b2fe792726791ef4550de299150053a24ad7f6ea5242f1936ba4",
    "size": 1793
  },
  "layers": [
    {
      "mediaType": "application/vnd.oci.image.layer.v1.tar+gzip",
      "digest": "sha256:76eb174b37c3e263a212412822299b58d4098a7f96715f18c7eb6932c98b7efd",
      "size": 3627864
    },
    {
      "mediaType": "application/vnd.oci.image.layer.v1.tar+gzip",
      "digest": "sha256:4f4fb700ef54461cfa02571ae0db9a0dc1e0cdb5577484a6d75e68dc38e8acc1",
      "size": 32
    }
  ]
}
```

Now what are annotations?
They are standardized, structured metadata key-value pairs defined by the Open Container Initiative (OCI) image specification. They allow developer tools, vulnerability scanners, and deployment systems to inspect information about an image's origin, configuration, and contents directly from the registry without needing to pull the entire image file.

How are they different from labels?
While both attach metadata, they serve different layers of the container ecosystem:
- Annotations target OCI infrastructure. They live in the image manifest or index. Registries and external tools can read them on demand without extracting container filesystems.
- Labels target the local Docker Engine. They are embedded directly inside the image configuration layers or local runtime objects (like containers and networks).

The spec for the annotations can be found here: [https://github.com/opencontainers/image-spec/blob/af26a05fba5ee648512f4ea3c9fda1fcc1b6d6dc/annotations.md](https://github.com/opencontainers/image-spec/blob/af26a05fba5ee648512f4ea3c9fda1fcc1b6d6dc/annotations.md)

We can see in there that a few can be very useful and it would behoove us to have them created by default by a centralized pipeline:
- `org.opencontainers.image.created`: date and time on which the image was built, conforming to RFC 3339.
- `org.opencontainers.image.source`: URL to get source code for building the image (string).
- `org.opencontainers.image.version`: version of the packaged software:
  - The version MAY match a label or tag in the source code repository
  - version MAY be Semantic versioning-compatible
- `org.opencontainers.image.revision`: source control revision identifier for the packaged software. Basically the git hash.

And at what level do these annotations live? Before I answer that, I want to ask another question: wouldn't it behoove me to have those annotations at all 3 levels (the manifest of manifests, the descriptors, and the image manifests)? The answer is an obvious yes: that way I can get the info no matter where I look.

Well, it's time to dig into more details. So far we called the top level index the "manifest of manifests". Well there are 2 types:
- Docker Manifest List aka Fat Manfest. You will see this as `"mediaType": "application/vnd.docker.distribution.manifest.list.v2+json"`
- OCI Index. You will see this as `"mediaType": "application/vnd.oci.image.index.v1+json"`

The former (Docker Manifest List) does not support annotations.  
The latter (OCI Index) does. Therefore this is what one should use to have the annotations in all 3 levels.

To make the OCI Index, a few tools can be leveraged, like `regctl index create`: [https://regclient.org/cli/regctl/index/create/](https://regclient.org/cli/regctl/index/create/).