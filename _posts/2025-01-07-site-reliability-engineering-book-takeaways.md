---
layout: post
title: "Site Reliability Engineering: How Google Runs Production Systems - Book Takeaways"
date: 2025-01-07 00:00:00-0000
categories: 
---
> SRE is what happens when you ask a software engineer to design an operations team.

![Google's SRE book]({{ site.baseurl }}/assets/images/sre-book-cover.webp){:style="display:block; margin-left:auto; margin-right:auto; width:33.33%"}

I read Google's "Site Reliability Engineering: How Google Runs Production Systems” during the year-end holidays.

The book includes a lot of principles and practices that we take for granted today.  
It has ~500 pages. There’s no way to sum it up in a 10min read.
However, here are some points that stuck with me:

## A cap on “ops” work
Google places a 50% cap on the aggregate “ops” work for all SREs – tickets, on-call, manual tasks, etc.  
The SRE team should end up with very little operational load and almost entirely engage in development tasks.  
They actually do measure the time spent on each type of work, and then enforce it by shifting some of the operations burden to the development team, or by adding staff.  
This ensures that SREs have the bandwidth to engage in creative, autonomous engineering, while still retaining the wisdom gleaned from the operations side of running a service.

I think this is a winning strategy. It fosters the creation of automatic (self-healing) systems, and it should also result in a higher retention rate of people. No SRE wants to be bored at work doing repetitive ops toil without any bandwidth to automate it.

## Error budget
Having developers and SREs agree on a quarterly error budget based on a service’s SLO is an objective and data driven way to eliminate the tension between the 2 teams. This tension should naturally exist by design because it allows reaching a healthy equilibrium between maintaining the status quo and change. In one word: homeostasis.  

The productivity of developers is measured based on how much code they push. The performance of SREs is evaluated based on the reliability of a service, which means an incentive to push back against change.  

This error budget metric removes the subjectivity in the negotiation between the 2 teams, and replaces that with a collaborative approach because they have a budget to spend together to preserve the common goal: the SLO.

## On call
SRE managers have the responsibility of keeping the on-call workload balanced and sustainable.  
Google says that night shifts have detrimental effects on people’s health, and a multi-site “follow the sun" rotation allows teams to avoid night shifts altogether (assuming that the decision was to go multi-site).  

This makes sense. Building a reliable SRE team is a long term game, not a sprint.

## Data integrity
Data availability is the goal. When designing and implementing a BCDR strategy, one should see it as a recovery system, not a backup system.  
It’s like an insurance policy: backup is just the premium, recovery is the payout.

In simple terms: do the backups, but regularly recover from those backups just to test them and make sure that the process works.

## Postmortems
It behooves an SRE to read postmortems. Especially to get familiar with a new service or environment.

## Conclusion
There are gold nuggets in this book.  
It was interesting to understand the story of how SRE, and how Borg (the predecessor to Kubernetes) came to be.  
You can read it for free at [https://sre.google/sre-book/table-of-contents/](https://sre.google/sre-book/table-of-contents/).

But there’s still an itch I can’t scratch. Why is there a lizard on the cover?  
It’s a Nile **monitor** (Varanus niloticus).  
And why do they call them monitor?  
Because of their habit of standing up on their hind legs, as though they are monitoring their surroundings.

This is it for now, and I hope you learned something.

![Monitor lizard standing on the two hind legs and appearing to monitor]({{ site.baseurl }}/assets/images/monitor-lizard-standing.jpg){:style="display:block; margin-left:auto; margin-right:auto; width:33.33%"}