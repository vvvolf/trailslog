---
category: Principle
knowledge_type: Knowledge acquisition
composed_by: agent
lead: agent
human_participation: none
participation_updated: 2026-10-26
scope_of_understanding: |
    Приватный слой проекта: private log и приватный конвейер живут в
    docs/tracks/private; публичный журнал остаётся docs/log. В границы
    входит разделение слоёв и канонические пути; за пределами — карта
    слоёв, миграция всех проектов и шаблон нового проекта.
---

# Приватный track проекта

## Было

Политика private log описывала `docs/log/private/`. Отдельного приватного track не было. Приватный лог оказывался подпапкой публичного журнала, а приватный конвейер не имел места.

## Стало

- Приватный слой проекта — `docs/tracks/private/`.
- Приватный лог — `docs/tracks/private/log/`.
- Приватный конвейер, приватные WI, tracks и материалы — в корне `docs/tracks/private/`.
- Публичный журнал — `docs/log/`; это не private log.
- Старый путь `docs/log/private/` устарел; существующие проекты мигрируют отдельно.
- WI-черновики — вне git; trail — в git; README хранилища trail — не Work Item.

## Почему

- Публичное и приватное разделяются по слою, а не по догадке.
- Приватный лог перестаёт быть подпапкой публичного журнала.
- Приватный конвейер получает место, не смешиваясь с публичным.
- Проекты могут ссылаться на единый слой, а не изобретать `private/`.

## Следствия

- `private-log-policy.md` обновлена на `docs/tracks/private/log/` и приватный track.
- `AGENTS.md` и `README.md` указывают новый путь.
- Старый путь считается устаревшим.

## Границы

Не решает: карту слоёв, миграцию всех проектов, шаблон/кит, автоматическую проверку ссылок.

## Связанные

- `docs/meta/artefacts/private-log-policy.md`
- `docs/meta/knowledge/2026-10-25_2-KA-private-observations-and-knowledge-layers.md`
