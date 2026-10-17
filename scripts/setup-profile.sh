#!/usr/bin/env sh
# One-shot setup for github.com/b1ll1eee. Requires: gh auth login (scopes: repo, workflow, user)
set -eu

# 1) Profile fields shown on the sidebar
gh api -X PATCH /user \
  -f name="Krirk (Bill) Klomkliang" \
  -f bio="Full-Stack Developer · Go (Gin) · Vue/Next.js · real-time & payment systems · Hexagonal Architecture" \
  -f location="Bangkok, Thailand" \
  -f blog="https://github.com/b1ll1eee" \
  -f hireable=true >/dev/null && echo "profile fields updated"

# 2) Descriptions + topics on the repos that have code
gh repo edit b1ll1eee/scribe-api  -d "Hexagonal Go API: Gin, PostgreSQL, ClickHouse analytics, Redis, Firebase + JWT auth" \
  --add-topic go --add-topic gin --add-topic hexagonal-architecture --add-topic clickhouse --add-topic postgresql --add-topic redis
gh repo edit b1ll1eee/scribe-web  -d "Frontend for Scribe"
gh repo edit b1ll1eee/flow-do-api -d "Task API in Go with Ports & Adapters (Hexagonal Architecture) and GORM" \
  --add-topic go --add-topic gin --add-topic hexagonal-architecture --add-topic gorm
gh repo edit b1ll1eee/morty-model -d "Local-first LLM assistant on Ollama: expert profiles, per-profile RAG, eval-driven iteration" \
  --add-topic python --add-topic ollama --add-topic llm --add-topic rag
echo "repo descriptions updated"

# 3) Empty scaffold repos: hide them until they have code (comment out to keep public)
for r in khong-dee-cron khong-dee-worker khong-dee-payment khong-dee-api khong-dee-admin khong-dee-web \
         chat-kub-worker chat-kub-credit chat-kub-ws chat-kub-api chat-kub-web \
         wang-plan-api wang-plan-web wang-plan-cron wang-plan-credit \
         tuean-noi-web tuean-noi-cron tuean-noi-api; do
  gh repo edit "b1ll1eee/$r" --visibility private --accept-visibility-change-consequences >/dev/null && echo "private: $r"
done

# 4) Pin the repos that represent you best
gh api graphql -f query='query{ user(login:"b1ll1eee"){ id repositories(first:100, ownerAffiliations:OWNER){ nodes{ id name } } } }' \
  --jq '.data.user.repositories.nodes[] | select(.name=="scribe-api" or .name=="flow-do-api" or .name=="morty-model" or .name=="b1ll1eee") | .id' \
  | while read -r id; do
      gh api graphql -f query="mutation{ pinRepository(input:{repositoryId:\"$id\"}){ clientMutationId } }" >/dev/null
    done && echo "pinned repos set"
