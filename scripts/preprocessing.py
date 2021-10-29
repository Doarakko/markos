import argparse
import re
import pandas as pd
import spacy
import swifter


nlp = spacy.load("ja_ginza")

code_regex = re.compile(
    "[!\"#$%&'\\\\()*+,-./:;<=>?@[\\]^_`{|}~「」〔〕“”〈〉『』【】＆＊・（）＄＃＠。、？！｀＋￥％…←↑→↓]"
)


def preprocessing(row):
    row["body"] = re.sub(":.+:", "", row["body"])
    row["body"] = code_regex.sub("", row["body"])

    if row["body"].startswith("p "):
        row["body"] = row["body"].replace("p ", "", 1)

    if row["body"].startswith("s "):
        row["body"] = row["body"].replace("s ", "", 1)

    doc = nlp(row["body"])
    l = []
    for sent in doc.sents:
        s = ""
        for ent in sent:
            if len(s) == 0:
                s = str(ent)
            else:
                s = "{} {}".format(s, ent)
        l.append(s)

    row["body_with_space"] = "\n".join(l)

    return row


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("user_id", help="slack user id")

    args = parser.parse_args()
    user_id = args.user_id

    comments = pd.read_csv("data/comments.csv")

    comments = comments[
        (comments["subtype"].isnull())
        & (comments["user"] == user_id)
        & (comments["body"].str.contains("<@.*>") == False)
        & (comments["body"].str.contains("```") == False)
        & (comments["body"].str.contains("<#.*>") == False)
        & (comments["body"].str.contains("<!subteam.*>") == False)
        & (comments["body"].str.contains("http") == False)
        & (comments["body"].str.contains("`.+`") == False)
        & (comments["body"].str.contains("m\(_ _\)m") == False)
        & (comments["body"].str.contains("ありがとう") == False)
        & (comments["body"].str.contains("おめでとう") == False)
        & (comments["body"].str.contains("お疲れ") == False)
        & (comments["body"].str.contains("botman") == False)
        & (comments["body"].str.contains("起票") == False)
        & (comments["body"].str.startswith("&gt;") == False)
        & (comments["body"].str.startswith("did") == False)
        & (comments["body"].str.startswith("todo") == False)
        & (comments["body"].str.startswith(" todo") == False)
        & (comments["body"].str.startswith("TODO") == False)
        & (comments["body"].str.startswith("done") == False)
        & (comments["body"].str.startswith("memo") == False)
        & (comments["body"].str.startswith("doing") == False)
        & (comments["body"].str.startswith("do ne") == False)
    ]

    comments = comments.swifter.apply(lambda x: preprocessing(x), axis=1)
    comments.to_csv("data/{}_comments.csv".format(user_id))
