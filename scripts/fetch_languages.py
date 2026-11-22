"""Sum language bytes across the user's own public repos -> data/languages.json.

Works without a token (60 API calls/hour); CI passes GITHUB_TOKEN for a higher limit.
"""

import json
import os
from collections import Counter

import requests

USER = (
    os.environ.get("GH_USER")
    or os.environ.get("GITHUB_REPOSITORY_OWNER")
    or "YosiaCoKR"
)
TOP = 6

s = requests.Session()
s.headers["Accept"] = "application/vnd.github+json"
if os.environ.get("GITHUB_TOKEN"):
    s.headers["Authorization"] = f"Bearer {os.environ['GITHUB_TOKEN']}"


def get(url):
    r = s.get(url, timeout=30)
    r.raise_for_status()
    return r.json()


repos, page = [], 1
while batch := get(
    f"https://api.github.com/users/{USER}/repos?type=owner&per_page=100&page={page}"
):
    repos += batch
    page += 1

totals = Counter()
for repo in repos:
    if not repo["fork"]:  # a fork's code isn't the user's own
        totals.update(get(repo["languages_url"]))
assert totals, f"no language data for {USER} - no public non-fork repos?"

all_bytes = sum(totals.values())
os.makedirs("data", exist_ok=True)
json.dump(
    {
        "user": USER,
        "repos": sum(not r["fork"] for r in repos),
        "languages": [
            {"name": name, "bytes": b, "pct": round(100 * b / all_bytes, 1)}
            for name, b in totals.most_common(TOP)
        ],
    },
    open("data/languages.json", "w"),
    indent=1,
)
print(f"{USER}: {len(totals)} languages across {len(repos)} repos")
