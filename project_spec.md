# PROJECT_SPEC.md

## Project Name
Tanach Gematria Reference App

---

## 1. Purpose (What This App Is)

A browser-based reference app that allows users to:
- Enter a **Hebrew word** or a **number**
- View **gematria-based matches** across the Hebrew Tanach
- See results **ordered by Tanach sequence**
- Expand results to view **full Hebrew verses**

The app functions primarily as a **Gematria lookup and reference guide**, with the potential to later expand into a broader Tanach text browser.

---

## 2. Non-Goals (What This App Is NOT)

This app explicitly does NOT:
- Generate interpretations, commentary, or explanations
- Use LLMs or AI reasoning for search results
- Perform live web searches
- Modify or paraphrase Tanach text
- Support translations (Hebrew only)
- Support user-generated content

All results are **deterministic and data-driven**.

---

## 3. Core User Flow

1. User lands on a simple page:
   - Title
   - One-line description
   - Single search bar

2. User enters:
   - A Hebrew word **or**
   - A number

3. App:
   - Normalizes input
   - Converts Hebrew → number if needed
   - Searches precomputed indexes

4. Results are displayed:
   - Ordered by Tanach sequence
   - Each result explicitly labeled as **Book Chapter:Verse**

---

## 4. Result Display Rules

### 4.1 Word Results

For each matching word:
- Display the word in Hebrew
- Display total occurrence count
- Show **first occurrence** reference formatted as **Book Chapter:Verse**
- Include dropdown arrow

Dropdown reveals:
- Full Hebrew verse of first occurrence
- Link to a page listing **all occurrences**
  - Target word bolded
  - Each occurrence labeled **Book Chapter:Verse**

### 4.2 Verse Results (Phase 2)

For each matching verse:
- Display **Book Chapter:Verse**
- Display the **full Hebrew verse inline whenever space allows**
- Include dropdown arrow

Dropdown reveals (when needed):
- Full Hebrew verse text
- If the verse text occurs **multiple times identically** in Tanach:
  - Display total duplicate count
  - Provide link to a page listing **all duplicate verse occurrences**
    - Each labeled **Book Chapter:Verse**

This requires the verse index to record:
- The verse text
- All references where that exact verse text occurs

---

## 5. Data Sources

- Hebrew Tanach text sourced from **Sefaria public domain dump**
- Hebrew text only
- No niqqud
- No cantillation
- No translations

---

## 6. Gematria Rules (Phase 1 — Locked)

### Supported System
- **Standard Gematria (Mispar Hechrechi)** only

### Letter Mapping

א=1  ב=2  ג=3  ד=4  ה=5  ו=6  ז=7  ח=8  ט=9
י=10 כ=20 ל=30 מ=40 נ=50 ס=60 ע=70 פ=80 צ=90
ק=100 ר=200 ש=300 ת=400

### Final Letters
Final letters are normalized **for computation only**:
- ך → כ
- ם → מ
- ן → נ
- ף → פ
- ץ → צ

Original verse text is **never modified for display**.

---

## 7. Data Architecture (High Level)

### Preprocessing (One-Time)

1. Extract Hebrew verses
2. Normalize text for computation
3. Generate:
   - Word-level gematria index
   - Verse-level gematria index

### Runtime

- No gematria computation at runtime
- Only lookups, filtering, grouping, and display

---

## 8. Core Data Artifacts

### Reference Format (Global Rule)

All references in **all data artifacts** must be stored and displayed in the explicit format:

```
Book Chapter:Verse
```

Examples:
- Genesis 1:1
- Deuteronomy 6:4
- Psalms 23:1

No alternative formats (IDs, abbreviations, numeric-only) are permitted for user-facing or internal references.

---

### Word Index (JSON)
- One entry per unique normalized Hebrew word
- Stores:
  - gematria value
  - total occurrence count
  - first occurrence reference (**Book Chapter:Verse**)
  - list of all occurrences (each as **Book Chapter:Verse**)

### Verse Index (JSON)
- One entry per **unique Hebrew verse text**
- Stores:
  - verse text (Hebrew)
  - gematria value
  - total occurrence count (for duplicate verses)
  - list of all occurrences, each stored as **Book Chapter:Verse**
  - Tanach order index for the first occurrence

This mirrors the Word Index structure intentionally, enabling:
- Duplicate verse detection
- Linked views of identical verses
- Consistent UI behavior between word and verse results

### Metadata

- Global bounds (min/max values)
- Stored separately

---

## 9. Ordering Rules

All results are ordered strictly by **canonical Tanach sequence**.

### Explicit Book Order

**Torah**
1. Genesis
2. Exodus
3. Leviticus
4. Numbers
5. Deuteronomy

**Prophets**
6. Joshua
7. Judges
8. I Samuel
9. II Samuel
10. I Kings
11. II Kings
12. Isaiah
13. Jeremiah
14. Ezekiel
15. Hosea
16. Joel
17. Amos
18. Obadiah
19. Jonah
20. Micah
21. Nahum
22. Habakkuk
23. Zephaniah
24. Haggai
25. Zechariah
26. Malachi


**Writings**
27. Psalms
28. Proverbs
29. Job
30. Song of Songs
31. Ruth
32. Lamentations
33. Ecclesiastes
34. Esther
35. Daniel
36. Ezra
37. Nehemiah
38. I Chronicles
39. II Chronicles

Book order, chapter order, and verse order are fixed and must never be inferred implicitly.

---

## 10. Extensibility (Later Phases)

Planned but NOT implemented initially:
- Additional gematria systems
- Combined word + verse queries
- Advanced filtering
- Cross-references
- App Store deployment

All extensions must:
- Preserve existing schemas
- Be additive, not destructive

---

## 11. Determinism Guarantee

Given the same input:
- The app must always return the same output
- No randomness
- No AI inference
- No hidden state

---

## 12. Development Discipline Rules

- Schemas are frozen once validated
- Changes require versioning
- Logic precedes UI
- Preprocessing precedes runtime logic
- External documentation is the source of truth, not chat history

---

## 13. Success Criteria (MVP)

The MVP is complete when:
- A user can enter a Hebrew word or number
- Matching words and verses are returned
- Results are ordered correctly
- Verses display with correct Hebrew spelling
- No runtime gematria computation occurs

---

## 14. Explicit Constraint

This project prioritizes:
- Correctness over speed
- Determinism over flexibility
- Simplicity over cleverness

No feature may violate these principles.

