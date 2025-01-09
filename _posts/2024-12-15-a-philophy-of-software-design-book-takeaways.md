---
layout: post
title: "A Philosophy of Software Design - Book Takeaways"
date: 2024-12-15 00:00:00-0000
categories: 
---
> The most fundamental problem in computer science is problem decomposition: how to take a complex problem and divide it up into pieces that can be solved independently.

![Book cover for A Philosophy of Software Design]({{ site.baseurl }}/assets/images/a-philosophy-of-software-design-book-cover.jpg){:style="display:block; margin-left:auto; margin-right:auto"}

This book is an easy and pleasant read. Each chapter comes with a conclusion. The last two pages are bullet points of the design principles and the red flags.

### Tactical vs Strategic coding
Are we hacking something quickly (for a POC, or for putting out a fire etc)? That’s tactical.
Or are we building something scalable and sustainable for the long term? That’s strategic.

### Module depth and information leakage
We want deep modules with simple interfaces. 
Take the complexity away from the interface and put it inside the module (in the implementation), so that the users of said module need to only understand the abstraction provided by its interface.

For example, the API of a commonly used feature should not force users to learn about features that are rarely used as that increases the cognitive load. If it doesn’t hide much information, then either it doesn’t have much functionality, or it has a complex interface; either way, the module is shallow.

Avoid unnecessary specialization. General-purpose modules are deeper.

This is efficient: the developer of the module takes a bit of extra pain to reduce the pain of everybody else, the users. It’s seeing development through a “customer service” lens. In reality, the user of the module is a customer of the module’s creator (even if it’s for internal use and there’s no monetary transaction involved).

### Design it twice
“What was I thinking when I did it this way? I could have just done it this other way and it would have been faster or less prone to error or...”.

The design of a system improves with iteration. Design as a skill improves with repetition.

### Comments
The comments should capture information that was in the mind of the designer but couldn’t be represented in the code.

If someone has to read the code in order to use it, then there’s no abstraction.

To avoid the “chore” of writing comments, start by writing them as part of the design process.

### Names
Naming (for variables or function etc) should be precise, consistent, and concise.