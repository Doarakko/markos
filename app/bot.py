import os
import logging
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from db import Database
from message import Message


logging.basicConfig(level=logging.WARNING)


app = App(token=os.environ["SLACK_BOT_TOKEN"])


@app.event("app_mention")
def message(say):
    message = Message()
    row = message.get_by_random()
    say(row.body)


if __name__ == "__main__":
    Database.initialise()

    handler = SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"])
    handler.start()
