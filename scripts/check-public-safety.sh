#!/usr/bin/env bash
set -euo pipefail

repo_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$repo_dir"

if git ls-files | rg -n '(^|/)(\.env|.*\.pem|.*\.key|.*\.p12|client_secret.*\.json)$'; then
  echo "A private runtime or key file is tracked" >&2
  exit 1
fi

mapfile -d '' tracked_files < <(git ls-files -z)
if rg -n -I \
  -e '-----BEGIN ([A-Z ]+ )?PRIVATE KEY-----' \
  -e 'sk-[A-Za-z0-9_-]{20,}' \
  -e 'AIza[A-Za-z0-9_-]{30,}' \
  "${tracked_files[@]}"; then
  echo "A value resembling a live credential is tracked" >&2
  exit 1
fi

echo "Public-safety scan passed"
