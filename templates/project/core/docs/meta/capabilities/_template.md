---
id: example.capability
title: Пример возможности
kind: capability
schema: 1
command: example-command --target <target>
plan: example-command --target <target> --dry-run
readonly: false
confirm: true
requires: [target]
---

## Когда использовать

Одно-два предложения: в какой ситуации человек или агент выбирает эту
возможность.

## Входы

- `<target>` — что это и как проверить.

## Выходы

Что изменится, что будет напечатано, какие файлы появятся.

## Ограничения

- что команда не делает;
- когда нужно остановиться и спросить человека.

## Пример

```bash
example-command --target /path/to/target --dry-run
```

## Связанное

- runbook: `docs/meta/artefacts/...`;
- KA: `docs/meta/knowledge/...`.
