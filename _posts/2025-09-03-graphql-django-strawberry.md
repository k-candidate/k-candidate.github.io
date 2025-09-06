---
layout: post
title: "GraphQL using Django and Strawberry"
date: 2025-09-03 00:00:00-0000
categories: 
---

![GraphQL Django Strawberry logos]({{ site.baseurl }}/assets/images/graphql-django-strawberry-logos.png){:style="display:block; margin-left:auto; margin-right:auto; width:50.00%"}

## Starting with Django

We will set up a customer database using Django and Strawberry to play around with GraphQL.

We will give the “Customer” a “username”, “name”, “signup_date”, and “total_purchases” attributes.

```
mkdir graphql-django-strawberry
codium graphql-django-strawberry
uv python pin 3.13
uv init
uv add django
uv sync
source .venv/bin/activate
```

We create a project which is basically a parent of the app:  
`django-admin startproject strawberry_django_test`

It creates a directory with the project name and with this content: 

![Django project files]({{ site.baseurl }}/assets/images/graphql-01.png){:style="display:block; margin-left:auto; margin-right:auto; width:100.00%"}

At this point we can already run the server thanks to the `manage.py` file we see in that screenshot.

But first, let’s create our app inside our project:  
```
cd strawberry_django_test/
python manage.py startapp customer
```

This has created more files in our directory:

![Django app files]({{ site.baseurl }}/assets/images/graphql-02.png){:style="display:block; margin-left:auto; margin-right:auto; width:100.00%"}

We run the server:  
`python manage.py runserver`

![Django server is up]({{ site.baseurl }}/assets/images/graphql-03.png){:style="display:block; margin-left:auto; margin-right:auto; width:100.00%"}

We define our customer model in `strawberry_django_test/customer/models.py`:
```
from django.db import models

class Customer(models.Model):
username = models.CharField(max_length=100)
name = models.CharField(max_length=100)
signup_date = models.DateField()
total_purchases = models.IntegerField()
```

We add the customer app to the `INSTALED_APPS` list in  `strawberry_django_test/strawberry_django_test/settings.py`

