---
layout: post
title: "Web Analytics for GitHub Pages"
date: 2026-02-02 00:00:00-0000
categories: 
---

There's [Google Analytics](https://developers.google.com/analytics). I discarded it, at least for now, as creating an account is a hassle.

There's [Matomo](https://github.com/matomo-org/matomo).

And I found this privacy-friendly tool called [GoatCounter](https://github.com/arp242/goatcounter). You can self-host it, or you can use the free version as long as you do not abuse it, or use the paid version.

The way these web analytics tools work basically, is that you have to embed a "small" piece of Javascript in every page of your website. And any time someone visits the website, the javascript runs (in their browser) and sends information to the web analytics servers, where you can later visualize the metrics. Simple.

In this case, I am using GitHub Pages with Jekyll's Minima theme.

The first thing to figure out is the version, which can be found here: [https://pages.github.com/versions.json](https://pages.github.com/versions.json). I had [this other link](https://pages.github.com/versions/) bookmarked but they removed it apparently.

Then I went to the repo for Minima and I sifted through the files of the right version (`v2.5.1`), and I found the file [`_includes/head.html`](https://github.com/jekyll/minima/blob/v2.5.1/_includes/head.html) which mentions the contiguous `google-analytics.html` file (where GA's script is stored).

The same place (head) should be good enough for GoatCounter as well, because in GoatCounter's page it says:
>  Getting started is pretty easy, just add the following JavaScript **anywhere** on the page
...

Creating an account in [https://www.goatcounter.com/](https://www.goatcounter.com/) is straightforward.

To set it up I created these 2 files:
- [https://github.com/k-candidate/k-candidate.github.io/blob/f3cca3f881d64ffacd8875a7b69904596df68ecd/_includes/goatcounter.html](https://github.com/k-candidate/k-candidate.github.io/blob/f3cca3f881d64ffacd8875a7b69904596df68ecd/_includes/goatcounter.html)
- [https://github.com/k-candidate/k-candidate.github.io/blob/f3cca3f881d64ffacd8875a7b69904596df68ecd/_includes/head.html](https://github.com/k-candidate/k-candidate.github.io/blob/f3cca3f881d64ffacd8875a7b69904596df68ecd/_includes/head.html)

And now I can have an idea of how many people are visiting the blog.