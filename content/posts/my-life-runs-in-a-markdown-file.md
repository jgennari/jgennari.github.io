---
title: "My Life Runs in a Markdown File"
date: 2026-04-27T22:36:21-04:00
draft: false
tags: ["claude", "automation", "personal", "tooling"]
author: "Me"
categories: ["Tech"]
series: []
---

I have a Claude Code-powered personal assistant that runs on a schedule. It reads my email, my calendar, my texts, the kids' school calendar, my plant care schedule, the weather, and my custody plan. It writes the day to a markdown file every morning and updates that file every 15 minutes throughout the work day. Most of the time it doesn't tell me anything — that's the point.

The whole thing lives in a git repo I call `life/`. About 6,000 lines of markdown, a handful of shell scripts, 17 slash commands. Here's a partial list of what it does in a normal week, all without me asking:

- triages my inbox and archives the noise
- drafts replies to my ex about custody schedule changes
- pulls the school calendar for early dismissals and closures
- reminds me which plants need water
- meal-plans around custody and adds groceries to Apple Reminders
- searches photos by OCR when I need a receipt
- manages my Hugo blog drafts and deploys them
- monitors my Unraid server and restarts misbehaving stacks
- resolves unknown phone numbers and updates the contacts file
- runs a structured weekly review every Sunday evening

This post is about the cornerstone: the daily journal file and the 15-minute check-in loop. Follow-ups will go deeper on the skills architecture, the auto-memory system, and the integrations layer. For now: what it does and why it works.

## The 30-second mental model

Three pieces, all simple:

1. **The repo.** A git directory with `journal/`, `people/`, `projects/`, and a top-level `CLAUDE.md` that tells Claude how to behave.
2. **Skills.** Slash commands like `/journal`, `/checkin`, `/groceries`. Each one is a markdown file that Claude reads when invoked. They define what to do, in what order, with what guardrails.
3. **Integrations.** MCP servers connect Claude to real systems — Fastmail for email, CalDAV and Google Calendar for events, AppleScript for Reminders/Notes/Contacts, a Telegram bot for notifications, an iMessage reader, a few others.

Claude Code runs in two modes here. Interactive: I open a terminal and type `/journal` or `/checkin` or `/groceries` myself. Scheduled: launchd kicks off a non-interactive `claude` process at fixed times and pipes the same skill commands. Same skills, two ways to invoke.

## The daily journal

Every morning at 6:27 AM, before I'm awake, a launchd job runs `claude /journal`. That command writes a single markdown file to `journal/2026-04-21.md` (or whatever today is) with three sections:

- **schedule** — every event from my personal calendar, work calendar, and the kids' school calendar, merged and sorted
- **tasks** — overdue reminders, things due today, actionable emails, unanswered messages
- **log** — append-only, timestamped. Starts with the morning briefing Claude wrote; gets added to throughout the day

The journal is the single source of truth for what's happening on a given day. If I want to know what's going on, I open the file. If I want to know what was happening three weeks ago, I open that file.

Here's what a morning briefing looks like:

> good morning — light day on your side. kids are at school, no meetings until the 2pm with the labs team. monstera needs water before you forget. school sent a permission-slip reminder for the friday field trip — pdf attached. one email worth your eyes from your accountant about q1 estimates; inbox is otherwise noise (archived 12 newsletters).

That's not a template. Claude reads everything fresh and writes the briefing in plain language each morning. It also pushes it to Telegram, so the briefing is on my phone before I open my laptop.

The briefing also gets stored as the first log entry in the journal file. Everything that happens after gets appended below.

## The 15-minute check-in

Once the day is going, a second launchd job runs `claude /checkin` every 15 minutes — at `:10`, `:25`, `:40`, and `:55`, Monday through Friday, 8 AM to 6 PM. That's 220 runs per work week.

Each run does roughly this:

1. Read today's journal so it knows what's already been reported.
2. Pull anything new from the last 20 minutes — email, iMessage, calendar updates.
3. Check the next 30 minutes of calendar for upcoming events.
4. Auto-archive obvious noise (newsletters, marketing emails, shipping confirmations).
5. **If something changed**, append a `### HH:MM — checkin` log entry to the journal and Telegram me a one-line summary. **If nothing changed**, exit silently — no journal write, no Telegram, no commit.

The silent exit is the most important rule. Most check-ins do nothing visible. If I'm sitting in a meeting and three check-ins fire while we're talking, I shouldn't notice. The point of the system is to reduce noise, not add to it.

When something does happen, it looks like this:

```markdown
### 10:25 — checkin

school sent an early-dismissal alert for friday (1:30 instead of 3:00) — added
to schedule. labs standup moved 2pm → 2:30pm. inbox: nothing new of substance.
```

The same line goes to Telegram. If it's actually urgent, I look. If not, the journal will be there when I do.

