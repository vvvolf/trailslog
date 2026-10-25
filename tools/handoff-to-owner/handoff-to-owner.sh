#!/usr/bin/env bash
# handoff-to-owner.sh
#
# RECOMMENDED (reusable: one command, nothing to copy):
#   sudo bash handoff-to-owner.sh --owner <owner> --agent <agent> --target <dir>
#
# ONE-SHOT COPY (only when the folder leaves the workspace):
#   cp handoff-to-owner.sh <dir>/
#   printf '%s\n' handoff-to-owner.sh >> <dir>/.git/info/exclude
#   sudo bash <dir>/handoff-to-owner.sh --owner <owner> --agent <agent>
# It transfers ownership and deletes itself.
#
# Local exclude: in one-shot mode add `handoff-to-owner.sh` to
# .git/info/exclude (not .gitignore). That file is local, is not committed and
# is not cloned; it protects from `git add .` but not from `git add -f`. The
# script removes its own line after a successful transfer.
set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  sudo bash handoff-to-owner.sh --owner <owner> --agent <agent> --target <dir>
  sudo bash handoff-to-owner.sh --owner <owner> --agent <agent>   # one-shot copy

Options:
  --owner <user>   human who receives ownership (required)
  --agent <user>   agent user who keeps ACL access (required)
  --target <dir>   folder to hand off; recommended for reusable mode;
                   default: the script's own folder (one-shot mode)
  -h, --help       show this help

Examples:
  # recommended: reusable, run from anywhere
  sudo bash handoff-to-owner.sh --owner alice --agent agent --target /path/to/target

  # one-shot: copy into the target and run without --target
  sudo bash /path/to/target/handoff-to-owner.sh --owner alice --agent agent
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

if [ -f "$TARGET_DIR/.canonical" ]; then
  echo "Refusing to hand off a directory marked .canonical: $TARGET_DIR" >&2
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

# Apply the agent's ACL before ownership changes. If ACLs are not supported,
# abort while the agent still owns the tree instead of locking it out.
if ! setfacl -R -m "u:$AGENT:rwX" "$TARGET_DIR"; then
  echo "setfacl failed; ownership not changed" >&2
  exit 1
fi
if ! find "$TARGET_DIR" -type d -exec setfacl \
    -m "d:u:$AGENT:rwx" -m "d:u:$OWNER:rwx" {} +; then
  echo "default ACL failed; ownership not changed" >&2
  exit 1
fi

chown -R "$OWNER:$OWNER_GROUP" "$TARGET_DIR"

if [ -d "$TARGET_DIR/.git" ]; then
  add_safe_directory() {
    local user="$1"
    if ! sudo -H -u "$user" git config --global --get-all safe.directory \
        2>/dev/null | grep -qxF "$TARGET_DIR"; then
      sudo -H -u "$user" git config --global --add safe.directory "$TARGET_DIR" 2>/dev/null || true
    fi
  }
  if command -v sudo >/dev/null 2>&1; then
    add_safe_directory "$OWNER"
    add_safe_directory "$AGENT"

    # Do not leave the agent's local git identity on the human's repository.
    owner_name="$(sudo -H -u "$OWNER" git config --global user.name 2>/dev/null || true)"
    owner_email="$(sudo -H -u "$OWNER" git config --global user.email 2>/dev/null || true)"
    if [ -n "$owner_name" ] && [ -n "$owner_email" ]; then
      sudo -H -u "$OWNER" git -C "$TARGET_DIR" config --local user.name "$owner_name" 2>/dev/null || true
      sudo -H -u "$OWNER" git -C "$TARGET_DIR" config --local user.email "$owner_email" 2>/dev/null || true
    else
      sudo -H -u "$OWNER" git -C "$TARGET_DIR" config --local --unset-all user.name 2>/dev/null || true
      sudo -H -u "$OWNER" git -C "$TARGET_DIR" config --local --unset-all user.email 2>/dev/null || true
    fi

    if ! sudo -H -u "$AGENT" test -w "$TARGET_DIR"; then
      echo "warning: $AGENT cannot write $TARGET_DIR" >&2
    fi
    if ! sudo -H -u "$OWNER" git -C "$TARGET_DIR" status >/dev/null 2>&1; then
      echo "warning: git status failed for $OWNER in $TARGET_DIR" >&2
    fi
    if ! sudo -H -u "$AGENT" git -C "$TARGET_DIR" status >/dev/null 2>&1; then
      echo "warning: git status failed for $AGENT in $TARGET_DIR" >&2
    fi
  else
    echo "warning: sudo not found; safe.directory and git check skipped" >&2
  fi
fi

if [ "$SELF_DELETE" -eq 1 ] && [ -f "$TARGET_DIR/.git/info/exclude" ]; then
  # Rewrite in place to keep the owner and ACL of the original file.
  tmp_exclude="$(mktemp)"
  grep -vxF 'handoff-to-owner.sh' "$TARGET_DIR/.git/info/exclude" > "$tmp_exclude" || true
  cat "$tmp_exclude" > "$TARGET_DIR/.git/info/exclude"
  rm -f -- "$tmp_exclude"
fi

echo "ownership transferred to $OWNER"
if [ "$SELF_DELETE" -eq 1 ]; then
  echo "removing $SCRIPT_PATH"
  rm -f -- "$SCRIPT_PATH"
else
  echo "reusable tool kept at $SCRIPT_PATH"
fi
