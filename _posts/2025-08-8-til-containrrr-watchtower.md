---
layout: post
title: "TIL - Containrrr Watchtower"
date: 2025-08-08 00:00:00-0000
categories: 
---

- [https://github.com/containrrr/watchtower](https://github.com/containrrr/watchtower)
- [https://containrrr.dev/watchtower/](https://containrrr.dev/watchtower/)

> With watchtower you can update the running version of your containerized app simply by pushing a new image to the Docker Hub or your own image registry. Watchtower will pull down your new image, gracefully shut down your existing container and restart it with the same options that were used when it was deployed initially.

> Watchtower is intended to be used in homelabs, ..., local dev environments

```
docker run -d \
--name watchtower \
-v /var/run/docker.sock:/var/run/docker.sock \
containrrr/watchtower \
--interval 14400
```

Or via Docker Compose:
```
services:
  watchtower:
    image: containrrr/watchtower
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
    command: --interval 14400
    restart: always
```