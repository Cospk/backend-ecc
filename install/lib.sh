#!/usr/bin/env bash
set -euo pipefail

backend_ecc_root() {
  local script_dir
  script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
  cd "$script_dir/.." && pwd
}

backend_ecc_version() {
  local root
  root="$(backend_ecc_root)"
  tr -d '\n' < "$root/VERSION"
}

backend_ecc_read_json_field() {
  local file="$1"
  local expr="$2"
  python3 - "$file" "$expr" <<'PY'
import json, sys
path, expr = sys.argv[1], sys.argv[2]
with open(path, 'r', encoding='utf-8') as f:
    data = json.load(f)
parts = expr.split('.') if expr else []
cur = data
for part in parts:
    cur = cur[part]
if isinstance(cur, (dict, list)):
    print(json.dumps(cur, ensure_ascii=False))
else:
    print(cur)
PY
}

backend_ecc_require_file() {
  local file="$1"
  if [[ ! -f "$file" ]]; then
    echo "[backend-ecc] 缺少文件: $file" >&2
    exit 1
  fi
}

backend_ecc_now_utc() {
  date -u +"%Y-%m-%dT%H:%M:%SZ"
}

backend_ecc_copy_file() {
  local src="$1"
  local dst="$2"
  mkdir -p "$(dirname "$dst")"
  cp "$src" "$dst"
}

backend_ecc_write_install_meta() {
  local file="$1"
  local version="$2"
  local target="$3"
  local profile="$4"
  local installed_at="$5"
  shift 5
  python3 - "$file" "$version" "$target" "$profile" "$installed_at" "$@" <<'PY'
import json, sys
file, version, target, profile, installed_at, *installed_files = sys.argv[1:]
data = {
    "version": version,
    "target": target,
    "profile": profile,
    "installed_at": installed_at,
    "installed_files": installed_files,
}
with open(file, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
    f.write('\n')
PY
}
