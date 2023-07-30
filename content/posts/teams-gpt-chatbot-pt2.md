---
title: "Adding Chat Context to Teams: Pt 2"
date: 2023-07-29T21:43:07-04:00
draft: false
tags: ["ai","chatgpt","microsoft","teams"]
author: "Me"
category: ["Tech"]
series: ["Build with Me"]
---

## Getting Started

In [Part 1]({{< ref teams-gpt-chatbot-pt1.md>}}) I explained how we were going to use Teams and Power Automate to generate a contextually aware chatbot for your team. We're going to use Teams channel communication to simplify how we "window" communication.

![Image 0](../../images/teams-gpt-chatbot-pt2_1690681544411.png)

That gives us a few nice things out of the box:

* A list of messages that we can easily iterate over
* Multi-user communication
* A clear "beginning" and "end" to a conversation

So I pulled in the "When a new channel message is added" trigger:

![Image 1](../../images/teams-gpt-chatbot-pt2_1690681753287.png)  

To avoid flooding the channel with chatbot responses, I added a condition to only trigger if the message subject is "Chat Bot":

![Image 2](../../images/teams-gpt-chatbot-pt2_1690681942370.png)  

Next thing I do is loop until a boolean variable named `isComplete` is true. This will be set to true when the chatbot response is "done". This also allows us to exit the loop in case of an error. So if you're paying attention, you might notice the first downside of this method: we're going to be "polling" Teams for new messages. There's a few downsides to this: 1. we're going to be utilizing a lot of Flow runs (you probably won't max out) and 2. there's going to be a delay. Ideally I'd like for this to be a webhook, but I we'll save that for another day.

![Image 4](../../images/teams-gpt-chatbot-pt2_1690682645721.png)  

So there's a lot to unpack here, and our first real detour. So one big downside of the Teams Power Automate connector is that it doesn't support querying replies natively. Luckily the Microsoft Graph *does* have that functionaility. And the `HTTP with Azure AD` connector makes this super simple. Basically, if the user running the flow has access to that information, you can access replies.

![Image 5](../../images/teams-gpt-chatbot-pt2_1690682758862.png)

So the basic flow is as follows:

1. Get the replies to the message
2. Parse the JSON response from the graph
3. Initialize the array to store the entire conversation (including the original prompt and initilization message)
4. Iterate over the replies and add them to the array
5. Set the `isComplete` variable to true if the last message is "done"
6. Clear the array
7. Wait a bit so we don't overwhelm the loop
8. Do it all again

## Recap

So we now have the basic structure of the flow, triggering off the original message, looping through the replies, and storing the conversation. In the next part we'll actually be generating the chatbot response.
