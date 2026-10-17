"""Generate the profile SVGs (white theme): hero, pulse, system, timeline, stack.

Usage: python3 scripts/gen_assets.py assets
Minimal, schematic look on white: hairline rules, monospace labels, one accent for moving parts.
"""
import json
import os
import sys

OUT = sys.argv[1] if len(sys.argv) > 1 else "assets"
os.makedirs(OUT, exist_ok=True)

THEMES = {
    # One theme only: white page, near-black ink, hairline rules, one accent for anything that moves.
    "light": dict(bg="#ffffff", line="#e6e8eb", text="#111827", muted="#6b7280",
                  dim="#9ca3af", accent="#0f766e"),
}
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, 'Liberation Mono', monospace"
SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif"


def label(t, x, y, s, size=12, fill=None, anchor="start", spacing=1.5, bold=False):
    fill = fill or t["muted"]
    w = ' font-weight="600"' if bold else ""
    return (f'<text x="{x}" y="{y}" font-family="{MONO}" font-size="{size}" fill="{fill}" '
            f'text-anchor="{anchor}" letter-spacing="{spacing}"{w}>{s}</text>')


def hero(t):
    W, H = 1200, 240
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Krirk Klomkliang, full-stack developer, Bangkok">
  <rect width="{W}" height="{H}" fill="{t["bg"]}"/>
  <line x1="0" y1="40" x2="{W}" y2="40" stroke="{t["line"]}"/>
  <line x1="0" y1="{H-40}" x2="{W}" y2="{H-40}" stroke="{t["line"]}"/>
  <line x1="820" y1="40" x2="820" y2="{H-40}" stroke="{t["line"]}"/>

  <!-- top rail -->
  {label(t, 24, 25, "B1LL1EEE", 11, t["dim"], spacing=3)}
  {label(t, 300, 25, "FULL-STACK DEVELOPER", 11, t["dim"], spacing=3)}
  {label(t, W-24, 25, "BANGKOK · 13.75N 100.50E", 11, t["dim"], anchor="end", spacing=2)}

  <!-- name -->
  <text x="24" y="118" font-family="{SANS}" font-size="40" font-weight="600" fill="{t["text"]}" letter-spacing="-0.5">Krirk Klomkliang</text>
  <text x="26" y="150" font-family="{MONO}" font-size="14" fill="{t["muted"]}">Go on the server. Vue and Next.js on the screen. Boring in production, on purpose.</text>

  <!-- status panel -->
  {label(t, 844, 76, "STATUS", 10, t["dim"], spacing=3)}
  <circle cx="850" cy="99" r="4" fill="{t["accent"]}">
    <animate attributeName="opacity" values="1;0.25;1" dur="2.4s" repeatCount="indefinite"/>
  </circle>
  <circle cx="850" cy="99" r="4" fill="none" stroke="{t["accent"]}" stroke-width="1">
    <animate attributeName="r" values="4;11" dur="2.4s" repeatCount="indefinite"/>
    <animate attributeName="opacity" values="0.7;0" dur="2.4s" repeatCount="indefinite"/>
  </circle>
  {label(t, 866, 103, "building real-time chat + sms platform", 12, t["text"], spacing=0)}
  {label(t, 844, 134, "STACK", 10, t["dim"], spacing=3)}
  {label(t, 844, 156, "go · typescript · python", 12, t["text"], spacing=0)}
  {label(t, 1050, 134, "SINCE", 10, t["dim"], spacing=3)}
  {label(t, 1050, 156, "2023", 12, t["text"], spacing=0)}
  {label(t, 1118, 134, "OPEN TO", 10, t["dim"], spacing=3)}
  {label(t, 1118, 156, "backend", 12, t["text"], spacing=0)}

  <!-- bottom rail with scanner -->
  <rect x="0" y="{H-40}" width="{W}" height="39" fill="none"/>
  <line x1="24" y1="{H-20}" x2="{W-24}" y2="{H-20}" stroke="{t["line"]}"/>
  <rect x="24" y="{H-21}" width="90" height="2" fill="{t["accent"]}" opacity="0.9">
    <animate attributeName="x" values="24;{W-24-90};24" dur="9s" repeatCount="indefinite" calcMode="spline" keySplines="0.4 0 0.6 1;0.4 0 0.6 1"/>
  </rect>
  {label(t, 24, H-27, "SYS", 9, t["dim"], spacing=3)}
  {label(t, W-24, H-27, "v2026.10", 9, t["dim"], anchor="end", spacing=2)}
