---
layout: post
title: "Corrupted Database!"
date: 2025-03-09 00:00:00-0000
categories: 
---

The PostgreSQL database (Terraform backend) got corrupted. Probably due to some improper shutdown.
I still have not made a backup and recovery strategy yet, but fortunately I have everything as code.

Initially, I thought about using `terraform import`. I tried it, however it did not work as expected due to limitations in Terraform’s libvirt provider: it replaces the disk instead of preserving it.

In for a penny, in for a pound! I destroyed everything and built it back up again just to confirm that actually everything is as code and no “glue” pieces were left out. I’m back on track.

As the timeless saying goes: Rome was not built in a day.  
Over a long period of time, hurdles will inevitably pop up while making a sizable environment.  
This underscores the importance of investing time in robust backup and recovery strategies.