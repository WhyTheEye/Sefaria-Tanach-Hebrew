# SCHEMA.md

This document defines the **frozen data schemas** for the Tanach Gematria Reference App.

These schemas are **authoritative**. Any code, search logic, or UI must conform to them exactly.

---

## Global Rules (Apply Everywhere)

### Reference Format (Non‑Negotiable)

All references MUST be stored and displayed as:

```
Book Chapter:Verse
```

Examples:
- Genesis 1:1
- Deuteronomy 6:4
- Psalms 23:1

No abbreviations, IDs, or alternate formats are permitted.

---

### Tanach Order Index

A single integer representing canonical Tanach order.

Ordering precedence:
1. Book order (as defined in PROJECT_SPEC.md)
2. Chapter number
3. Verse number

This value is used **only for sorting**, never display.

---

## 1. Word Index Schema

**File:** `tanach_word_index.json`

### Purpose
Provides fast lookup of Hebrew words by gematria value, including occurrence counts and verse references.

### Key
- Normalized Hebrew word (final letters normalized, no punctuation)

### Value Object

```json
{
  "gematria": 541,
  "count": 3,
  "first_occurrence": {
    "reference": "Genesis 32:29",
    "order_index": 12345
  },
  "occurrences": [
    {
      "reference": "Genesis 32:29",
      "order_index": 12345
    },
    {
      "reference": "Exodus 6:2",
      "order_index": 23456
    }
  ]
}
```

### Field Definitions

| Field | Type | Description |
|-----|-----|------------|
| gematria | integer | Standard gematria value (Mispar Hechrechi) |
| count | integer | Total number of occurrences |
| first_occurrence | object | First appearance in Tanach order |
| occurrences | array | All verse occurrences |

`count` MUST equal `len(occurrences)`.

---

## 2. Verse Index Schema

**File:** `tanach_verse_index.json`

### Purpose
Provides gematria lookup for verses, including detection of duplicate verse texts.

### Key
- Normalized Hebrew verse text (exact string match)

### Value Object

```json
{
  "gematria": 913,
  "count": 2,
  "first_occurrence": {
    "reference": "Genesis 1:1",
    "order_index": 1
  },
  "occurrences": [
    {
      "reference": "Genesis 1:1",
      "order_index": 1
    },
    {
      "reference": "Psalms 33:6",
      "order_index": 15432
    }
  ],
  "verse_text": "בראשית ברא אלהים את השמים ואת הארץ"
}
```

### Field Definitions

| Field | Type | Description |
|-----|-----|------------|
| gematria | integer | Gematria of full verse |
| count | integer | Number of identical verse occurrences |
| first_occurrence | object | First appearance in Tanach order |
| occurrences | array | All identical verse locations |
| verse_text | string | Hebrew verse text for display |

---

## 3. Gematria Bounds Metadata

**File:** `tanach_gematria_bounds.json`

### Purpose
Stores global min/max values and examples for UI guidance and validation.

### Schema

```json
{
  "word": {
    "min": 1,
    "max": 2147,
    "lowest_examples": ["א"],
    "highest_examples": ["..."]
  },
  "verse": {
    "min": 14,
    "max": 42317,
    "lowest_examples": ["Genesis 1:2"],
    "highest_examples": ["..."]
  }
}
```

---

## 4. Input Normalization Rules

Applied consistently to:
- Indexing
- Runtime search

Rules:
- Remove punctuation
- Normalize final letters
- Collapse whitespace
- Hebrew letters only for computation

Display text is **never normalized**.

---

## 5. Determinism Contract

Given the same:
- Input text
- Schema version
- Gematria system

The output MUST always be identical.

No schema field may be overloaded or repurposed.

---

## 6. Versioning Rule

If any schema field changes:
- A new schema version MUST be created
- Existing data files MUST NOT be silently modified

---

## 7. Implementation Warnings

- Do NOT infer order from strings
- Do NOT compute gematria at runtime
- Do NOT store display-only data in indexes
- Do NOT mix schemas between phases

---

## 8. Schema Lock

This schema is frozen for MVP development.

Changes require:
- Explicit justification
- Version increment
- Regeneration of affected indexes

