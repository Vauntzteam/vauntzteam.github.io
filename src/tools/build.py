#!/usr/bin/env python3
"""Build the Evenstep website. Sources live in src/; the built pages go to the repo root,
which GitHub Pages serves from the main branch.

Edit the Markdown in src/content/, update UPDATED and VERSION below, then run:
    python3 src/tools/build.py
"""
import html, re, shutil
from pathlib import Path
import markdown

ROOT = Path(__file__).resolve().parent.parent          # src/
OUT = ROOT.parent                                       # repo root (published)
GENERATED = ["index.html", "404.html", "favicon.svg", "apple-touch-icon.png", ".nojekyll", "assets"]
UPDATED = "22 October 2026"
VERSION = "1.0 (pre-launch)"
EMAIL = "vauntz.team@gmail.com"

LOGO = ('<svg viewBox="14 14 36 36" aria-hidden="true"><circle class="lgn" cx="23.4" cy="23.4" r="7.2"/>'
        '<rect class="lgc" x="33.7" y="17.1" width="13.2" height="13.2" rx="3.5"/>'
        '<rect class="lgc" x="17.1" y="33.7" width="13.2" height="13.2" rx="3.5"/>'
        '<circle class="lgn" cx="40.6" cy="40.6" r="7.2"/></svg>')

LAUNCH = "the day Evenstep is first released (see the note below)"
PAGES = {
    "privacy": dict(
        title="Privacy Policy", h1="Privacy Policy", toc=True, legal=True,
        desc="How Evenstep, the co-parenting app, collects, uses and protects your data.",
        notice="<strong>Evenstep hasn't launched yet.</strong> The parts of this policy about our website and emails to us apply now. "
               "The rest takes effect on the day the app is first released, including to testers, and we'll show that date here."),
    "terms": dict(
        title="Terms of Use", h1="Terms of Use", toc=True, legal=True,
        desc="The terms for using Evenstep and the Evenstep Plus subscription.",
        notice="<strong>Evenstep hasn't launched yet.</strong> These Terms take effect on the day the app is first released, "
               "including to testers, and we'll show that date here. Until then, they explain the rules the app will have."),
    "support": dict(
        title="Support", h1="Support", toc=False, legal=False,
        desc="Get help with Evenstep: subscriptions, refunds, records and your account.",
        notice="<strong>Evenstep isn't in the App Store or Google Play yet.</strong> You can still email us with any question."),
    "delete-account": dict(
        title="Delete your account", h1="Delete your Evenstep account", toc=False, legal=False,
        desc="How to delete your Evenstep account, with or without the app, and what is deleted or kept.",
        notice="<strong>Evenstep hasn't launched yet, so there are no accounts to delete.</strong> This page explains how deletion will work."),
}
NAV = [("support", "Support"), ("privacy", "Privacy"), ("terms", "Terms")]
FOOT = [("support", "Support"), ("privacy", "Privacy Policy"), ("terms", "Terms of Use"), ("delete-account", "Delete your account")]
CHANGES = f"\n\n## Changes\n\n- **Version {VERSION}, {UPDATED}:** first published.\n"


def slug(value, sep):
    s = re.sub(r"[^\w\s-]", "", value).strip().lower()
    return re.sub(r"[\s_]+", sep, s)


def tables(h):
    """Give every cell its column name (for stacked phone layout) and make the first cell a row header."""
    def one(m):
        t = m.group(0)
        heads = [re.sub("<[^>]+>", "", x).strip() for x in re.findall(r"<th[^>]*>(.*?)</th>", t.split("</thead>")[0], re.S)]
        head, body = t.split("</thead>", 1)

        def row(rm):
            cells = re.findall(r"<td[^>]*>(.*?)</td>", rm.group(0), re.S)
            out = []
            for i, c in enumerate(cells):
                if i == 0:
                    out.append(f'<th scope="row">{c}</th>')
                else:
                    lab = html.escape(heads[i] if i < len(heads) else "", quote=True)
                    out.append(f'<td data-label="{lab}">{c}</td>')
            return "<tr>" + "".join(out) + "</tr>"

        body = re.sub(r"<tr>.*?</tr>", row, body, flags=re.S)
        return '<div class="tbl">' + head + "</thead>" + body + "</div>"

    return re.sub(r"<table>.*?</table>", one, h, flags=re.S)


