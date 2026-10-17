"""Generate hero + architecture SVGs (dark/light) for the profile README.

Usage: python3 scripts/gen_assets.py assets
"""
import sys, os

OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)

THEMES = {
    "dark": dict(bg="#0d1117", card="#161b22", border="#30363d", text="#e6edf3",
                 muted="#8b949e", accent="#2dd4bf", accent2="#f5b84b", grid="#1b222c",
                 dim="#6e7681", green="#3fb950", red="#ff7b72"),
    "light": dict(bg="#ffffff", card="#f6f8fa", border="#d0d7de", text="#1f2328",
                  muted="#656d76", accent="#0e7c6b", accent2="#b7791f", grid="#eef1f4",
                  dim="#8c959f", green="#1a7f37", red="#cf222e"),
}
SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, 'Liberation Mono', monospace"


def fade(begin):
    return (f'<animate attributeName="opacity" from="0" to="1" dur="0.15s" '
            f'begin="{begin}s" fill="freeze"/>')


def pills(t, labels, x=60, y=204, size=13):
    out, cw = [], size * 0.62  # approx monospace advance
    for lab in labels:
        w = int(len(lab) * cw) + 30
        out.append(f'<rect x="{x}" y="{y}" width="{w}" height="26" rx="13" fill="none" stroke="{t["border"]}"/>'
                   f'<text x="{x + w/2}" y="{y + 17}" text-anchor="middle" font-family="{MONO}" font-size="{size}" fill="{t["muted"]}">{lab}</text>')
        x += w + 10
    return "\n  ".join(out)


def hero(t):
    W, H = 1200, 300
    lines = [  # (y, prompt, cmd, out, begin)
        (92,  "$", "whoami", "bill · bangkok, th", 0.6),
        (146, "$", "go run ./cmd/api", "api listening on :8090", 1.8),
        (200, "$", "tail -f api.log | grep ERROR", "", 3.2),
    ]
    term = []
    for y, p, cmd, out, b in lines:
        term.append(f'<g opacity="0">{fade(b)}'
                    f'<text x="730" y="{y}" font-family="{MONO}" font-size="15" fill="{t["accent"]}">{p}</text>'
                    f'<text x="748" y="{y}" font-family="{MONO}" font-size="15" fill="{t["text"]}">{cmd}</text></g>')
        if out:
            term.append(f'<g opacity="0">{fade(b + 0.5)}'
                        f'<text x="748" y="{y + 24}" font-family="{MONO}" font-size="15" fill="{t["muted"]}">{out}</text></g>')
    # final line: comment + blinking cursor
    term.append(f'<g opacity="0">{fade(3.9)}'
                f'<text x="748" y="224" font-family="{MONO}" font-size="15" fill="{t["dim"]}">— nothing yet. good.</text>'
                f'<rect x="938" y="211" width="9" height="17" fill="{t["accent"]}">'
                f'<animate attributeName="opacity" values="1;1;0;0" dur="1.1s" begin="4s" repeatCount="indefinite"/></rect></g>')
    term_svg = "\n".join(term)

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Krirk Klomkliang — full-stack developer">
  <defs>
    <pattern id="grid" width="28" height="28" patternUnits="userSpaceOnUse">
      <path d="M 28 0 L 0 0 0 28" fill="none" stroke="{t["grid"]}" stroke-width="1"/>
    </pattern>
    <linearGradient id="fadeR" x1="0" x2="1">
      <stop offset="0" stop-color="{t["bg"]}" stop-opacity="0"/>
      <stop offset="1" stop-color="{t["bg"]}" stop-opacity="1"/>
    </linearGradient>
  </defs>
  <rect width="{W}" height="{H}" rx="14" fill="{t["bg"]}"/>
  <rect width="{W}" height="{H}" rx="14" fill="url(#grid)"/>
  <rect x="0" y="0" width="{W}" height="{H}" rx="14" fill="none" stroke="{t["border"]}"/>

  <!-- left: identity -->
  <text x="60" y="78" font-family="{MONO}" font-size="14" fill="{t["accent"]}">~/b1ll1eee</text>
  <text x="58" y="136" font-family="{SANS}" font-size="46" font-weight="700" fill="{t["text"]}" letter-spacing="-0.5">Krirk Klomkliang</text>
  <text x="60" y="172" font-family="{SANS}" font-size="20" fill="{t["muted"]}">Full-stack developer. Go on the server, Vue &amp; Next.js on the screen.</text>

  {pills(t, ["real-time chat", "payments", "sms pipelines", "local LLMs"])}
  <text x="60" y="262" font-family="{SANS}" font-size="14" fill="{t["dim"]}">Bangkok, Thailand · open to backend / full-stack work</text>

  <!-- right: terminal -->
  <rect x="700" y="44" width="450" height="212" rx="10" fill="{t["card"]}" stroke="{t["border"]}"/>
  <circle cx="722" cy="62" r="5" fill="{t["red"]}"/>
  <circle cx="740" cy="62" r="5" fill="{t["accent2"]}"/>
  <circle cx="758" cy="62" r="5" fill="{t["green"]}"/>
  <text x="925" y="66" text-anchor="middle" font-family="{MONO}" font-size="12" fill="{t["dim"]}">zsh — scribe-api</text>
  <line x1="700" y1="78" x2="1150" y2="78" stroke="{t["border"]}"/>
  {term_svg}
