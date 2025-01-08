---
layout: post
title: "What is Web Assembly?"
date: 2024-12-11 00:00:00-0000
categories: 
---
Let's quickly explore Web Assembly (Wasm).
All the code can be found in [https://github.com/k-candidate/hello-wasm-world](https://github.com/k-candidate/hello-wasm-world)

### First, what is it?
Imagine a world in which you can write code in Python or Rust or Go and have it run in a web browser (client-side). This became possible in 2019 thanks to Web Assembly. You can write in those languages and others, and then set Wasm as the compilation target.

The browser's engine,V8 for Chromium or Spider Monkey for Firefox, can run your Wasm in the client-side.

It is not meant to replace JavaScript, but instead work alongside it.

### Let's test
Let’s use Python. The first simple thing that comes to mind is to do sum operations, and run the pystone test.

The code can be found here: [https://github.com/k-candidate/hello-wasm-world/blob/main/hello-wasm-world.py](https://github.com/k-candidate/hello-wasm-world/blob/main/hello-wasm-world.py)

Running `python hello-wasm-world.py`:
```
Elapsed time for range sum: 0.001385 seconds
Pystone(1.1) time for 50000 passes = 0.124373
This machine benchmarks at 402016 pystones/second
```

Running `wasmer run hello-wasm-world.wasm`:
```
Elapsed time for range sum: 0.000775 seconds
Pystone(1.1) time for 50000 passes = 0.227372
This machine benchmarks at 219904 pystones/second
```

The sum operation completes quicker using the compiled wasm than the interpreted python script.
However, the pystone test is slower. At this stage, I am not sure why. I'll have to revisit this later.

### Wasm with Docker. But why?
Docker and Wasm are different layers of abstraction. If Docker is a "container for the OS", then Wasm would be a "container for the application". That leads to the conclusion that you can prescind from Docker altogether, theoretically.

However, in the real world, there are more factors at play: orchestration and scaling (there's still no k8s equivalent for Wasm, afaik), developer experience, maturity (the Wasm ecosystem is relatively young), cost of change etc. So, I personally think as of now, if some organization, that is already running microservices, were to use Wasm in the server side, it would do it with Docker.

### How does Docker work with Wasm?
![Wasm and docker]({{ site.baseurl }}/assets/images/wasm-docker.png)

Notice that the `wasm rt` is where the lower level engine like `runc` (or `crun`) would be.

To create the wasm docker image:
```
docker build -t kcandidate/hello-wasm-world:v1 --platform wasi/wasm32 .
```
To use a wasm runtime for docker, follow these instructions: 
[https://docs.docker.com/engine/daemon/alternative-runtimes/](https://docs.docker.com/engine/daemon/alternative-runtimes/). But they are incomplete (as of December 2024).

The daemon configuration file is `/etc/docker/daemon.json`:
```
{
  "features": {
    "containerd-snapshotter": true
  }
}
```

To build the wasmtime binary, you'll need `protobuf-compiler` and `libseccomp-dev` which are not present in the build stage image used in the Docker docs. Alternatively, you can just get the precompiled binary from [https://github.com/containerd/runwasi/releases](https://github.com/containerd/runwasi/releases)
```
docker build --output . - <<EOF
FROM rust:latest as build
RUN apt update && apt install -y protobuf-compiler libseccomp-dev
RUN cargo install \
    --git https://github.com/containerd/runwasi.git \
    --bin containerd-shim-wasmtime-v1 \
    --root /out \
    containerd-shim-wasmtime
FROM scratch
COPY --from=build /out/bin /
EOF
```

To run the wasm docker image:
```
docker run --runtime=io.containerd.wasmtime.v1 --platform=wasi/wasm kcandidate/hello-wasm-world:v1
```

That's it for this quick exploration of Wasm. I hope you learned something.