# Interview Answers — Day 9 PM | Tuples & Sets

---

## Q1 — Conceptual: Tuple with Mutable Elements

### The Code

```python
t = ([1, 2], [3, 4])
t[0][0] = 99
print(t)   # ([99, 2], [3, 4])
```

### Does it work?

**Yes, it works without error.**

### Why?

Tuple immutability means the **references** stored inside the tuple cannot be
changed. The tuple `t` holds two references — one pointing to list `[1, 2]` and
another pointing to list `[3, 4]`. Those references are fixed and cannot be
reassigned.

However, `t[0]` gives you the *list object itself*. Lists are mutable, so you
can freely modify the contents of that list (`t[0][0] = 99`).

Think of it like this:

```
Tuple  →  [ref_A,  ref_B]   ← these references are frozen
              ↓        ↓
           [1, 2]   [3, 4]  ← the list contents are mutable
```

You **cannot** do `t[0] = [99, 2]` — that would try to replace the reference
inside the tuple, which raises `TypeError`.

### What this reveals about tuple immutability

> Tuple immutability is **shallow**, not deep.

The tuple guarantees that its *own* slots will always point to the same objects.
It does NOT guarantee that those objects themselves are unchanged. If a tuple
contains mutable objects (lists, dicts), those objects can still be mutated.

### Practical takeaway

If you want a truly immutable data structure, either:
- Use only immutable types inside tuples (int, str, other tuples), or
- Use a `namedtuple` with immutable field values.

---

## Q2 — Coding: `find_duplicates(lst)` using set operations, O(n)

### Approach

Use two sets:
- `seen` — elements encountered so far
- `duplicates` — elements seen more than once

This is a single pass → **O(n) time, O(n) space**.

```python
def find_duplicates(lst):
    
    seen       = set()
    duplicates = set()

    for item in lst:
        if item in seen:          # O(1) lookup — this is why sets are used
            duplicates.add(item)
        else:
            seen.add(item)

    return duplicates


# ── Tests ──────────────────────────────────────────────────────────────────
print(find_duplicates([1, 2, 3, 2, 4, 3, 5]))   # {2, 3}
print(find_duplicates(['a', 'b', 'a', 'c']))      # {'a'}
print(find_duplicates([1, 2, 3]))                  # set()  (no duplicates)
print(find_duplicates([]))                          # set()  (empty)
```

### Why O(n)?

- We iterate through the list exactly **once** → O(n) iterations.
- `item in seen` and `seen.add(item)` are both **O(1)** for sets (hash table).
- No nested loops, no sorting.

---

## Q3 — Debug Problem

### The Buggy Code

```python
def unique_to_each(a, b):
    result = set(a) - set(b)
    return list(result)

unique_to_each([1, 2, 3], [3, 4, 5])
# Returns: [1, 2]   ← WRONG
# Expected: [1, 2, 4, 5]
```

### Why it's wrong

`set(a) - set(b)` computes the **one-sided difference** — elements in `a` that
are NOT in `b`. This gives `{1, 2}`.

It completely ignores elements in `b` that are NOT in `a` (which is `{4, 5}`).

### The Fix — Symmetric Difference

The correct operation is the **symmetric difference** (`^` or
`.symmetric_difference()`), which returns elements that belong to exactly one
of the two sets (but not both).

```
set(a) = {1, 2, 3}
set(b) = {3, 4, 5}

symmetric difference = elements in one set but not the other
                     = {1, 2} ∪ {4, 5}
                     = {1, 2, 4, 5}  ✅
```

### Fixed Function

```python
def unique_to_each(a, b):
    result = set(a).symmetric_difference(set(b))
    return list(result)


#Test
print(unique_to_each([1, 2, 3], [3, 4, 5]))   # [1, 2, 4, 5] 
print(unique_to_each([1, 2],    [1, 2]))        # []         (identical)
print(unique_to_each([],        [1, 2]))        # [1, 2]    (one empty)
```

### Quick Reference — Set Difference Operations

| Operation              | Symbol | Meaning                                          |
|------------------------|--------|--------------------------------------------------|
| `a - b`                | `-`    | Elements in a but NOT in b (one-sided)           |
| `b - a`                | `-`    | Elements in b but NOT in a (one-sided)           |
| `a.symmetric_difference(b)` | `^` | Elements in EITHER a or b, but NOT BOTH ✅    |


