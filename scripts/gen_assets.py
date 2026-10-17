"""Generate the profile SVGs (dark + light): hero.svg, system.svg and stack.svg.

Usage: python3 scripts/gen_assets.py assets
Minimal, schematic look: one accent colour, 1px lines, monospace labels.
"""
import json
import os
import sys

OUT = sys.argv[1] if len(sys.argv) > 1 else "assets"
os.makedirs(OUT, exist_ok=True)

THEMES = {
    "dark": dict(bg="#0a0c10", line="#1f2630", text="#e6edf3", muted="#7d8590",
                 dim="#4b535e", accent="#22d3ee"),
    "light": dict(bg="#ffffff", line="#e3e7ec", text="#1f2328", muted="#656d76",
                  dim="#9aa3ad", accent="#0891b2"),
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
  <!-- frame -->
  <rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" fill="none" stroke="{t["line"]}"/>
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
  <rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" fill="none" stroke="{t["line"]}"/>
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
  <rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" fill="none" stroke="{t["line"]}"/>
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


for name, t in THEMES.items():
    with open(f"{OUT}/hero-{name}.svg", "w") as f:
        f.write(hero(t))
    with open(f"{OUT}/system-{name}.svg", "w") as f:
        f.write(system(t))
    with open(f"{OUT}/stack-{name}.svg", "w") as f:
        f.write(stack(t))
print("written:", sorted(os.listdir(OUT)))
