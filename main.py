import sys
import string
import ijson
from collections import defaultdict
from pydantic import ValidationError
from schemas import TGMessage
from config import (
    JSON_PATH,
    STOPLIST,
    TEXT_LIKE_ENTITY_TYPES,
    DEVELOPMENT_MODE,
)

if __name__ == "__main__":
    # {user: int}
    total_chars: dict[str, int] = defaultdict(
        int
    )  # total amount of characters for a user
    # {user: int}
    msg_counts: dict[str, int] = defaultdict(int)  # total amount of messages for a user
    # {user: {word: int}}
    words: dict[str, dict[str, int]] = defaultdict(
        lambda: defaultdict(int)
    )  # words data for a user

    print("=== ULTIMATE TELEGRAM CHAT ANALYZER 3000 ===")
    print("BEGINNING ANALYSIS... (this may take a while on large files)")

    try:
        with open(JSON_PATH, "rb") as file:
            messages_stream = ijson.items(file, "messages.item")

            for raw_msg in messages_stream:
                if "from" not in raw_msg:
                    continue

                try:
                    message = TGMessage.model_validate(raw_msg)
                except ValidationError:
                    if DEVELOPMENT_MODE:
                        raise
                    continue

                if message.from_field is None:
                    continue

                length = 0
                msg_words = []

                for entity in message.text_entities:
                    if entity.type in TEXT_LIKE_ENTITY_TYPES:
                        clean_text = entity.text.strip()
                        length += len(clean_text)
                        msg_words.extend(clean_text.split(" "))

                user = message.from_field
                total_chars[user] += length
                msg_counts[user] += 1

                user_word_stats = words[user]
                for word in msg_words:
                    clean_word = word.lower().strip(string.punctuation + "—«»…")
                    if len(clean_word) <= 3 or clean_word in STOPLIST:
                        continue
                    user_word_stats[clean_word] += 1

    except FileNotFoundError:
        print("File not found! Check config.py")
        sys.exit(1)

    grand_total_len = sum(total_chars.values())

    if grand_total_len == 0:
        print("No text data found.")
        sys.exit(0)

    for user, total_user_len in total_chars.items():
        count = msg_counts[user]
        avg_len = total_user_len / count if count > 0 else 0
        percentage = (total_user_len / grand_total_len) * 100

        print(
            f"{user}: {percentage:.2f}%, average message is {avg_len:.2f} characters long"
        )

        top_3 = sorted(words[user].items(), key=lambda x: x[1], reverse=True)[:3]
        print(f"{user}'s TOP 3 most used words:")
        for i, (word, freq) in enumerate(top_3, 1):
            print(f"{i}. {word} - {freq} times")
