#!/usr/bin/env bash
# Reproduce every number reported in 2026bo.
#
# Two steps, deliberately separated: this script fetches the data of record from
# Hugging Face, and the coding script then runs entirely offline. Keeping the
# network out of the coding script is what lets the paper claim it performs no
# network access.
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ID="spectralbranding/boundary-adjudication-data"
DATA_DIR="${HERE}/data"

echo "==> 1/2  fetching the data of record from ${REPO_ID}"
if [ -f "${DATA_DIR}/appstream-primary.xml.gz" ] && [ -f "${DATA_DIR}/baseos-primary.xml.gz" ]; then
  echo "        already present in ${DATA_DIR} — skipping download"
else
  mkdir -p "${DATA_DIR}"
  uv run --with huggingface_hub python - "$REPO_ID" "$DATA_DIR" <<'PY'
import sys
from huggingface_hub import snapshot_download
repo_id, dest = sys.argv[1], sys.argv[2]
snapshot_download(repo_id=repo_id, repo_type="dataset", local_dir=dest,
                  allow_patterns=["*.xml.gz", "*.htm", "*.txt"])
print(f"        downloaded into {dest}")
PY
fi

echo "==> 2/2  running the persistence coding (deterministic, offline, no seed)"
uv run python "${HERE}/code/code_persistence_content.py"

echo
echo "Done. Expected headline figures:"
echo "  2,093 distinct source packages; 2,060 codeable"
echo "  inside   90  (.044)   outside 1,970  (.956)"
echo "  sensitivity floor: inside 418 (.203), outside 1,642 (.797)"
echo "  pre-registered failure condition (inside > .500): not met"
