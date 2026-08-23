#!/usr/bin/env python3
"""Render the profile SVGs.

Everything the README shows is drawn here and committed to the repo, so the
page never waits on a third-party badge service. Run with a GITHUB_TOKEN in the
environment to refresh the numbers; without one the last committed data.json is
reused and only the artwork is redrawn.

    python3 tools/render.py

Fonts are deliberately generic. GitHub renders README SVGs through an <img>,
which blocks webfonts, so the display face has to be a system serif.
"""

from __future__ import annotations

import json
import os
import pathlib
import sys
import urllib.error
import urllib.request

USER = "sharmapuneet1510"
ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "tools" / "data.json"

SERIF = "Georgia,'Times New Roman','Nimbus Roman',serif"
MONO = "'SFMono-Regular',Consolas,'Liberation Mono',Menlo,monospace"

THEMES = {
    "dark": {
        "suffix": "",
        "ground": "#000000",
        "panel": "#080706",
        "text": "#E8DFD8",
        "gold": "#D4AF37",
        "muted": "#cbb59d",
        "dim": "#6b6259",
        "rule": "#3a342d",
        "grain": 0.055,
        # Monotonic descending ramp: share of code reads as falling luminance,
        # with steps wide enough that adjacent bar segments stay legible.
        "ramp": ["#D4AF37", "#b09a72", "#8a7a68", "#6b6259", "#514a42", "#3a342d"],
    },
    "light": {
        "suffix": "-light",
        "ground": "#F4EEE7",
        "panel": "#FBF7F2",
        "text": "#1a1613",
        "gold": "#9a7818",
        "muted": "#6f6252",
        "dim": "#938776",
        "rule": "#d8cec1",
        "grain": 0.032,
        "ramp": ["#9a7818", "#7d6a4e", "#6f6252", "#938776", "#b3a897", "#cdc4b6"],
    },
}

# The portfolio's reveal curve, reused everywhere so the whole page breathes
# at one tempo.
EASE = "cubic-bezier(.16,1,.3,1)"


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


# --------------------------------------------------------------------------
# data
# --------------------------------------------------------------------------

QUERY = """
{
  user(login: "%s") {
    createdAt
    contributionsCollection {
      totalCommitContributions
      restrictedContributionsCount
      totalPullRequestContributions
    }
    repositories(first: 100, ownerAffiliations: OWNER, isFork: false) {
      totalCount
      nodes { name languages(first: 20) { edges { size node { name } } } }
    }
  }
}
""" % USER


