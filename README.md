# TrailsLog

TrailsLog is a Telegram bot for capturing observations about everyday life.

Instead of forcing rigid data structures, it records what people actually want to remember. The accumulated observations later become material for analysis, reflection and AI-assisted insights.

Current status: early development.

The project is a loop: capture → files → interpretation. Capture is the
only stage that must be cheap and in the moment; interpretation is
deliberately deferred and replaceable — a person, a script, or any AI
model. What persists is the raw data and the conventions for working with
it. Portability of data and conventions is therefore a core requirement,
not a nice-to-have: the interpreter is interchangeable, the accumulated
material is the asset.

## Current features

- records predefined activities using Telegram commands;
- suggests commands directly in Telegram;
- stores every activity as a raw Telegram message;
- stores every plain text message sent in private chat;
- preserves original Telegram payload for future parsing;
- keeps data unstructured at the logging stage.

### Interaction model

Logging should be as frictionless as possible.

1. User sends a command (for example `/reading`).
2. The activity is immediately recorded.
3. The bot confirms that the activity was saved.
4. The user may reply to the bot's confirmation message to add arbitrary details.
5. The user may reply `DEL` or `-` to cancel the activity.

The bot intentionally postpones parsing and interpretation. Raw data is considered more valuable than forcing users into predefined forms.

## Project structure

- `src/` — source code
- `config/` — example configuration files
- `data/` — runtime data and local user configuration

### Documentation

- `docs/meta/` — project history, design notes and rationale; includes the
  knowledge conveyor (`work_items/`, `work_item_trails/`);
- `docs/log/` — project journal: course and key questions;
- `docs/meta/knowledge/` — knowledge base; key documents:
  `2026-07-13-why-trailslog.md` (project origins),
  `2026-07-14_2-capture-principles.md` (capture principles);
- `docs/meta/artefacts/` — derived documents and their support prompts:
  `working_set.md` (compact digest for AI dialogue with no repository
  access; may lag behind current understanding — the living sources are
  the documents in `docs/meta/knowledge/`) and `glossary.md` (terms with
  sources and readiness marks); the folder readme lists all files;
- `docs/tracks/ideas/` — implementation tasks and ideas; draft `work_items/`
  are kept locally and are not versioned.

The project grows incrementally. Every new component should solve a real problem and remain understandable.
