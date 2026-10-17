<div align="center">

# Hi, I'm Krirk "Bill" Klomkliang 👋

**Full-Stack Developer** · Go backends, Vue / Next.js frontends, real-time & payment systems

[![Email](https://img.shields.io/badge/Email-krirk.klomkliang%40gmail.com-D14836?style=flat-square&logo=gmail&logoColor=white)](mailto:krirk.klomkliang@gmail.com)
[![Location](https://img.shields.io/badge/Bangkok-Thailand-2E8B57?style=flat-square&logo=googlemaps&logoColor=white)](#)
[![Profile views](https://komarev.com/ghpvc/?username=b1ll1eee&style=flat-square&color=0e7c6b)](https://github.com/b1ll1eee)

</div>

## About me

- 🔧 I build backend services in **Go (Gin)** with **PostgreSQL, Redis, RabbitMQ and ClickHouse**, structured around **Hexagonal Architecture** so the core stays framework-free and testable.
- 🖥️ On the frontend I ship with **Vue (TypeScript), Nuxt, Next.js and Tailwind CSS**.
- 💳 Worked on a Japan-based **payment gateway** (PCI DSS): batch processing, parallel workloads, third-party API integration, security reviews.
- 💬 Currently building **real-time chat** and **SMS platform** features at scale, with observability on the **LGTM stack** (Loki · Grafana · Tempo · Mimir).
- 🤖 Exploring **local LLM tooling** with Python + Ollama, with a bias for eval-driven iteration.
- 📐 I care about clean code, refactoring, design patterns and systems that are boring to operate.

## Tech stack

**Languages**

<img src="https://skillicons.dev/icons?i=go,ts,js,python,java,php&theme=dark" alt="Go, TypeScript, JavaScript, Python, Java, PHP" height="40" />

**Backend**

<img src="https://skillicons.dev/icons?i=gin,spring,nodejs,express,nestjs,dotnet&theme=dark" alt="Gin, Spring Boot, Node.js, Express, NestJS, .NET" height="40" />

**Frontend**

<img src="https://skillicons.dev/icons?i=vue,nuxtjs,react,nextjs,tailwind,vuetify&theme=dark" alt="Vue, Nuxt, React, Next.js, Tailwind CSS, Vuetify" height="40" />

**Data & messaging**

<img src="https://skillicons.dev/icons?i=postgres,mysql,mongodb,redis,rabbitmq,firebase&theme=dark" alt="PostgreSQL, MySQL, MongoDB, Redis, RabbitMQ, Firebase" height="40" />&nbsp;<img src="https://img.shields.io/badge/ClickHouse-FFCC01?style=for-the-badge&logo=clickhouse&logoColor=black" alt="ClickHouse" height="40" />

**DevOps & observability**

<img src="https://skillicons.dev/icons?i=docker,githubactions,linux,grafana,prometheus,git&theme=dark" alt="Docker, GitHub Actions, Linux, Grafana, Prometheus, Git" height="40" />

## Featured projects

| Project | What it is | Stack |
|---|---|---|
| [**scribe-api**](https://github.com/b1ll1eee/scribe-api) | Hexagonal Go API with Firebase + JWT auth, PostgreSQL for records, ClickHouse for analytics, Redis cache. Deployed on Railway. | Go · Gin · PostgreSQL · ClickHouse · Redis · Firebase |
| [**flow-do-api**](https://github.com/b1ll1eee/flow-do-api) | Production-style task API built on Ports & Adapters with a framework-free core and GORM persistence. | Go · Gin · GORM · Docker |
| [**morty-model**](https://github.com/b1ll1eee/morty-model) | Local-first LLM assistant on Ollama: one base model, many expert profiles via TOML, RAG per profile, eval sets to measure every change. | Python · Ollama · RAG |

> More repos are in progress; several are still private or being cleaned up before publishing.

## How I work

```text
hexagonal core  →  thin adapters (HTTP / DB / queue)  →  Dockerised  →  observed (LGTM)
tests on the core, migrations versioned, every change measurable
```

## GitHub stats

<div align="center">

<img src="https://github-readme-stats.vercel.app/api?username=b1ll1eee&show_icons=true&theme=github_dark&hide_border=true&include_all_commits=true&count_private=true" alt="GitHub stats" height="165" />
<img src="https://github-readme-stats.vercel.app/api/top-langs/?username=b1ll1eee&layout=compact&theme=github_dark&hide_border=true&langs_count=8" alt="Top languages" height="165" />

<img src="https://streak-stats.demolab.com?user=b1ll1eee&theme=github-dark-blue&hide_border=true" alt="GitHub streak" height="165" />

</div>

## Contribution graph

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/b1ll1eee/b1ll1eee/output/github-contribution-grid-snake-dark.svg" />
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/b1ll1eee/b1ll1eee/output/github-contribution-grid-snake.svg" />
  <img alt="Contribution snake" src="https://raw.githubusercontent.com/b1ll1eee/b1ll1eee/output/github-contribution-grid-snake.svg" />
</picture>

---

<div align="center">
<sub>Open to backend / full-stack roles and interesting Go projects. Say hi via email.</sub>
</div>
