# Layer map

Canonical map of project layers: path, git status, purpose. Read before creating, moving or deleting documents, Work Items and private notes.

| Layer | Path in a project | In git? | Purpose |
| --- | --- | --- | --- |
| KA | `docs/meta/knowledge/` | yes | read-only provenance trail of understanding |
| WI draft | `docs/meta/work_items/` | no | current work, local draft |
| WI draft in a track | `docs/tracks/ideas/work_items/` | no | local drafts for ideas and tasks |
| WI trail | `docs/meta/work_item_trails/` | yes | committed history of a Work Item |
| Public log | `docs/log/` | yes | course of work, decisions, questions |
| Private log | `docs/tracks/private/log/` | no / private | raw observations and evidence |
| Private pipeline | `docs/tracks/private/` | no / private | private tracks, WIs and materials |
| Public tracks | `docs/tracks/ideas/` | yes | public ideas and tasks |
| Artefacts | `docs/meta/artefacts/` | yes | derived documents, policies, maps |
| Session and tasks | `docs/session.md`, `docs/next-tasks.md` | no | local session plan and task list |
| Code and tools | project-specific | yes | implementation and reference tools |

## Rules

- Work Item drafts live outside git; a trail lives in git.
- `docs/meta/work_item_trails/README.md` documents the trail store; it is not a Work Item.
- The private layer is `docs/tracks/private`: `log/` for the private log, the root for the private pipeline.
- The public journal is `docs/log/`; it is not a private log.
- A public document does not link to the private log; a private document may link to a public one.
- If a new kind of material does not fit a layer, stop and ask. Do not invent a new folder.

## Private track

`docs/tracks/private/` is a private track of a project repository. It can contain:

```text
docs/tracks/private/log/       — private observations and evidence
docs/tracks/private/           — private pipeline, WI, tracks, materials
```

The private track is not part of the public knowledge layer. It is not a second knowledge base.

## Migration note

The earlier policy used `docs/log/private/`. The canonical path is now `docs/tracks/private/log/`. Existing project-private logs may still need migration; the path in this map is the target.

## References

- `private-log-policy.md`
- `../knowledge/2026-10-25_2-KA-private-observations-and-knowledge-layers.md`
- `../knowledge/2026-10-26_2-KA-private-track.md`
- `../knowledge/2026-10-26_3-KA-layer-map.md`
