import argparse
import pandas as pd

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("user_id", help="slack user id")
    parser.add_argument(
        "-min", help="minimum word count in sentence", default=5, type=int
    )
    parser.add_argument("-max", help="max word count in sentence", default=10, type=int)

    args = parser.parse_args()
    user_id = args.user_id
    min_word_count = args.min
    max_word_count = args.max

    comments = pd.read_csv("data/{}_comments.csv".format(user_id))

    with open("data/{}_sentences.txt".format(user_id), mode="w") as f:
        for index, row in comments.iterrows():
            sentences = str(row["body_with_space"]).split("\n")
            for i in sentences:
                count = len(i.split())
                if count >= min_word_count and count <= max_word_count:
                    f.write(i + "\n")
