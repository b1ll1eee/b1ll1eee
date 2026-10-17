"""Fetch public GitHub activity for the profile strip and write data/stats.json.

Usage: GITHUB_TOKEN=... python3 scripts/fetch_stats.py [login] [out.json]
Falls back to `gh auth token` when GITHUB_TOKEN is unset. Only public data is used.
"""
import datetime as dt
import json
import os
import subprocess
import sys
import urllib.request

LOGIN = sys.argv[1] if len(sys.argv) > 1 else "b1ll1eee"
OUT = sys.argv[2] if len(sys.argv) > 2 else "data/stats.json"
DAYS = 30
HIDE_LANGUAGES = {"Jupyter Notebook"}  # notebook JSON (with outputs) inflates byte counts

QUERY = """
query($login: String!, $from: DateTime!, $to: DateTime!) {
  user(login: $login) {
    contributionsCollection(from: $from, to: $to) {
      totalCommitContributions
      contributionCalendar { weeks { contributionDays { date contributionCount } } }
    }
    repositories(first: 100, ownerAffiliations: OWNER, privacy: PUBLIC, isFork: false,
                 orderBy: {field: PUSHED_AT, direction: DESC}) {
      totalCount
      nodes {
        name
        pushedAt
        languages(first: 10, orderBy: {field: SIZE, direction: DESC}) {
          edges { size node { name } }
        }
      }
    }
  }
}
"""


def token() -> str:
    t = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if t:
        return t
    return subprocess.check_output(["gh", "auth", "token"], text=True).strip()


def graphql(query: str, variables: dict) -> dict:
    body = json.dumps({"query": query, "variables": variables}).encode()
    req = urllib.request.Request(
        "https://api.github.com/graphql", data=body,
        headers={"Authorization": f"bearer {token()}", "Content-Type": "application/json",
                 "User-Agent": "profile-stats"})
    with urllib.request.urlopen(req, timeout=60) as r:
        data = json.load(r)
    if "errors" in data:
        raise SystemExit(f"GraphQL error: {data['errors']}")
    return data["data"]


def main() -> None:
    now = dt.datetime.now(dt.timezone.utc).replace(microsecond=0)
    start = (now - dt.timedelta(days=DAYS - 1)).replace(hour=0, minute=0, second=0)
    user = graphql(QUERY, {"login": LOGIN, "from": start.isoformat(), "to": now.isoformat()})["user"]

    days = {}
    for week in user["contributionsCollection"]["contributionCalendar"]["weeks"]:
        for d in week["contributionDays"]:
            days[d["date"]] = d["contributionCount"]
    series = []
    for i in range(DAYS):
        day = (start + dt.timedelta(days=i)).date().isoformat()
        series.append({"date": day, "count": days.get(day, 0)})

    lang_bytes: dict[str, int] = {}
    for repo in user["repositories"]["nodes"]:
        for edge in repo["languages"]["edges"]:
            if edge["node"]["name"] in HIDE_LANGUAGES:
                continue
            lang_bytes[edge["node"]["name"]] = lang_bytes.get(edge["node"]["name"], 0) + edge["size"]
    total_bytes = sum(lang_bytes.values()) or 1
    languages = [{"name": n, "share": round(b / total_bytes, 4)}
                 for n, b in sorted(lang_bytes.items(), key=lambda kv: -kv[1])[:5]]

    repos = user["repositories"]["nodes"]
    last = repos[0] if repos else None

    stats = {
        "login": LOGIN,
        "generated_at": now.isoformat(),
        "window_days": DAYS,
        "commits_30d": user["contributionsCollection"]["totalCommitContributions"],
        "contributions_by_day": series,
        "languages": languages,
        "public_repos": user["repositories"]["totalCount"],
        "last_push": {"repo": last["name"], "at": last["pushedAt"]} if last else None,
    }
    os.makedirs(os.path.dirname(OUT) or ".", exist_ok=True)
    with open(OUT, "w") as f:
        json.dump(stats, f, indent=2)
        f.write("\n")
    print(f"wrote {OUT}: {stats['commits_30d']} commits / {DAYS}d, "
          f"{len(languages)} languages, last push {stats['last_push']}")


if __name__ == "__main__":
    main()
