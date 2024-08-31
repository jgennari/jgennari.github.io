---
title: "On Troubleshooting"
date: 2024-08-23T18:57:38-04:00
draft: false
tags: ["philosophy","programming"]
author: "Me"
categories: ["Tech"]
---

As a long time contributor to StackOverflow, the quality of posts are wide ranging. In the hay-day, a contributor could rack up tons of points by pointing low-effort posters in the right direction with a single line of code. Now I'm sure the majority of those questions could be (and are) answered by AI, which was trained on my answers. But I think troubleshooting is the [hallmark](https://www.etymonline.com/word/hallmark) of a great engineer. Over time, you learn to hone troubleshooting skills and you can often tell a lot about an engineering by the tooling they surround themselves with.

An electrical engineer with a quality multimeter on their desk is clearly outclassed by one with a oscilloscope, and further by one with a logic analyzer, and so on and so forth. The same for a software engineer. The number of engineers I've worked with who didn't know understand the basics of a software debugger is mind blowing. My advice is to spend almost as much time as you spend writing code - on your tooling. Being able to quickly troubleshoot the problem, research information and revert your changes will serve you greatly.

Similarly, you need to hone your mind. Some troubleshooting session can last hours, days or even weeks. A bug can creep into a project and consume your every thought until you fix it. Even at the age of 42, I still find myself doubting if I can figure something out, questioning why it's taken so long, or in the case of bugs that I've faced before, wondering why I'm facing them again. Here are some helpful reminders:

* Bugs are a fact of life, take a deep breath, you'll solve this one.
* If your eyes and head hurt, step away from the keyboard. Take a walk and come back to it.
* If the walk didn't help, sleep on it.
* Branch your code if you think you're headed for a refactor.
* Sometimes updating dependancies can solve the issue, sometimes it creates more.
* If you're basing your implementation off of some reference, re-read the reference. You probably missed something.