</svg>
'''


def node(t, x, y, name, sub=None, accent=False):
    """Small square node with labels underneath."""
    col = t["accent"] if accent else t["text"]
    s = f'<rect x="{x-5}" y="{y-5}" width="10" height="10" fill="{t["bg"]}" stroke="{col}" stroke-width="1.25"/>'
    s += label(t, x, y + 26, name, 12, t["text"], anchor="middle", spacing=0.5)
    if sub:
        s += label(t, x, y + 42, sub, 10, t["dim"], anchor="middle", spacing=0.5)
    return s


def system(t):
    W, H = 1200, 300
    Y = 150          # main rail
    xs = [80, 300, 520, 740]   # client, edge, core, ports
    stores = [(960, 60, "postgres", "truth"), (960, 105, "mongodb", "documents"),
              (960, 150, "redis", "cache"), (960, 195, "rabbitmq", "events"),
              (960, 240, "clickhouse", "analytics")]
    main_path = f"M {xs[0]} {Y} L {xs[3]} {Y}"
    p = [f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Signal path of a typical system: client to Gin edge to framework-free core to ports, then PostgreSQL, MongoDB, Redis, RabbitMQ, ClickHouse and workers, with telemetry underneath">
  <rect width="{W}" height="{H}" fill="{t["bg"]}"/>
  {label(t, 24, 25, "SIGNAL PATH · A TYPICAL SERVICE I BUILD", 11, t["dim"], spacing=3)}
  {label(t, W-24, 25, "GO · PORTS &amp; ADAPTERS", 11, t["dim"], anchor="end", spacing=3)}
  <line x1="0" y1="40" x2="{W}" y2="40" stroke="{t["line"]}"/>

  <!-- rails -->
  <path d="{main_path}" stroke="{t["muted"]}" stroke-width="1" fill="none"/>''']
    # fan-out from ports to stores
    for sx, sy, _, _ in stores:
        p.append(f'<path d="M {xs[3]} {Y} C {xs[3]+100} {Y}, {sx-120} {sy}, {sx} {sy}" stroke="{t["line"]}" stroke-width="1" fill="none"/>')
    # stores -> workers (from rabbitmq)
    p.append(f'<path d="M 1088 195 L 1116 195" stroke="{t["line"]}" stroke-width="1" fill="none"/>')
    # core bracket (framework-free zone)
    p.append(f'<rect x="{xs[2]-80}" y="{Y-38}" width="160" height="94" fill="none" stroke="{t["accent"]}" stroke-width="1" stroke-dasharray="3 4" opacity="0.8"/>')
    p.append(label(t, xs[2], Y-46, "NO FRAMEWORK IMPORTS", 9, t["accent"], anchor="middle", spacing=2))

    # nodes
    p.append(node(t, xs[0], Y, "client", "vue · next.js"))
    p.append(node(t, xs[1], Y, "edge", "gin http · auth"))
    p.append(node(t, xs[2], Y, "core", "domain · services", accent=True))
    p.append(node(t, xs[3], Y, "ports", "interfaces only"))
    for sx, sy, n, sub in stores:
        p.append(f'<circle cx="{sx}" cy="{sy}" r="4" fill="{t["bg"]}" stroke="{t["text"]}" stroke-width="1.25"/>')
        p.append(label(t, sx+14, sy+4, n, 12, t["text"], spacing=0.5))
        p.append(label(t, sx+14+len(n)*7.6+8, sy+4, sub, 10, t["dim"], spacing=0.5))
    p.append(f'<circle cx="1120" cy="195" r="4" fill="{t["bg"]}" stroke="{t["text"]}" stroke-width="1.25"/>')
    p.append(label(t, 1120, 221, "workers", 12, t["text"], anchor="middle", spacing=0.5))

    # moving packet along main rail, then onto one store path
    p.append(f'''<circle r="3" fill="{t["accent"]}">
    <animateMotion dur="4s" repeatCount="indefinite" path="{main_path} C {xs[3]+100} {Y}, 840 60, 960 60" keyPoints="0;1" keyTimes="0;1" calcMode="linear"/>
    <animate attributeName="opacity" values="0;1;1;1;0" keyTimes="0;0.05;0.9;0.97;1" dur="4s" repeatCount="indefinite"/>
  </circle>''')

    # telemetry rail at bottom
    p.append(f'<line x1="0" y1="{H-40}" x2="{W}" y2="{H-40}" stroke="{t["line"]}"/>')
    p.append(label(t, 24, H-16, "TELEMETRY", 10, t["dim"], spacing=3))
    p.append(label(t, 120, H-16, "loki · tempo · mimir · grafana · prometheus", 11, t["muted"], spacing=0.5))
    p.append(label(t, W-24, H-16, "docker · github actions", 11, t["muted"], anchor="end", spacing=0.5))
    p.append("</svg>\n")
    return "\n".join(p)


