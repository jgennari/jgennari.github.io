---
title: "Adding Chat Context to Teams: Pt 1"
date: 2023-07-25T20:33:32-04:00
draft: false
tags: ["ai","chatgpt","microsoft","teams"]
author: "Me"
category: ["Tech"]
series: ["Build with Me"]
---

Chatbots are handy, but let's be honest, they can be a bit forgetful. Frustrated with bot conversations that felt like starting from scratch with every message, I decided to roll up my sleeves and tackle the problem. Armed with Power Automate and OpenAI, I started a quest to build a Microsoft Teams chatbot that could actually remember our chat history. Here's a walkthrough of what I learned along the way - the successes, the hurdles, and everything in between. Let's get into it.

![Image 7](../../images/teams-gpt-chatbot-pt1_1690670504505.png)  

## The Goal

So what exactly are we trying to accomplish here? Well, the goal is to build a chatbot that can remember the context of a conversation. For example, if I ask the bot "What's the weather like today?", it should be able to respond with something like "It's sunny and 75 degrees". If I then ask "What about tomorrow?", it should be able to respond with something like "Tomorrow will be sunny and 80 degrees". In other words, the bot should be able to remember the context of the conversation and use that context to provide a more meaningful response. I also would like for the solution to be low or no code.

* The user shouldn't be forced to leave teams
* The bot should accept a general prompt
* It should keep track of multiple users

## The Tools

So how do we do this? Well, we'll need to use a few different tools to make this happen. 

* Microsoft Power Automate - an iPaas (integration platform as a service) that allows you to connect different services together
* OpenAI API - a powerful API that allows you to generate text using AI
* Microsoft Teams - a collaboration platform that allows you to chat with other users

## The Process

So conceptually the idea is that Power Automate will trigger a flow when a user sends a message to the bot. The flow will then send the message to OpenAI, which will generate a response. The response will then be sent back to the user. The flow will also keep track of the conversation history and send that to OpenAI as well. This will allow OpenAI to generate a response that is based on the conversation history.

So here is the conceptual flow:

![Image 8](../../images/teams-gpt-chatbot-pt1_1690671754402.png)  

In part 2 we'll start to glue this solution together in Power Automate and quickly come across some limitations of the Teams/Power Automate integration.