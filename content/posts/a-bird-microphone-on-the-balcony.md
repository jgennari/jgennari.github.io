---
title: "A Bird Microphone on the Balcony"
date: 2026-08-23T09:15:00-04:00
lastmod: 2026-09-18T08:48:00-04:00
draft: false
tags: ["birdnet", "ai", "homelab", "maker"]
author: "Me"
categories: ["Tech"]
description: "An old Intel NUC, a balcony microphone, and the troubleshooting involved in figuring out which birds are making all that noise."
---

I have a microphone listening for birds on my balcony. It's connected to an Intel NUC running BirdNET-Go, which processes the audio and keeps track of what it thinks it heard.

This is a fairly predictable project for me. Take something outside, attach a computer to it, and eventually start researching microphones that cost more than the thing I originally plugged in.

The starting hardware was pretty modest: the NUC and a USB lavalier microphone. Enough to get audio into the system and start detecting birds. I used an AI assistant to help work through the configuration, inspect the machine, and figure out which parts were worth improving. That last question turned out to have several answers, depending on how far down the rabbit hole I wanted to go.

## Two models and one uncooperative GPU

The setup runs BirdNET v2.4 and Perch v2 against the same microphone. Having two classifiers gives me another way to look at the audio. They won't necessarily identify the same things, and comparing their results is more interesting than staring at a single confidence number.

Getting Perch running took a detour. The installation completed, but the NUC's older Intel GPU spent about five minutes compiling the model and then failed.

Naturally, the supposedly faster option was the one preventing anything from happening.

We switched to the ONNX CPU backend and checked the actual processing times. Perch was taking roughly 438 milliseconds for a five-second audio window. There were no queued or dropped chunks in that check. The CPU had plenty of room to do the job, so I left it there.

I like this kind of troubleshooting result. There was a concrete failure, a different path through the software, and a measurement showing that the alternative was adequate. I didn't need to buy another computer to listen to birds.

## How sure is sure enough?

A label in the interface doesn't make a detection correct. Wind, background noise, and a mediocre recording can all make this more complicated than it looks.

I kept the Moderate filter, which in this configuration required three confirmations, along with a 0.7 confidence threshold. One inspection showed a Blue-gray Gnatcatcher prediction at 78 percent with five confirmations, and a Blue Jay at 94 percent with four. Both came from Perch; BirdNET hadn't contributed to either detection.

A later Blue Jay prediction reached 73 percent but appeared only once. The filter discarded it.

That was useful to see. Simply exceeding the confidence threshold wasn't enough. The system was also asking for repetition before retaining the detection. And neither number was proof that the bird was actually there; the recording was still something I could go back and listen to.

There's a temptation with any dashboard to assume that a precise number represents a precise answer. A bird classifier reporting 94 percent certainly looks authoritative. I find it more useful as a reason to investigate a clip.

## The microphone rabbit hole

Once the models were working, I started looking at the audio going into them. The lav was convenient, but a small general-purpose microphone isn't necessarily the best way to capture a distant bird over background noise.

We researched replacing the capsule, reusing the USB board, and using a finished microphone with a separate interface. This led to a surprising amount of discussion about plugs, microphone power, and adapters. Two connectors can both be 3.5 mm and still be entirely the wrong combination.

The no-solder option we settled on researching was a Clippy EM272 Mono, a RØDE AI-Micro interface, and a furry windshield. I haven't treated that as an installed upgrade; it's the next hardware option on the list. The existing microphone got the project working, which was a good reason to use it first.

Then I asked about bats.

The current USB microphone records at 48 kHz. Even before considering the capsule itself, that puts its theoretical upper frequency limit around 24 kHz. Much of the ultrasonic audio I'd want for bat detection is beyond that. Downloading another classifier wouldn't make the microphone record it.

So the bat project can wait for suitable hardware. Apparently one balcony can support several unfinished hobbies.

## A useful little project

What I like about this setup is that the output has something to do with the place I live. The NUC is processing whatever the microphone actually picks up outside, including all the inconvenient noise that comes with that.

It's also given me a good reason to learn a little more about audio. Model selection matters, but so do the microphone, its placement, and whether the computer can keep up. Each is a fairly approachable problem on its own.

For now, the old NUC is keeping up. I'm leaving the GPU alone.