ICONS = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "icons.json")))
GROUPS = [
    ("LANGUAGES", [("go", "go"), ("typescript", "typescript"), ("python", "python"), ("php", "php")]),
    ("BACKEND", [("gin", "gin"), ("springboot", "spring boot"), ("dotnet", ".net")]),
    ("FRONTEND", [("vuedotjs", "vue"), ("nuxt", "nuxt"), ("nextdotjs", "next.js"), ("tailwindcss", "tailwind")]),
    ("DATA", [("postgresql", "postgres"), ("mongodb", "mongodb"), ("redis", "redis"), ("rabbitmq", "rabbitmq"), ("clickhouse", "clickhouse")]),
    ("OPS", [("docker", "docker"), ("githubactions", "actions"), ("grafana", "grafana"), ("prometheus", "prometheus")]),
]
ROWS = [GROUPS[:3], GROUPS[3:]]


def stack(t):
    W, H = 1200, 290
    cell, icon, gap = 76, 26, 36
    p = [f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Stack: Go, TypeScript, Python, PHP; Gin, Spring Boot, .NET; Vue, Nuxt, Next.js, Tailwind; PostgreSQL, MongoDB, Redis, RabbitMQ, ClickHouse; Docker, GitHub Actions, Grafana, Prometheus">
  <rect width="{W}" height="{H}" fill="{t["bg"]}"/>
  {label(t, 24, 25, "STACK", 11, t["dim"], spacing=3)}
  {label(t, W-24, 25, "WHAT I REACH FOR FIRST", 11, t["dim"], anchor="end", spacing=3)}
  <line x1="0" y1="40" x2="{W}" y2="40" stroke="{t["line"]}"/>
  <line x1="0" y1="{40 + (H-40)//2}" x2="{W}" y2="{40 + (H-40)//2}" stroke="{t["line"]}"/>''']
    row_h = (H - 40) // 2
    for ri, groups in enumerate(ROWS):
        top = 40 + ri * row_h
        x = 24
        for gi, (name, items) in enumerate(groups):
            p.append(label(t, x, top + 30, name, 10, t["dim"], spacing=3))
            for slug, text in items:
                cx = x + cell / 2
                iy = top + 50
                sc = icon / 24
                p.append(f'<g transform="translate({cx - icon/2:.1f} {iy}) scale({sc:.4f})"><path d="{ICONS[slug]}" fill="{t["text"]}" opacity="0.92"/></g>')
                p.append(label(t, cx, iy + icon + 20, text, 10, t["muted"], anchor="middle", spacing=0.3))
                x += cell
            if gi < len(groups) - 1:
                x += gap
                p.append(f'<line x1="{x - gap/2}" y1="{top + 14}" x2="{x - gap/2}" y2="{top + row_h - 14}" stroke="{t["line"]}"/>')
    p.append("</svg>\n")
    return "\n".join(p)


def _ago(now_iso, then_iso):
    import datetime as dt
    now = dt.datetime.fromisoformat(now_iso.replace("Z", "+00:00"))
    then = dt.datetime.fromisoformat(then_iso.replace("Z", "+00:00"))
    s = int((now - then).total_seconds())
    if s < 3600: return f"{max(s // 60, 1)}m ago"
    if s < 86400: return f"{s // 3600}h ago"
    return f"{s // 86400}d ago"


def pulse(t, st):
    """Activity strip rendered from data/stats.json (refreshed by the stats workflow)."""
    W, H = 1200, 130
    p = [f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Public GitHub activity: {st["commits_30d"]} commits in the last {st["window_days"]} days, top languages, last push">
  <rect width="{W}" height="{H}" fill="{t["bg"]}"/>
  <line x1="0" y1="40" x2="{W}" y2="40" stroke="{t["line"]}"/>
  <line x1="440" y1="40" x2="440" y2="{H}" stroke="{t["line"]}"/>
  <line x1="860" y1="40" x2="860" y2="{H}" stroke="{t["line"]}"/>
  {label(t, 24, 25, "PUBLIC ACTIVITY", 11, t["dim"], spacing=3)}
  {label(t, W-24, 25, "AUTO-REFRESHED " + st["generated_at"][:10].upper() + " UTC", 11, t["dim"], anchor="end", spacing=2)}''']
    # --- commits sparkline ---
    days = st["contributions_by_day"]; mx = max([d["count"] for d in days] + [1])
    bw, gap, base, hmax = 8, 4, 112, 44
    x0 = 24
    for i, d in enumerate(days):
        h = max(2, round(d["count"] / mx * hmax)) if d["count"] else 2
        col = t["accent"] if d["count"] else t["line"]
        p.append(f'<rect x="{x0 + i*(bw+gap)}" y="{base-h}" width="{bw}" height="{h}" fill="{col}" opacity="{0.95 if d["count"] else 1}"/>')
    p.append(f'<text x="{x0 + 30*(bw+gap) + 16}" y="{base-2}" font-family="{MONO}" font-size="30" font-weight="600" fill="{t["text"]}">{st["commits_30d"]}</text>')
    p.append(label(t, x0, 62, f"COMMITS · LAST {st['window_days']} DAYS", 10, t["dim"], spacing=2))
    # --- languages bar ---
    lx, lw = 464, 372
    p.append(label(t, lx, 62, "LANGUAGES · PUBLIC REPOS", 10, t["dim"], spacing=2))
    x = lx; y = 76
    shades = [1.0, 0.75, 0.55, 0.4, 0.28]
    for i, lang in enumerate(st["languages"]):
        w = max(2, round(lang["share"] * lw) - 2)
        p.append(f'<rect x="{x}" y="{y}" width="{w}" height="6" fill="{t["accent"]}" opacity="{shades[i]}"/>')
        x += w + 2
    x = lx
    short = {"jupyter notebook": "jupyter", "javascript": "js", "typescript": "ts", "dockerfile": "docker"}
    for i, lang in enumerate(st["languages"][:5]):
        name = lang["name"].lower(); name = short.get(name, name)
        text = f"{name} {round(lang['share']*100)}%"
        if x + 12 + len(text) * 6.9 > lx + lw: break
        p.append(f'<rect x="{x}" y="{y+22}" width="6" height="6" fill="{t["accent"]}" opacity="{shades[i]}"/>')
        p.append(label(t, x + 12, y + 28, text, 11, t["muted"], spacing=0.3))
        x += 12 + len(text) * 6.9 + 18
    # --- last push / repos ---
    rx = 884
    p.append(label(t, rx, 62, "LAST PUSH", 10, t["dim"], spacing=2))
    lp = st.get("last_push") or {"repo": "-", "at": st["generated_at"]}
    p.append(label(t, rx, 86, lp["repo"], 14, t["text"], spacing=0, bold=True))
    p.append(label(t, rx, 106, _ago(st["generated_at"], lp["at"]), 11, t["muted"], spacing=0.3))
    p.append(label(t, W-24, 62, "PUBLIC REPOS", 10, t["dim"], anchor="end", spacing=2))
    p.append(f'<text x="{W-24}" y="106" text-anchor="end" font-family="{MONO}" font-size="30" font-weight="600" fill="{t["text"]}">{st["public_repos"]}</text>')
    p.append("</svg>\n")
    return "\n".join(p)


