import os
import logging
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import db


logging.basicConfig(level=logging.WARNING)


app = App(token=os.environ["SLACK_BOT_TOKEN"])

db.init()


@app.event("app_mention")
def message(say):
    row = db.get_message_by_random()
    if row is None:
        return

    say(row["body"])


if __name__ == "__main__":
    handler = SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"])
    handler.start()
