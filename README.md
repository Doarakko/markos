# markos

Create Slack bot using Slack past messages and markov chain.

You can also use a CSV file instead of Slack comments.

## Requirements

- docker-compose
- Slack
- Heroku
  - Not required if run on local
- CSV file
  - Not required if use Slack comments

### Expected CSV format

| id  | body                                       |
| :-- | :----------------------------------------- |
| 1   | 私は天才エンジニアです。                   |
| 2   | お腹空き空き空き空き空きっ腹。寿司食うぞ。 |
| ... | ...                                        |

## Usage

### 1. Create `.env` file

```sh
cp .env.example .env
```

### 2. Create Slack app

Easy to create using `manifest.yml`.

Get App-Level Token(`xapp-aaaa`) and Bot User OAuth Token(`xoxb-bbbb`).

### 3. Edit `.env` file

Enter `SLACK_APP_TOKEN` and `SLACK_BOT_TOKEN`.

### 4. Run

```sh
docker-compose up
```

### 5. Get Slack comments

`q` specifies the name of the channels from which to get the comments.

All channels containing `q` are included.
If you specify `times`, you can get it from `*times*`.

```sh
docker exec -it app python scripts/1_save_slack_comments.py <query>
```

Choose a user to create a bot.
User id is like `U0123abcd`.

```sh
docker exec -it app python scripts/2_select_slack_user.py <user id>
```

If you use the CSV file you have already prepared, skip it.

### 7. Preprocessing and make text file

You can specify the input and output file path by specifying the `-i` and `-o` options.(optional)

```sh
docker exec -it app python scripts/3_preprocessing.py -i <input> -o <output>
```

You can use `-min` and `-max` options to limit the size of the sentence you use.(optional)

If the `-min` is 6, then `我々4歳くらいです`(`我々 4 歳 くらい です`) is excluded.

```sh
docker exec -it app python scripts/4_make_sentences.py -i <input> -o <output> -min <minimum word count> -max <max word count>
```

### 8. Generate sentences

You can use `-s` to specify how many morphemes of the original sentence to use.

Larger will produce the correct sentece, but it's boring.

```sh
docker exec -it app python scripts/5_generate.py -i <input> -o <output> -n <count of generate sentences> -s <state size>
```

Let's enjoy tuning!

### 9. Create table and insert records

```sh
docker exec -it app python scripts/6_create_table.py
```

```sh
docker exec -it app python scripts/7_insert.py
```

## Run on Heroku

Click "Deploy to Heroku" Button and enter your environment valiables.

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

Get `DATABASE_URL` from `Settings/Config Vars` on Heroku dashboard.

On local enter the `DATABASE_URL`, other data create and insert methods are the same as the above local step.
