"""Generate the profile SVGs: hero, pulse, system, timeline, stack (dark + light).

Usage: python3 scripts/gen_assets.py assets
Every panel is a rounded card with the same header, so the README reads as one document.
Colours follow GitHub's own palette so the cards sit naturally on either theme.
"""
import datetime as dt
import json
import os
import sys

OUT = sys.argv[1] if len(sys.argv) > 1 else "assets"
os.makedirs(OUT, exist_ok=True)
HERE = os.path.dirname(os.path.abspath(__file__))

THEMES = {
    "dark": dict(bg="#0d1117", card="#0d1117", line="#30363d", soft="#21262d", text="#e6edf3",
                 muted="#9198a1", dim="#6e7681", accent="#4493f8"),
    "light": dict(bg="#ffffff", card="#ffffff", line="#d1d9e0", soft="#eff2f5", text="#1f2328",
                  muted="#59636e", dim="#818b98", accent="#0969da"),
}
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, 'Liberation Mono', monospace"
SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', Helvetica, Arial, sans-serif"
W = 1200


# ---------------------------------------------------------------- primitives
def text(t, x, y, s, size=13, fill="text", anchor="start", weight=400, font=SANS, spacing=0):
    return (f'<text x="{x}" y="{y}" font-family="{font}" font-size="{size}" font-weight="{weight}" '
            f'fill="{t[fill]}" text-anchor="{anchor}" letter-spacing="{spacing}">{s}</text>')


def cap(t, x, y, s, anchor="start", fill="dim"):
    """Small uppercase caption used for field labels."""
    return text(t, x, y, s, 10, fill, anchor, 500, MONO, 1.6)


def card(t, H, title=None, meta=None, aria=""):
    """Open an SVG with a rounded card and an optional header row."""
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
           f'role="img" aria-label="{aria}">',
           f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="12" fill="{t["card"]}" stroke="{t["line"]}"/>']
    if title:
        out.append(text(t, 28, 29, title, 14, "text", weight=600))
        if meta:
            out.append(text(t, W - 28, 29, meta, 11, "dim", "end", font=MONO, spacing=0.4))
        out.append(f'<line x1="1" y1="46" x2="{W-1}" y2="46" stroke="{t["line"]}"/>')
    return out


def close(parts):
    parts.append("</svg>\n")
    return "\n".join(parts)


def pill(t, x, y, s):
    w = int(len(s) * 7.0) + 26
    return w, (f'<rect x="{x}" y="{y}" width="{w}" height="26" rx="13" fill="{t["soft"]}"/>'
               + text(t, x + w / 2, y + 17, s, 12, "muted", "middle", 500))


def pulse_dot(t, cx, cy):
    return (f'<circle cx="{cx}" cy="{cy}" r="4" fill="{t["accent"]}"/>'
            f'<circle cx="{cx}" cy="{cy}" r="4" fill="none" stroke="{t["accent"]}">'
            f'<animate attributeName="r" values="4;10" dur="2.6s" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values="0.6;0" dur="2.6s" repeatCount="indefinite"/></circle>')


