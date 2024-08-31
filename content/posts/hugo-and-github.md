---
title: "Hugo and Github"
date: 2023-07-28T17:22:03-04:00
draft: false
tags: ["hugo","github"]
author: "Me"
categories: ["Tech"]
---

I'd been running my blog on Ghost and DigitalOcean for a bit now, and while it's not super expensive, it's certainly not free. And I wasn't comfortable with the fragility of the config. And while the editor was nice, it seemed like overkill for the type of blog I was hoping to have. I wanted something I could quickly get my thoughts on to paper. So after a little research I ended up configuring Hugo and publishing it to Github Pages. But the process wasn't seamless, so here's my notes:

* Good god the versioning on Hugo seems to be a mess. Starting with the config situation. It seems like the original project started with TOML, but allowed(?) for other formats. It seems like there's TOML, YAML, and JSON now. The problem is every theme and walkthrough use something different. And you'll need to mix and match for your needs, and you end up spending a lot of brain power switching between the 3.
*  Speaking of standards, it seems like there's two different ways to do plugins: Git Submodule and Go modules. It took a little configuring to get Go working, but it wasn't too bad.
* For the reasons above, finding a theme is painful. It makes me think I'll pick one and stick with it.
* I love being able to write in VS Code. I set up some tasks for running the server and creating new posts:

```json
{
    "version": "2.0.0",
    "tasks": [
        {
            "label": "Hugo Start Server",
            "type": "shell",
            "command": "hugo server",
            "problemMatcher": []
        },
        {
            "label": "Hugo New Post",
            "type": "shell",
            "command": "hugo new --kind post posts/\"${input:postName}.md\"",
            "problemMatcher": []
        }
    ],
    "inputs": [
      {
        "id": "postName",
        "type": "promptString",
        "description": "Post title"
      }
    ]
}
```
