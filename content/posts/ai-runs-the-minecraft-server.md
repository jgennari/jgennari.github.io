---
title: "AI Runs the Minecraft Server"
date: 2026-09-18T08:00:00-04:00
lastmod: 2026-09-18T08:48:00-04:00
draft: false
tags: ["minecraft", "ai", "homelab", "family", "gorchestra"]
author: "Me"
categories: ["Tech"]
description: "AI does most of the administration for our Monkey Island Minecraft server. The plugin migrations have given us plenty to work through."
---

Our Minecraft server is called Monkey Island. It has a website now, [monkeyisland.fyi](https://monkeyisland.fyi), because of course a family Minecraft server needs a website.

It also has an AI doing most of the administration. I ask for changes, question the results, and decide what we actually want. The agent inspects the server, researches plugins, changes configuration, reads the logs, and works through the fixes. It keeps the project context in Gorchestra so we can come back to it without starting over every time.

I want to be clear about the division of labor here, because it would be pretty misleading to write a post about all the server work I did. I mostly had the conversation. The AI did most of the server work.

That has been useful. It has also produced a few very good examples of why I keep asking follow-up questions.

## Can we upgrade yet?

We're running Paper with a collection of plugins for permissions, building tools, protection, the web map, and client compatibility. Updating the server means figuring out what happens to that collection.

I asked the agent to audit upgrade readiness. It checked the installed versions, researched releases, and identified the plugins that might hold us back. That kind of inventory is exactly the work I'm happy to delegate. There are a lot of release pages to read before changing one server.

The first answer wasn't the final answer. CoreProtect initially looked like a blocker, but a follow-up found a distinction between the community and paid editions that changed the available options. The agent had missed it.

Then we hit a more concrete problem with squaremap. The newer jar was built for a newer server API and wouldn't load on the server we were still running. Paper rejected it with an unsupported API version error.

We put a compatible squaremap build in place, checked that it loaded, and verified that the map responded. The full server upgrade remained under evaluation.

This was a useful correction to the idea that we could update the plugins first and the server later. Some of those updates have to move together. A compatibility table is a starting point; the running server gets a vote.

## Where did the warps go?

Removing EssentialsX gave us another little migration to work through. It's a broad plugin, and once it was gone, the convenience commands it had supplied needed attention too.

The agent installed SimpleWarps and recreated five saved destinations using the old coordinates. It also configured the permissions and checked persistence. The world data wasn't the problem. The way people moved around that world was.

I also asked what had happened to new-player spawn. That turned out to be a good question with a reassuring answer. The spawn settings we'd been looking at belonged to a separate EssentialsX module that hadn't been installed. They had been sitting in configuration without doing anything. The server had been using the normal world spawn and bed behavior all along.

That's the sort of detail I like having an agent trace. Read the actual installation, work out which configuration is active, and explain what changes for the people using it. A setting existing in a file isn't enough.

## Let them fly

Permissions needed another pass. I asked whether everyone could change game mode, weather, and time, and whether they could fly. The answer was no: the access hadn't been set up that way, and there wasn't a fly command installed.

The agent added a small flight plugin and granted the intended commands through LuckPerms. It kept changing someone else's flight state and setting warps restricted to the operator, then verified the permissions with an export.

This part still needed a decision from me about how we wanted to play. The agent could implement a permissions policy, but it couldn't infer all our preferences from the fact that this was a Minecraft server. I wanted to give the players those controls. Once that was clear, it could do the fiddly part.

## Backups are part of the work

The server normally sleeps when it isn't being used, and the maintenance workflow includes verified archives. The plugin changes had a pre-change snapshot and a fresh archive afterward, with the world returned to its usual stopped state.

I care about that more than I care about immediately running the newest version. There are builds in this world that people spent time on. Getting an upgrade slightly earlier doesn't compensate for losing them.

The AI helps with the repetitive checks, but I still want the evidence in the result: what changed, whether the plugins loaded, whether the map worked, and where the backup fits into the sequence. A clean startup is useful. So is noticing that the warp commands disappeared.

For me, this is one of the better uses of an agent. I can ask for something in the terms I care about, like letting everyone fly or preserving the old destinations, and it can work through the server details. When it gets something wrong, we have the logs and the saved state to work from.

Monkey Island now has its warps back, the players have their flying permissions, and the bigger upgrade can wait until the plugin situation makes sense. That's a pretty productive conversation about a game.
