"""
Checks whether GH_USERNAME has authored any commit today (UTC date),
across public AND private repos the PAT can see.

Writes has_commits=true/false to $GITHUB_OUTPUT so the workflow can
decide whether to run the fallback step.
"""
import os
import sys
import datetime
import requests

USERNAME = os.environ["GH_USERNAME"]
TOKEN = os.environ["GH_PAT"]

today = datetime.datetime.utcnow().strftime("%Y-%m-%d")

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/vnd.github+json",
}

# GitHub's commit Search API — searches public repos + private repos
# the token's owner has access to.
query = f"author:{USERNAME} author-date:>={today}"
resp = requests.get(
    "https://api.github.com/search/commits",
    headers=headers,
    params={"q": query, "per_page": 1},
    timeout=15,
)

if resp.status_code != 200:
    print(f"Warning: search API returned {resp.status_code}: {resp.text}", file=sys.stderr)
    # Fail safe: assume commits exist so we don't spam a commit on an API hiccup
    has_commits = True
else:
    total = resp.json().get("total_count", 0)
    has_commits = total > 0

print(f"Commits found today for {USERNAME}: {has_commits}")

gh_output = os.environ.get("GITHUB_OUTPUT")
if gh_output:
    with open(gh_output, "a") as f:
        f.write(f"has_commits={'true' if has_commits else 'false'}\n")
