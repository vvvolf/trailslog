from collections import defaultdict
from datetime import datetime
from datetime import timedelta
from datetime import timezone

from trailslog.activities import ACTIVITIES
from trailslog.goals import GOALS
from trailslog.database.database import get_root_records_for_period
from trailslog.database.database import get_record
from trailslog.models import Block


def render_block(report, block, level):
    indent = "    " * level

    report.append(
        f"{indent}{block.row['text']}"
    )

    for child in visible_children(block):
        render_block(
            report,
            child,
            level + 1,
        )


def render_record(
    report: list[str],
    record: Block,
):
    text = record.row["text"]

    if text.startswith("/"):
        command = text[1:].split()[0]

        title = ACTIVITIES.get(
            command,
            command,
        )
    else:
        title = text

    report.append(
        f"• {title}"
    )

    for child in visible_children(record):
        render_block(
            report,
            child,
            level=1,
        )


def visible_children(block):
    result = []

    for child in block.children:
        if is_bot_message(child):
            result.extend(
                visible_children(child)
            )
        else:
            result.append(child)

    return result


def is_bot_message(block: Block) -> bool:
    return int(block.row["is_bot"]) == 1


def build_today_report(chat_id: int, user_id: int):

    now = datetime.now()

    start = datetime(
        now.year,
        now.month,
        now.day,
    )

    end = start + timedelta(days=1)

    roots = get_root_records_for_period(
        chat_id,
        user_id,
        int(start.timestamp()),
        int(end.timestamp()),
    )

    completed = set()

    report = []

    for root in roots:
        record = get_record(
            chat_id,
            root["telegram_message_id"],
        )

        render_record(
            report,
            record,
        )
        
        if root["text"].startswith("/"):

            completed.add(
                root["text"][1:].split()[0]
            )

        report.append("")
    
    append_goal_status(
        report,
        completed,
    )

    if not report:
        return "Nothing recorded today."

    return "\n".join(report)


def append_goal_status(report, completed):

    goal = GOALS.get("daily")

    if goal is None:
        return

    missing = [
        command
        for command in goal.required
        if command not in completed
    ]

    report.append("────────────")
    report.append("")

    if not missing:

        report.append(goal.success_message)
        return

    report.append(goal.failure_message)
    report.append("")

    for command in missing:

        report.append(
            f"• {ACTIVITIES.get(command, command)}"
        )

