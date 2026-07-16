from collections import defaultdict
from datetime import datetime
from datetime import timedelta
from datetime import timezone

from trailslog.activities import ACTIVITIES
from trailslog.goals import GOALS
from trailslog.database.database import get_messages_for_date


def build_today_report(chat_id: int, user_id: int):

    now = datetime.now(timezone.utc)

    start = datetime(
        now.year,
        now.month,
        now.day,
        tzinfo=timezone.utc,
    )

    end = start + timedelta(days=1)

    rows = get_messages_for_date(
        chat_id,
        user_id,
        int(start.timestamp()),
        int(end.timestamp()),
    )

    completed = collect_completed_commands(rows)

    messages = {}

    children = defaultdict(list)

    for row in rows:

        messages[row["telegram_message_id"]] = row

        if row["reply_to_message_id"]:
            children[
                row["reply_to_message_id"]
            ].append(row)

    report = []

    for message_id, row in messages.items():

        if row["reply_to_message_id"]:
            continue

        text = row["text"]

        if text.startswith("/"):

            command = text[1:].split()[0]

            title = ACTIVITIES.get(
                command,
                command,
            )

        else:

            title = text

        report.append(f"• {title}")

        for child in children.get(message_id, []):

            report.append(
                f"    {child['text']}"
            )

        report.append("")
    
    append_goal_status(
        report,
        completed,
    )

    if not report:
        return "Nothing recorded today."

    return "\n".join(report)


def collect_completed_commands(rows):

    completed = set()

    for row in rows:

        text = row["text"]

        if not text.startswith("/"):
            continue

        command = text[1:].split()[0]

        completed.add(command)

    return completed


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

