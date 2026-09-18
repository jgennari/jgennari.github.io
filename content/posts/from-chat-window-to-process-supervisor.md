---
title: "From Chat Window to Process Supervisor"
date: 2026-08-15T10:30:00-04:00
lastmod: 2026-09-18T08:48:00-04:00
draft: false
tags: ["ai", "gorchestra", "automation", "tooling"]
author: "Me"
categories: ["Tech"]
series: ["Life Admin"]
description: "Building Gorchestra, and why long-running AI work needs run IDs, persistent results, and a way to tell what actually happened."
---

I've accumulated a pretty ridiculous number of conversations with AI. There's one for the Minecraft server, one for the bird microphone, one for the farm application, one for this blog. And then there's the conversation about the application I built to manage all the other conversations.

That application is called Gorchestra. Yes, I built more software to keep track of the software I was already building. This is apparently how I relax.

When I wrote about [my life running in a markdown file](/posts/my-life-runs-in-a-markdown-file/), the useful part was having somewhere to put context. The assistant could read the journal, understand what had happened, and pick up where it left off. But as I gave agents more work, I started needing answers to much more ordinary questions. Is it still running? Did it finish? Is it waiting for me? Which attempt produced this result?

Those questions turned into most of the interesting work on Gorchestra.

## A conversation can contain a lot of attempts

I keep a Minecraft conversation around because it knows about the server. Within that conversation I might ask for a plugin audit, come back later to restore some warps, and then ask why the website won't load. Same subject, separate jobs.

Gorchestra gives the conversation a session ID and each execution a run ID. That distinction sounds like the sort of thing you can defer until later. You can, but later gets annoying pretty quickly.

Suppose an agent starts work and hands control back to its parent. By the time the parent asks for the result, another request might already be running in that session. Asking for the latest response would answer the wrong question. It needs the result of the particular run it started.

Cancellation has the same problem, with worse consequences. If I ask to stop one job, I want that job stopped. I don't want a delayed cancellation to land on whatever happens to be running next.

So starting work returns a receipt containing both IDs. Following the work means following that run all the way through.

## Closing the window shouldn't lose the job

There are a few ways to watch a run. I can watch output stream in the foreground, start it detached and check later, or use the dashboard. The result needs to survive whichever way I happen to be looking at it.

That meant persisting the full final response, keeping event history, and giving a reconnecting client a way to catch up. A live stream is useful while I'm watching. If my connection drops, I still need the missing part of the story.

It also meant accounting for the awkward moment when the service has accepted a request but hasn't started the agent yet. Restarting the service in that interval shouldn't quietly discard the work. And retrying a submission shouldn't accidentally launch the same job twice.

None of this makes the model smarter. It makes the system around it something I can leave alone for a while.

## Agents get to use it too

The next step was giving agents a CLI for the same operations. They can discover available commands, start a job, wait for its exact run, and retrieve the report. They can also tell when a run needs attention instead of waiting indefinitely for it to finish.

Once that existed, delegation became much easier to follow. A parent session can start a child for a specific piece of work. The relationship gets stored, along with the run that created it. The dashboard can show the children underneath the parent, and I can see where the work went.

There are limits on how deep that tree can get and how many children can be active. Giving every agent the ability to create more agents seemed like a good place to have a limit.

The practical advantage is that a long conversation doesn't have to carry every detail of every task. A child can concentrate on a bounded job and return a result, while the parent keeps track of what I actually asked for.

## The familiar part

I've [written before about spending time on your tooling](/posts/on-troubleshooting/). This project feels like a continuation of that habit. Better tools let me ask better questions when something breaks.

With an agent, a confident final paragraph can make a task feel finished. I still need to know whether the build ran, whether the deployment happened, or whether it stopped after editing a file. Keeping the run and its output gives me somewhere to look when those things don't line up.

I still spend plenty of time talking to the models. But now I can leave a job running, work on something else, and come back to a specific result. For the collection of projects I've managed to give myself, that's been worth building another application.
