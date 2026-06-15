#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
# shellcheck source=./lib.sh
source "$SCRIPT_DIR/lib.sh"

TARGET=""
DEST_ROOT=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --target)
      TARGET="$2"
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

if [[ -z "$TARGET" ]]; then
  echo "用法: uninstall.sh --target <claude|codex> [--dest <目录>]" >&2
  exit 1
fi

ROOT="$(backend_ecc_root)"
ADAPTER_FILE="$ROOT/adapters/$TARGET/install-map.json"
backend_ecc_require_file "$ADAPTER_FILE"

TARGET_ROOT="$(backend_ecc_read_json_field "$ADAPTER_FILE" root)"
if [[ -n "$DEST_ROOT" ]]; then
  INSTALL_ROOT="$DEST_ROOT/$TARGET_ROOT/backend-ecc"
else
  INSTALL_ROOT="$PWD/$TARGET_ROOT/backend-ecc"
fi

if [[ -d "$INSTALL_ROOT" ]]; then
  rm -rf "$INSTALL_ROOT"
  echo "[backend-ecc] 卸载完成"
  echo "- target: $TARGET"
  echo "- root: $INSTALL_ROOT"
else
  echo "[backend-ecc] 未发现可卸载目录"
  echo "- target: $TARGET"
  echo "- root: $INSTALL_ROOT"
fi