def links(h, page):
    h = h.replace(EMAIL, f'<a href="mailto:{EMAIL}">{EMAIL}</a>')
    if page == "delete-account":  # step 1 pre-fills the subject line
        h = h.replace(f'<strong><a href="mailto:{EMAIL}">{EMAIL}</a></strong>',
                      f'<strong><a href="mailto:{EMAIL}?subject=Delete%20my%20account">{EMAIL}</a></strong>', 1)
    return h


def shell(page, title, desc, body, h1=None):
    nav = "".join(f'<li><a href="/{k}/"{" aria-current=page" if k == page else ""}>{v}</a></li>' for k, v in NAV)
    foot = "".join(f'<li><a href="/{k}/">{v}</a></li>' for k, v in FOOT)
    full = f"{title} – Evenstep" if page != "home" else "Evenstep – calm co-parenting for two homes"
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{full}</title>
<meta name="description" content="{html.escape(desc, quote=True)}">
<meta name="color-scheme" content="light dark">
<meta name="theme-color" content="#fbeee6" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#0d0f24" media="(prefers-color-scheme: dark)">
<meta name="referrer" content="no-referrer">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="stylesheet" href="/assets/style.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<div class="wrap">
<header class="top">
<a class="brand" href="/" aria-label="Evenstep home">{LOGO}<span>Evenstep</span></a>
<nav aria-label="Site"><ul class="nav">{nav}</ul></nav>
</header>
<main id="main">
{body}
</main>
<footer class="foot">
<nav aria-label="Help and policies"><ul>{foot}</ul></nav>
<p>Evenstep is made by Wong Shou Hong, an individual developer in Singapore.</p>
<p>Email: <a href="mailto:{EMAIL}">{EMAIL}</a></p>
</footer>
</div>
</body>
</html>
"""


def legal_page(key, cfg):
    src = (ROOT / "content" / f"{key}.md").read_text(encoding="utf-8")
    if cfg["legal"]:
        src += CHANGES
    md = markdown.Markdown(extensions=["tables", "sane_lists", "toc"],
                           extension_configs={"toc": {"slugify": slug, "toc_depth": "2"}})
    h = md.convert(src)
    h = links(tables(h), key)
    parts = [f"<h1>{cfg['h1']}</h1>"]
    if cfg["legal"]:
        parts.append(f'<p class="meta">Effective: {LAUNCH}<br>Last updated: {UPDATED}<br>Version {VERSION}</p>')
    if cfg.get("notice"):  # remove a page's notice at the first tester release
        parts.append(f'<div class="notice" role="note"><p>{cfg["notice"]}</p></div>')
    if cfg["toc"]:
        items = "".join(f'<li><a href="#{t["id"]}">{html.escape(t["name"])}</a></li>' for t in md.toc_tokens)
        parts.append(f'<details class="toc"><summary>Jump to a section</summary><ul>{items}</ul></details>')
    parts.append(f'<div class="doc">{h}</div>')
    return shell(key, cfg["title"], cfg["desc"], "\n".join(parts))


SCENE = """<svg class="scene" viewBox="0 0 320 150" role="img" aria-label="Two homes, one navy and one coral, joined by a path under the hills">
<path class="m1" d="M-10 98C50 72 110 74 170 92S280 82 330 94V150H-10z"/>
<path class="m2" d="M-10 116C50 100 120 102 170 114S270 108 330 116V150H-10z"/>
<path class="tr" d="M14 124h20L24 98zM16 110h16L24 84z"/>
<path class="tr" d="M296 126h16L304 105zM297.6 114.8h12.8L304 93.8z"/>
<path class="pth" d="M80 124C130 136 200 136 248 124"/>
<path class="wl" d="M44 118V80h56v38z"/><path class="rf rn" d="M36 82L72 46 108 82z"/>
<rect class="rn" x="66" y="94" width="12" height="24" rx="3"/><rect class="wn" x="50" y="90" width="10" height="10" rx="2"/>
<path class="wl" d="M226 118V80h56v38z"/><path class="rf rc" d="M218 82L254 46 290 82z"/>
<rect class="rc" x="248" y="94" width="12" height="24" rx="3"/><rect class="wn" x="266" y="90" width="10" height="10" rx="2"/>
<path class="tr" d="M-10 142C60 132 130 138 190 142S290 136 330 142V150H-10z"/>
</svg>"""

HOME = f"""<section class="hero">
<h1>One calm place for two homes.</h1>
<p class="lede">Evenstep is a co-parenting app for separated parents. You share one custody calendar, agree on expenses, and keep a clear record of what was said.</p>
<p class="soon">Coming soon to the App Store and Google Play</p>
{SCENE}
</section>
<div class="doc">
<h2>What it does</h2>
<ul>
<li><strong>Custody calendar.</strong> See who has the children each day, plan holidays and ask for swaps that the other parent approves.</li>
<li><strong>Shared expenses.</strong> Log costs with a receipt photo. The other parent approves each one, and you can make Excel or PDF reports.</li>
<li><strong>Messages you can rely on.</strong> Every message is time-stamped and can't be edited or deleted. A tone check on your phone helps you keep it calm.</li>
<li><strong>To-dos and private notes.</strong> Share what needs doing, and keep private notes your co-parent never sees.</li>
</ul>
<p>One Evenstep Plus subscription covers both parents, with a 7-day free trial.</p>
<h2>Questions</h2>
<p>Read our <a href="/support/">support page</a>, or email <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
</div>"""

NOTFOUND = """<h1>This page doesn't exist.</h1>
<div class="doc"><p>Check the address, or go to the <a href="/">Evenstep home page</a>. Our <a href="/support/">support page</a>, <a href="/privacy/">Privacy Policy</a> and <a href="/terms/">Terms of Use</a> are always there.</p></div>"""


def favicon():
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="#fbeee6"/>'
            '<circle cx="23.4" cy="23.4" r="7.2" fill="#2b2c55"/><rect x="33.7" y="17.1" width="13.2" height="13.2" rx="3.5" fill="#ee8c7e"/>'
            '<rect x="17.1" y="33.7" width="13.2" height="13.2" rx="3.5" fill="#ee8c7e"/><circle cx="40.6" cy="40.6" r="7.2" fill="#2b2c55"/></svg>')


def touch_icon(path):
    from PIL import Image, ImageDraw
    n = 180 * 4
    s = n / 64
    im = Image.new("RGB", (n, n), "#fbeee6")
    d = ImageDraw.Draw(im)
    for cx, cy in ((23.4, 23.4), (40.6, 40.6)):
        d.ellipse([(cx - 7.2) * s, (cy - 7.2) * s, (cx + 7.2) * s, (cy + 7.2) * s], fill="#2b2c55")
    for x, y in ((33.7, 17.1), (17.1, 33.7)):
        d.rounded_rectangle([x * s, y * s, (x + 13.2) * s, (y + 13.2) * s], radius=3.5 * s, fill="#ee8c7e")
    im.resize((180, 180), Image.LANCZOS).save(path, optimize=True)


def main():
    for name in GENERATED + list(PAGES):  # only ever remove what this script makes
        p = OUT / name
        if p.is_dir():
            shutil.rmtree(p)
        elif p.exists():
            p.unlink()
    (OUT / "assets").mkdir(parents=True)
    shutil.copy(ROOT / "assets" / "style.css", OUT / "assets" / "style.css")
    (OUT / ".nojekyll").write_text("")
    (OUT / "favicon.svg").write_text(favicon())
    touch_icon(OUT / "apple-touch-icon.png")
    (OUT / "index.html").write_text(shell("home", "Evenstep", "Evenstep is a calm co-parenting app for separated parents: a shared custody calendar, expenses, messages and to-dos.", HOME))
    (OUT / "404.html").write_text(shell("404", "Page not found", "This page doesn't exist.", NOTFOUND))
    for k, cfg in PAGES.items():
        (OUT / k).mkdir()
        (OUT / k / "index.html").write_text(legal_page(k, cfg))
    built = [p for n in GENERATED + list(PAGES) for p in ([OUT / n] if (OUT / n).is_file() else (OUT / n).rglob("*")) if p.is_file()]
    left = [str(p.relative_to(OUT)) for p in built if p.suffix == ".html" if re.search(r"\[[^\]]*\]", re.sub(r"<[^>]+>", "", p.read_text()))]
    print("built", sorted(str(p.relative_to(OUT)) for p in built))
    print("pages with [brackets] :", left or "none")


if __name__ == "__main__":
    main()
