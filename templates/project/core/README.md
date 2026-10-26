# <Project>

<purpose>

Статус: ранняя разработка.

## Структура

- `docs/meta/knowledge/` — живые знания и KA;
- `docs/meta/artefacts/` — производные документы и runbook;
- `docs/log/` — журнал проекта;
- `docs/tracks/ideas/` — идеи и задачи;
- `docs/meta/work_items/` — черновики Work Item (вне git);
- `docs/meta/work_item_trails/` — следы Work Item (в git);
- `docs/tracks/private/` — private track: `log/` для private log,
  остальное — приватный конвейер и материалы (вне git или в приватном
  репозитории).

В шаблон уже входят `docs/meta/capabilities/` для карточек возможностей и
`prompts/` для команд проекта. `src/` и `tests/` добавляются для кодового
проекта.

## Запуск

Если это кодовый проект — опишите команду запуска. Если проект
knowledge-only — удалите этот раздел.
