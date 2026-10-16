# Rule: explain legacy code before judging it (Chesterton's Fence)

Onboarding often surfaces code that looks odd, dead, or wrong. In a long-lived enterprise repository, the strange code is frequently load-bearing.

- When you describe code that appears unusual, redundant, or obsolete, first state what it does and the most plausible reason it might exist.
- Mark a suspicion as a suspicion, grounded in a file reference, not as a verdict. For example: "Appears unused (`legacy/auth.go:88`); UNKNOWN whether a batch job still calls it. To confirm: grep for the symbol across the repo and any scheduler config."
- Never recommend deleting or rewriting something in an onboarding artifact. Onboarding documents the territory; it does not redraw it.
- Treat undocumented conventions as Chesterton's Fences: describe them faithfully so a newcomer understands the rule before anyone considers changing it.