## The four rules that make it work

Running an unattended Claude that touches my email and texts could go wrong in obvious ways. Four rules keep it boring:

1. **Read-only on email and iMessage.** It will never reply or send unless I explicitly ask in an interactive session. The auto-runs can read everything; they can't speak.
2. **Never modify calendar events.** Reports only. Same logic — observation, not action.
3. **Deduplicate against the journal.** Before reporting anything, the check-in reads the existing log entries. If something was already flagged, it doesn't flag it again.
4. **Silent runs stay silent.** No journal write, no Telegram, no git commit when nothing actually happened. The launchd log is the audit trail.

The first three remove the failure modes I'm worried about. The fourth makes the alerts I do get matter.

## A day in the journal

Abbreviated walkthrough of a Tuesday, with names and details swapped:

```markdown
---
date: 2026-04-21
custody: joey
---

## schedule

- 08:30 — drop kids at school
- 14:00 — labs sync (work)
- 17:30 — pickup grocery order at trader joe's

## tasks

- [ ] water monstera (5 days overdue per Planta)
- [ ] sign lily's zoo trip permission slip (due thursday)
- [ ] reschedule dentist (email from monday)

## log

### 06:27 — morning briefing
good morning — light day. kids at school, no meetings until 2pm. one email
worth your eyes from your accountant about q1 estimates. inbox: 12 newsletters
archived.

### 10:25 — checkin
school sent early-dismissal alert for friday (1:30 instead of 3:00) — schedule
updated. permission slip for lily's zoo trip due thursday.

### 12:55 — checkin
labs standup moved 2pm → 2:30pm. accountant replied with the q1 numbers — left
in inbox so you can review before signing.

### 16:40 — checkin
nothing new. heads up: 17:00 reminder to leave for trader joe's in 5 min.
```

Most of the day's 40 check-ins had nothing to report. Those silent runs aren't in the journal at all. The launchd log shows they ran; they just had nothing to say.

## What this changes

The headline change is that I'm not the person doing inbox triage anymore. I'm the person reviewing a list of things flagged worth my attention. Most days that list is two or three items.

A few smaller changes that have stuck:

- **I stopped opening the inbox in the morning.** The briefing tells me what's actually there.
- **I stopped missing schedule shifts.** School early-dismissals, meetings moved on the work calendar, family logistics over text — the check-in surfaces them within 15 minutes.
- **I stopped checking notification apps.** Telegram is the one channel for assistant messages. Everything else stays quiet.
- **The journal is a searchable record of my life.** `grep` on `journal/` answers "when did Lily's last fever start" or "when did I last hear from Gary" surprisingly well.

This is not a productivity hack. It's closer to delegating the parts of the day that don't require me to a system that's good at them.

## Limits and lessons

A few things I had to figure out, mostly the hard way:

- **The check-in can't write to the calendar or send messages.** That's by design (rule 1), but it means I still have to act when something needs action. The system surfaces; I do.
- **ICS feeds lag.** The kids' school calendar updates a few hours after the school posts a change. The check-in catches it eventually but not always immediately.
- **The Telegram MCP plugin can't run in cron.** Telegram's bot API only allows one `getUpdates` poller per token. The plugin grabs the lock; if a cron-driven Claude loaded the plugin, it would silently kill the poller in my active terminal session. I learned this the hard way — my interactive Claude went mute mid-afternoon and I couldn't figure out why for an hour. Fix was disabling the plugin in cron settings and using a small `curl` wrapper for outbound messages.
- **Free-text dedup is fuzzy.** If the morning briefing says "an email from your accountant about q1" and the 10:25 check-in says "your accountant replied re: april estimates," the dedup logic mostly catches it — but not always. Some days I get told the same thing twice.

## What's next

Three follow-ups planned:

1. **The skills architecture.** How `/journal`, `/checkin`, `/groceries`, `/blog`, and the rest are all just markdown files in a `.claude/skills/` directory. Why this is more powerful than it sounds.
2. **The auto-memory system.** A small file-based memory layer that persists across conversations. How it learns who I am, what I prefer, what to stop doing.
3. **The integrations layer.** MCP servers, the iMessage reader, the Telegram bot, the AppleScript glue holding it all together.

## The companion repo

The full structure is published at **[github.com/jgennari/claude-life-template](https://github.com/jgennari/claude-life-template)** — same `CLAUDE.md`, all 17 slash commands, the same launchd automation, populated around a fictional persona (a software engineer in Austin named Alex Rivera) so it works as a living example rather than empty scaffolding. Fork it, replace the persona, plug in your own accounts.

My actual `life/` repo is private — it has my email, my kids' names, my therapy schedule — but the pattern isn't. If your inbox runs you, or you've wanted a personal assistant without paying for one, the cost of building something like this is now mostly the time to figure out what you want it to do.
