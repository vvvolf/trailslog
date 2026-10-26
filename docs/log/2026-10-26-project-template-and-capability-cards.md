---
recorded: 2026-10-26
---

# Шаблон проекта и карточки возможностей

## Что сделано

- канонический шаблон нового проекта: `templates/project/core/`;
- `tools/new-project/new-project.sh` — создание проекта без handoff;
- карточка `docs/meta/capabilities/new-project.md`;
- формат карточек `docs/meta/capabilities/README.md`;
- KA о шаблоне — `docs/meta/knowledge/2026-10-26_5-KA-project-template.md`;
- KA о карточках — `docs/meta/knowledge/2026-10-26_6-KA-capability-cards.md`.

Коммит: `0905460 feat(tools): add canonical project template and new-project script`.

## Что не входит

- список источников карточек;
- реализация индекса и локального агента;
- миграция существующих проектов.

## Следующий шаг

Проверить шаблон на реальном проекте и решить, достаточно ли `core/` для
knowledge-only и code-проектов.
