#!/usr/bin/env bash
# Create a project from the canonical TrailsLog template.
# Usage:
#   new-project.sh --name demo --path /tmp/demo --purpose "..." \
#     [--kind knowledge|code] [--dry-run]
#
# The script copies templates/project/core, replaces project placeholders,
# creates local ignored files, and initializes git. It does not commit or push.

set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
TRAILSLOG_ROOT="$(cd -- "$SCRIPT_DIR/../.." && pwd -P)"
TEMPLATE="$TRAILSLOG_ROOT/templates/project/core"

NAME=""
TARGET_ARG=""
PURPOSE=""
KIND="knowledge"
DRY_RUN=0

usage() {
  cat <<'EOF'
Usage:
  new-project.sh --name <name> --path <path> --purpose "<purpose>" \
    [--kind knowledge|code] [--dry-run]

Options:
  --name      project name: letters, digits, dot, dash, underscore
  --path      target directory; must be missing or empty
  --purpose   one or two sentences about the project
  --kind      knowledge (default) or code
  --dry-run   validate and show the plan; do not write
  -h, --help  show this help
EOF
}

die() {
  echo "new-project: $*" >&2
  exit 2
}

while [ "$#" -gt 0 ]; do
  case "$1" in
    --name) [ "$#" -ge 2 ] || die "--name requires a value"; NAME="$2"; shift 2 ;;
    --path) [ "$#" -ge 2 ] || die "--path requires a value"; TARGET_ARG="$2"; shift 2 ;;
    --purpose) [ "$#" -ge 2 ] || die "--purpose requires a value"; PURPOSE="$2"; shift 2 ;;
    --kind) [ "$#" -ge 2 ] || die "--kind requires a value"; KIND="$2"; shift 2 ;;
    --dry-run) DRY_RUN=1; shift ;;
    -h|--help) usage; exit 0 ;;
    *) die "unknown argument: $1" ;;
  esac
done

[ -n "$NAME" ] && [ -n "$TARGET_ARG" ] && [ -n "$PURPOSE" ] \
  || { usage; exit 2; }

[[ "$NAME" =~ ^[A-Za-z0-9][A-Za-z0-9._-]*$ ]] \
  || die "invalid name: $NAME"
[ "$KIND" = "knowledge" ] || [ "$KIND" = "code" ] \
  || die "kind must be knowledge or code: $KIND"
[ -d "$TEMPLATE" ] || die "template not found: $TEMPLATE"

TARGET="$(realpath -m -- "$TARGET_ARG")"
[ "$TARGET" != "/" ] || die "refusing /"
if [ -e "$TARGET" ]; then
  [ -d "$TARGET" ] || die "target is not a directory: $TARGET"
  [ -z "$(ls -A "$TARGET")" ] || die "target is not empty: $TARGET"
fi

if [ "$DRY_RUN" -eq 1 ]; then
  echo "would create: $TARGET"
  echo "kind: $KIND"
  echo "template: $TEMPLATE"
  exit 0
fi

mkdir -p "$TARGET"
cp -a "$TEMPLATE/." "$TARGET/"

escape_sed() {
  printf '%s' "$1" | sed 's/[\\&|]/\\&/g'
}

ESC_PURPOSE="$(escape_sed "$PURPOSE")"

find "$TARGET" -type f -exec sed -i \
  -e "s|<Project>|$NAME|g" \
  -e "s|<project>|$NAME|g" \
  -e "s|<purpose>|$ESC_PURPOSE|g" {} +

mkdir -p \
  "$TARGET/docs/meta/work_items" \
  "$TARGET/docs/tracks/ideas/work_items" \
  "$TARGET/docs/tracks/private/log/archive"

STAMP="$(date '+%Y-%m-%d %H:%M')"
TODAY="$(date '+%Y-%m-%d')"

cat > "$TARGET/docs/session.md" <<EOF
## $NAME-$TODAY — active
owner: agent
opened: $STAMP
updated: $STAMP

### Нити

- Инициализация проекта.
EOF

cat > "$TARGET/docs/next-tasks.md" <<EOF
# Актуальные задачи ($NAME)

Обновлён: $TODAY.

## Задачи

1. Проверить структуру проекта и первый коммит.
EOF

cat > "$TARGET/docs/tracks/private/README.md" <<'EOF'
# Private track

Приватный слой проекта. Не публикуется и не коммитится.

- `log/` — private log;
- остальное — приватный конвейер, WI, tracks и материалы.

Политика — в TrailsLog: `docs/meta/artefacts/private-log-policy.md`.
EOF

cat > "$TARGET/docs/tracks/private/log/index.md" <<'EOF'
# Private log index

id | date | topic | status | links | retention
EOF

if [ "$KIND" = "code" ]; then
  mkdir -p "$TARGET/src" "$TARGET/tests"
  cat > "$TARGET/src/README.md" <<'EOF'
# Код проекта

Стек выбирается отдельно; шаблон не навязывает язык и фреймворк.
EOF
  cat > "$TARGET/tests/README.md" <<'EOF'
# Тесты проекта

Тесты кода и проверки контрактов. Перед коммитом должны проходить.
EOF
fi

if ! git -C "$TARGET" init -b main >/dev/null 2>&1; then
  git -C "$TARGET" init >/dev/null
  git -C "$TARGET" symbolic-ref HEAD refs/heads/main
fi

echo "created: $TARGET"
echo "kind: $KIND"
echo "git: initialized; no commit"
