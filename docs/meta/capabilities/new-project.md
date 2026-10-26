---
id: project.create
title: Создать проект по методике TrailsLog
kind: capability
schema: 1
command: /media/sokv/data/workspace/working-local/sokv-pet-projects/trailslog_root/trailslog/tools/new-project/new-project.sh --name <name> --path <path> --purpose "<purpose>"
plan: /media/sokv/data/workspace/working-local/sokv-pet-projects/trailslog_root/trailslog/tools/new-project/new-project.sh --name <name> --path <path> --purpose "<purpose>" --dry-run
readonly: false
confirm: true
requires: [name, path, purpose]
---

## Когда использовать

Когда человек просит создать новый проект по структуре TrailsLog, а не
копировать содержимое существующего проекта.

## Входы

- `name` — имя проекта: латиница, цифры, точка, дефис, подчёркивание;
- `path` — путь; папка должна отсутствовать или быть пустой;
- `purpose` — одно-два предложения;
- опционально `--kind code`; по умолчанию knowledge.

## Порядок

1. Выполнить `plan` с `--dry-run`.
2. Показать человеку путь, kind и шаблон.
3. Получить подтверждение.
4. Выполнить `command` без `--dry-run`.
5. Скрипт копирует шаблон, создаёт локальные файлы и делает `git init`;
   коммит и push он не делает.
6. Первый коммит — только по явной команде.

## Выходы

Созданный проект, инициализированный git без коммита, локальные
`docs/session.md`, `docs/next-tasks.md`, `docs/tracks/private/` вне git.

## Ограничения

- не перезаписывать непустую папку;
- не выполнять коммит или push;
- не копировать приватные документы TrailsLog;
- не выдумывать стек для кодового проекта.

## Пример

```bash
/.../trailslog/tools/new-project/new-project.sh \
  --name demo-project \
  --path /tmp/opencode/demo-project \
  --purpose "Проверка сценария" \
  --dry-run
```

## Связанное

- `tools/new-project/README.md`;
- `docs/meta/artefacts/project-template.md`;
- `docs/meta/knowledge/2026-10-26_5-KA-project-template.md`.
