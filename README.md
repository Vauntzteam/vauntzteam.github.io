# Evenstep website

The public pages for Evenstep, a co-parenting app by Wong Shou Hong. They live at **https://vauntzteam.github.io/**:

- [Privacy Policy](https://vauntzteam.github.io/privacy/): the App Store and Google Play privacy URL
- [Terms of Use](https://vauntzteam.github.io/terms/)
- [Support](https://vauntzteam.github.io/support/): Apple's Support URL
- [Delete your account](https://vauntzteam.github.io/delete-account/): Google Play's account-deletion URL

## How it's built

- **Sources** live in `src/`:
  - `src/content/` holds the page texts in Markdown;
  - `src/assets/style.css` holds the styles;
  - `src/tools/build.py` holds the home and 404 copy, the "not launched yet" notices, the version and the date.
- **Built pages** sit at the repo root, which GitHub Pages serves from the `main` branch. Don't edit them by hand.
- **To change a page:**
  1. Edit `src/`.
  2. For a legal change, update `UPDATED` and `VERSION` in `build.py` and add a line to `CHANGES`.
  3. Run `python3 src/tools/build.py`, check the pages, and push.
  4. Copy the changed text back into `launch-handoff/03`–`06` in the claude.ai project.

There are no cookies, no scripts and no outside requests. The handover is `launch-handoff/07 Website handover.md` in the claude.ai project "Co Parenting App".
