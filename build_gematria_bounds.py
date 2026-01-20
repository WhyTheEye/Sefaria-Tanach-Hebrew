import json

WORD_INDEX_FILE = "tanach_word_index.json"
VERSE_INDEX_FILE = "tanach_verse_index.json"
OUTPUT_FILE = "tanach_gematria_bounds.json"


def build_word_bounds(word_index):
    items = [
        (entry["gematria"], word)
        for word, entry in word_index.items()
    ]

    items.sort(key=lambda x: x[0])

    min_val = items[0][0]
    max_val = items[-1][0]

    lowest = [word for val, word in items if val == min_val][:5]
    highest = [word for val, word in reversed(items) if val == max_val][:5]

    return {
        "min": min_val,
        "max": max_val,
        "lowest_examples": lowest,
        "highest_examples": highest
    }


def build_verse_bounds(verse_index):
    items = [
        (entry["gematria"], entry["first_occurrence"]["reference"])
        for entry in verse_index.values()
    ]

    items.sort(key=lambda x: x[0])

    min_val = items[0][0]
    max_val = items[-1][0]

    lowest = [ref for val, ref in items if val == min_val][:5]
    highest = [ref for val, ref in reversed(items) if val == max_val][:5]

    return {
        "min": min_val,
        "max": max_val,
        "lowest_examples": lowest,
        "highest_examples": highest
    }


def main():
    with open(WORD_INDEX_FILE, encoding="utf-8") as f:
        word_index = json.load(f)

    with open(VERSE_INDEX_FILE, encoding="utf-8") as f:
        verse_index = json.load(f)

    bounds = {
        "word": build_word_bounds(word_index),
        "verse": build_verse_bounds(verse_index)
    }

    with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
        json.dump(bounds, out, ensure_ascii=False, indent=2)

    print(f"Gematria bounds written to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
