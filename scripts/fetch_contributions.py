"""Scrape the public contribution calendar (no token) -> data/contributions.json."""
import json
import os
import re
from collections import Counter

import requests
from bs4 import BeautifulSoup

USER = os.environ.get("GH_USER") or os.environ.get("GITHUB_REPOSITORY_OWNER") or "YosiaCoKR"

html = requests.get(f"https://github.com/users/{USER}/contributions", timeout=30)
html.raise_for_status()
soup = BeautifulSoup(html.text, "html.parser")

tips = {t["for"]: t.get_text() for t in soup.select("tool-tip[for]")}
days = []
for td in soup.select("td.ContributionCalendar-day[data-date]"):
    dow, week = map(int, td["id"].rsplit("-", 2)[1:])  # contribution-day-component-<dow>-<week>
    m = re.match(r"(\d[\d,]*) contribution", tips.get(td["id"], ""))
    days.append({"date": td["data-date"], "count": int(m[1].replace(",", "")) if m else 0,
                 "level": int(td["data-level"]), "week": week, "dow": dow})
days.sort(key=lambda d: d["date"])
assert days, "no contribution cells found - did GitHub change the markup?"

longest = run = 0
for d in days:
    run = run + 1 if d["count"] else 0
    longest = max(longest, run)
current = 0
for d in reversed(days):
    if d["count"]:
        current += 1
    elif current or d is not days[-1]:  # today having 0 yet doesn't break the streak
        break

months = Counter()
for d in days:
    months[d["date"][:7]] += d["count"]
best = max(days, key=lambda d: d["count"])

os.makedirs("data", exist_ok=True)
json.dump({"user": USER, "total": sum(d["count"] for d in days), "current_streak": current,
           "longest_streak": longest, "best_day": {"date": best["date"], "count": best["count"]},
           "months": dict(months), "days": days}, open("data/contributions.json", "w"), indent=1)
print(f"{USER}: {len(days)} days, {sum(months.values())} contributions")
