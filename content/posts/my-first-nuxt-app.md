---
title: "My First Nuxt App"
date: 2024-10-22T16:55:01-04:00
draft: false
tags: ["nuxt","javascript","AI"]
author: "Me"
categories: ["Tech"]
---

I've had this idea in mind for an AI-assisted tool that allows you to chat with your workout data, as well as generate new titles and descriptions. I've been obsessed with hosting on Cloudflare, had a pg project in Supabase, and have a looked at Vue longingly in the past, so I thought it was a good opportunity to combine all of these for a little project. I've included some screenshots for those without Strava accounts (required to pull in data), but if you do ... give it a try: https://kalla.app

### What I liked:

- **Typescript**: TS seems like the perfect balance of strongly typed goodness with the option to drop back to `any` when it makes sense.
- **Nuxt**: I found Nuxt early on and fell in love with all the nice-to-haves within the framework. I stopped for a minute and tried to go back to vanilla Vue and quickly realized I'd be reinventing the wheel over and over.
- **VS Code & GitHub Copilot**: When learning a new language, having an AI that understands the context of your questions is HUGE. I estimate I saved 100 hours using AI to help me solve issues. The biggest benefit is getting a red squiggly line and invoking AI to explain the error and propose a solution. 9 out of 10 times I could take the suggestion as-is.
- **Supabase and Cloudflare**: I was using Supabase in another project for server-less pg hosting, but in searching for an auth solution, I realized how powerful that platform was. I implemented auth and data persistence in a few hours. And I'm still not sure how CF makes money on Pages projects.
- **Vercel AI**: I was almost set to write my own OpenAI client until I found Vercel's AI SDK - and holy smokes I'm glad I did. It simplified the process significantly.

### Where I struggled:

- **Understanding SSR and client-only rendering**: Still breaks my brain sometimes. I understand it conceptually, but in practice it seems like magic. I had a rash of hydration errors getting started until I understood reactive components and the role SSR played.
- **HTML/CSS**: Still seems like a nightmare to me in 2024. I love NuxtUI and Tailwind greatly simplifies things. Being able to build one site for responsive layouts is a godsend, but all too often I'm finding myself nesting divs within divs to get my layout pixel perfect ... and it feels wrong.
- **Package management**: Seems like it could get fun down the road. Starting off you think you might need a package (thank goodness for the community) but eventually abandon the idea ... who knows how many unused packages I have.

### Overall thoughts:

Overall I'm hugely impressed with the framework. Almost never was the framework missing something I needed it to do. And on the rare occasion it did, npm came to the rescue. And as a C# fanboy for years, I have to say I'm a little shook by how much I liked the TS dev experience. 

If you check it out and have any feedback, I'd love to hear it!

![Image 0](../../images/my-first-nuxt-app_1729630592665.png)  
