---
category: Principle
knowledge_type: Knowledge acquisition
scope_of_understanding: |
    Почему шаблон нового проекта должен принадлежать TrailsLog, а не
    workspace-контейнеру: каноническая структура, private track и контракт
    new-project script. В границы входит шаблон и его владение; за
    пределами — миграция существующих проектов, реализация агента и
    автоматический doctor.
composed_by: agent
lead: agent
human_participation: none
participation_updated: 2026-10-26
---

# Шаблон проекта принадлежит TrailsLog

## Исходная ситуация

Шаблон нового проекта жил в `workspace-knowledge/templates/repo/` и не
содержал private track. Private log в policy уже был исправлен на
`docs/tracks/private/log/`, но шаблон это не отражал. Получалось, что
технология создания проекта находится в workspace, а TrailsLog — только
источник ссылок.

## Приобретённое понимание

1. **Канонический шаблон — в TrailsLog.** `templates/project/core/` — это
   структура и контракты, а не знания конкретного проекта.
2. **Создание — один скрипт.** `tools/new-project/new-project.sh` копирует
   шаблон, заменяет placeholders, создаёт локальные файлы и делает
   `git init`.
3. **Private track — часть шаблона.** `.gitignore` исключает
   `docs/tracks/private/`; private log и приватный конвейер описаны в
   README/AGENTS шаблона.
4. **Workspace-специфика — снаружи.** Пользователи, абсолютные пути и
   capability cards не входят в публичный шаблон.
5. **Один источник — один шаблон.** Если шаблон нужен workspace-слою, он
   ссылается на TrailsLog, а не копирует структуру.
6. **Создание — один shell-скрипт.** Профили, модули и отдельная упаковка
   не нужны; шаблон, скрипт и карточка остаются в TrailsLog.

## Изменение модели

**Было:** шаблон в workspace-knowledge, private track отсутствует;
private log приходилось добавлять вручную.

**Стало:** канонический `trailslog/templates/project/core/`; его копирует
`tools/new-project/new-project.sh`; workspace-шаблон становится указателем,
а не второй копией; private track входит в контракт шаблона.

## Границы

- не переносит существующие проекты;
- не заменяет `doctor` и проверку всех репозиториев;
- не реализует локального агента;
- не добавляет workspace-пользователей и пути в публичный TrailsLog.

## Что я не проверял

- миграция `workspace-knowledge/templates/repo` и `new-project` skill
  завершена, но скрипт ещё не прогнан на реальном новом проекте;
- `doctor` по существующим репозиториям не запускался;
- не проверено, достаточно ли `core/` для всех типов проектов.

## Замечания генерации

Записано 2026-10-26 после обсуждения принадлежности шаблона и private
track. Связанные документы: `../artefacts/project-template.md`,
`../artefacts/layer-map.md`, `../artefacts/private-log-policy.md`,
`../capabilities/new-project.md`,
`2026-10-26_2-KA-private-track.md`, `2026-10-26_3-KA-layer-map.md`,
`../../../templates/project/README.md`,
`../../../tools/new-project/README.md`.
