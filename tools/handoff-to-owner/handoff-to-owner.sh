#!/usr/bin/env bash
# handoff-to-owner.sh
#
# COPY-PASTE COMMAND (generic):
#   sudo bash handoff-to-owner.sh --owner <owner> --agent <agent> [--target <dir>]
#
# One-shot mode: copy this script into the target folder and run without
# --target. It transfers ownership and deletes itself.
# Reusable mode: run from this tools directory with --target; it does not delete
# itself.
#
# Local exclude: in one-shot mode add `handoff-to-owner.sh` to
# .git/info/exclude (not .gitignore). That file is local, is not committed and
# is not cloned; it protects from `git add .` but not from `git add -f`. The
# script removes its own line after a successful transfer.
set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  sudo bash handoff-to-owner.sh --owner <owner> --agent <agent> [--target <dir>]

Options:
  --owner <user>   human who receives ownership (required)
  --agent <user>   agent user who keeps ACL access (required)
  --target <dir>   folder to hand off; default: the script's own folder
  -h, --help       show this help

Examples:
  # one-shot: copy into the target and run
  sudo bash /path/to/target/handoff-to-owner.sh --owner alice --agent agent

  # reusable: run from the tools directory
  sudo bash handoff-to-owner.sh --owner alice --agent agent --target /path/to/target
EOF
}

OWNER=""
AGENT=""
TARGET_ARG=""

while [ "$#" -gt 0 ]; do
  case "$1" in
    --owner)
      [ "$#" -ge 2 ] || { usage; exit 2; }
      OWNER="$2"
      shift 2
      ;;
    --agent)
      [ "$#" -ge 2 ] || { usage; exit 2; }
      AGENT="$2"
      shift 2
      ;;
    --target)
      [ "$#" -ge 2 ] || { usage; exit 2; }
      TARGET_ARG="$2"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "unknown argument: $1" >&2
      usage
      exit 2
      ;;
  esac
done

if [ -z "$OWNER" ] || [ -z "$AGENT" ]; then
  usage
  exit 2
fi

SCRIPT_PATH="$(readlink -f -- "${BASH_SOURCE[0]}")"
SCRIPT_DIR="$(dirname -- "$SCRIPT_PATH")"

if [ -n "$TARGET_ARG" ]; then
  TARGET_DIR="$(readlink -f -- "$TARGET_ARG")"
else
  TARGET_DIR="$SCRIPT_DIR"
fi

if [ -z "$TARGET_DIR" ] || [ ! -d "$TARGET_DIR" ]; then
  echo "target is not a directory: ${TARGET_ARG:-$TARGET_DIR}" >&2
  exit 2
fi

if [ "$TARGET_DIR" = "/" ]; then
  echo "Refusing to chown /" >&2
  exit 2
fi

# Protect the canonical public copy from accidental self-chown.
if [ "$TARGET_DIR" = "$SCRIPT_DIR" ] && [ -f "$SCRIPT_DIR/.canonical" ]; then
  echo "This is the canonical tool. Copy it into the target or use --target." >&2
  exit 2
fi

if [ "$(id -u)" -ne 0 ]; then
  echo "Run with sudo: sudo bash $SCRIPT_PATH --owner $OWNER --agent $AGENT" >&2
  exit 1
fi

if ! id "$OWNER" >/dev/null 2>&1; then
  echo "owner user does not exist: $OWNER" >&2
  exit 2
fi

if ! id "$AGENT" >/dev/null 2>&1; then
  echo "agent user does not exist: $AGENT" >&2
  exit 2
fi

if ! command -v setfacl >/dev/null 2>&1; then
  echo "setfacl is required for agent ACL access" >&2
  exit 2
fi

OWNER_GROUP="$(id -gn "$OWNER")"
SELF_DELETE=0
if [ "$TARGET_DIR" = "$SCRIPT_DIR" ]; then
  SELF_DELETE=1
fi

echo "target: $TARGET_DIR"
echo "owner:  $OWNER ($OWNER_GROUP)"
echo "agent:  $AGENT (ACL access will be preserved)"
echo "mode:   $([ "$SELF_DELETE" -eq 1 ] && echo one-shot || echo reusable)"

chown -R "$OWNER:$OWNER_GROUP" "$TARGET_DIR"
setfacl -R -m "u:$AGENT:rwX" "$TARGET_DIR"
find "$TARGET_DIR" -type d -exec setfacl -m "d:u:$AGENT:rwx" {} +

if [ -d "$TARGET_DIR/.git" ]; then
  if command -v sudo >/dev/null 2>&1; then
    sudo -u "$OWNER" git config --global --add safe.directory "$TARGET_DIR" 2>/dev/null || true
    sudo -u "$AGENT" git config --global --add safe.directory "$TARGET_DIR" 2>/dev/null || true
  fi
fi

if [ "$SELF_DELETE" -eq 1 ] && [ -f "$TARGET_DIR/.git/info/exclude" ]; then
  sed -i '\|^handoff-to-owner\.sh$|d' "$TARGET_DIR/.git/info/exclude" 2>/dev/null || true
fi

echo "ownership transferred to $OWNER"
if [ "$SELF_DELETE" -eq 1 ]; then
  echo "removing $SCRIPT_PATH"
  rm -f -- "$SCRIPT_PATH"
else
  echo "reusable tool kept at $SCRIPT_PATH"
fi
