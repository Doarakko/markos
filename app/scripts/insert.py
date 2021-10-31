import argparse
import os
import sys

sys.path.append(os.path.abspath("."))
from db import Database
from message import Message

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("user_id", help="slack user id")

    args = parser.parse_args()
    user_id = args.user_id

    Database.initialise()
    message = Message()
    with open("data/{}_output.txt".format(user_id)) as f:
        list = []
        for line in f:
            t = (line,)
            list.append(t)

        message.adds(list)
