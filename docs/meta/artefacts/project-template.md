# Project template: контракт

Живой контракт шаблона нового проекта. Каноническая структура —
`../../templates/project/core/`.

## Что входит

- README и AGENTS проекта;
- `docs/meta/` — knowledge, artefacts, Work Item trails;
- `docs/log/` — публичный журнал;
- `docs/tracks/ideas/` — публичный трек идей;
- `docs/tracks/private/` — private track: `log/` и приватный конвейер;
- `.gitignore` для локальных файлов и private track.

## Чего не входит

- стек кодового проекта;
- знания конкретного проекта;
- workspace-пользователи и пути;
- готовые карточки возможностей и команды конкретного проекта — их
  добавляет проект; шаблон даёт только формат и заготовки.

## Создание

`core/` уже включает `docs/meta/capabilities/` и `prompts/`. Скрипт
`tools/new-project/new-project.sh`:

- копирует `core/`;
- заменяет placeholders;
- создаёт локальные файлы и private track;
- делает `git init`.

Флаг `--kind code` добавляет нейтральные `src/` и `tests/`; стек проект
выбирает сам. Отдельного инструмента с профилями нет.

## Private track

- `docs/tracks/private/log/` — private log;
- `docs/tracks/private/` — private pipeline, WI, tracks, materials;
- private track не входит в публичный слой;
- `.gitignore` исключает `docs/tracks/private/`;
- старый `docs/log/private/` устарел.

## Первый коммит

1. Создать структуру и локальные ignored-файлы.
2. Проверить структуру.
3. Сделать первый коммит только по явной команде; без `git add .` и push.

## Связанное

- `layer-map.md` — карта слоёв;
- `private-log-policy.md` — private log и private track;
- `../knowledge/2026-10-26_2-KA-private-track.md`;
- `../knowledge/2026-10-26_5-KA-project-template.md`;
- `../../templates/project/README.md`.
