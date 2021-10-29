import argparse
import pandas as pd

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("user_id", help="slack user id")
    parser.add_argument("-min", help="minimum word count in sentence", default=5)

    args = parser.parse_args()
    user_id = args.user_id
    min_word_count = args.min

    comments = pd.read_csv("data/{}_comments.csv".format(user_id))

    with open("data/{}_sentences.txt".format(user_id), mode="w") as f:
        for index, row in comments.iterrows():
            sentences = str(row["body_with_space"]).split("\n")
            for i in sentences:
                if len(i.split()) >= min_word_count:
                    f.write(i + "\n")
