import csv
import json
import re

INPUT_CSV = "tanach_hebrew.csv"
OUTPUT_JSON = "tanach_word_index.json"

GEMATRIA_MAP = {
    "א": 1,  "ב": 2,  "ג": 3,  "ד": 4,  "ה": 5,
    "ו": 6,  "ז": 7,  "ח": 8,  "ט": 9,
    "י": 10, "כ": 20, "ל": 30, "מ": 40, "נ": 50,
    "ס": 60, "ע": 70, "פ": 80, "צ": 90,
    "ק": 100, "ר": 200, "ש": 300, "ת": 400
}

FINAL_LETTERS = {
    "ך": "כ",
    "ם": "מ",
    "ן": "נ",
    "ף": "פ",
    "ץ": "צ"
}


def normalize_hebrew(text: str) -> str:
    text = re.sub(r"[\u0591-\u05C7]", "", text)
    for final, regular in FINAL_LETTERS.items():
        text = text.replace(final, regular)
    text = re.sub(r"[^\u05D0-\u05EA\s]", "", text)
    return re.sub(r"\s+", " ", text).strip()


def gematria(word: str) -> int:
    return sum(GEMATRIA_MAP.get(letter, 0) for letter in word)


word_index = {}
order_counter = 0

with open(INPUT_CSV, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)

    for row in reader:
        order_counter += 1

        book = row["book"]
        chapter = int(row["chapter"])
        verse = int(row["verse"])
        hebrew_text = row["hebrew"]

        reference = f"{book} {chapter}:{verse}"
        normalized_text = normalize_hebrew(hebrew_text)
        words = normalized_text.split(" ")

        for word in words:
            if not word:
                continue

            entry = word_index.setdefault(word, {
                "gematria": gematria(word),
                "count": 0,
                "first_occurrence": None,
                "occurrences": []
            })

            occurrence = {
                "reference": reference,
                "order_index": order_counter
            }

            entry["occurrences"].append(occurrence)
            entry["count"] += 1

            if entry["first_occurrence"] is None:
                entry["first_occurrence"] = occurrence

with open(OUTPUT_JSON, "w", encoding="utf-8") as out:
    json.dump(word_index, out, ensure_ascii=False, indent=2)

print(f"Word index created: {OUTPUT_JSON}")
print(f"Unique words indexed: {len(word_index)}")
