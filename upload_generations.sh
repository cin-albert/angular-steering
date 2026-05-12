#!/bin/bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [[ -f "$SCRIPT_DIR/.env" ]]; then
    export "$(grep -v '^#' "$SCRIPT_DIR/.env" | xargs)"
fi

HF_HUB_DISABLE_XET=1 huggingface-cli upload \
    --repo-type dataset \
    LoneResearch/thinking-steering-generations \
    /home/ian/repos/albert-steering/output/thinking_steering_generations \
    .
