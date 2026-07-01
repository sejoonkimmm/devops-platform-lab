# Task 7 — AI in DevOps

When someone asks what I do for a living, I don't round it down to "software engineer." I say DevOps engineer. Most people have no idea what that means, and I've never minded. I keep explaining until they get the actual thing I do, not the blurred version of it.

I've spent years in this role, and it's one of the few choices I'd make again without a second of thought. I'm not saying that as a warm-up. It's the frame for everything below. I'm not a neutral observer of where this field goes. I have a stake in it.

Here's what I actually believe, after using these tools every day for about three years. The value was never whether you use AI. It's whether you build the system around the place where AI fails.

That sounds obvious. It's not how most people use it.

From my own experience, the biggest opportunity isn't the exciting one. It's the daily grind of writing and changing infrastructure config. Helm charts, Kubernetes manifests, pipeline files. That's where my real hours go, and it's where AI gives the most time back.

The same work also showed me exactly where AI breaks.

Last February, when everyone was busy with harness engineering, I had an AI assistant editing a Helm chart. It kept adding values that looked completely reasonable and did not exist in the official chart. Keys that were never defined upstream. The output read like valid config, so I trusted it, and then lost hours chasing a problem that was never real. Our environments are split cleanly into dev, stage and prod, so nothing bad reached production. But I still burned an afternoon in the lower environments debugging a value that didn't exist.

That's the failure mode I watch for now. AI doesn't fail loudly. It fails by producing something plausible. In application code a wrong guess usually throws an error. In infrastructure config a wrong guess can look right, pass review, and fail quietly later. For a DevOps engineer that's the dangerous kind of wrong.

I didn't stop using AI after that. I did the opposite. Before any change to a Helm chart now, I run a small harness of five Haiku agents. They scrape the official chart and the official docs, then fact-check each other before anything reaches my editor. Only verified values get through. Since I attached that harness to this kind of work, the same error hasn't come back.

That's the thesis in practice. I didn't fix an AI problem by using less AI. I fixed it by designing the system around the exact point where it was failing.

That's also where I put the real risk. It isn't that AI writes bad code. It's that we stop checking. The more fluent the output gets, the easier it is to hand over the one part of the job that was never safe to hand over, which is judging whether the thing is actually true. Reliability, security and trust all sit downstream of that one habit. The skill I care about most now isn't prompting. It's knowing which output I'm allowed to believe, and building the checks that decide it for me.

<!-- PLACEHOLDER: replace with your real "next 12 months" voice. Draft below is pulled from your own trajectory. -->
Over the next year I want to take that harness idea past config. Most of mine today guard narrow tasks. I want to see how far the pattern goes. Agents that check each other on incident response, that read my Terraform before it ever plans, that catch the plausible-but-wrong answer before I see it. I'm also curious where the line is. At some point a check that's itself AI needs its own check, and I want to find where that stops being worth it.

That's also why I still introduce myself the way I do. The job isn't disappearing into the tools. It's moving into the space around them, into deciding what to trust and building the things that enforce it. That's the work I want to keep doing. It's why I'd still say DevOps engineer, out loud, every time.
