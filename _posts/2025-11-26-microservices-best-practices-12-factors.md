---
layout: post
title: "Microservices Best Practices - The 12 Factors"
date: 2025-11-26 00:00:00-0000
categories: 
---

Just notes for myself.

More information here: [https://12factor.net/](https://12factor.net/).

The 12 Factor App is a set of best practices for building web or SaaS applications.

## Benefits
- This design helps decouple the components of the application, so that each component can be deployed using CD (continuous deployment) and scale up/down seamlessly.
- Maximize portability to different environments.
- Can be applied to a variety of applications because the factors are independent of any programming language or software stack.

## Factors
1. **Codebase**: One codebase tracked in revision control, many deploys
  - Use a version control system like Git.
  - Each app has one code repo and vice versa.
2. **Dependencies**: Explicitly declare nd isolate dependencies
  - Use a package manager like Maven, Pip, NPM to install dependencies.
  - Declare depedencies in your codebase.
3. **Config**: Store config in the environment
  - Don't put secrets, connection strings, endpoints, etc., in your source code.
  - Store those as environment variables.
4. **Backing Services**: Treat baking services as attached resources
  - Databases, caches, queues, and other services are accessed via URLs.
  - Should be easy to swap one implementation for another.
5. **Build, release, run**: Strictly separate build and run stages
  - Build creates a deployment package from the source code.
  - Release combines the deployment with configuration in the runtime environment.
  - Run executes the application.
6. **Processes**: Execute the app as one or more stateless processes
  - Apps run in one or more processes.
  - Each instance of the app gets its data from a separate database service.
7. **Port binding**: Export services via port binding
  - Apps are self-contained and expose a port and protocol internally.
  - Apps are not injected into a separate server like Apache.
8. **Concurrency**: Scale out via the process model
  - Because apps are self-contained and run in separate process, they scale easily by adding instances.
9. **Disposability**: Maximize robustnes with fast startup and graceful shutdown
  - App instances should scale quickly when needed.
  - If an instance is not needed, you should be able to turn it off with no side effects.
10. **Dev/prod parity**: Keep development, staging, and production as similar as possible
  - Container systems like Docker makes this easier.
  - Leverage infrastructure as code to make environments easy to create.
11. **Logs**: Treat logs as event streams
  - Write log messages to standard output and aggregate all logs to a single source.
12. **Admin processes**: Run admin/management tasks as one-off processes
  - Admin tasks should be repeatable processes, not of-off manual tasks.
  - Admin tasks shouldn't be a part of the application.