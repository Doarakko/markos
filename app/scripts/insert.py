import argparse
import os
import sys

sys.path.append(os.path.abspath("."))
import db

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("user_id", help="slack user id")

    args = parser.parse_args()
    user_id = args.user_id

    with open("data/{}_output.txt".format(user_id)) as f:
        list = []
        for line in f:
            t = (line,)
            list.append(t)

        db.add_messages(list)
