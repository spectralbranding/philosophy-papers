#!/usr/bin/env bash
# Run every paper's reproduction script in turn.
#
# Each paper owns its own reproduce.sh, because each fetches a different data of
# record. This orchestrator only iterates; it holds no per-paper logic, so adding
# a paper needs no edit here.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

found=0
for script in "${ROOT}"/*/reproduce.sh; do
  [ -e "$script" ] || continue
  found=1
  paper="$(basename "$(dirname "$script")")"
  echo
  echo "########## ${paper} ##########"
  ( cd "$(dirname "$script")" && ./reproduce.sh )
done

if [ "$found" -eq 0 ]; then
  echo "No per-paper reproduce.sh found under ${ROOT}." >&2
  exit 1
fi
echo
echo "All papers reproduced."
