import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class GematriaSearchEngine:
    def __init__(self, word_index_path, verse_index_path, stats_path):
        self.word_index = self._load_json(os.path.join(BASE_DIR, word_index_path))
        self.verse_index = self._load_json(os.path.join(BASE_DIR, verse_index_path))
        self.stats = self._load_json(os.path.join(BASE_DIR, stats_path))

    def _load_json(self, path):
        with open(path, encoding="utf-8") as f:
            return json.load(f)

    # -----------------------------
    # Normalizers (ENGINE CONTRACT)
    # -----------------------------

    def _normalize_word_hit(self, word, entry, source):
        return {
            "type": "word",
            "text": word,
            "gematria": entry["gematria"],
            "source": {
                "section": source["section"],
                "book": source["book"],
                "chapter": source["chapter"],
                "verse": source["verse"],
                "verse_index": source["verse_index"]
            }
        }

    def _normalize_verse_hit(self, entry):
        return {
            "type": "verse",
            "text": entry.get("text", ""),
            "gematria": entry["gematria"],
            "source": {
                "section": entry["section"],
                "book": entry["book"],
                "chapter": entry["chapter"],
                "verse": entry["verse"],
                "verse_index": entry["verse_index"]
            }
        }

    # -----------------------------
    # Search
    # -----------------------------

    def search(self, value: int):
        results = []

        # ---------- WORD SEARCH ----------
        w_min = self.stats["words"]["range"]["lowest"]
        w_max = self.stats["words"]["range"]["highest"]

        if w_min <= value <= w_max:
            for word, data in self.word_index.items():
                if data["gematria"] != value:
                    continue

                for source in data["sources"]:
                    results.append(
                        self._normalize_word_hit(word, data, source)
                    )

        # ---------- VERSE SEARCH ----------
        v_min = self.stats["verses"]["range"]["lowest"]
        v_max = self.stats["verses"]["range"]["highest"]

        if v_min <= value <= v_max:
            for entry in self.verse_index:
                if entry["gematria"] == value:
                    results.append(
                        self._normalize_verse_hit(entry)
                    )

        return {
            "query": value,
            "total_results": len(results),
            "results": results
        }