def fetch() -> dict:
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if not token:
        return json.loads(DATA.read_text())

    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY}).encode(),
        headers={
            "Authorization": f"bearer {token}",
            "Content-Type": "application/json",
            "User-Agent": f"{USER}-profile-render",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            payload = json.load(resp)
    except (urllib.error.URLError, TimeoutError) as exc:
        print(f"! api unreachable ({exc}); reusing committed data.json", file=sys.stderr)
        return json.loads(DATA.read_text())

    if "errors" in payload:
        print(f"! api errors {payload['errors']}; reusing data.json", file=sys.stderr)
        return json.loads(DATA.read_text())

    user = payload["data"]["user"]
    contrib = user["contributionsCollection"]

    sizes: dict[str, int] = {}
    for node in user["repositories"]["nodes"]:
        for edge in node["languages"]["edges"]:
            name = edge["node"]["name"]
            sizes[name] = sizes.get(name, 0) + edge["size"]

    total = sum(sizes.values()) or 1
    langs = [
        {"name": n, "pct": round(100 * s / total, 1)}
        for n, s in sorted(sizes.items(), key=lambda kv: -kv[1])
    ][:6]

    data = {
        "commits": contrib["totalCommitContributions"]
        + contrib["restrictedContributionsCount"],
        "prs": contrib["totalPullRequestContributions"],
        "repos": user["repositories"]["totalCount"],
        "since": int(user["createdAt"][:4]),
        "langs": langs,
    }
    DATA.write_text(json.dumps(data, indent=2) + "\n")
    return data


# --------------------------------------------------------------------------
# shared chrome
# --------------------------------------------------------------------------

def grain(t: dict, w: int, h: int) -> str:
    """Film grain. Cheap, static, and the single biggest cue that this is a
    frame rather than a web page."""
    return (
        f'<rect width="{w}" height="{h}" filter="url(#grain)" '
        f'opacity="{t["grain"]}" fill="{t["text"]}"/>'
    )


GRAIN_FILTER = (
    '<filter id="grain" x="0" y="0" width="100%" height="100%">'
    '<feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="3" seed="7"/>'
    '<feColorMatrix type="saturate" values="0"/>'
    '<feComponentTransfer><feFuncA type="linear" slope="1.4"/></feComponentTransfer>'
    '<feComposite operator="in" in2="SourceGraphic"/>'
    "</filter>"
)


def card_frame(t: dict, w: int, h: int, title: str) -> str:
    """The rounded panel + hairline + title shared by the two stat cards."""
    return f"""
<rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="3" fill="{t['panel']}" stroke="{t['rule']}"/>
<rect x="1" y="1" width="{w - 2}" height="3" fill="{t['gold']}" opacity=".55"/>
<text class="rv" style="animation-delay:.15s" x="22" y="38" font-family="{MONO}" font-size="11"
      letter-spacing="3.2" fill="{t['gold']}">{esc(title)}</text>
<line class="draw" style="animation-delay:.3s" x1="22" y1="52" x2="{w - 22}" y2="52"
      stroke="{t['rule']}" stroke-width="1"/>
<g clip-path="url(#cardclip)"><rect class="sheen" x="-200" y="0" width="150" height="{h}" fill="url(#sheen)"/></g>
"""


def card_defs(t: dict, w: int, h: int) -> str:
    return f"""
<clipPath id="cardclip"><rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="3"/></clipPath>
<linearGradient id="sheen" x1="0" y1="0" x2="1" y2="0">
  <stop offset="0%" stop-color="{t['text']}" stop-opacity="0"/>
  <stop offset="50%" stop-color="{t['text']}" stop-opacity=".05"/>
  <stop offset="100%" stop-color="{t['text']}" stop-opacity="0"/>
</linearGradient>
{GRAIN_FILTER}
"""


CARD_CSS = f"""
.rv{{opacity:0;animation:rv .9s {EASE} forwards}}
@keyframes rv{{from{{opacity:0;transform:translateY(8px)}}to{{opacity:1;transform:translateY(0)}}}}
.draw{{stroke-dasharray:600;stroke-dashoffset:600;animation:draw 1.4s {EASE} forwards}}
@keyframes draw{{to{{stroke-dashoffset:0}}}}
.sheen{{animation:sheen 9s ease-in-out 2.5s infinite}}
@keyframes sheen{{0%{{transform:translateX(0)}}55%,100%{{transform:translateX(760px)}}}}
@media (prefers-reduced-motion:reduce){{
  .rv,.draw,.grow{{animation:none;opacity:1;transform:none;stroke-dashoffset:0}}
  .sheen{{animation:none;opacity:0}}
}}
"""


# --------------------------------------------------------------------------
# banner
# --------------------------------------------------------------------------

NAME = "PUNEET SHARMA"
W, H = 1280, 420


def banner(t: dict) -> str:
    advance = 49.0
    n = len(NAME)
    first = W / 2 - (n - 1) * advance / 2

    letters = []
    for i, ch in enumerate(NAME):
        if ch == " ":
            continue
        delay = 0.35 + i * 0.075
        letters.append(
            f'<text class="ltr" style="animation-delay:{delay:.2f}s" '
            f'x="{first + i * advance:.1f}" y="212" text-anchor="middle" '
            f'font-family="{SERIF}" font-size="60" fill="{t["text"]}">{ch}</text>'
        )

    motes = []
    for i, (x, size, dur, delay) in enumerate(
        [(180, 1.6, 17, 0), (395, 1.1, 21, 3.5), (610, 1.9, 15, 7),
         (835, 1.2, 23, 1.8), (1010, 1.5, 19, 5.2), (1150, 1.0, 25, 9)]
    ):
        motes.append(
            f'<circle class="mote" style="animation-duration:{dur}s;animation-delay:{delay}s" '
            f'cx="{x}" cy="352" r="{size}" fill="{t["gold"]}"/>'
        )

    # Camera framing brackets, one per corner of the letterboxed frame.
    brackets = []
    for x, y, dx, dy in [(64, 64, 1, 1), (1216, 64, -1, 1), (64, 356, 1, -1), (1216, 356, -1, -1)]:
        brackets.append(
            f'<path class="rv" style="animation-delay:.9s" d="M{x} {y + 18 * dy}L{x} {y}L{x + 18 * dx} {y}" '
            f'fill="none" stroke="{t["gold"]}" stroke-width="1.5" opacity=".55"/>'
        )

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Puneet Sharma — Lead Architect, AI Systems, Tokyo">
<title>Puneet Sharma — Lead Architect · AI Systems · Tokyo</title>
<defs>
<style type="text/css"><![CDATA[
.ltr{{opacity:0;animation:ltr 1.1s {EASE} forwards}}
@keyframes ltr{{from{{opacity:0;transform:translateY(18px);filter:blur(6px)}}
              to{{opacity:1;transform:translateY(0);filter:blur(0)}}}}
.rv{{opacity:0;animation:rv 1.1s {EASE} forwards}}
@keyframes rv{{from{{opacity:0;transform:translateY(10px)}}to{{opacity:1;transform:translateY(0)}}}}
.draw{{stroke-dasharray:320;stroke-dashoffset:320;animation:draw 1.6s {EASE} 1.35s forwards}}
@keyframes draw{{to{{stroke-dashoffset:0}}}}
.frameline{{stroke-dasharray:1160;stroke-dashoffset:1160;animation:fl 2.2s {EASE} .1s forwards}}
@keyframes fl{{to{{stroke-dashoffset:0}}}}
.mote{{opacity:0;animation-name:rise;animation-timing-function:linear;animation-iteration-count:infinite}}
@keyframes rise{{0%{{transform:translateY(0);opacity:0}}18%{{opacity:.5}}
                82%{{opacity:.5}}100%{{transform:translateY(-250px);opacity:0}}}}
.pulse{{animation:pulse 3.4s ease-in-out 2s infinite}}
@keyframes pulse{{0%,100%{{opacity:.25}}50%{{opacity:.9}}}}
@media (prefers-reduced-motion:reduce){{
  .ltr,.rv,.draw,.frameline{{animation:none;opacity:1;transform:none;filter:none;stroke-dashoffset:0}}
  .mote{{animation:none;opacity:.4}}
  .pulse{{animation:none;opacity:.7}}
}}
]]></style>
<radialGradient id="vig" cx="50%" cy="46%" r="72%">
  <stop offset="0%" stop-color="{t['ground']}" stop-opacity="0"/>
  <stop offset="62%" stop-color="{t['ground']}" stop-opacity="0"/>
  <stop offset="100%" stop-color="{'#000' if t['suffix'] == '' else '#c9bdae'}" stop-opacity=".85"/>
</radialGradient>
<radialGradient id="key" cx="50%" cy="48%" r="46%">
  <stop offset="0%" stop-color="{t['gold']}" stop-opacity=".085"/>
  <stop offset="100%" stop-color="{t['gold']}" stop-opacity="0"/>
</radialGradient>
{GRAIN_FILTER}
</defs>

<rect width="{W}" height="{H}" fill="{t['ground']}"/>
<rect width="{W}" height="{H}" fill="url(#key)"/>

{''.join(motes)}

<line class="frameline" x1="64" y1="64" x2="1216" y2="64" stroke="{t['gold']}" stroke-width="1" opacity=".45"/>
<line class="frameline" x1="64" y1="356" x2="1216" y2="356" stroke="{t['gold']}" stroke-width="1" opacity=".45"/>
{''.join(brackets)}

<text class="rv" style="animation-delay:.55s" x="64" y="44" font-family="{MONO}" font-size="11"
      letter-spacing="3" fill="{t['dim']}">SCENE 01 — ARCHITECTURE</text>
<text class="rv" style="animation-delay:.65s" x="1216" y="44" text-anchor="end" font-family="{MONO}"
      font-size="11" letter-spacing="3" fill="{t['dim']}">35.6762°N 139.6503°E</text>

{''.join(letters)}

<line class="draw" x1="480" y1="248" x2="800" y2="248" stroke="{t['gold']}" stroke-width="1"/>

<text class="rv" style="animation-delay:1.55s" x="{W // 2}" y="286" text-anchor="middle"
      font-family="{MONO}" font-size="13" letter-spacing="6.5" fill="{t['muted']}">LEAD ARCHITECT · AI SYSTEMS · TOKYO</text>
<text class="rv" style="animation-delay:1.75s" x="{W // 2}" y="322" text-anchor="middle"
      font-family="{SERIF}" font-style="italic" font-size="19" fill="{t['dim']}">capital markets infrastructure → systems that run themselves</text>

<text class="rv" style="animation-delay:1.95s" x="64" y="384" font-family="{MONO}" font-size="10.5"
      letter-spacing="2.5" fill="{t['dim']}">EST. 2014</text>
<circle class="pulse" cx="1122" cy="380" r="3.5" fill="{t['gold']}"/>
<text class="rv" style="animation-delay:1.95s" x="1216" y="384" text-anchor="end" font-family="{MONO}"
      font-size="10.5" letter-spacing="2.5" fill="{t['dim']}">SHIPPING</text>

{grain(t, W, H)}
</svg>
"""


# --------------------------------------------------------------------------
# stat cards
# --------------------------------------------------------------------------

CW, CH = 496, 236


def stats(t: dict, d: dict) -> str:
    rows = [
        ("COMMITS · PAST YEAR", f"{d['commits']:,}"),
        ("PULL REQUESTS", f"{d['prs']:,}"),
        ("REPOSITORIES", f"{d['repos']:,}"),
        ("YEARS SHIPPING", str(2026 - d["since"])),
    ]

    out = []
    y = 88
    for i, (label, value) in enumerate(rows):
        delay = 0.5 + i * 0.13
        # Dotted leader between label and figure — the table-of-contents look,
        # which keeps the numbers from posturing.
        out.append(f"""
<g class="rv" style="animation-delay:{delay:.2f}s">
  <text x="22" y="{y}" font-family="{MONO}" font-size="11" letter-spacing="2.2" fill="{t['muted']}">{label}</text>
  <line x1="{24 + len(label) * 7.4:.0f}" y1="{y - 4}" x2="{CW - 96}" y2="{y - 4}"
        stroke="{t['rule']}" stroke-width="1" stroke-dasharray="1 4"/>
  <text x="{CW - 22}" y="{y + 3}" text-anchor="end" font-family="{SERIF}" font-size="30" fill="{t['text']}">{value}</text>
</g>""")
        y += 42

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {CW} {CH}" width="{CW}" height="{CH}" role="img" aria-label="GitHub activity">
<title>Activity</title>
<defs><style type="text/css"><![CDATA[{CARD_CSS}]]></style>{card_defs(t, CW, CH)}</defs>
<rect width="{CW}" height="{CH}" fill="{t['ground']}"/>
{card_frame(t, CW, CH, 'THE LEDGER')}
{''.join(out)}
{grain(t, CW, CH)}
</svg>
"""


def langs(t: dict, d: dict) -> str:
    items = d["langs"][:6]
    total = sum(i["pct"] for i in items) or 1
    ramp = t["ramp"]

    bar, legend = [], []
    x = 22.0
    span = CW - 44
    for i, item in enumerate(items):
        w = span * item["pct"] / total
        bar.append(
            f'<rect class="grow" style="animation-delay:{0.55 + i * 0.09:.2f}s;transform-origin:{x:.1f}px 0" '
            f'x="{x:.1f}" y="72" width="{w:.1f}" height="9" fill="{ramp[i % len(ramp)]}"/>'
        )
        x += w

    for i, item in enumerate(items):
        col, row = i % 2, i // 2
        lx = 22 + col * 236
        ly = 116 + row * 34
        legend.append(f"""
<g class="rv" style="animation-delay:{0.85 + i * 0.08:.2f}s">
  <rect x="{lx}" y="{ly - 9}" width="9" height="9" fill="{ramp[i % len(ramp)]}"/>
  <text x="{lx + 18}" y="{ly}" font-family="{MONO}" font-size="11.5" fill="{t['muted']}">{esc(item['name'])}</text>
  <text x="{lx + 208}" y="{ly}" text-anchor="end" font-family="{MONO}" font-size="11.5" fill="{t['text']}">{item['pct']:.1f}%</text>
</g>""")

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {CW} {CH}" width="{CW}" height="{CH}" role="img" aria-label="Languages by share of code">
<title>Languages</title>
<defs><style type="text/css"><![CDATA[{CARD_CSS}
.grow{{transform:scaleX(0);animation:grow 1.5s {EASE} forwards}}
@keyframes grow{{to{{transform:scaleX(1)}}}}
]]></style>{card_defs(t, CW, CH)}</defs>
<rect width="{CW}" height="{CH}" fill="{t['ground']}"/>
{card_frame(t, CW, CH, 'THE MATERIAL')}
{''.join(bar)}
{''.join(legend)}
{grain(t, CW, CH)}
</svg>
"""


def main() -> None:
    data = fetch()
    for theme in THEMES.values():
        s = theme["suffix"]
        (ROOT / f"banner{s}.svg").write_text(banner(theme))
        (ROOT / f"stats{s}.svg").write_text(stats(theme, data))
        (ROOT / f"langs{s}.svg").write_text(langs(theme, data))
    print(f"rendered 6 svgs · {data['commits']} commits · {len(data['langs'])} languages")


if __name__ == "__main__":
    main()
