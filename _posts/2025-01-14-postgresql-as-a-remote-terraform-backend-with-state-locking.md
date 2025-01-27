---
layout: post
title: "PostgreSQL as a Remote Terraform Backend with State Locking"
date: 2025-01-14 00:00:00-0000
categories: 
---
Today we will set up a remote Terraform backend with state storage and state locking.

![PostgreSQL as a Terraform backend]({{ site.baseurl }}/assets/images/pg-backend.png){:style="display:block; margin-left:auto; margin-right:auto"}

## 1. What is a Terraform backend? What is a state? What is a lock?
Terraform persists the state of data to keep track of the resources it manages.

By default, it uses a backend called `local` which stores state as a local file on disk. That’s why you see the `tfstate` file when you run the apply locally.

Using the `local` backend is not sustainable, because you can lose that directory, or because you might want to collaborate with other people. It’s not practical to share the state every time someone makes a change.

Using a state that is stored remotely allows multiple people to access the state data and work together on those infrastructure resources.

As you can imagine, an issue might arise in this scenario: what if someone is running an apply, and someone else is trying to apply a change on the same component? We would have conflicts and inconsistencies.  
Hence, we need to have a `lock` that is also stored remotely, that would allow one entity at a time to make changes on a component.  
More information on locking here: [https://developer.hashicorp.com/terraform/language/state/locking](https://developer.hashicorp.com/terraform/language/state/locking).

## 2. Choosing a Backend
If I were on AWS, I’d use S3 for storing the state, and DynamoDB for state locking and consistency checking.

But we’re making a self-hosted homelab here.

We want a backend that fulfills both requirements: storing the state, and state locking.

As per the documentation, [https://developer.hashicorp.com/terraform/language/backend](https://developer.hashicorp.com/terraform/language/backend), we have multiple options.  
We’re choosing PostgreSQL.

## 3. Setting up the PostgreSQL backend
I have created this component [https://github.com/k-candidate/tf-pg-backend](https://github.com/k-candidate/tf-pg-backend) using the Terraform module I had made previously ([https://github.com/k-candidate/tf-module-kvm-vm](https://github.com/k-candidate/tf-module-kvm-vm)).
It does the following:
- Terraform provisions the VM.
- Terraform triggers the user data (cloud-init) to install PostgreSQL.
- Terraform launches Ansible.
- Ansible creates the database and prepares it for usage.

## 4. How to use
We explicitly add a backend block to a component:
{% highlight terraform %}
terraform {
    backend "pg" {}
}
{% endhighlight %}
And then use environment variables (more secure) to provide the credentials and the ip/fqdn.  
We can use just one variable with all the information:
{% highlight bash %}
export PG_CONN_STR=postgres://<user>:<pass>@<fqdn_or_ip>/<db_name>
{% endhighlight %}
Terraform understands the `libpq` environment variables for PostgreSQL. For more information, see [https://www.postgresql.org/docs/current/libpq-envars.html](https://www.postgresql.org/docs/current/libpq-envars.html).

And then as usual, we use `terraform apply`.

I have tested the scenario of 2 people making changes at the same time, and this works like a charm:  whoever “takes the lock” is in control. The other person is unable to make changes until the lock is released.

## 5. What’s in that DB?
I am curious to see what’s in that DB.  
We deploy some dummy component just to test, like this one for example: [https://github.com/k-candidate/tf-vm-test](https://github.com/k-candidate/tf-vm-test).

We connect to our database using psql or PgAdmin:
{% highlight bash %}
psql -h <fqdn_or_ip> -U <user> <db_name>
{% endhighlight %}
First let’s see the schema:
{% highlight sql %}
\dn+
{% endhighlight %}
Or via:
{% highlight sql %}
SELECT schema_name FROM information_schema.schemata;
{% endhighlight %}
This shows us that Terraform created a new schema instead of using the default schema named `public`.  

Now let’s see the tables:
{% highlight sql %}
\dt terraform_remote_state.*
{% endhighlight %}
To view the table structure:
{% highlight sql %}
\d terraform_remote_state.states
{% endhighlight %}
Now let’s see what the data looks like:
{% highlight sql %}
SELECT * FROM terraform_remote_state.states;
{% endhighlight %}

## 6. Migrating the already deployed components
When you change a backend's configuration, you must run `terraform init` again to validate and configure the backend before you can perform any plans, applies, or state operations.

When you change backends, Terraform gives you the option to migrate your state to the new backend. This lets you adopt backends without losing any existing state.
It’s as easy as:
{% highlight bash %}
terraform init -migrate-state
{% endhighlight %}

## 7. Conclusion
Now we have the states of the already existing components in the remote PostgreSQL backend, and we are able to directly store the new ones in there as well.  

This is it for now, and I hope you learned something.