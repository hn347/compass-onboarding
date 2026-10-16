# Rule: honor .bobignore

Treat `.bobignore` as the boundary of what is worth indexing.

- Skip anything matched by `.bobignore`: build artifacts, vendored dependencies, generated code, large binaries and assets, lockfiles, and anything sensitive.
- Never read secrets or credential files even if they are not yet listed; if you encounter one, note its existence without reading or reproducing its contents.
- If the repository has no `.bobignore`, suggest adding the bundled sample before a full index, and exclude the obvious noise directories in the meantime.
- Compass's own output under `docs/onboarding/` is not source to explore.