Now we create and apply the migrations.  
What are the migrations? From [https://www.geeksforgeeks.org/python/django-basic-app-model-makemigrations-and-migrate/](https://www.geeksforgeeks.org/python/django-basic-app-model-makemigrations-and-migrate/):
> Migrations are files that store instructions about how to modify the database schema. These files help ensure that the database is in sync with the models defined in your Django project. Whenever you make changes to your models—such as adding, modifying, or deleting fields—Django uses migrations to apply these changes to the database.  
Two main commands related to migrations in Django:  
- makemigrations: Creates migration files based on changes made to your models.
- migrate: Applies the generated migration files to the database.

```
python manage.py makemigrations
python manage.py migrate
```

## Adding Strawberry to the mix

Let’s start by installing strawberry: [https://github.com/strawberry-graphql/strawberry-django](https://github.com/strawberry-graphql/strawberry-django)  
`uv add strawberry-graphql-django`

Now we need to add `strawberry_django` to the `INSTALLED_APPS` in `settings.py`, as per [https://strawberry.rocks/docs/integrations/django](https://strawberry.rocks/docs/integrations/django).

Next, we create `strawberry_django_test/customer/schema.py` and we fill it with content similar to [https://strawberry.rocks/docs/integrations/django#solution-3-use-strawberry_django-recommended](https://strawberry.rocks/docs/integrations/django#solution-3-use-strawberry_django-recommended)  
What’s happening here?  
- We convert our Customer model over to a Strawberry type, mapping the model fields to GraphQL fields, with the `@strawberry_django.type` decorator.
- `auto` is a utility provided by strawberry to automatically infer the field types, ensuring consistency between the Django model and the GraphQL schema. See [https://strawberry.rocks/api-reference/strawberry.auto](https://strawberry.rocks/api-reference/strawberry.auto). We can use it directly in our case as `auto` instead of `strawberry.auto` because we are importing it directly: `from strawberry import auto`.
- The `Query` class defines the root query type for our GraphQL API. The Query type is used to define which queries clients can run against our data. In this case, it only has a field `customers` which when queried would return a list of `CustomerType` objects. Since we have mapped `CustomerType` (strawberry) to the `Customer` model (django), querying customers would automatically query all `Customer` objects from the database.

Now we create the endpoint by making the file `strawberry_django_test/customer/urls.py`, like here [https://strawberry.rocks/docs/integrations/django#django](https://strawberry.rocks/docs/integrations/django#django) 

Next we point the project's urls to the app’s urls we just made by modifying `strawberry_django_test/strawberry_django_test/urls.py`. 


## Mutations
[https://strawberry.rocks/docs/django/guide/mutations](https://strawberry.rocks/docs/django/guide/mutations)  
As opposed to queries, mutations in GraphQL represent operations that modify server-side data and/or cause side effects on the server. Strawberry handles input by allowing us to define input types, which specify the structure of the data that can be sent to our GraphQL mutations. Input types in Strawberry are created using the `@strawberry_django.input` decorator for Django models or `@strawberry.input` for custom input types. In our customer application, we’ll add a mutation to enable adding new customers.

In `schema.py`, we define `CustomerInput`. I used the `@strawberry_django.input` decorator because I am tying it to the Django model. I could use `@strawberry.input` if I wanted it standalone and I would have to specify the input types, e.g. `str`.

Also, in `schema.py`, we define the mutation which will accept an argument of the input and use the provided data to perform the action, e.g. creating a new customer in the database.

We do something similar for `CustomerUpdateInput`.

In the Mutation we have to add a function for updating a customer, and another one for deleting.

We end by adding the mutation and query to the `strawberry.Schema`.

## Testing what we have
[https://strawberry.rocks/docs/django#using-the-api](https://strawberry.rocks/docs/django#using-the-api)  
We run `python manage.py runserver` and go to `http://localhost/8000/graphql`. We’re greeted with the playground: 

![GraphQL Playground]({{ site.baseurl }}/assets/images/graphql-04.png){:style="display:block; margin-left:auto; margin-right:auto; width:100.00%"}

I have disabled csrf, given that this is for a quick local test. We can see that in `strawberry_django_test/customer/urls.py`.

This will be our first query:
```
mutation CREATE_CUSTOMERS {
  createCustomer(data: {
    username: "bumblebee",
    name: "John Doe",
    signupDate: "2020-01-30",
    totalPurchases: 11
  }) {
    id
    username
  }
}
```

![GraphQL Playground]({{ site.baseurl }}/assets/images/graphql-05.png){:style="display:block; margin-left:auto; margin-right:auto; width:100.00%"}

Let’s explain everything in that query:  
- Mutation keyword and operation name
  - `mutation`: This keyword indicates the operation will modify data in the backend (for example, create, update, or delete).
  - `CREATE_CUSTOMERS`:  This is the operation name. It identifies this query in client logs or debugging but does not interact with the schema. Its presence is optional.
- Mutation Field
  - `createCustomer`: This is the mutation field exposed by the GraphQL API. It matches a resolver function on the backend, typically defined as a method in the Mutation class. In our Mutation class, we defined a field named “create_customer”. By default, Strawberry exposes this as the GraphQL mutation “createCustomer”. The conversion follows a typical Python-to-GraphQL convention: underscores in Python become camelCase in GraphQL.
- Arguments and Input Object
  - `data: {...}`: The argument data is an input object passed to the mutation. It contains all the parameters the mutation needs:
    - notice that all parameters are strings between quotes, except for one which is not because it is an integer (as we defined it in the Django model)
- Selection set
  - This section specifies which fields of the newly created customer should be retirned in the response


This query returns the data for all customers, which is just "John Doe" because he is the only one we have created so far:
```
query GET_CUSTOMERS {
  customers {
    id
    username
    name
    signupDate
    totalPurchases
  }
}
```

This query changes the username for "John Doe":
```
mutation UPDATE_CUSTOMER {
  updateCustomer(customerId:1, data: {
    username: "yellowleggedhornet"
  }){
    id
    name
    username
  }
}
```

This query deletes John Doe from our database:
```
mutation DELETE_CUSTOMER {
  deleteCustomer(customerId: 1)
}
```