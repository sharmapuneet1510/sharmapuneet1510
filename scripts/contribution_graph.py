#!/usr/bin/env python3
"""Render a self-hosted GitHub contribution graph (dark + light SVG).

Standard library only. Fetches the last-year contribution calendar through
GitHub's GraphQL API and writes two SVGs that the profile README swaps between
with <picture> based on the viewer's colour scheme.

Usage:
    GITHUB_TOKEN=... python scripts/contribution_graph.py --out assets
    python scripts/contribution_graph.py --input fixture.json --out /tmp/x   # offline
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import sys
import urllib.request
from html import escape
from pathlib import Path

GRAPHQL_URL = "https://api.github.com/graphql"

QUERY = """
query($login: String!) {
  user(login: $login) {
    contributionsCollection {
      contributionCalendar {
        totalContributions
        weeks {
          contributionDays { date weekday contributionCount }
        }
      }
    }
  }
}
"""

CELL = 11
GAP = 3
PITCH = CELL + GAP
GRID_LEFT = 44
GRID_TOP = 96
WIDTH = 840
HEIGHT = 330

# Palettes match tools/render.py (the profile's cards and snake) so the
# contribution graph sits with the rest of the README.
THEMES = {
    "dark": {
        "bg": "#080706",
        "border": "#3a342d",
        "title": "#E8DFD8",
        "text": "#E8DFD8",
        "muted": "#cbb59d",
        "accent": "#D4AF37",
        # empty -> most intense (gold)
        "levels": ["#201c17", "#514a42", "#6b6259", "#b09a72", "#D4AF37"],
    },
    "light": {
        "bg": "#FBF7F2",
        "border": "#d8cec1",
        "title": "#1a1613",
        "text": "#1a1613",
        "muted": "#6f6252",
        "accent": "#9a7818",
        "levels": ["#ece4d8", "#cdc4b6", "#b3a897", "#938776", "#9a7818"],
    },
}


def fetch_calendar(login: str, token: str) -> dict:
    body = json.dumps({"query": QUERY, "variables": {"login": login}}).encode()
    req = urllib.request.Request(
        GRAPHQL_URL,
        data=body,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "User-Agent": "contribution-graph-renderer",
        },
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        payload = json.load(resp)
    if payload.get("errors"):
        raise SystemExit(f"GraphQL error: {payload['errors']}")
    user = payload["data"]["user"]
    if user is None:
        raise SystemExit(f"No GitHub user named {login!r}")
    return user["contributionsCollection"]["contributionCalendar"]


def load_fixture(path: str) -> dict:
    with open(path, encoding="utf-8") as fh:
        data = json.load(fh)
    # Accept either the raw GraphQL response or the bare calendar object.
    if "data" in data:
        data = data["data"]["user"]["contributionsCollection"]["contributionCalendar"]
    return data


def flatten(calendar: dict) -> list[dict]:
    """Return every day with its grid position: col = week index, row = weekday (0 = Sunday)."""
    days = []
    for col, week in enumerate(calendar["weeks"]):
        for day in week["contributionDays"]:
            days.append({**day, "col": col, "row": day["weekday"]})
    days.sort(key=lambda d: d["date"])
    return days


def compute_stats(days: list[dict], today: dt.date) -> dict:
    counts = [d["contributionCount"] for d in days]
    active = [d for d in days if d["contributionCount"] > 0]

    longest = run = 0
    prev: dt.date | None = None
    for d in days:
        if d["contributionCount"] > 0:
            cur = dt.date.fromisoformat(d["date"])
            run = run + 1 if prev and (cur - prev).days == 1 else 1
            prev = cur
            longest = max(longest, run)
        else:
            run = 0

    # Current streak: count back from today; today may still be in progress,
    # so a zero today does not break the streak that ended yesterday.
    by_date = {d["date"]: d["contributionCount"] for d in days}
    cursor = today
    if by_date.get(cursor.isoformat(), 0) == 0:
        cursor -= dt.timedelta(days=1)
    current = 0
    while by_date.get(cursor.isoformat(), 0) > 0:
        current += 1
        cursor -= dt.timedelta(days=1)

    peak = max(days, key=lambda d: d["contributionCount"]) if days else None
    return {
        "total": sum(counts),
        "active_days": len(active),
        "current_streak": current,
        "longest_streak": longest,
        "peak": peak,
    }


def levels_for(days: list[dict]) -> dict[str, int]:
    """Map each day to intensity 0-4 using quartiles of non-zero days."""
    nonzero = sorted(d["contributionCount"] for d in days if d["contributionCount"] > 0)
    if not nonzero:
        return {d["date"]: 0 for d in days}

    def quantile(q: float) -> float:
        return nonzero[min(len(nonzero) - 1, int(q * len(nonzero)))]

    cuts = [quantile(0.25), quantile(0.5), quantile(0.75)]
    out = {}
    for d in days:
        c = d["contributionCount"]
        if c == 0:
            out[d["date"]] = 0
        elif c <= cuts[0]:
            out[d["date"]] = 1
        elif c <= cuts[1]:
            out[d["date"]] = 2
        elif c <= cuts[2]:
            out[d["date"]] = 3
        else:
            out[d["date"]] = 4
    return out


def render(days: list[dict], stats: dict, login: str, theme: str, today: dt.date) -> str:
    t = THEMES[theme]
    levels = levels_for(days)
    num_cols = max(d["col"] for d in days) + 1

    parts: list[str] = []
    add = parts.append
    add(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" '
        f'viewBox="0 0 {WIDTH} {HEIGHT}" role="img" '
        f'aria-label="{escape(login)} GitHub contribution graph, last 12 months">'
    )
    add(
        f'<rect x="0.5" y="0.5" width="{WIDTH - 1}" height="{HEIGHT - 1}" rx="12" '
        f'fill="{t["bg"]}" stroke="{t["border"]}"/>'
    )
    add(
        f'<text x="24" y="38" fill="{t["title"]}" font-family="system-ui,-apple-system,Segoe UI,sans-serif" '
        f'font-size="20" font-weight="700">Puneet Sharma\'s Contribution Graph</text>'
    )
    add(
        f'<text x="{WIDTH - 24}" y="38" text-anchor="end" fill="{t["muted"]}" '
        f'font-family="system-ui,sans-serif" font-size="12">'
        f'{stats["total"]:,} contributions in the last year</text>'
    )

    # Month labels: label the first week column in which each month starts
    # (skipping a label that would crowd the one before it).
    last_month = None
    last_label_x = -PITCH * 4
    for day in days:
        if day["row"] != 0:  # a week starts on its Sunday
            continue
        d = dt.date.fromisoformat(day["date"])
        x = GRID_LEFT + day["col"] * PITCH
        if d.month != last_month and x - last_label_x >= PITCH * 3 and day["col"] < num_cols - 1:
            last_month = d.month
            last_label_x = x
            add(
                f'<text x="{x}" y="{GRID_TOP - 10}" fill="{t["muted"]}" '
                f'font-family="system-ui,sans-serif" font-size="11">{d.strftime("%b")}</text>'
            )

    # Weekday labels (Mon / Wed / Fri).
    for row, label in ((1, "Mon"), (3, "Wed"), (5, "Fri")):
        y = GRID_TOP + row * PITCH + CELL - 2
        add(
            f'<text x="{GRID_LEFT - 8}" y="{y}" text-anchor="end" fill="{t["muted"]}" '
            f'font-family="system-ui,sans-serif" font-size="10">{label}</text>'
        )

    # Day cells. Column = weeks since the first day, row = weekday (0 = Sunday).
    for d in days:
        if d["date"] > today.isoformat():
            continue
        x = GRID_LEFT + d["col"] * PITCH
        y = GRID_TOP + d["row"] * PITCH
        fill = t["levels"][levels[d["date"]]]
        tip = f'{d["contributionCount"]} contribution(s) on {d["date"]}'
        add(
            f'<rect x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="2" fill="{fill}">'
            f"<title>{escape(tip)}</title></rect>"
        )

    # Stats strip.
    cards = [
        ("Total", f'{stats["total"]:,}', "last 12 months"),
        ("Current streak", f'{stats["current_streak"]} d', "days in a row"),
        ("Longest streak", f'{stats["longest_streak"]} d', "best run"),
        ("Active days", f'{stats["active_days"]}', "with a contribution"),
    ]
    card_w = (WIDTH - 48 - 3 * 12) / 4
    for i, (label, value, sub) in enumerate(cards):
        x = 24 + i * (card_w + 12)
        y = 232
        add(
            f'<rect x="{x:.1f}" y="{y}" width="{card_w:.1f}" height="76" rx="10" '
            f'fill="none" stroke="{t["border"]}"/>'
        )
        add(
            f'<text x="{x + 14:.1f}" y="{y + 26}" fill="{t["muted"]}" '
            f'font-family="system-ui,sans-serif" font-size="11">{escape(label)}</text>'
        )
        add(
            f'<text x="{x + 14:.1f}" y="{y + 52}" fill="{t["accent"]}" '
            f'font-family="system-ui,sans-serif" font-size="22" font-weight="700">{escape(value)}</text>'
        )
        add(
            f'<text x="{x + 14:.1f}" y="{y + 68}" fill="{t["muted"]}" '
            f'font-family="system-ui,sans-serif" font-size="10">{escape(sub)}</text>'
        )

    # Legend + footer.
    legend_y = GRID_TOP + 7 * PITCH + 14
    lx = WIDTH - 24 - 5 * PITCH - 80
    add(
        f'<text x="{lx - 6}" y="{legend_y + 9}" text-anchor="end" fill="{t["muted"]}" '
        f'font-family="system-ui,sans-serif" font-size="10">Less</text>'
    )
    for i, color in enumerate(t["levels"]):
        add(f'<rect x="{lx + i * PITCH}" y="{legend_y}" width="{CELL}" height="{CELL}" rx="2" fill="{color}"/>')
    add(
        f'<text x="{lx + 5 * PITCH + 2}" y="{legend_y + 9}" fill="{t["muted"]}" '
        f'font-family="system-ui,sans-serif" font-size="10">More</text>'
    )
    add(
        f'<text x="24" y="{legend_y + 9}" fill="{t["muted"]}" font-family="system-ui,sans-serif" '
        f'font-size="10">Updated {today.isoformat()} · self-hosted, refreshed daily</text>'
    )
    add("</svg>")
    return "\n".join(parts) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--login", default=os.environ.get("GITHUB_LOGIN", "sharmapuneet1510"))
    ap.add_argument("--input", help="Use a saved GraphQL response instead of calling the API")
    ap.add_argument("--out", default="assets", help="Output directory for the SVG files")
    args = ap.parse_args()

    if args.input:
        calendar = load_fixture(args.input)
    else:
        token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
        if not token:
            print("Set GITHUB_TOKEN (or GH_TOKEN), or pass --input.", file=sys.stderr)
            return 2
        calendar = fetch_calendar(args.login, token)

    days = flatten(calendar)
    if not days:
        print("Calendar returned no days; refusing to overwrite the graph.", file=sys.stderr)
        return 1

    today = dt.date.today()
    stats = compute_stats(days, today)
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    for theme in THEMES:
        svg = render(days, stats, args.login, theme, today)
        (out_dir / f"contrib-{theme}.svg").write_text(svg, encoding="utf-8")
        print(f"wrote {out_dir / f'contrib-{theme}.svg'}")
    print(json.dumps({k: v for k, v in stats.items() if k != "peak"}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
