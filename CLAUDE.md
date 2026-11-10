# Instructions for Claude sessions in this repo

This repo is the public legal and support website for Evenstep, a co-parenting app. It's published by GitHub Pages from the repo root on `main`. The founder is non-technical and works from a phone only, so explain in plain English.

- Edit only `src/` (content, styles, `src/tools/build.py`). Then run `python3 src/tools/build.py`, which rebuilds the root pages and prints any leftover `[brackets]`. Never hand-edit the built HTML.
- Before pushing, check the pages in Chromium (Playwright) at 360 px and 1280 px, with the browser set to light and to dark (the site is light only since 7 Nov 2026, so both must show the light colours):
  - no sideways scroll;
  - only local requests;
  - one h1 per page;
  - every link and section anchor resolves.
- Legal pages need a version, a "Last updated" date and a line under Changes for every change. Copy changed text back into `launch-handoff/03`–`06` in the claude.ai project. Those copies keep the private founder notes, which never go on the site.
- Keep it free of cookies, analytics, scripts and web fonts. The privacy policy promises this.
- The logo, favicon and home-screen icon are the app's "e" (7 Nov 2026). `src/assets/app-icon-1024.png` is a copy of the Evenstep repo's `assets/images/ios-icon.png`; copy it again if the app icon changes.
- Read `launch-handoff/07 Website handover.md` in the claude.ai project for decisions, open items and what to change at the first tester release.
- Founder preferences: ask before decisions you're unsure about; have independent agents review legal or visible changes; take a git snapshot before big changes.
