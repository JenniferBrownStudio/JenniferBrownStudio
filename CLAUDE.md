# CLAUDE.md

Guidance for working in this repository.

## What this is
Static website for jenniferbrown.xyz (performer / teacher / fitness coach).
All 14 pages are generated from one template in `build.py`.

## Editing
- **Edit `build.py`, not the `*.html` files** — the HTML is generated output and is overwritten on every build.
- Rebuild with: `python3 build.py` (regenerates all pages into the repo root).

## Required workflow on every change
1. **Rebuild**: run `python3 build.py`.
2. **Verify desktop + mobile**: preview and check the change renders at both desktop (1280×800) and mobile (375×812) before considering it done — don't ask the user to check manually.
3. **Commit + push**: after each change, run
   `git add -A && git commit -m "Auto-commit: site update $(date '+%Y-%m-%d %H:%M:%S')" && git push origin HEAD`

## Local preview
The preview server serves a mirror under `/private/tmp/.../scratchpad/preview_site` (configured in `.claude/launch.json`), because the sandboxed preview helper cannot read this repo under `~/Documents`. After rebuilding, re-sync the mirror before previewing:
```
rsync -a --delete --include='*/' --include='*.html' --include='assets/***' --exclude='*' ./ <mirror>/
```
In a normal terminal you can instead run `python3 serve.py` (a `getcwd`-free static server) and open http://127.0.0.1:8099.
