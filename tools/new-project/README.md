# new-project

Create a project from the canonical TrailsLog template.

## Contract

```bash
new-project.sh \
  --name <name> \
  --path <path> \
  --purpose "<purpose>" \
  [--kind knowledge|code] \
  [--dry-run]
```

- `name` — letters, digits, dot, dash, underscore;
- `path` — missing or empty directory; non-empty is refused;
- `purpose` — one or two sentences;
- `kind` — `knowledge` (default) or `code`;
- `dry-run` — validate and show the plan without writing.

The script does not commit or push.

## What it does

1. Copies `templates/project/core/`.
2. Replaces `<Project>`, `<project>`, `<purpose>`.
3. Creates local ignored files:
   - `docs/session.md`;
   - `docs/next-tasks.md`;
   - `docs/tracks/private/README.md`;
   - `docs/tracks/private/log/index.md`;
   - Work Item draft directories.
4. Adds `src/README.md` and `tests/README.md` for `--kind code`.
5. Runs `git init -b main`.

## After creation

Review the structure, then commit only by explicit command, with an explicit
file list.

## Boundaries

- no code stack is chosen;
- no knowledge is copied from TrailsLog;
- no project-specific capability cards or prompts are guessed;
- existing projects are not migrated;
- private track is local/private, not public;
- no commit or push.

## Why one script, not a framework

A Python package with profiles and modules was more than this task needs.
The template is files; the repeated work is one copy/replace/init sequence.
One shell script is enough. If the logic grows (multiple templates,
migration, several consumers), it can be promoted to a separate tool then.