# ---------------------------------------------------------------- hero
def hero(t):
    H = 230
    p = card(t, H, aria="Krirk Klomkliang, full-stack developer with a backend focus, Bangkok, Thailand")
    p.append(cap(t, 32, 58, "FULL-STACK DEVELOPER · BACKEND FOCUS", fill="accent"))
    p.append(text(t, 30, 108, "Krirk Klomkliang", 44, "text", weight=600, spacing=-0.6))
    p.append(text(t, 32, 142, "I build Go services and Vue / Next.js frontends for real-time", 16, "muted"))
    p.append(text(t, 32, 164, "messaging, payments and SMS platforms.", 16, "muted"))
    x = 32
    for s in ["Go", "Distributed systems", "Hexagonal architecture", "Observability"]:
        w, svg = pill(t, x, 184, s)
        p.append(svg)
        x += w + 8

    # facts panel
    p.append(f'<line x1="880" y1="28" x2="880" y2="{H-28}" stroke="{t["line"]}"/>')
    cols, rows = [910, 1060], [66, 136]
    facts = [("LOCATION", "Bangkok, Thailand"), ("EXPERIENCE", "Since 2023"),
             ("FOCUS", "Backend · Go"), ("STATUS", "Open to roles")]
    for i, (k, v) in enumerate(facts):
        cx, cy = cols[i % 2], rows[i // 2]
        p.append(cap(t, cx, cy, k))
        if k == "STATUS":
            p.append(pulse_dot(t, cx + 4, cy + 20))
            p.append(text(t, cx + 16, cy + 25, v, 15, "text", weight=500))
        else:
            p.append(text(t, cx, cy + 25, v, 15, "text", weight=500))
    return close(p)


# ---------------------------------------------------------------- activity
def _ago(now_iso, then_iso):
    now = dt.datetime.fromisoformat(now_iso.replace("Z", "+00:00"))
    then = dt.datetime.fromisoformat(then_iso.replace("Z", "+00:00"))
    s = int((now - then).total_seconds())
    if s < 3600:
        return f"{max(s // 60, 1)} min ago"
    if s < 86400:
        return f"{s // 3600} h ago"
    return f"{s // 86400} d ago"


def pulse(t, st):
    H = 150
    p = card(t, H, "GitHub activity", f"updated {st['generated_at'][:10]}",
             f"Public GitHub activity: {st['commits_30d']} commits in the last {st['window_days']} days")
    for x in (420, 840):
        p.append(f'<line x1="{x}" y1="62" x2="{x}" y2="{H-18}" stroke="{t["line"]}"/>')

    # commits
    p.append(cap(t, 28, 74, f"COMMITS · LAST {st['window_days']} DAYS"))
    days = st["contributions_by_day"]
    mx = max([d["count"] for d in days] + [1])
    base, hmax = 128, 40
    for i, d in enumerate(days):
        h = max(2, round(d["count"] / mx * hmax)) if d["count"] else 2
        col = t["accent"] if d["count"] else t["soft"]
        p.append(f'<rect x="{28 + i*9}" y="{base-h}" width="6" height="{h}" rx="1" fill="{col}"/>')
    p.append(text(t, 396, 128, str(st["commits_30d"]), 32, "text", "end", 600))

    # languages
    lx, lw = 448, 364
    p.append(cap(t, lx, 74, "LANGUAGES · PUBLIC REPOS"))
    shades = [1.0, 0.72, 0.52, 0.36, 0.24]
    x = lx
    for i, lang in enumerate(st["languages"]):
        w = max(2, round(lang["share"] * lw) - 2)
        r = ' rx="3"' if i in (0, len(st["languages"]) - 1) else ""
        p.append(f'<rect x="{x}" y="90" width="{w}" height="8"{r} fill="{t["accent"]}" opacity="{shades[i]}"/>')
        x += w + 2
    x = lx
    for i, lang in enumerate(st["languages"]):
        s = f"{lang['name']} {round(lang['share']*100)}%"
        if x + 12 + len(s) * 6.8 > lx + lw:
            break
        p.append(f'<rect x="{x}" y="113" width="8" height="8" rx="2" fill="{t["accent"]}" opacity="{shades[i]}"/>')
        p.append(text(t, x + 14, 122, s, 12, "muted"))
        x += 14 + len(s) * 6.8 + 16

    # last push / repos
    lp = st.get("last_push") or {"repo": "-", "at": st["generated_at"]}
    p.append(cap(t, 868, 74, "LAST PUSH"))
    p.append(text(t, 868, 102, lp["repo"], 16, "text", weight=600))
    p.append(text(t, 868, 124, _ago(st["generated_at"], lp["at"]), 12, "muted"))
    p.append(cap(t, W - 28, 74, "PUBLIC REPOS", "end"))
    p.append(text(t, W - 28, 128, str(st["public_repos"]), 32, "text", "end", 600))
    return close(p)


# ---------------------------------------------------------------- architecture
def node(t, x, y, name, sub, accent=False):
    col = t["accent"] if accent else t["text"]
    return (f'<rect x="{x-6}" y="{y-6}" width="12" height="12" rx="3" fill="{t["card"]}" stroke="{col}" stroke-width="1.5"/>'
            + text(t, x, y + 30, name, 14, "text", "middle", 600)
            + text(t, x, y + 48, sub, 11, "dim", "middle", font=MONO))


def system(t):
    H = 310
    Y = 160
    xs = [90, 310, 530, 750]
    stores = [(940, 72, "PostgreSQL", "source of truth"), (940, 116, "MongoDB", "documents"),
              (940, 160, "Redis", "cache · sessions"), (940, 204, "RabbitMQ", "events → workers"),
              (940, 248, "ClickHouse", "analytics")]
    rail = f"M {xs[0]} {Y} L {xs[3]} {Y}"
    p = card(t, H, "Architecture", "how I structure a Go service",
             "Typical service: client, Gin HTTP edge, framework-free domain core, ports, then PostgreSQL, MongoDB, Redis, RabbitMQ, ClickHouse and workers")
    p.append(f'<path d="{rail}" stroke="{t["muted"]}" stroke-width="1.25" fill="none"/>')
    for sx, sy, _, _ in stores:
        p.append(f'<path d="M {xs[3]} {Y} C {xs[3]+110} {Y}, {sx-120} {sy}, {sx} {sy}" stroke="{t["line"]}" stroke-width="1.25" fill="none"/>')
    p.append(f'<rect x="{xs[2]-86}" y="{Y-40}" width="172" height="100" rx="10" fill="none" stroke="{t["accent"]}" stroke-dasharray="4 4" opacity="0.7"/>')
    p.append(cap(t, xs[2], Y - 50, "FRAMEWORK-FREE CORE", "middle", "accent"))
    p.append(node(t, xs[0], Y, "Client", "Vue · Next.js"))
    p.append(node(t, xs[1], Y, "HTTP edge", "Gin · auth"))
    p.append(node(t, xs[2], Y, "Domain", "services · rules", accent=True))
    p.append(node(t, xs[3], Y, "Ports", "interfaces"))
    for sx, sy, n, sub in stores:
        p.append(f'<circle cx="{sx}" cy="{sy}" r="5" fill="{t["card"]}" stroke="{t["text"]}" stroke-width="1.5"/>')
        p.append(text(t, sx + 16, sy + 5, n, 14, "text", weight=600))
        p.append(text(t, sx + 112, sy + 5, sub, 11, "dim", font=MONO))
    p.append(f'''<circle r="3.5" fill="{t["accent"]}">
  <animateMotion dur="4.5s" repeatCount="indefinite" path="{rail} C {xs[3]+110} {Y}, 830 72, 940 72"/>
  <animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.06;0.92;1" dur="4.5s" repeatCount="indefinite"/>
</circle>''')
    p.append(f'<line x1="1" y1="{H-44}" x2="{W-1}" y2="{H-44}" stroke="{t["line"]}"/>')
    p.append(cap(t, 28, H - 18, "OBSERVABILITY"))
    p.append(text(t, 150, H - 18, "Loki · Tempo · Mimir · Grafana · Prometheus", 12, "muted"))
    p.append(text(t, W - 28, H - 18, "Shipped with Docker and GitHub Actions", 12, "muted", "end"))
    return close(p)


# ---------------------------------------------------------------- experience
def timeline(t):
    H = 210
    Y = 92
    stops = [
        (80, "Apr – Jun 2023", "Intern Developer", "Zip Event",
         "Public-space booking platform, Bangkok", "ASP.NET MVC · MongoDB · Bootstrap"),
        (460, "Mar 2024 – Mar 2025", "Programmer", "Tech Horizon",
         "Payment gateway for the Japanese market", "PCI DSS · batch & parallel processing"),
        (840, "May 2025 – Present", "Full-Stack Developer", "Real-time chat · SMS platform",
         "High-traffic APIs and observability", "Go · Gin · Vue (TS) · RabbitMQ · ClickHouse"),
    ]
    p = card(t, H, "Experience", "2023 – present",
             "Experience: Intern Developer at Zip Event 2023; Programmer at Tech Horizon 2024 to 2025; Full-Stack Developer since 2025")
    p.append(f'<line x1="40" y1="{Y}" x2="{W-40}" y2="{Y}" stroke="{t["line"]}" stroke-width="1.25"/>')
    for i, (x, when, role, org, l3, l4) in enumerate(stops):
        cur = i == len(stops) - 1
        p.append(text(t, x, Y - 16, when, 11, "dim", font=MONO, spacing=0.3))
        if cur:
            p.append(pulse_dot(t, x + 5, Y))
        else:
            p.append(f'<circle cx="{x+5}" cy="{Y}" r="5" fill="{t["card"]}" stroke="{t["muted"]}" stroke-width="1.5"/>')
        p.append(text(t, x, Y + 34, role, 16, "text", weight=600))
        p.append(text(t, x, Y + 54, org, 13, "accent" if cur else "muted", weight=500))
        p.append(text(t, x, Y + 76, l3.replace("&", "&amp;"), 12, "muted"))
        p.append(text(t, x, Y + 94, l4.replace("&", "&amp;"), 11, "dim", font=MONO))
    return close(p)


# ---------------------------------------------------------------- stack
ICONS = json.load(open(os.path.join(HERE, "icons.json")))
GROUPS = [
    ("LANGUAGES", [("go", "Go"), ("typescript", "TypeScript"), ("python", "Python"), ("php", "PHP")]),
    ("BACKEND", [("gin", "Gin"), ("springboot", "Spring Boot"), ("dotnet", ".NET")]),
    ("FRONTEND", [("vuedotjs", "Vue"), ("nuxt", "Nuxt"), ("nextdotjs", "Next.js"), ("tailwindcss", "Tailwind")]),
    ("DATA", [("postgresql", "PostgreSQL"), ("mongodb", "MongoDB"), ("redis", "Redis"),
              ("rabbitmq", "RabbitMQ"), ("clickhouse", "ClickHouse")]),
    ("DEVOPS", [("docker", "Docker"), ("githubactions", "Actions"), ("grafana", "Grafana"),
                ("prometheus", "Prometheus")]),
]
ROWS = [GROUPS[:3], GROUPS[3:]]


def stack(t):
    H = 300
    cell, icon, gap = 80, 26, 36
    p = card(t, H, "Technical skills", "tools I use day to day",
             "Skills: Go, TypeScript, Python, PHP; Gin, Spring Boot, .NET; Vue, Nuxt, Next.js, Tailwind; "
             "PostgreSQL, MongoDB, Redis, RabbitMQ, ClickHouse; Docker, GitHub Actions, Grafana, Prometheus")
    row_h = (H - 46) // 2
    p.append(f'<line x1="28" y1="{46 + row_h}" x2="{W-28}" y2="{46 + row_h}" stroke="{t["soft"]}"/>')
    for ri, groups in enumerate(ROWS):
        top = 46 + ri * row_h
        x = 28
        for gi, (name, items) in enumerate(groups):
            p.append(cap(t, x, top + 30, name))
            for slug, label in items:
                cx = x + cell / 2
                iy = top + 48
                p.append(f'<g transform="translate({cx - icon/2:.1f} {iy}) scale({icon/24:.4f})">'
                         f'<path d="{ICONS[slug]}" fill="{t["text"]}"/></g>')
                p.append(text(t, cx, iy + icon + 22, label, 12, "muted", "middle"))
                x += cell
            if gi < len(groups) - 1:
                x += gap
                p.append(f'<line x1="{x - gap/2}" y1="{top + 18}" x2="{x - gap/2}" y2="{top + row_h - 14}" stroke="{t["soft"]}"/>')
    return close(p)


# ---------------------------------------------------------------- build
STATS_PATH = os.path.join(HERE, "..", "data", "stats.json")
STATS = json.load(open(STATS_PATH)) if os.path.exists(STATS_PATH) else None

for name, t in THEMES.items():
    files = {"hero": hero(t), "system": system(t), "timeline": timeline(t), "stack": stack(t)}
    if STATS:
        files["pulse"] = pulse(t, STATS)
    for key, svg in files.items():
        with open(f"{OUT}/{key}-{name}.svg", "w") as f:
            f.write(svg)
print("written:", sorted(os.listdir(OUT)))
