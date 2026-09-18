---
title: "Teaching an AI to Use My 3D Printer"
date: 2026-09-01T18:20:00-04:00
lastmod: 2026-09-18T08:48:00-04:00
draft: false
tags: ["ai", "3d printing", "maker", "automation"]
author: "Me"
categories: ["Tech"]
description: "Letting an AI operate Bambu Studio, from choosing a fidget model to discovering that someone still has to check the build plate."
---

My 3D printer is named McPrintyFace. I feel like that establishes the level of seriousness with which this project began.

I wanted to see how much of the printing workflow I could hand to an AI assistant. Find the model, choose a version, open Bambu Studio, configure the print, and send it to the printer. Computer use gives the assistant access to the actual desktop application, so this could go beyond giving me a list of settings to enter myself.

The test subject was a spiral ball fidget. There are several sizes and link counts, which made it a good little exercise in following a request through to a physical object. It also meant I could keep asking for smaller ones.

## Smaller, and then smaller again

We had a 100 mm project, then moved to a 60 mm, 12-link version. The assistant preserved the original project separately and prepared the smaller one with 0.20 mm layers, three walls, 15 percent infill, and no supports.

That job used green PLA from the AMS and had an estimated print time of four hours and forty minutes, using about 112 grams of filament. Those were the slicer's estimates, which are useful numbers to have before sending a job that will occupy the printer for most of a morning.

Next came the 40 mm version in purple. The download offered different link counts, so the assistant checked which file matched the request instead of assuming that scaling the previous project was the right approach. We went with the 12-link version.

The smaller job came out to about two hours and twenty-six minutes and 40 grams. Same basic print settings, considerably less material. It was ready to go.

Except the assistant couldn't tell whether the plate was empty.

## The camera has to be useful

The printer has a camera. That sounds like it should answer a fairly simple question: is the previous print still sitting there?

In this case the image was too blurry to answer confidently, so the assistant asked me. That was exactly the right place to stop. All the slicing work could be correct and we'd still have a problem if it started printing on top of something.

We also updated the workflow to start the live camera feed before checking the bed. Looking at a camera panel and getting a useful view of the current printer state are separate steps, apparently.

After the check, the purple job was sent and the printer began loading filament and heating the bed. That's what we verified. A successful send doesn't tell me how the finished object will look a couple of hours later.

## Desktop software remains desktop software

The rest of the process had some very normal computer problems. At one point the desktop controls weren't exposed to the session. Later, Bambu Studio's full-screen window was visible but briefly refusing input. There was also a crash-recovery copy of a duplicated project to deal with.

These are all things I could work through myself, but they matter when someone else is operating the application. A visible window doesn't mean the controls are responding. A recovery dialog doesn't mean the original project has been lost.

Keeping the original 100 mm project separate paid off here. The assistant could identify the broken recovery copy and ask about discarding that specific copy while leaving the original alone. Saving a few distinct project files was a lot easier than trying to reconstruct which settings belonged to which attempt.

## Where I fit in

The assistant did the repetitive desktop work: finding the right variant, entering settings, selecting the filament, slicing, and checking the estimate. I supplied preferences like size and color, and answered the physical question it couldn't resolve from the camera.

That division was useful. I didn't have to sit there entering every setting, and it didn't have to guess about the state of a machine sitting in my home.

I've spent plenty of time using AI to change code and configuration. Watching it operate the slicer feels a little different because the result is going to move motors and use real material. The checks become very concrete. Is that the right spool? Is that the right plate? Did it actually start?

There's still a person required to take the fidget off the printer. McPrintyFace has made no progress on that part.
