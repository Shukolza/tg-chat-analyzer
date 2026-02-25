# Telegram chat analyzer

![Python version](https://img.shields.io/badge/Python%20version-3.9+-3776AB?logo=python&logoColor=3776AB)

## Description

**UPD: Tested on large (200MB+) dumps, works with group chats and DMs**  
A blazingly fast and memory-efficient Python tool to analyze your personal Telegram chat exports.
Ever wondered who texts more in your relationships, or what your most used words are? The analyzer reads through massive JSON chat dumps using memory streaming, calculates text volume percentages, average message lengths, and extracts the top 3 most used words for each participant.

## Table of Contents

1. [Example Output](#example-output)
2. [How to get the Telegram Chat Dump](#how-to-get-the-telegram-chat-dump)
3. [Installation & Usage](#installation--usage)
4. [Configuration](#configuration)

## Example Output

```text
=== ULTIMATE TELEGRAM CHAT ANALYZER 3000 ===
BEGINNING ANALYSIS... (this may take a while on large files)
Alice: 68.20%, average message is 45.12 characters long
Alice's TOP 3 most used words:
1. really - 142 times
2. coffee - 98 times
3. think - 87 times
Bob: 31.80%, average message is 16.05 characters long
Bob's TOP 3 most used words:
1. lmao - 215 times
2. sure - 180 times
3. beer - 105 times
```

## How to get the Telegram Chat Dump

To use this script, you need to export your chat history in JSON format. **You can only do this via Telegram Desktop.**

1. Open **Telegram Desktop** on your PC/Mac.
2. Open the personal chat you want to analyze.
3. Click on the **three dots** (⋮) in the top right corner.
4. Select **"Export chat history"**.
5. Uncheck photos, videos, and files (functionality with these turned on was not tested)
6. **IMPORTANT:** Change the **Format** from HTML to **JSON**.
7. Click **"Export"**.
8. Locate the `result.json` file in the exported folder.

## Installation & Usage

1. Clone this repository to your local machine:

    ```bash
    git clone https://github.com/Shukolza/tg-chat-analyzer.git
    cd telegram-chat-analyzer
    ```

2. Install the required dependencies (Pydantic for validation and ijson for memory-efficient streaming):

    ```bash
    python3 -m venv .venv
    source .venv/bin/activate  # on Windows use: .venv\Scripts\activate
    pip install -r requirements.txt
    ```

3. Place your exported `result.json` file into the root folder of the project (or change path in config.py if you want for some reason).
4. Run the script:

    ```bash
    python main.py
    ```

## Configuration

All settings are stored in `config.py`. You can easily tweak the script's behavior without modifying the core logic:

- `JSON_PATH`: Path to your chat dump. Defaults to `./result.json`.
- `DEVELOPMENT_MODE`: Set to `True` if you want the script to crash and print a traceback when encountering a validation error (useful for debugging schema changes). Set to `False` to simply skip invalid messages.
- `STOPLIST`: A set of words to ignore during the top-3 calculation (e.g., pronouns, prepositions).
    - _Bilingual support:_ To enable Russian stop-words alongside English ones, uncomment the combination line: `STOPLIST = STOP_WORDS | STOP_WORDS_RU`.
    - _Disable filtering:_ If you want to count every single word, set `STOPLIST = set()`.
- `TEXT_LIKE_ENTITY_TYPES`: A list of Telegram text entities (like bold, spoilers, code blocks) that will be counted towards the message length.
