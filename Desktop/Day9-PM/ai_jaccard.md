# AI-Augmented Task — Jaccard Similarity
## Day 9 PM | Part D

---

## Step 1 — Exact Prompt Used

> "Write a Python function that calculates the Jaccard similarity between two
> sets of strings. Explain what Jaccard similarity is and where it is used in
> industry."

---

## Step 2 — AI Output (pasted verbatim)

### What is Jaccard Similarity?

Jaccard similarity is a metric that measures how similar two sets are by
comparing the size of their **intersection** (elements in common) to the size
of their **union** (all unique elements across both sets).

**Formula:**

```
Jaccard(A, B) = |A ∩ B| / |A ∪ B|
```

- Returns **1.0** when the sets are identical.
- Returns **0.0** when the sets share no elements at all.
- Always a value between 0.0 and 1.0.

### Python Function

```python
def jaccard_similarity(set_a, set_b):
    """
    Calculate the Jaccard similarity between two sets of strings.

    Formula: |A ∩ B| / |A ∪ B|

    Returns:
        float between 0.0 (no overlap) and 1.0 (identical sets)
        Returns 0.0 if both sets are empty (avoids ZeroDivisionError)
    """
    if not set_a and not set_b:       # both empty → define similarity as 0
        return 0.0

    intersection = set_a & set_b      # elements in BOTH sets
    union        = set_a | set_b      # elements in EITHER set

    return len(intersection) / len(union)
```

---

## Step 3 — Testing the Function

```python
def jaccard_similarity(set_a, set_b):
    if not set_a and not set_b:
        return 0.0
    intersection = set_a & set_b
    union        = set_a | set_b
    return len(intersection) / len(union)


# ── Provided test ──────────────────────────────────────────────────────────
set_a = {'python', 'java', 'sql'}
set_b = {'python', 'sql', 'docker', 'aws'}

score = jaccard_similarity(set_a, set_b)
print(f"Jaccard similarity: {score:.4f}")

# Manual verification:
#   intersection = {'python', 'sql'}           → size 2
#   union        = {'python','java','sql','docker','aws'} → size 5
#   score        = 2/5 = 0.4000  ✅


# ── Edge case tests ────────────────────────────────────────────────────────
print(jaccard_similarity(set(),  set()))           # 0.0  (both empty)
print(jaccard_similarity({'a'},  set()))           # 0.0  (one empty)
print(jaccard_similarity({'a','b'}, {'a','b'}))   # 1.0  (identical)
print(jaccard_similarity({'a'},  {'b'}))           # 0.0  (no overlap)
```

**Output:**
```
Jaccard similarity: 0.4000
0.0
0.0
1.0
0.0
```

---

## Step 4 — Evaluation of the AI Output

### Is the formula correct?

**Yes.** The formula `|A ∩ B| / |A ∪ B|` is the standard Jaccard index. The
implementation using Python's `&` and `|` set operators is idiomatic and
correct.

### Does it handle edge cases?

| Edge Case                     | Handled? | Notes                                      |
|-------------------------------|----------|--------------------------------------------|
| Both sets empty               | ✅ Yes   | Returns 0.0 explicitly, avoids `ZeroDivisionError` |
| One set empty, other non-empty| ✅ Yes   | Union = non-empty set, intersection = ∅ → 0.0 |
| Identical sets                | ✅ Yes   | intersection == union → 1.0                |
| No overlap at all             | ✅ Yes   | intersection = ∅ → 0.0                    |
| Single element sets           | ✅ Yes   | Works naturally                            |

The only edge case NOT handled is non-set inputs (e.g., lists). Adding a type
check or converting inputs with `set()` would make it more robust:

```python
set_a, set_b = set(set_a), set(set_b)   # defensive conversion
```

---

## Step 5 — Where Jaccard Similarity Is Used in Industry

**Recommendation Systems:** Streaming platforms like Netflix and Spotify use
Jaccard similarity to compare users' listening or viewing histories. If two
users have listened to many of the same songs (high Jaccard score), songs one
user likes are likely to appeal to the other — driving the "Users like you also
enjoyed…" feature.

**Natural Language Processing (NLP):** In text analysis, documents are
converted to sets of words or n-grams and compared with Jaccard similarity to
detect near-duplicate content, measure document similarity, or cluster articles
by topic. This is simpler and faster than cosine similarity for large corpora
with sparse feature sets.

**Plagiarism Detection:** Tools like Turnitin and academic integrity software
use Jaccard-based methods (often combined with shingling — breaking text into
overlapping word sequences) to measure how much two documents share. A
Jaccard score above a threshold flags potential plagiarism for human review.

**E-commerce & Search:** Retailers compare product tags, customer purchase
histories, and search query sets using Jaccard similarity to power "frequently
bought together" suggestions and to de-duplicate near-identical product
listings in large catalogs.
