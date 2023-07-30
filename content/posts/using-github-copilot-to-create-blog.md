---
title: "Using Github Copilot to Create Blog Posts"
date: 2023-07-30T10:15:11-04:00
draft: false
tags: ["ai","github","copilot","blog","hugo"]
author: "Me"
category: ["Tech"]
series: []
---

First, let me show you:

{{< screenrecording src="copilot" >}}

I recently installed the Github Copilot extension for VS Code. I've been using it for a few days now, and I'm really impressed. I've been using it to generate the basic structure of my blog posts. I'm going to use this post to show you how I'm using it, and how I'm going to use it in the future.

I mean, I guess I already showed you. The crazy part is that it's contextual with my whole blog. So it knows the other source files, projects I'm working on, tags and categories. Super useful. In the recording above I'm using some actions I created in my [Hugo and Github post]({{< ref "hugo-and-github.md" >}}).

Credit to Matteo Mazzarolo for [this tutorial](https://mmazzarolo.com/blog/2022-05-25-how-i-capture-encode-and-embed-videos/) on creating embedded screen recordings like the one above. I created the following shortcode for Hugo to embed the recording:

#### screenrecording.html
```html
<div class="screen-recording">
    <video autoplay controls loop muted playsinline>
        <source src="../../video/{{ .Get "src" }}.webm" type="video/webm; codecs=vp9,vorbis" />
        <source src="../../video/{{ .Get "src" }}.mp4" type="video/mp4" />
    </video>
</div>

<style>
    .screen-recording {
        display: flex;
        flex-direction: row;
        flex-wrap: wrap;
        align-items: center;
        justify-content: center;
    }

    .screen-recording>video {
        max-width: 100%;
        height: auto;
        border-radius: 4px;
    }
</style>
```

And embed it with the following tag `{{</* screenrecording src="copilot" */>}}`.