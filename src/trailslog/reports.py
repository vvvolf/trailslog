from collections import defaultdict
from datetime import datetime
from datetime import timedelta
from datetime import timezone

from trailslog.activities import ACTIVITIES
from trailslog.database.database import get_messages_for_date


def build_today_report(chat_id: int):

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
        int(start.timestamp()),
        int(end.timestamp()),
    )

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

    if not report:
        return "Nothing recorded today."

    return "\n".join(report)
    