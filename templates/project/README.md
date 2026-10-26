# Project template

Канонический шаблон проекта по методике TrailsLog.

`core/` — базовый слой: README, AGENTS, документация, публичный журнал,
треки, Work Item trails и правила private track. Это **не** копия
содержимого TrailsLog: только структура и контракты.

## Использование

Шаблон не копируется вручную в новые проекты. Его применяет
`tools/new-project/new-project.sh`:

```bash
tools/new-project/new-project.sh \
  --name <name> \
  --path <path> \
  --purpose "<purpose>" \
  --owner <owner> \
  --agent <agent> \
  --dry-run
```

`core/` уже включает `docs/meta/capabilities/` и `prompts/`. Флаг
`--kind code` добавляет нейтральные `src/` и `tests/`; стек проект выбирает
сам. Отдельного инструмента с профилями нет.

## Слои

- `docs/meta/` — живые знания, KA, артефакты, Work Item trails;
- `docs/log/` — публичный журнал;
- `docs/tracks/ideas/` — публичные идеи и задачи;
- `docs/tracks/private/` — private track: `log/` и приватный конвейер;
- локальные `docs/session.md`, `docs/next-tasks.md`, Work Item drafts и
  private track — вне git.

## Private track

- private log: `docs/tracks/private/log/`;
- private pipeline, WI, tracks и материалы: `docs/tracks/private/`;
- private track не является публичной частью проекта;
- public→private ссылки запрещены, private→public допустимы;
- старый путь `docs/log/private/` устарел; миграция существующих проектов —
  отдельно.

## Границы

- шаблон не выбирает стек кодового проекта;
- шаблон не переносит знания TrailsLog;
- workspace-специфичные пользователи и пути в шаблон не входят;
- миграция существующих проектов и автоматический doctor — отдельные
  работы.
