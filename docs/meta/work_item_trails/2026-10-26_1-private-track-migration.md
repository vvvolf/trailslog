---
category: Inbox
status: meta_integrated_partially
work_item_scope: |
  Завершить миграцию технологии private track: обновить шаблон нового
  проекта и кит на docs/tracks/private, проверить остальные проекты,
  убрать устаревшие ссылки на docs/log/private. В единицу не входит
  изменение самого KA/политики private track: они уже зафиксированы.
reason_for_capture: |
  Политика и карта слоёв обновлены, но шаблон/кит и часть проектов могут
  ещё использовать старый путь. Без отдельной задачи миграция потеряется.
resume_context: |
  В TrailsLog уже есть:
  - private-log-policy.md с docs/tracks/private/log/;
  - layer-map.md;
  - KA 2026-10-26_2-KA-private-track.md и 2026-10-26_3-KA-layer-map.md.
  Trail-games и workspace-knowledge уже переведены; шаблон/кит — отдельная
  сессия.
---

# Миграция private track

## Что осталось

- Сверить с текущим контрактом шаблона
  (`docs/meta/artefacts/project-template.md`) и KA ownership: где теперь
  живёт core и kit; не дублировать шаблон в workspace-knowledge.
- Обновить `new-project` skill и kit:
  - `docs/tracks/private/` в `.gitignore`;
  - `docs/tracks/private/log/` в структуре;
  - ссылки на layer-map;
  - явно: WI-черновики вне git, trail-README не WI.
- Проверить другие проекты на `docs/log/private/`.
- Убрать устаревшие ссылки в публичных документах.
- Проверить, что приватные файлы не попали в git.
- Решить, нужен ли автоматический линтер публичных ссылок на private.

## Границы

Не менять KA/политику private track без нового понимания. Не переносить чужие приватные данные без отдельного решения.


## Итог

- Канонический шаблон перенесён в
  `templates/project/core/`; создание — `tools/new-project/new-project.sh`.
- Отдельный kit удалён; его функции заменены одним скриптом.
- В шаблоне private track: `docs/tracks/private/` в `.gitignore`,
  `docs/tracks/private/log/` создаётся локально.
- `workspace-knowledge` и `trail-games` используют
  `docs/tracks/private/log/`; старый `docs/log/private/` не используется.
- Живые ссылки обновлены; исторические KA остаются историей.
- Не сделано: автоматический линтер/doctor для всех репозиториев.

Связанные документы: `../../../templates/project/README.md`,
`../../../docs/meta/artefacts/project-template.md`,
`../../../docs/meta/knowledge/2026-10-26_5-KA-project-template.md`.
