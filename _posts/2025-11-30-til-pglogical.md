---
layout: post
title: "TIL - pglogical"
date: 2025-11-30 02:00:00-0000
categories: 
---

[https://github.com/2ndQuadrant/pglogical](https://github.com/2ndQuadrant/pglogical)

`pglogical` is a PostgreSQL extension that implements logical streaming replication using a publish/subscribe model (one provider can feed multiple subscribers), allowing fine-grained data replication between databases rather than copying the entire database cluster at the storage level. It is commonly used for tasks such as online migrations, multi-version replication, high availability, and complex topologies like multi-master or cascading replication where data needs to flow between multiple PostgreSQL instances.​

It extracts data changes from a source (provider/publisher) database and replays them as SQL-level changes on one or more target (subscriber) databases. This is the "logical replication".

It works per database instead of per whole server, so you can choose specific databases, tables, and even rows/columns to replicate, enabling selective and filtered replication.

AWS doc: [https://docs.aws.amazon.com/dms/latest/sbs/chap-manageddatabases.postgresql-rds-postgresql-full-load-pglogical.html](https://docs.aws.amazon.com/dms/latest/sbs/chap-manageddatabases.postgresql-rds-postgresql-full-load-pglogical.html)

GCP doc: [https://cloud.google.com/blog/products/databases/best-practices-for-migrating-postgresql-to-cloud-sql-with-dms](https://cloud.google.com/blog/products/databases/best-practices-for-migrating-postgresql-to-cloud-sql-with-dms)

I took it for a vanilla test ride: migrating a PostgreSQL VM instance to GCP's Cloud SQL for PostgreSQL using Database Migration Service.