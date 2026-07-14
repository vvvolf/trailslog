# TrailsLog

TrailsLog is a Telegram bot for capturing observations about everyday life.

Instead of forcing rigid data structures, it records what people actually want to remember. The accumulated observations later become material for analysis, reflection and AI-assisted insights.

Current status: early development.

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
- `docs/meta/` — project history, design notes and rationale

The project grows incrementally. Every new component should solve a real problem and remain understandable.
