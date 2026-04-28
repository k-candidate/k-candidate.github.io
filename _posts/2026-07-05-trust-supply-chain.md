---
layout: post
title: "Supply Chain Security and Trust"
date: 2026-07-05 00:00:00-0000
categories: 
---

A brief warning, before you continue.

What follows is not dangerous in the usual sense. It won’t harm you, exactly. But it has a way of lingering, quietly, persistently, long after you’ve finished reading.

Some people report a subtle shift. Thoughts that loop. Questions that don’t quite resolve. The uncomfortable sense that something, somewhere, no longer fits the way it used to.

It is strongly advised that you do not proceed if you value undisturbed sleep, stable certainties, or the comforting assumption that reality is as straightforward as it appears.

If, however, you feel that pull, the small, insistent curiosity that says “just a little further”, then go on.

Just don’t expect to put it down again once it starts.

![red vs blue pill]({{ site.baseurl }}/assets/images/red_and_blue_pill.jpg){:style="display:block; margin-left:auto; margin-right:auto; width:66.67%"}

Consider something simple.

You buy a brand new laptop. Sealed, pristine, straight from the manufacturer. You trust it.

Why?

Because it came directly from the source? Then consider the possibility of a malicious insider. 

Because of Secure Boot? As if that mechanism itself couldn’t be subverted. 

Because the supply chain is controlled? As if hardware can’t be swapped, modified, or intercepted somewhere between factory and doorstep.

At which exact point did you decide it was safe?

Now consider downloading a program from a website you “trust.”

You verify the hash. Good practice.

But if someone can tamper with the executable in transit, what stops them from tampering with the hash displayed right next to it? Why does one string of characters feel more trustworthy than the other?

Or take something more mundane.

You download a browser. Say, Firefox. It comes with a set of trusted root certificates. Authorities you are told to rely on.

But how did you obtain the browser in the first place?

You needed a trusted browser… to download a trusted browser.

Somewhere, the chain had to begin. Where was that point?

You run your Python code. You trust the interpreter. Because it’s open source? Because people you respect built it? Because “someone would have noticed”?

History suggests otherwise.

Complex systems can hide flaws for years. Entire industries exist to quietly discover and trade those flaws. If you possessed a powerful vulnerability that no one else seemed to know about, would you disclose it… or keep it?

What if the compiler that builds your code is compromised?

What about the compiler that built that compiler?

At what level does verification actually mean anything?

What if the kernel is compromised?

What if the hardware is?

What if the very assumptions you rely on to verify everything else are the first things that were quietly replaced?

At some point, the recursion stops, not because you reached certainty, but because you ran out of places to stand.

As I said in [https://k-candidate.github.io/2024/11/23/real-world-cryptography-book-takeaways.html](https://k-candidate.github.io/2024/11/23/real-world-cryptography-book-takeaways.html): 
> In the real world, software runs on hardware. Both have supply chains. At some point, you have no other choice but to trust or assume security. Hence the importance of risk management, and defense in depth.

You don’t prove trust.  
You decide where to stop questioning.  
Hopefully, you make that decision consciously.

Some will object: “_I’ll make local copies and self-host everything in internal repositories and registries. I’ll control the entire stack._”

But if a tool is already compromised when you obtain it, what exactly have you secured by hosting it yourself?  
You’ve just moved the problem closer.

“_I’ll scan it_”, they might say.

With what? Another tool?

And how far down does that go before you’re right back where you started?

This assumption of trusting the scanner reminds me of August 2021: I found a zero-day in Sophos. The flaw let a macOS endpoint appear healthy and protected in Sophos Central (the portal used to manage Sophos endpoints on laptops and servers) when in reality it was not. In practice, that meant someone could do anything they wanted on the machine while the admins saw nothing unusual.

I disclosed the find responsibly by submitting a detailed report via Bugcrowd where Sophos had a bug bounty program. Sophos responded. They acknowledged the vulnerability and classified it as a duplicate because someone else had reported the same before me. But still they awarded me with some swag as a thank-you for the report and the suggested mitigations.

I will conclude with an excerpt from Ken Thompson's 1984 Turing Award (equivalent for the Nobel Prize but for computer science) Lecture.  
It was called "Reflections on Trusting Trust".  
You can find it in the ACM website [https://dl.acm.org/doi/epdf/10.1145/358198.358210](https://dl.acm.org/doi/epdf/10.1145/358198.358210):
> The moral is obvious. You can't trust code that you did not totally create yourself. (Especially code from companies that employ people like me.) No amount of source-level verification or scrutiny will protect you [...]

So here is the uncomfortable question you’re left with: not whether your system is secure, but where, exactly, you chose to stop asking.