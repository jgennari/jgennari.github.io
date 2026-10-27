---
title: "Giving Bloops a Visual Brake Cue"
date: 2026-10-26T22:05:08-04:00
draft: false
tags: ["sim-racing", "iracing", "simhub", "tooling"]
author: "Me"
categories: ["Tech"]
series: []
description: "Using Bloops reference telemetry and SimHub to turn my gear display into a visual braking guide, including the bugs that made it stay red."
---

The first version of my visual braking indicator had one small problem: it told me to brake forever.

I'd added coaching colors to the gear numbers on my sim's LED flag displays. Purple approaching a braking point, red for braking, green for a throttle cue. It looked promising until the red stayed on after the corner. Apparently I'd built a very confident driving instructor with exactly one piece of advice.

Getting that right turned into a useful little project with [Bloops](https://bloo.ps/), [SimHub](https://www.simhubdash.com/), and the hardware already sitting on my rig.

## From a sound to a color

Bloops compares live iRacing telemetry with a reference lap from Garage61. Its overlay lets you compare inputs, and its audio cues help you learn braking points. The creator's [introduction](https://www.reddit.com/r/iRacing/comments/1isp06a/bloops_overlay_for_live_comparison_to_garage61/) explains the idea and the optional lift and throttle cues.

I wanted to put some of that information on my existing flag displays. They already show the current gear through SimHub, so changing the color could add a coaching cue without adding another number or graph to read.

The gear itself stays mine. If I'm in third, the display still says third. The coaching color comes from Bloops. That distinction matters, especially once the color starts following reference brake input: it tells me what the reference driver is doing, rather than confirming what my own foot just did.

With Milo, my assistant, I added conditional layers to the SimHub RGB Matrix profile. Each coaching layer uses a copy of the gear display with its own color. The normal gear remains underneath, and flags and spotter information stay above the coaching layers.

That last part was deliberate. A lesson about braking shouldn't cover up a flag or information about a car alongside me.

## The first stuck-red bug

The installed Bloops plugin exposes properties with names like `BrakeBloopActive`. I initially treated those as booleans. The name makes that a fairly tempting assumption.

In the version on my machine, they're event counters. A cue increments the number. It doesn't turn the property on and then back off.

So a condition equivalent to “is this nonzero?” becomes true after the first event and stays true. The display was doing exactly what we'd asked. We'd asked the wrong question.

For the short approach and throttle cues, we changed the logic to detect an increase in the counter and show a 300-millisecond pulse. Starting up with an existing counter value doesn't trigger a cue. Resets and reconnects establish a new baseline.

That solved the event behavior, but braking deserved a different treatment.

## Where braking starts is only part of the lesson

A brief red flash can tell me when to start braking. It can't tell me how long the reference driver keeps braking, or when that input fades away.

I wanted the red gear to hold through the reference braking zone. We switched that layer to `BloopsPlugin.ReferenceBrake`, a normalized input from zero to one, and kept it active while the reference was braking.

Then I tested it. Red still wasn't releasing correctly.

This time, the reference brake value was about `0.002289`, or 0.23%, while reference throttle was at 100%. Our condition was simply greater than zero, so a tiny residual brake value still counted as braking.

We added a release threshold instead of requiring a perfect zero. That version worked well in my driving test. It also exposed a smaller usability problem: full red through very light trail braking was hard to interpret.

## Giving trail braking its own color

The latest profile splits the reference brake input into three ranges:

| Reference brake input | Gear display |
| --- | --- |
| 10% or more | Red |
| Above 0.5%, below 10% | Light pink |
| 0.5% or less | Brake color clears |

The idea is that red marks the stronger part of braking, then pink marks the lighter release into the corner. Clearing the brake color lets the other display layers show through again.

Those are my current display thresholds, not a prescription for how much brake to use. Ten percent is a starting point for making the phases visually distinct. The pink/red version is installed and checked in SimHub; I still need to judge the contrast and transitions while driving.

## A frozen reference shouldn't become permanent advice

There's another wrinkle: the plugin can retain its last reference values when updates stop. A positive brake reading by itself doesn't establish that the reference is still live.

Our expressions watch for changes across several reference properties and clear the brake cue after 1.5 seconds without a change. Missing or invalid data also clears it, and an evaluation gap causes the state to rebaseline.

That's a practical freshness check, not a dedicated connection-status signal. It can clear a cue if every watched value genuinely stays identical long enough. I'd rather have the coaching color disappear than keep showing an old instruction indefinitely.

I'm not claiming a lap-time improvement from any of this yet. What I have is a working way to put reference braking information on a display I already use, with one more refinement ready to test.

And I've learned to be suspicious of a property called `Active`. Sometimes it means “this happened once,” which is a surprisingly different instruction when you're heading toward a corner.
