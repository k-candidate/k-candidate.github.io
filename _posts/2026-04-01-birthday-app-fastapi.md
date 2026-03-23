---
layout: post
title: "The Birthday App - From FastAPI and SQLAlchemy to GitOps: Building a Kubernetes Delivery Platform with Helm, ArgoCD, Terraform, and Minikube"
date: 2026-04-01 00:00:00-0000
categories: 
---

## Quick Start

### What This System Is

There are 4 repos, each with a separate responsibility:

- `fastapi-app`: [https://github.com/k-candidate/fastapi-app](https://github.com/k-candidate/fastapi-app)  
  The application source code, tests, Docker image build, and release pipeline.  
  See that repo’s README.md for local app details.

- `helm-charts`: [https://github.com/k-candidate/helm-charts](https://github.com/k-candidate/helm-charts)  
  The reusable Helm chart for deploying fastapi-app.  
  See that repo’s README.md and charts/fastapi-app/README.md.

- `gitops-apps`: [https://github.com/k-candidate/gitops-apps](https://github.com/k-candidate/gitops-apps)  
  The Argo CD application definitions and environment-specific deployment values.  
  See that repo’s README.md.

- `tf-minikube`: [https://github.com/k-candidate/tf-minikube](https://github.com/k-candidate/tf-minikube)  
  The cluster/bootstrap repo.  
  It creates Minikube, installs Argo CD, and bootstraps GitOps.
This is the repo you start with.   
  See that repo’s README.md.

### How To Start On A Fresh Laptop

1. Install the prerequisites mentioned in the repo READMEs.
2. Clone `tf-minikube`.
3. Run:
```bash
terraform init
terraform apply -auto-approve
```
4. Terraform will:
  - create the Minikube cluster
  - install Argo CD
  - bootstrap Argo CD to read gitops-apps
5. Argo CD will then:
  - read gitops-apps
  - create the fastapi-app-prereqs app
  - create the fastapi-app app
  - pull the Helm chart from helm-charts
  - deploy the app and its bundled PostgreSQL for the minikube environment

### How To Check It

Use the commands documented in:
- `tf-minikube/README.md`
- `gitops-apps/README.md`

Typical checks are:

```bash
minikube status -p terraform-provider-minikube
kubectl get applications -n argocd
kubectl get pods -n argocd
kubectl get pods -n fastapi-app
```

### How To Access Argo CD

Get the admin password using the command from `tf-minikube/README.md`, then port-forward the Argo CD server and log in.

### How To Test The App

Port-forward the fastapi-app service and call the API with curl, as shown in `gitops-apps/README.md`.

### Where To Change Things

- app code or API behavior: `fastapi-app`
- deployment chart behavior: `helm-charts`
- environment-specific deployment values: `gitops-apps`
- cluster/bootstrap behavior: `tf-minikube`

### How To Tear It Down
From `tf-minikube`:

```bash
terraform destroy -auto-approve
```

## If I were to deploy this into AWS assuming high criticality and usage

![aws diagram]({{ site.baseurl }}/assets/images/fastapi-app-01.png){:style="display:block; margin-left:auto; margin-right:auto; width:100.00%"}

This architecture shows how the current local platform could be evolved into a resilient AWS-based production setup for a high-traffic, business-critical application.

For the repositories and responsibilities, I'd keep the separation we already have:
  - `fastapi-app`  
    application code, tests, Docker image build.
  - `helm-charts`  
    deployable Helm chart.
  - `gitops-apps`  
    environment-specific desired state for Argo CD.
  - `tf-aws`  
    AWS infrastructure and cluster bootstrap.

### Main Request Flow

User traffic would follow this path:

- Route 53 resolves the domain
- CloudFront and WAF protect and route public traffic
- an Application Load Balancer sends traffic into Kubernetes
- an Ingress Controller routes requests to the FastAPI service
- fastapi-app pods handle the request inside EKS

### Deployment Flow

The deployment flow would remain GitOps-based:

- developers push code to GitHub
- GitHub Actions tests the app, builds the image, and pushes it to ECR
- Argo CD watches Git for the desired deployment state
- Argo CD pulls the Helm chart from helm-charts
- Argo CD applies the environment configuration from gitops-apps
- Kubernetes deploys the app into EKS

This keeps CI responsible for building artifacts and GitOps responsible for deciding what runs.

### Application Dependencies

In AWS, the application would rely on managed services:

- Amazon RDS PostgreSQL for the database
- AWS Secrets Manager for secrets such as database credentials

This is the main difference from the Minikube setup, where PostgreSQL was bundled for simplicity.

### Scaling

Because this is a high-usage system, scaling should happen at both the cluster and application levels:
  - Karpenter can scale EKS worker capacity up and down as workload demand changes
  - HPA or KEDA can scale the FastAPI application pods horizontally based on traffic or workload signals

That gives the platform elasticity both for infrastructure capacity and for application replicas.

### Basic Monitoring and Logging

For day-2 operations, I would include in the platform:

- Prometheus for metrics collection
- Grafana for dashboards
- Fluent Bit for log collection
- CloudWatch for centralized logs

That gives enough visibility to monitor application health, cluster behavior, and runtime failures.

### How This Would Be Built

The rollout would look like this:
- Provision AWS infrastructure with Terraform:
  - VPC
  - subnets across multiple Availability Zones
  - ALB
  - EKS
  - RDS
  - supporting IAM and networking
- Install cluster platform components:
  - Argo CD
  - ingress controller
  - karpenter for node scaling
  - HPA or KEDA for workload scaling
  - basic monitoring and logging stack
- Connect the delivery pipeline:
  - GitHub Actions builds and pushes images to ECR
  - Argo CD syncs from gitops-apps
  - Helm charts from helm-charts are used for deployment
- Deploy the application:
  - FastAPI runs in EKS
  - database runs in RDS
  - secrets come from Secrets Manager
