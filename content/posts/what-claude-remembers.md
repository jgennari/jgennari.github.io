---
title: "What Claude Remembers"
date: 2026-04-28T12:15:05-04:00
draft: false
tags: ["claude", "automation", "tooling"]
author: "Me"
categories: ["Tech"]
series: ["Life Admin"]
---

The [first post](/posts/my-life-runs-in-a-markdown-file/) talked about the journal and check-in loop. The [second](/posts/skills-are-just-markdown/) talked about skills — markdown files Claude reads to know what to do. This last one is about how Claude remembers things across sessions.

Claude Code ships with a feature called auto-memory: a small filesystem of facts the model can write to and read from, scoped to a project. When I correct Claude ("stop appending 'Sent by Claude' to my texts"), that becomes a memory file. When I confirm a non-obvious decision ("yes, the bundled PR was the right call"), that's also a memory. Anything I wouldn't want to repeat to a fresh session — preferences, project context, pointers to where things live — goes there.

Mine has 19 entries. They live at `~/.claude/projects/<project-id>/memory/` and a small index of them is loaded into the system prompt at the start of every conversation. That's how Claude in this repo "knows" who I am, who's in the phone book, why I disable the Telegram MCP plugin in cron, and that I want responses on Telegram instead of the terminal when I'm away from my desk.

Same mechanic as skills: a directory of markdown files. The interesting part is what to put in there.

## The four types

Memories sort into four categories. Mine looks like this:

| Type | Count | Examples |
|---|---|---|
| **user** | 1 | who I am, what I do, what I know |
| **feedback** | 6 | "lowercase iMessages always", "no Claude signatures", "ack long skills" |
| **project** | 5 | divorce planning, custody pattern, fitness rehab |
| **reference** | 7 | Forgejo server, DNS topology, Engage Boston 2026 |

Brief description of each:

- **user** — who I am, what I do, what I know. Slow-changing. One file is usually enough.
- **feedback** — guidance I've given Claude about how to work with me. Both corrections (*stop adding signatures*) and validated approaches (*yes, the bundled PR was the right call*). The most behaviorally-impactful type.
- **project** — ongoing initiatives, deadlines, who's doing what. Decays fastest of the four, because projects move quickly.
- **reference** — pointers to where things live. *"Bugs are tracked in Linear project INGEST."* *"The latency dashboard is at grafana.internal/d/api-latency."*

Each memory is a markdown file with frontmatter (name, description, type) and a body. The description shows up in the index and decides whether the memory gets pulled into a conversation; the body is the actual content.

## Anatomy of a memory

Here's a real one from my repo — the memory that explains why my cron jobs disable a specific MCP plugin. Without this memory, Claude will keep re-discovering the polling-conflict bug from scratch every time I touch the launchd config.

```markdown
---
name: Telegram cron isolation
description: Cron-driven claude sessions must not load the telegram MCP plugin
  — it would steal the poller from interactive sessions. Use scripts/tg-send instead.
type: project
---

The telegram bot API allows exactly one getUpdates poller per token. The
telegram MCP plugin enforces single-poller via a PID-file lock — every
new server instance SIGTERMs whatever PID is in that file.

My hourly /checkin and morning /journal launchd jobs both run claude
in the same project as my interactive session. If the cron loaded the
telegram plugin, it would silently kill the interactive session's poller
on each fire, and inbound Telegram messages would stop reaching me until
I restarted.

**Why:** Surfaced as "Telegram disconnects after a few hours" — actually
"until the next cron fire, max." Confirmed by `replacing stale poller pid=X`
lines in the plugin's MCP logs lining up with cron firing times.

**How to apply:**
- Cron plists pass `--settings ~/.claude/cron-settings.json` which sets
  `enabledPlugins.telegram@claude-plugins-official: false`. Don't add
  the channel back to those plists.
- /checkin and /journal SKILL.md call `bash scripts/tg-send "msg"` for
  outbound, NOT the MCP `reply` tool.
- If "telegram stopped working again," check the MCP plugin logs for
  fresh `replacing stale poller` entries around the cron schedule —
  that means something regressed.
```

The **Why** and **How to apply** lines aren't required by the format — they're a convention I picked up because they make memories useful at the edges. If I'm in a future conversation and the situation is *like* but not exactly *like* the one in the memory, the "Why" lets Claude judge whether the rule still applies. The "How to apply" gives it specific things to check.

## The index

The memory directory has a file at the top called `MEMORY.md`. It's just one line per memory, a pointer with a one-sentence hook:

