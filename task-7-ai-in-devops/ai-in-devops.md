# Task 7 — AI in DevOps

I have used AI tools daily for about three years, and my position is simple. The value was never whether you use AI, but whether you build the system around the place where it fails. Most of my hours go into infrastructure config, Helm charts, manifests and pipelines, and that is where AI returns the most time. It is also where it broke on me.

Last February an AI assistant kept adding values to a Helm chart that looked reasonable and did not exist in the upstream chart. The output read like valid config, so I trusted it, and lost an afternoon chasing a problem that was never real. Nothing reached production, since our environments split cleanly into dev, stage and prod, but the time was gone.

That taught me which failure to watch for. AI does not fail loudly; it produces something plausible. In application code a wrong guess usually throws. In infrastructure config it can look right, pass review, and fail later without a sound, the same shape as the silent Kafka bug in Task 1.

I did the opposite of stopping. Every Helm change now goes through a small harness of five Haiku agents that scrape the official chart and docs, fact-check each other, and let only verified values through. The error has not come back. I fixed an AI problem with more AI, aimed at the exact point of failure.

The risk I actually worry about is that we stop checking. The more fluent the output gets, the easier it is to hand over the one part of the job that was never safe to hand over, which is judging whether the thing is true. The skill I care about most is not prompting; it is knowing which output I am allowed to believe, and building the checks that decide it for me.

Over the next year I want to push the harness idea past config, into agents that cross-check incident response, read my Terraform before it plans, and catch the plausible-but-wrong answer before I see it. I also want to find where that stops being worth it, because at some point a check that is itself AI needs its own check. The job is not disappearing into the tools; it is moving into deciding what to trust.
