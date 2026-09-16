---
layout: post
title: "Blog Subscriptions"
date: 2026-09-13 00:00:00-0000
categories: 
---

## What and Why

In the previous post [https://k-candidate.github.io/2026/02/02/web-analytics.html](https://k-candidate.github.io/2026/02/02/web-analytics.html), I did set up the privacy-friendly web analytics tool GoatCounter.

I noticed that recently there are a few visits per month. So I decided to give people the option to subscribe so that they get notified whenever I publish a post.

## Choosing the Tool

What a rabbit hole ...

The issue is that all the tools out there are a hassle in some way or another. I do not want to name names. Just look them up, see how they work, who they charge, and you'll understand the incentives.

But I found a tool made by somebody from down under: [Feedrabbit](https://feedrabbit.com/). This is an independent utility: I have no affiliation with them.

:heavy_check_mark: It is reader-focused, not publisher-focused. The reader is in control. The publisher collects zero PII.

:heavy_check_mark: The publisher does not get to see any email addresses.

:heavy_check_mark: Zero maintenance for the publisher. Set it and forget it.

:heavy_check_mark: The subscriber never gets to see a dashboard or a configuration screen.

:heavy_check_mark: The free tier covers my use case: I do not need anything fancy, and I do not need your email.

## Architecture

It's pretty simple. 

But first, you gotta know that my gh pages jekyll blog has a feed: [https://k-candidate.github.io/feed.xml](https://k-candidate.github.io/feed.xml).

The flow is simple:
1. I write a post
2. Jekyll puts it in `feed.xml`
3. FeedRabbit sends the notification to subscribers
4. The reader clicks "Read more" and they land on the blog post

## Implementation

First I went to [https://pages.github.com/versions.json](https://pages.github.com/versions.json) to find the versions I am working with: `2.5.1` for `minima`.

Here's the plugin I need: [https://github.com/jekyll/minima/blob/v2.5.1/_config.yml#L46](https://github.com/jekyll/minima/blob/v2.5.1/_config.yml#L46).

So I went back to that versions page and I see that the version for `jekyll-feed` is `0.17.0`.

I went to [https://github.com/jekyll/jekyll-feed/tree/v0.17.0](https://github.com/jekyll/jekyll-feed/tree/v0.17.0) and from the whole thing, I needed just this snippet in `_config.yml` which is in [this commit](https://github.com/k-candidate/k-candidate.github.io/commit/be78c7718a2157be8abc9c8e8e688ee86a7d2457):

```yaml
feed:
  path: feed.xml
  excerpt_only: true
```

The `path` part I already mentioned in the Architecture section.

The `excerpt_only` is because I do not want the xml feed to contain the whole post: too big and can break if there's images etc. So only the first paragraph shows in the feed, which is what the subscriber will get. Wanna see the rest? Go to the blog.

Now the next part is to add a button at the bottom of each post to allow the reader to click it and subscribe. For that I went to [https://github.com/jekyll/minima/blob/v2.5.1/_layouts/post.html](https://github.com/jekyll/minima/blob/v2.5.1/_layouts/post.html). And basically I added a button to redirect to Feedrabbit's page. See [this commit](https://github.com/k-candidate/k-candidate.github.io/commit/7c8c5c95d8beb276dd02ced47aa020665297ec69).

```html
  <!-- ==================================================== -->
  <!-- FeedRabbit Redirect                                  -->
  <!-- ==================================================== -->
  <div class="subscribe-box" style="margin: 40px 0 20px 0; padding: 24px; background-color: var(--code-background-color, #fdfdfd); border: 1px solid var(--border-color-light, #e8e8e8); border-radius: 4px; text-align: center;">
    <h3 style="margin-top: 0; margin-bottom: 8px; color: var(--text-color, #111);">Privacy-First Subscription</h3>
    <p style="font-size: 15px; color: var(--text-color, #666); margin-bottom: 20px; line-height: 1.6; max-width: 500px; margin-left: auto; margin-right: auto;">
      Receive a notification in your inbox whenever I publish a new post. This is a reader-focused subscription loop built for absolute privacy: you stay in control, and I do not see, track, or collect your email address.
    </p>

    <a href="https://feedrabbit.com/signup?return_url=%2Fsubscriptions%2Fnew%3Furl%3Dhttps%253A%252F%252Fk-candidate.github.io%252Ffeed.xml" 
       target="_blank" 
       style="display: inline-block; padding: 10px 24px; background-color: var(--brand-color, #2a7ae2); color: #fff; border: none; border-radius: 4px; cursor: pointer; font-size: 15px; font-weight: bold; text-decoration: none; transition: opacity 0.2s;">
      Follow via FeedRabbit
    </a>
  </div>
  <!-- ==================================================== -->
```

And voila!

Now I can say: if you'd like to subscribe for free, all you have to do is click the button down in the box below.
