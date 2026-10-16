# Rule: ground every claim, abstain when unsure

This is the most important rule in the pack. Onboarding docs that sound confident but are wrong are worse than no docs, because a newcomer will trust them.

- Every architectural or behavioral claim must cite the `file:line` (or `file`) it is based on. No citation, no claim.
- Quote at most two lines when illustrating. Never paste large file contents.
- If you cannot confidently determine something, write it as `UNKNOWN: <what you could not determine>` and add `To confirm: <the one check that would resolve it>`. Do not guess.
- Abstaining is a successful outcome. "Could not determine the test runner" is a better answer than a plausible wrong one.
- Before writing any artifact, verify that the paths you cited actually exist.

Example:

> The HTTP entry point is the Express app created in `src/server.ts:14`, which mounts routers from `src/routes/` (`src/server.ts:22-27`).
> UNKNOWN: which environment selects the production database. To confirm: locate where `DATABASE_URL` is read.