def timeline(t):
    """Work history as a single rail with three stops."""
    W, H = 1200, 190
    Y = 72
    stops = [
        (130, "APR – JUN 2023", "intern developer", "Zip Event",
         "public-space booking platform for Bangkok", "asp.net mvc · mongodb · bootstrap"),
        (500, "MAR 2024 – MAR 2025", "programmer", "Tech Horizon",
         "payment gateway (japan) · batch processing", "pci dss · parallel workloads · security reviews"),
        (850, "MAY 2025 – NOW", "full-stack developer", "real-time chat platform · sms platform",
         "high-traffic apis · agile sprints · observability", "go · gin · vue (ts) · rabbitmq · clickhouse"),
    ]
    p = [f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Experience: intern developer at Zip Event 2023; programmer at Tech Horizon 2024 to 2025 on a payment gateway; full-stack developer since 2025 on a real-time chat platform and an SMS platform">
  <rect width="{W}" height="{H}" fill="{t["bg"]}"/>
  <line x1="0" y1="40" x2="{W}" y2="40" stroke="{t["line"]}"/>
  {label(t, 24, 25, "EXPERIENCE", 11, t["dim"], spacing=3)}
  {label(t, W-24, 25, "2023 → NOW", 11, t["dim"], anchor="end", spacing=3)}
  <line x1="60" y1="{Y}" x2="{W-60}" y2="{Y}" stroke="{t["muted"]}" stroke-width="1"/>
  <path d="M {W-66} {Y-4} L {W-58} {Y} L {W-66} {Y+4}" fill="none" stroke="{t["muted"]}" stroke-width="1"/>''']
    for i, (x, when, role, org, line3, line4) in enumerate(stops):
        current = i == len(stops) - 1
        col = t["accent"] if current else t["text"]
        p.append(label(t, x, Y - 14, when, 10, t["dim"], spacing=2))
        p.append(f'<rect x="{x-5}" y="{Y-5}" width="10" height="10" fill="{t["accent"] if current else t["bg"]}" stroke="{col}" stroke-width="1.25"/>')
        if current:
            p.append(f'<rect x="{x-5}" y="{Y-5}" width="10" height="10" fill="none" stroke="{t["accent"]}" stroke-width="1">'
                     f'<animate attributeName="x" values="{x-5};{x-13}" dur="2.4s" repeatCount="indefinite"/>'
                     f'<animate attributeName="y" values="{Y-5};{Y-13}" dur="2.4s" repeatCount="indefinite"/>'
                     f'<animate attributeName="width" values="10;26" dur="2.4s" repeatCount="indefinite"/>'
                     f'<animate attributeName="height" values="10;26" dur="2.4s" repeatCount="indefinite"/>'
                     f'<animate attributeName="opacity" values="0.8;0" dur="2.4s" repeatCount="indefinite"/></rect>')
        p.append(label(t, x, Y + 30, role, 14, t["text"], spacing=0, bold=True))
        p.append(label(t, x, Y + 50, org, 11, t["accent"] if current else t["muted"], spacing=0.3))
        p.append(label(t, x, Y + 68, line3, 11, t["muted"], spacing=0.3))
        p.append(label(t, x, Y + 86, line4, 10, t["dim"], spacing=0.3))
    p.append("</svg>\n")
    return "\n".join(p)


STATS_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "stats.json")
STATS = json.load(open(STATS_PATH)) if os.path.exists(STATS_PATH) else None

for name, t in THEMES.items():
    with open(f"{OUT}/hero.svg", "w") as f:
        f.write(hero(t))
    with open(f"{OUT}/system.svg", "w") as f:
        f.write(system(t))
    with open(f"{OUT}/stack.svg", "w") as f:
        f.write(stack(t))
    with open(f"{OUT}/timeline.svg", "w") as f:
        f.write(timeline(t))
    if STATS:
        with open(f"{OUT}/pulse.svg", "w") as f:
            f.write(pulse(t, STATS))
print("written:", sorted(os.listdir(OUT)))
