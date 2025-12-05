---
layout: post
title: "Container Image Media Types"
date: 2025-11-30 04:00:00-0000
categories: 
---

[https://github.com/opencontainers/image-spec/blob/26647a49f642c7d22a1cd3aa0a48e4650a542269/media-types.md](https://github.com/opencontainers/image-spec/blob/26647a49f642c7d22a1cd3aa0a48e4650a542269/media-types.md)

A concise summary of the parts I'm interested in.

<table>
  <thead>
    <tr>
      <th>Aspect</th>
      <th>Docker V2 Schema 1</th>
      <th>Docker V2 Schema 2 (v2.2)</th>
      <th>OCI image format</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Status</td>
      <td>Deprecated/legacy</td>
      <td>Current Docker default</td>
      <td>Current OCI standard</td>
    </tr>
    <tr>
      <td>Structure</td>
      <td>More complex, v1-compat quirks</td>
      <td>Simple, config + layers, digest-based</td>
      <td>Very similar to Schema 2, plus index/layout/descriptors</td>
    </tr>
    <tr>
      <td>Single-image mediaType</td>
      <td><code>application/vnd.docker.distribution.manifest.v1+json</code></td>
      <td><code>application/vnd.docker.distribution.manifest.v2+json</code></td>
      <td><code>application/vnd.oci.image.manifest.v1+json</code></td>
    </tr>
    <tr>
      <td>Multi-arch list type</td>
      <td>Not defined; no native schema-1 manifest list</td>
      <td><code>application/vnd.docker.distribution.manifest.list.v2+json</code></td>
      <td><code>application/vnd.oci.image.index.v1+json</code></td>
    </tr>
    <tr>
      <td>Layer media types</td>
      <td><code>application/vnd.docker.container.image.rootfs.diff+x-gtar</code></td>
      <td><code>application/vnd.docker.image.rootfs.diff.tar.gzip</code></td>
      <td><code>application/vnd.oci.image.layer.v1.tar+gzip and variants</code></td>
    </tr>
    <tr>
      <td>Tooling support</td>
      <td>Declining, often disabled</td>
      <td>Very widely supported</td>
      <td>Very widely supported</td>
    </tr>
  </tbody>
</table>
