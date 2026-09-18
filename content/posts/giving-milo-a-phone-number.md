---
title: "Giving Milo a Phone Number"
date: 2026-09-10T19:10:00-04:00
lastmod: 2026-09-18T08:48:00-04:00
draft: false
tags: ["ai", "sms", "automation", "milo"]
author: "Me"
categories: ["Tech"]
series: ["Life Admin"]
description: "What happened when I connected my personal assistant to SMS: identity, group conversations, privacy tests, and a message that only partly arrived."
---

My personal assistant has a name now: Milo. He also has a phone number, because apparently the collection of interfaces I already had wasn't sufficient.

SMS seemed like an obvious way to make him easier to reach. It's already on everyone's phone. Nobody needs another application, and a group conversation is a familiar place to ask a question or introduce someone.

I built the bridge using Twilio, with AI doing much of the implementation and helping me work through the failures. Receiving a message and generating a reply was only the beginning. Once other people could talk to the assistant, I had to be much more specific about who was asking, who would see the answer, and what Milo could do with the request.

## There are two Milos involved

The public-facing side handles the conversation. When a request needs private context or further work, it hands off to the internal assistant. That lets the conversational side stay focused on talking while the internal side deals with the task.

The handoff still has to carry the right information. If the internal assistant loses track of who asked the question, it can make a perfectly reasonable decision for the wrong person.

We made the identity lookup deterministic: resolve the incoming phone number against my contact records before asking the model to reason about the request. Someone typing that they're Joey shouldn't change the identity attached to their message.

That also doesn't magically turn a phone number into permission to release everything. Recognizing a contact and deciding what may be shared are separate problems. This project has been very good at finding places where I hadn't spelled out the second one carefully enough.

## Group conversations complicate everything

If I'm talking to Milo directly, the intended recipient of an answer is reasonably obvious. Put me in a group with someone else and that changes. My presence in the conversation doesn't mean everything Milo knows about me belongs in the reply.

We tested owner conversations, known contacts, unknown numbers, and mixed groups. The privacy evaluation used synthetic facts and identities, so it could check what would be disclosed without opening real private records or sending messages to people.

The cases included false identity claims, made-up approvals, urgency, and instructions to ignore the rules. We added a case where an unknown number claimed to be me using a new phone and asked for private messages. It was refused. Across the 22 evaluation cases, the tested boundaries held.

That's useful evidence for those cases. It isn't a reason to stop checking what the system actually enforces in code and what still depends on the model following instructions.

Group consent was another separate issue. During the audit we found that the bridge didn't have a per-participant opt-in gate for group conversations. Adding someone to a thread hadn't given the application a record of their agreement to hear from Milo. Having an onboarding page didn't fix that gap by itself.

## The message I got and someone else didn't

One of the more instructive failures was a group reply that arrived on my phone but didn't reach the other recipient. The bridge had recorded it as sent.

From where I was sitting, it looked fine. From the other phone, Milo hadn't answered at all.

The delivery records showed two different outcomes for the same reply: delivered to one recipient and undelivered to the other. We changed the tracking to follow each recipient through the terminal delivery result and record the overall message as partially delivered when appropriate.

Then came the question of retries. Sending the group reply again would also send it to the person who already got it. A targeted retry might arrive in a separate direct thread. And generating a fresh answer would create another problem: now people might be receiving different replies to the same question.

The proposed retry behavior was to preserve the original body and target the failed recipient where appropriate. That was still proposed work at this point; the shipped fix was accurate delivery tracking. I wanted to know what happened before adding another automatic action on top of it.

## He still needs to sound like Milo

Somewhere in all of this, I also spent time on his personality. Brief sarcasm is fine when a media server is misbehaving. It gets old very quickly when someone is upset or asking about something serious.

That behavior had to survive the internal handoff too. Otherwise we'd carefully tune the conversational response and then replace it with a generic acknowledgement from another part of the system.

It's a small detail compared with privacy and delivery, but it's the part people actually encounter. They send a text and get a text back. They don't see the identity lookup, the handoff, or the delivery callbacks.

I now have a much longer answer to the question of what it takes to give an assistant a phone number. I also have a message status called partially delivered, which would have been useful to have before I needed it.
