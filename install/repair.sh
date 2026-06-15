#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
# shellcheck source=./lib.sh
source "$SCRIPT_DIR/lib.sh"

TARGET=""
PROFILE=""
DEST_ROOT=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --target)
      TARGET="$2"
      shift 2
      ;;
    --profile)
      PROFILE="$2"
      shift 2
      ;;
    --dest)
      DEST_ROOT="$2"
      shift 2
      ;;
    *)
      echo "[backend-ecc] 未知参数: $1" >&2
      exit 1
      ;;
  esac
done

if [[ -z "$TARGET" || -z "$PROFILE" ]]; then
  echo "用法: repair.sh --target <claude|codex> --profile <minimal|backend-go|author> [--dest <目录>]" >&2
  exit 1
fi

ROOT="$(backend_ecc_root)"
VERSION="$(backend_ecc_version)"
PROFILE_FILE="$ROOT/profiles/$PROFILE.json"
ADAPTER_FILE="$ROOT/adapters/$TARGET/install-map.json"
MANIFEST_FILE="$ROOT/manifest.json"

backend_ecc_require_file "$PROFILE_FILE"
backend_ecc_require_file "$ADAPTER_FILE"
backend_ecc_require_file "$MANIFEST_FILE"

TARGET_ROOT="$(backend_ecc_read_json_field "$ADAPTER_FILE" root)"
if [[ -n "$DEST_ROOT" ]]; then
  INSTALL_ROOT="$DEST_ROOT/$TARGET_ROOT/backend-ecc"
else
  INSTALL_ROOT="$PWD/$TARGET_ROOT/backend-ecc"
fi
mkdir -p "$INSTALL_ROOT"

INSTALLED_FILES=()
NOW="$(backend_ecc_now_utc)"
RESTORED=0

restore_if_missing() {
  local src="$1"
  local dst="$2"
  local record="$3"
  if [[ ! -f "$dst" ]]; then
    backend_ecc_require_file "$src"
    backend_ecc_copy_file "$src" "$dst"
    RESTORED=$((RESTORED+1))
    echo "RESTORE\t$record"
  fi
  INSTALLED_FILES+=("$record")
}

while IFS= read -r item; do
  [[ -z "$item" ]] && continue
  restore_if_missing "$ROOT/commands/$item.md" "$INSTALL_ROOT/commands/$item.md" "${TARGET_ROOT}/backend-ecc/commands/$item.md"
done < <(python3 - "$PROFILE_FILE" <<'PY'
import json, sys
with open(sys.argv[1], 'r', encoding='utf-8') as f:
    data = json.load(f)
for item in data.get('commands', []):
    print(item)
PY
)

while IFS= read -r item; do
  [[ -z "$item" ]] && continue
  restore_if_missing "$ROOT/agents/$item.md" "$INSTALL_ROOT/agents/$item.md" "${TARGET_ROOT}/backend-ecc/agents/$item.md"
done < <(python3 - "$PROFILE_FILE" <<'PY'
import json, sys
with open(sys.argv[1], 'r', encoding='utf-8') as f:
    data = json.load(f)
for item in data.get('agents', []):
    print(item)
PY
)

while IFS= read -r item; do
  [[ -z "$item" ]] && continue
  restore_if_missing "$ROOT/skills/$item/SKILL.md" "$INSTALL_ROOT/skills/$item/SKILL.md" "${TARGET_ROOT}/backend-ecc/skills/$item/SKILL.md"
done < <(python3 - "$PROFILE_FILE" <<'PY'
import json, sys
with open(sys.argv[1], 'r', encoding='utf-8') as f:
    data = json.load(f)
for item in data.get('skills', []):
    print(item)
PY
)

while IFS='|' read -r group rule_name; do
  [[ -z "$group" ]] && continue
  restore_if_missing "$ROOT/rules/$group/$rule_name.md" "$INSTALL_ROOT/rules/$group/$rule_name.md" "${TARGET_ROOT}/backend-ecc/rules/$group/$rule_name.md"
done < <(python3 - "$PROFILE_FILE" <<'PY'
import json, sys
with open(sys.argv[1], 'r', encoding='utf-8') as f:
    data = json.load(f)
for group, items in data.get('rules', {}).items():
    for item in items:
        print(f"{group}|{item}")
PY
)

while IFS= read -r item; do
  [[ -z "$item" ]] && continue
  restore_if_missing "$ROOT/hooks/$item" "$INSTALL_ROOT/hooks/$item" "${TARGET_ROOT}/backend-ecc/hooks/$item"
done < <(python3 - "$PROFILE_FILE" <<'PY'
import json, sys
with open(sys.argv[1], 'r', encoding='utf-8') as f:
    data = json.load(f)
for item in data.get('hooks', []):
    print(item)
PY
)

restore_if_missing "$ROOT/README.md" "$INSTALL_ROOT/README.md" "${TARGET_ROOT}/backend-ecc/README.md"
restore_if_missing "$ROOT/VERSION" "$INSTALL_ROOT/VERSION" "${TARGET_ROOT}/backend-ecc/VERSION"
restore_if_missing "$ROOT/manifest.json" "$INSTALL_ROOT/manifest.json" "${TARGET_ROOT}/backend-ecc/manifest.json"
restore_if_missing "$ROOT/docs/verification.md" "$INSTALL_ROOT/docs/verification.md" "${TARGET_ROOT}/backend-ecc/docs/verification.md"

META_FILE="$INSTALL_ROOT/.install-meta.json"
backend_ecc_write_install_meta "$META_FILE" "$VERSION" "$TARGET" "$PROFILE" "$NOW" "${INSTALLED_FILES[@]}"

echo
echo "[backend-ecc] repair 完成"
echo "- target: $TARGET"
echo "- profile: $PROFILE"
echo "- root: $INSTALL_ROOT"
echo "- restored: $RESTORED"
echo "- metadata: rebuilt"
