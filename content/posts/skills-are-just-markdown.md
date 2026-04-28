---
title: "Skills Are Just Markdown"
date: 2026-04-28T11:17:47-04:00
draft: false
tags: ["claude", "automation", "tooling"]
author: "Me"
categories: ["Tech"]
series: []
---

The [first post in this series](/posts/my-life-runs-in-a-markdown-file/) talked about `/journal` and `/checkin` — a daily journal and a 15-minute check-in loop that runs unattended on a schedule. I called them "skills" without explaining what that means. This post is about the mechanism.

A skill is a markdown file. That's the whole abstraction.

Specifically: a directory under `.claude/skills/<name>/` with a `SKILL.md` inside. The directory name is the slash command. The contents of `SKILL.md` are the instructions Claude reads when you invoke it. There's no plugin API, no shell wrapper, no "register your command." Drop a directory in, the command exists. Edit the file, the behavior changes.

I have 17 of them. The largest is `/journal` at ~200 lines; the smallest is `/save` at ~36. None of them contain code — they're prose, with a few code blocks for examples. The model does the work. The markdown tells it what work to do.

That setup turns out to be surprisingly powerful, and the rest of this post is about why.

## Anatomy of a skill

Here's `/save` in full. It commits whatever is outstanding in the working directory and pushes to the remote:

````markdown
---
name: save
description: Commit any outstanding changes and push to the remote. Use when Joey says "save", "commit and push", or wants to checkpoint his work.
---

# Save

Commit all outstanding changes in the working directory and push to the remote.

## Steps

1. Run `git status` to see what's changed (staged, unstaged, untracked).
2. If there are no changes at all, tell Joey there's nothing to save and stop.
3. Review the diff (`git diff` and `git diff --cached`) and any new untracked files to understand what changed.
4. Stage all changes with `git add -A`.
5. Write a concise commit message — summarize the changes (1-2 sentences, focus on the "why"). End with the co-author trailer.
6. Commit and push:
   ```
   git commit -m "<message>

   Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>"
   git push
   ```
7. Report what was committed and pushed.

## Rules

- Do NOT skip the review step — always look at what's being committed.
- Do NOT commit files that look like secrets (.env, credentials, tokens). Warn Joey if any are present.
- Use a HEREDOC for the commit message to handle multi-line formatting.
- If the push fails (e.g. no upstream), set it up with `git push -u origin <branch>`.
- **Route the final confirmation to wherever the request came from.** If Joey asked for the save via Telegram, send the confirmation through the Telegram reply tool — not just as terminal output. Same applies for iMessage.
````

Three things to notice:

1. **The frontmatter** has a `name` (the command) and a `description` written so the routing layer can decide when to trigger the skill from natural language. "Joey says 'save'" is a literal trigger; "wants to checkpoint his work" is a paraphrase trigger. The description matters — write it like you're handing the skill a memo about when to introduce itself.
2. **The body has two halves: steps and rules.** Steps are the procedure. Rules are the constraints — what not to do, what to confirm, what to route where. Keeping them separate makes the rules harder to ignore.
3. **There is no code.** The skill describes what to do, not how. Claude already knows how to run `git status`. Telling it to do so is enough.

Bigger skills (`/checkin`, `/groceries`, `/inbox`) follow the same shape — more steps, more rules, sometimes a worked example or two pasted in. They scale linearly. There's no point at which a skill needs to "graduate" to code.

## How invocation works

When I type `/save` in a Claude Code session, Claude reads `.claude/skills/save/SKILL.md` and treats the body as a top-level instruction. It still has access to all of its normal tools — `Bash` for shell commands, `Edit` for file changes, `Read`, `Grep`, MCP tools for external services. The skill doesn't grant or revoke access; it just shapes the behavior.

The same `/save` works whether I run it from a terminal or whether `/journal` invokes it as the last step of its morning routine. Same skill, same instructions, different invocation source.

This is why I keep saying the model does the work. There's no dispatcher. There's no "skill runtime." Claude reads the markdown and acts on it.

## Skills compose

Most of my skills end with a line that says "now run `/save`." That's not a code call — it's an instruction. Claude, mid-task, reads "now run `/save`" and invokes the save skill, which reads its own `SKILL.md`, and follows it.

The pattern shows up everywhere:

- `/journal` writes the morning briefing, then runs `/save` to commit and push
- `/checkin` appends a log entry, then runs `/save`
- `/groceries` plans meals, then calls `/reminders` to add items to Apple Reminders
- `/inbox` triages email, then sometimes calls `/reminders` for follow-ups
- `/weekly` calls `/inbox`, `/checkin`, and `/journal` to assemble its review

Composition without imports. A new skill can use any existing one by name, the same way a human would say "OK, now save it."

I add skills the same way I add a new function in a codebase. Identify a thing I do regularly, write a `SKILL.md` describing what it should do and what to avoid, drop it under `.claude/skills/`. The first version is usually wrong; I edit the markdown until it isn't. The whole feedback loop is "open the file, change the words, run it again."

## Why this is more powerful than it sounds

A few reasons "markdown file in a directory" beats the alternatives:

- **Editable in seconds.** Bug in `/groceries`? Open the file, change a sentence, save. No deploy, no restart, no test run.
- **Versionable.** Every skill is a markdown file in git. `git blame` on a `SKILL.md` shows when a behavior changed and why.
- **Branchable.** Trying a different approach to checkin? `cp -r checkin checkin-experimental`, edit the copy, invoke `/checkin-experimental`. Two skills, no conflict.
- **Forkable.** Sharing a skill is sharing a directory.
- **Reviewable.** The skill is the source of truth. To know what `/inbox` will do, you read `/inbox/SKILL.md`. There's no implementation hiding behind the spec — they're the same file.

Compare this to the alternative I used to think I'd need: a Python or Node project that registers commands, parses arguments, calls APIs, and dispatches to handlers. To add a new command, you'd write code, tests, and glue. To change behavior, you'd edit code, run tests, deploy. Markdown skills skip every step except the one that actually matters: describing what you want.

## Tips from writing 17 of them

A few things I've learned:

- **Lead with rules.** "Read-only on email" near the top of `/checkin` is more reliable than the same sentence buried in step 5. The model takes earlier instructions more seriously.
- **Numbered steps for procedures.** Bullet steps work for parallel options; numbers work for "do this, then this." `/journal` is numbered; `/save` is numbered. They follow the order.
- **Examples beat explanations.** If a skill needs to write a specific output format, paste a real example. "Write a markdown file with this structure" + an example block is shorter and more accurate than three paragraphs describing the structure.
- **Scope tightly.** A skill that "checks email and also organizes contacts and also drafts replies" gets confused. Split it. `/inbox` triages. `/contacts` updates the address book. `/messages` handles iMessage. Each one knows one job.
- **Failure modes belong in the skill.** If something can go wrong, write what to do about it. `/save` says "if push fails for no-upstream, set it up with `git push -u origin <branch>`." Without that line, Claude makes the same mistake every other Tuesday.
- **Don't reach for code when prose works.** Most skills have zero code. The model is good at running shell commands, calling MCP tools, and parsing structured output. Telling it what to run is usually enough.

## When to break out of markdown

A few of my skills ship with a helper script. Not because the skill itself is code — the `SKILL.md` is still markdown — but because there's a chunk of plumbing that would be wasteful to do in prose every invocation:

- **`/plants`** ships a `planta` shell script that wraps the [Planta](https://getplanta.com) API with OAuth refresh and on-disk caching. Doing OAuth+caching in prose every time would burn tokens and time.
- **`/photos`** ships a small wrapper around `osxphotos` that sets sensible defaults and handles the flags I always forget.
- **`tg-send`** isn't a skill at all — it's a shell script in `scripts/` that cron-driven `/journal` and `/checkin` use to send Telegram messages without loading the Telegram MCP plugin (which would step on the polling slot of any active interactive session).

Rule of thumb: if the same boilerplate would appear in three or more invocations of a skill, extract it. Otherwise leave it in prose.

## Closing

Skills work because the model is good at following well-written instructions. Once you accept that, "drop a markdown file in a directory" turns into a usable command. It's not a framework; it's a convention. The convention is small enough that it doesn't get in the way, and it's loose enough that the same shape works for `/save` (30-ish lines, runs in 2 seconds) and `/journal` (200 lines, runs every morning before I'm awake).

All 17 of mine live at [github.com/jgennari/claude-life-template/tree/main/.claude/skills](https://github.com/jgennari/claude-life-template/tree/main/.claude/skills). Browse them as a starting point.

Next post: the **auto-memory system** — same kind of small filesystem convention, big multiplier. Claude maintains a set of notes about who I am and what I've taught it, and uses them to stay coherent across conversations.