</svg>
'''


def box(t, x, y, w, h, title, sub=None, accent=False, dashed=False):
    stroke = t["accent"] if accent else t["border"]
    dash = ' stroke-dasharray="6 5"' if dashed else ""
    s = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{t["card"]}" stroke="{stroke}"{dash}/>'
    cy = y + h / 2
    if sub:
        s += f'<text x="{x + w/2}" y="{cy - 4}" text-anchor="middle" font-family="{SANS}" font-size="15" font-weight="600" fill="{t["text"]}">{title}</text>'
        s += f'<text x="{x + w/2}" y="{cy + 15}" text-anchor="middle" font-family="{MONO}" font-size="12" fill="{t["muted"]}">{sub}</text>'
    else:
        s += f'<text x="{x + w/2}" y="{cy + 5}" text-anchor="middle" font-family="{SANS}" font-size="15" font-weight="600" fill="{t["text"]}">{title}</text>'
    return s


def arrow(t, x1, y1, x2, y2, label=None, dashed=False, below=False):
    dash = ' stroke-dasharray="5 5"' if dashed else ""
    s = f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{t["muted"]}" stroke-width="1.5" marker-end="url(#arr)"{dash}/>'
    if label:
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2 + (18 if below else -7)
        s += f'<text x="{mx}" y="{my}" text-anchor="middle" font-family="{MONO}" font-size="11" fill="{t["dim"]}">{label}</text>'
    return s


def arch(t):
    W, H = 1200, 430
    p = []
    p.append(f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Typical system: clients, Go service with hexagonal core, data stores, workers, observability">
  <defs>
    <marker id="arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="{t["muted"]}"/>
    </marker>
  </defs>
  <rect width="{W}" height="{H}" rx="14" fill="{t["bg"]}" stroke="{t["border"]}"/>''')

    # column headers
    for x, label in ((40, "clients"), (330, "service"), (760, "state"), (1000, "async")):
        p.append(f'<text x="{x}" y="42" font-family="{MONO}" font-size="12" fill="{t["dim"]}" letter-spacing="1">{label.upper()}</text>')

    # clients
    p.append(box(t, 40, 70, 200, 60, "Vue 3 + TypeScript", "nuxt · tailwind"))
    p.append(box(t, 40, 150, 200, 60, "Next.js", "react · tailwind"))
    p.append(box(t, 40, 230, 200, 60, "Cron / schedulers", "batch jobs"))

    # service: outer adapters + inner core
    p.append(f'<rect x="330" y="70" width="380" height="250" rx="10" fill="none" stroke="{t["accent"]}" stroke-dasharray="6 5"/>')
    p.append(f'<text x="520" y="92" text-anchor="middle" font-family="{SANS}" font-size="14" font-weight="600" fill="{t["accent"]}">Go service · ports &amp; adapters</text>')
    p.append(box(t, 346, 106, 110, 44, "HTTP · Gin"))
    p.append(box(t, 346, 160, 110, 44, "Auth adapter", None))
    p.append(f'<text x="401" y="194" text-anchor="middle" font-family="{MONO}" font-size="10" fill="{t["muted"]}"></text>')
    p.append(box(t, 346, 214, 110, 44, "Postgres repo"))
    p.append(box(t, 346, 268, 110, 44, "Redis · AMQP"))
    # core
    p.append(f'<rect x="478" y="106" width="216" height="206" rx="8" fill="{t["card"]}" stroke="{t["text"]}" stroke-width="1.5"/>')
    p.append(f'<text x="586" y="150" text-anchor="middle" font-family="{SANS}" font-size="16" font-weight="700" fill="{t["text"]}">domain + services</text>')
    for i, line in enumerate(["no gin, no gorm imports", "state machines, invariants", "unit-tested in isolation", "swap any adapter in one file"]):
        p.append(f'<text x="586" y="{184 + i*26}" text-anchor="middle" font-family="{MONO}" font-size="12" fill="{t["muted"]}">{line}</text>')
    # inner arrows adapters -> core
    for y in (128, 182, 236, 290):
        p.append(arrow(t, 456, y, 476, y))

    # client -> service arrows
    p.append(arrow(t, 240, 100, 330, 118, "REST / JSON"))
    p.append(arrow(t, 240, 180, 330, 160))
    p.append(arrow(t, 240, 260, 330, 280, "ticks", dashed=True))

    # state column
    p.append(box(t, 760, 70, 200, 56, "PostgreSQL", "source of truth"))
    p.append(box(t, 760, 142, 200, 56, "Redis", "cache · sessions"))
    p.append(box(t, 760, 214, 200, 56, "RabbitMQ", "events out"))
    p.append(box(t, 760, 286, 200, 56, "ClickHouse", "analytics, append-only"))
    p.append(arrow(t, 710, 236, 760, 98))
    p.append(arrow(t, 710, 250, 760, 170))
    p.append(arrow(t, 710, 290, 760, 242))
    p.append(arrow(t, 710, 300, 760, 314, "fire &amp; forget", dashed=True, below=True))

    # async column
    p.append(box(t, 1000, 142, 160, 56, "Workers", "go consumers"))
    p.append(box(t, 1000, 214, 160, 56, "Payments · SMS", "3rd-party APIs"))
    p.append(arrow(t, 960, 242, 1000, 170))
    p.append(arrow(t, 1080, 198, 1080, 214))

    # observability bar
    p.append(f'<rect x="40" y="350" width="1120" height="50" rx="8" fill="{t["card"]}" stroke="{t["border"]}"/>')
    p.append(f'<text x="60" y="381" font-family="{SANS}" font-size="14" font-weight="600" fill="{t["text"]}">Everything ships in Docker and is watched</text>')
    p.append(f'<text x="1140" y="381" text-anchor="end" font-family="{MONO}" font-size="13" fill="{t["muted"]}">Loki · Grafana · Tempo · Mimir · Prometheus · GitHub Actions</text>')
    p.append("</svg>\n")
    return "\n".join(p)


for name, t in THEMES.items():
    with open(f"{OUT}/hero-{name}.svg", "w") as f:
        f.write(hero(t))
    with open(f"{OUT}/arch-{name}.svg", "w") as f:
        f.write(arch(t))
print("written:", sorted(os.listdir(OUT)))
