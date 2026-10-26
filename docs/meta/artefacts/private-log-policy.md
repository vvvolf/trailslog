# Private log policy

Практическая политика для приватных наблюдений. Источник решения:
[`../knowledge/2026-10-25_2-KA-private-observations-and-knowledge-layers.md`](../knowledge/2026-10-25_2-KA-private-observations-and-knowledge-layers.md).
Каноническая карта слоёв: [`layer-map.md`](layer-map.md).

## Слои

```text
KA            — обобщённое понимание, без приватных идентификаторов
public log    — публичный журнал проекта, docs/log/
private log   — сырые наблюдения и evidence, docs/tracks/private/log/
private track — приватный конвейер и материалы, docs/tracks/private/
WI            — будущая работа, черновик вне git
Trail         — история WI, в том же слое
```

## Что попадает в private log

- имена проектов и пути;
- размеры и результаты прогонов;
- приватные примеры;
- evidence для KA/WI.

Не попадают:

- пароли, токены, ключи;
- полные секреты;
- лишние персональные данные;
- материал, который можно обобщить без потери смысла.

## Жизненный цикл

```text
raw → triaged → linked / compacted / archived / deleted
```

- `raw` — только что записано;
- `triaged` — просмотрено, решено, что делать;
- `linked` — связано с KA или WI;
- `compacted` — сжато до evidence;
- `archived` — убрано в приватный архив;
- `deleted` — удалено после истечения срока или по решению.

## Индекс

В приватном track проекта:

```text
docs/tracks/private/log/index.md
docs/tracks/private/log/YYYY-MM-DD-topic.md
docs/tracks/private/log/archive/
```

Запись индекса:

```text
id | date | topic | status | links | retention
```

Поиск идёт по индексу, а не по всему сырому журналу.

## Private track

`docs/tracks/private/` — приватный track проекта. В нём:

```text
log/    — private log
...     — приватный конвейер, WI, tracks и материалы
```

Private track не является публичной частью проекта и не заменяет KA. WI и Trail наследуют слой источника: приватный WI — приватный Trail.

## Миграция

Старый путь `docs/log/private/` устарел. Целевой путь — `docs/tracks/private/log/`. Существующие приватные логи мигрируют отдельно; публичный журнал остаётся в `docs/log/`.

## Retention

| Класс | Срок |
|---|---|
| `session` | до конца сессии/недели |
| `evidence` | пока жив KA/WI, затем ревизия |
| `archive` | долго, ограниченный доступ |
| `secret` | не хранить |

## Ревизия

Триггеры:

- конец сессии;
- накопилось N записей;
- прошло 7/30/90 дней;
- KA/WI закрыт;
- перед публикацией или передачей проекта.

Действия:

1. Просмотреть новые `raw`.
2. Обновить статусы.
3. Связать с KA/WI.
4. Сжать evidence.
5. Удалить или archived лишнее.
6. Обновить индекс.

## Ссылки

- private log → public KA: допустимо;
- public KA → private log: запрещено;
- private KA → private log: допустимо;
- публичный артефакт должен быть понятен без private log;
- карта слоёв: [`layer-map.md`](layer-map.md).
