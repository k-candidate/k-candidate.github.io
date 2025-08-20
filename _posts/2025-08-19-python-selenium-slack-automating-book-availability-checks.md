---
layout: post
title: "Python, Selenium, Slack, and GHA - Automating Book Availability Checks"
date: 2025-08-19 00:00:00-0000
categories: 
---

![Logos of Python, Selenium, Slack, and GHA]({{ site.baseurl }}/assets/images/bookstore-se-py-slack-gha-logos.png){:style="display:block; margin-left:auto; margin-right:auto; width:50.00%"}

## Introduction

There’s a second-hand bookstore nearby, and I have a growing list of books I’d love to read. Since I’m not in a rush to get these titles, I wanted a way to be notified whenever any of them are in stock so I can drop by and pick them up.

However, the bookstore’s website doesn’t offer a notification feature where you can set a book and choose how to get alerted. Until now, I had to manually visit the site and search for each book on my list one by one. Boring.

So, I decided to build my own automated solution to save time and get notified instantly.

## Solution

I am using Python, Selenium, Slack, and Github Actions for this.  
The whole thing can be found in this repo: [https://github.com/k-candidate/selenium-book-search-slack-alerts](https://github.com/k-candidate/selenium-book-search-slack-alerts).

I will probably modify it down the road. Here's the repo at this point in time: [https://github.com/k-candidate/selenium-book-search-slack-alerts/blob/795ee8314aa8290721d1d03f4eb681fb6a190d2f/README.md](https://github.com/k-candidate/selenium-book-search-slack-alerts/blob/795ee8314aa8290721d1d03f4eb681fb6a190d2f/README.md).

There's a readme, and the code is self-explanatory and annotated. So I will just put bullet points of what I did:
- Make the repo, and clone it locally
```
git clone https://github.com/k-candidate/selenium-book-search-slack-alerts.git
codium selenium-book-search-slack-alerts
pyenv local 3.13.1
python -m venv .venv
source .venv/bin/activate
pip install selenium
```
- I need the Driver for Selenium. I am using Chromium, which I have installed via snap (`sudo snap install chromium`). It comes with the driver located at `/snap/bin/chromium.chromedriver`
- While developing the script, I want to use Selenium in headed mode to be able to see the browser and interact with it. I left the option commented in the script to make future maintenance easier.
- Slack
  - [https://api.slack.com/apps](https://api.slack.com/apps)
  - Click “Create New App” > “From Scratch” > Give it a name and choose the workspace > “Create App”
  - Go to “Oauth & Permissions” > “Bot Token Scopes”  “Add an Oauth Scope” > “chat:write” > Click “Install to ${workspace name}” > “Allow” > Save the “Bot User Oauth Token” (`xoxb-…`)
  - Go to slack and create a new channel > In the channel, invite the bot using the slash command: `/invite @AppName`
  - What I have done so far would allow me to send messages using the Slack SDK, which I have used in the past. But I do not want to do that here. I will use webhooks as they’ll need less maintenance.
  - Click on “Incoming Webhooks” > Toggle to “On” > Click on “Reinstall your app” > choose the channel in the dropdown menu > “Allow”
  - Copy the Webhook URL and save it.
- Test locally via 
```
python main.py \
  --book-list "Sherlock Holmes; The snows of Kilimanjaro; Dr. Seuss" \
  --slack-webhook-url "https://hooks.slack.com/your/webhook" \
  --website-url "https://my.local.bookstore"
```
- Make the github action run daily.
- Put all variables in GHA secrets (for privacy).

## Conclusion

It's doing what I want it to do. Here's a screenshot of the final result which is the slack notification:
![Slack notification of books found]({{ site.baseurl }}/assets/images/selenium-books-slack-notification.png){:style="display:block; margin-left:auto; margin-right:auto; width:100.00%"}