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
  echo "用法: install.sh --target <claude|codex> --profile <minimal|backend-go|author> [--dest <目录>]" >&2
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

copy_command() {
  local name="$1"
  local src="$ROOT/commands/$name.md"
  local dst="$INSTALL_ROOT/commands/$name.md"
  backend_ecc_require_file "$src"
  backend_ecc_copy_file "$src" "$dst"
  INSTALLED_FILES+=("${TARGET_ROOT}/backend-ecc/commands/$name.md")
}

copy_agent() {
  local name="$1"
  local src="$ROOT/agents/$name.md"
  local dst="$INSTALL_ROOT/agents/$name.md"
  backend_ecc_require_file "$src"
  backend_ecc_copy_file "$src" "$dst"
  INSTALLED_FILES+=("${TARGET_ROOT}/backend-ecc/agents/$name.md")
}

copy_skill() {
  local name="$1"
  local src="$ROOT/skills/$name/SKILL.md"
  local dst="$INSTALL_ROOT/skills/$name/SKILL.md"
  backend_ecc_require_file "$src"
  backend_ecc_copy_file "$src" "$dst"
  INSTALLED_FILES+=("${TARGET_ROOT}/backend-ecc/skills/$name/SKILL.md")
}

copy_rule_group() {
  local group="$1"
  local rule_name="$2"
  local src="$ROOT/rules/$group/$rule_name.md"
  local dst="$INSTALL_ROOT/rules/$group/$rule_name.md"
  backend_ecc_require_file "$src"
  backend_ecc_copy_file "$src" "$dst"
  INSTALLED_FILES+=("${TARGET_ROOT}/backend-ecc/rules/$group/$rule_name.md")
}

copy_hook() {
  local hook_name="$1"
  local src="$ROOT/hooks/$hook_name"
  local dst="$INSTALL_ROOT/hooks/$hook_name"
  backend_ecc_require_file "$src"
  backend_ecc_copy_file "$src" "$dst"
  INSTALLED_FILES+=("${TARGET_ROOT}/backend-ecc/hooks/$hook_name")
}

while IFS= read -r item; do
  [[ -z "$item" ]] && continue
  copy_command "$item"
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
  copy_agent "$item"
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
  copy_skill "$item"
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
  copy_rule_group "$group" "$rule_name"
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
  copy_hook "$item"
done < <(python3 - "$PROFILE_FILE" <<'PY'
import json, sys
with open(sys.argv[1], 'r', encoding='utf-8') as f:
    data = json.load(f)
for item in data.get('hooks', []):
    print(item)
PY
)

backend_ecc_copy_file "$ROOT/README.md" "$INSTALL_ROOT/README.md"
INSTALLED_FILES+=("${TARGET_ROOT}/backend-ecc/README.md")
backend_ecc_copy_file "$ROOT/VERSION" "$INSTALL_ROOT/VERSION"
INSTALLED_FILES+=("${TARGET_ROOT}/backend-ecc/VERSION")
backend_ecc_copy_file "$ROOT/manifest.json" "$INSTALL_ROOT/manifest.json"
INSTALLED_FILES+=("${TARGET_ROOT}/backend-ecc/manifest.json")
backend_ecc_copy_file "$ROOT/docs/verification.md" "$INSTALL_ROOT/docs/verification.md"
INSTALLED_FILES+=("${TARGET_ROOT}/backend-ecc/docs/verification.md")

META_FILE="$INSTALL_ROOT/.install-meta.json"
backend_ecc_write_install_meta "$META_FILE" "$VERSION" "$TARGET" "$PROFILE" "$NOW" "${INSTALLED_FILES[@]}"
INSTALLED_FILES+=("${TARGET_ROOT}/backend-ecc/.install-meta.json")

echo "[backend-ecc] 安装完成"
echo "- target: $TARGET"
echo "- profile: $PROFILE"
echo "- version: $VERSION"
echo "- root: $INSTALL_ROOT"
echo "- files: ${#INSTALLED_FILES[@]}"
