---
layout: post
title: "Terraform - Factoids and Annoyances"
date: 2026-04-13 00:00:00-0000
categories: 
---

Terraform is great. But 

- The Terraform Template Provider has been deprecated since 2020. But it is still used out there... And you'll find that it is not supported by the new arm Mac (darwin_arm64). Thankfully there's Rosetta. Meaning, you have to use the darwin_**amd64** version of Terraform on your arm Mac.
  - [https://discuss.hashicorp.com/t/template-v2-2-0-does-not-have-a-package-available-mac-m1/35099](https://discuss.hashicorp.com/t/template-v2-2-0-does-not-have-a-package-available-mac-m1/35099)
  - [https://github.com/hashicorp/terraform-provider-template](https://github.com/hashicorp/terraform-provider-template)
  - [https://registry.terraform.io/providers/hashicorp/template/latest/docs](https://registry.terraform.io/providers/hashicorp/template/latest/docs)
- You cannot use variables in `lifecycle` blocks. Requested since July 2020.
  - [https://github.com/hashicorp/terraform/issues/25534](https://github.com/hashicorp/terraform/issues/25534)
- There's no Wasm (Web Assembly) binary format for Terraform.
  - [https://github.com/hashicorp/terraform/issues/32079](https://github.com/hashicorp/terraform/issues/32079)

I probably will be adding more items to the list with time, or whenever I remember other peculiarities that gave me a hard time.