```
- [User identity](user_name.md) — Joey Gennari, Bullhorn Labs, Delray Beach FL
- [Lowercase iMessages](feedback_lowercase_texts.md) — Always text in all lowercase
- [Telegram cron isolation](project_telegram_cron_isolation.md) — Cron must NOT
  load telegram MCP plugin (would steal poller); use scripts/tg-send for outbound
- [Apple Notes checklists](feedback_apple_notes_checklists.md) — Never write/
  append to notes with checkboxes via AppleScript `body` — strips checklist class
```

The index is what gets loaded automatically into every conversation. Full memory bodies aren't loaded by default — Claude reads them when the index entry suggests one is relevant. So the description in the index matters: it's how Claude decides whether to pull in the full file.

This is also why the index has a soft cap. It loads into every conversation, so a 200-line `MEMORY.md` eats context. Mine sits at 19 entries; I prune when I notice old ones.

## What gets saved

Claude decides what to save, mostly. The triggers, in order of how often they fire for me:

1. **I correct it.** "No, don't do that." "Stop adding signatures."
2. **I confirm a non-obvious choice it made.** "Yes exactly." "Perfect, keep doing that." Or just accepting the work without redirecting.
3. **I tell it something about myself, my role, or my schedule.** "I'm at Bullhorn." "Sundays are for the weekly review."
4. **I mention an external system and what it's for.** "Bugs are in Linear project X." "The dashboard at this URL is what oncall watches."

The confirmation trigger is the one I missed when I started using this. Confirmations are quieter than corrections — easier to forget that they're load-bearing. If you only save what went wrong, you'll keep relitigating decisions you've already settled.

## What NOT to save

This was the rule that took me longest to internalize. **Code patterns, project structure, file paths, conventions** — those get derived from the actual repo state at any point. Memorizing them means the memory rots fast and crowds out the useful entries.

The dividing line: if reading the current state of the project would tell Claude the same thing, don't make it a memory. Save things you can't see in `git log` or by `ls`-ing a directory.

So:
- ✓ "The 6:27 AM cron disables the Telegram plugin because of the poller conflict"
- ✗ "The journal lives at `journal/YYYY-MM-DD.md`" — Claude will see that immediately
- ✓ "The blog repo is at `~/Source/jgennari.github.io`"
- ✗ "Use the `/save` skill to commit and push" — it's documented in `CLAUDE.md`
- ✓ "I want iMessages drafted in lowercase, always"
- ✗ "There's a `journal/2026-04-21.md` file" — transient, will be true tomorrow but not the day after

## When memories go stale

The auto-memory system is frozen-in-time. The fact you saved is true at the moment you saved it. Three months later it might not be.

I noticed this when Claude told me one morning that "Lily and Dylan are 8 and 6" — they were when I wrote that memory in February, but Lily had a birthday since. The fix: the memory now says "DOBs in `people/`" instead of `Lily 8, Dylan 6`, and Claude reads the live profile for the current age.

The general rule: **prefer pointers over snapshots**. *"See `projects/divorce.md`"* beats *"we're in the financial modeling phase"*. Snapshots decay; pointers track the underlying file.

The system actually knows this. When I read a memory file directly today, it came back with a warning attached: *"This memory is 11 days old. Memories are point-in-time observations, not live state — claims about code behavior or file:line citations may be outdated. Verify against current code before asserting as fact."* The user has to know it too.

## Limits and lessons

- **Memory is project-scoped.** The directory path includes the project ID. Each repo has its own memory store. This is right — what I want Claude to remember about my life repo is different from what I'd want it to remember about a work codebase.
- **Claude pushes back on questionable saves.** It's been instructed (in the system prompt) not to save derivable things. I've had to argue once or twice that something I wanted saved was genuinely non-derivable. The bias toward "less is more" is mostly the right one.
- **The "feedback" type is the most underrated.** Most people I've talked to about this default to "user" and "project" memories. The "feedback" entries are the ones that change Claude's behavior session-to-session — corrections and validated approaches. They're worth more than they look.
- **Memory loss is not catastrophic.** If `MEMORY.md` got wiped tomorrow, I'd recreate the load-bearing entries within a week of normal use, because Claude would re-encounter the situations that prompted them. Memories are an optimization, not a foundation.

## Closing

A directory of markdown files. An index that loads automatically. A model that reads them and acts. Same mechanic as [skills](/posts/skills-are-just-markdown/), smaller scope, different lifecycle.

That's the third post in this series. The first was about the journal and check-in loop; the second was about skills as a convention; this one is about memory as a convention. In a different sense, all three posts have been about the same idea: a small filesystem layout, plus a model that reads it, beats most of the framework-shaped solutions you'd otherwise reach for.

The companion repo at [github.com/jgennari/claude-life-template](https://github.com/jgennari/claude-life-template) doesn't ship with a populated `MEMORY.md` — there's nothing useful to copy, only a shape to fill in. Memory builds up as you use the system. It takes a few weeks before it starts paying off, and then you stop noticing it because Claude already knows.
