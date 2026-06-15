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
  echo "用法: doctor.sh --target <claude|codex> --profile <minimal|backend-go|author> [--dest <目录>]" >&2
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

TOTAL=0
FAILS=0
WARNS=0

report_pass() {
  TOTAL=$((TOTAL+1))
  echo "PASS\t$1"
}

report_warn() {
  TOTAL=$((TOTAL+1))
  WARNS=$((WARNS+1))
  echo "WARN\t$1"
}

report_fail() {
  TOTAL=$((TOTAL+1))
  FAILS=$((FAILS+1))
  echo "FAIL\t$1"
}

if [[ "$(backend_ecc_read_json_field "$MANIFEST_FILE" version)" == "$VERSION" ]]; then
  report_pass "VERSION 与 manifest.json 一致"
else
  report_fail "VERSION 与 manifest.json 不一致"
fi

if [[ -d "$INSTALL_ROOT" ]]; then
  report_pass "安装根目录存在: $INSTALL_ROOT"
else
  report_fail "安装根目录不存在: $INSTALL_ROOT"
fi

META_FILE="$INSTALL_ROOT/.install-meta.json"
if [[ -f "$META_FILE" ]]; then
  report_pass "安装元数据存在"
else
  report_fail "缺少安装元数据 .install-meta.json"
fi

while IFS= read -r item; do
  [[ -z "$item" ]] && continue
  if [[ -f "$INSTALL_ROOT/commands/$item.md" ]]; then
    report_pass "command: $item"
  else
    report_fail "缺少 command: $item"
  fi
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
  if [[ -f "$INSTALL_ROOT/agents/$item.md" ]]; then
    report_pass "agent: $item"
  else
    report_fail "缺少 agent: $item"
  fi
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
  if [[ -f "$INSTALL_ROOT/skills/$item/SKILL.md" ]]; then
    report_pass "skill: $item"
  else
    report_fail "缺少 skill: $item"
  fi
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
  if [[ -f "$INSTALL_ROOT/rules/$group/$rule_name.md" ]]; then
    report_pass "rule: $group/$rule_name"
  else
    report_fail "缺少 rule: $group/$rule_name"
  fi
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
  if [[ -f "$INSTALL_ROOT/hooks/$item" ]]; then
    report_pass "hook: $item"
  else
    report_warn "缺少 hook: $item"
  fi
done < <(python3 - "$PROFILE_FILE" <<'PY'
import json, sys
with open(sys.argv[1], 'r', encoding='utf-8') as f:
    data = json.load(f)
for item in data.get('hooks', []):
    print(item)
PY
)

echo
if [[ "$FAILS" -eq 0 ]]; then
  if [[ "$WARNS" -eq 0 ]]; then
    echo "[backend-ecc] doctor 结果：PASS ($TOTAL checks)"
  else
    echo "[backend-ecc] doctor 结果：WARN ($TOTAL checks, $WARNS warnings)"
  fi
else
  echo "[backend-ecc] doctor 结果：FAIL ($TOTAL checks, $FAILS failures, $WARNS warnings)"
  exit 1
fi
