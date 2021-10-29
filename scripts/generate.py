import argparse
import markovify


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("user_id", help="slack user id")
    parser.add_argument("-n", help="count of generate sentences", default=10)

    args = parser.parse_args()
    user_id = args.user_id
    n = args.n

    with open("data/{}_sentences.txt".format(user_id)) as f:
        text = f.read()

    text_model = markovify.NewlineText(text, well_formed=False, state_size=2)

    with open("data/{}_output.txt".format(user_id), mode="w") as f:
        for i in range(n):
            s = text_model.make_sentence()
            if s is None:
                continue

            s = s.replace(" ", "")
            f.write(s + "\n")
