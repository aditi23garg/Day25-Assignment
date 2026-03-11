
"""
TASK 1 — RESEARCH: frozenset

WHAT IS frozenset?
──────────────────
A frozenset is an IMMUTABLE version of a Python set.
Once created, you cannot add or remove elements from it.

  fs = frozenset({'Electronics', 'Books'})
  fs.add('Clothing')    # AttributeError — frozenset has no .add()

SET vs FROZENSET
────────────────
  Feature              set           frozenset
  ─────────────────────────────────────────────────
  Mutable              Yes           No
  Hashable             No            Yes
  Can be dict key      No            Yes
  Can be set element   No            Yes
  Supports |, &, -     Yes           Yes

KEY DIFFERENCE — hashability:
  • A regular set is mutable → not hashable → CANNOT be used as a dict key
  • A frozenset is immutable → hashable → CAN be used as a dict key

WHEN TO USE frozenset IN REAL SYSTEMS
──────────────────────────────────────
1. DICT KEYS   → When you need a set as a dictionary key
                 (e.g., bundle pricing: {frozenset({'A','B'}): 10%})

2. SET OF SETS → When you need a set whose elements are themselves sets
                 (e.g., storing unique permission groups)

3. SAFE CONFIG → When you want to pass a set to a function and guarantee
                 it won't be modified inside (defensive programming)

4. CACHING     → frozensets can be hashed, so they work as keys in
                 @functools.lru_cache and other memoisation patterns
"""

import timeit
from collections import namedtuple

# Reuse the Product namedtuple from Part A
Product = namedtuple("Product", ["id", "name", "category", "price"])

# Sample products for demonstration
p1  = Product(1,  "Laptop",             "Electronics", 75000)
p2  = Product(2,  "Smartphone",         "Electronics", 45000)
p9  = Product(9,  "Clean Code",         "Books",         700)
p10 = Product(10, "Python Crash Course","Books",         600)
p5  = Product(5,  "Running Shoes",      "Clothing",     3000)
p13 = Product(13, "Air Purifier",       "Home",         8000)
p14 = Product(14, "Desk Lamp",          "Home",         1200)


# TASK 2 — Bundle Discount Dictionary

bundle_discounts = {
    frozenset({'Electronics', 'Books'}):           10,   # 10% off
    frozenset({'Electronics', 'Clothing'}):         8,   #  8% off
    frozenset({'Books', 'Home'}):                   7,   #  7% off
    frozenset({'Electronics', 'Home'}):            12,   # 12% off
    frozenset({'Electronics', 'Books', 'Home'}):   15,   # 15% off (triple bundle)
    frozenset({'Clothing', 'Home'}):                5,   #  5% off
}

# TASK 3 — Bundle Checker Function

def check_bundle_discount(cart):
    # Step 1 — collect categories in this cart
    cart_categories = {product.category for product in cart}

    best_discount = 0
    best_bundle   = None

    # Step 2 — check each bundle
    for bundle, discount in bundle_discounts.items():
        if bundle.issubset(cart_categories):
            if discount > best_discount:
                best_discount = discount
                best_bundle   = bundle

    return best_discount, best_bundle

# TASK 4 — Performance Benchmark: set vs frozenset creation
"""
BENCHMARK METHODOLOGY
─────────────────────
We use timeit.timeit() with number=100_000 to measure total seconds for
100,000 creations of each type, then convert to microseconds per operation.

Expected finding:
  • frozenset creation is slightly slower than set because Python needs to
    make the object immutable and compute its hash.
  • The difference is tiny (microseconds) and negligible in most real code.
  • For lookup / membership testing, both are O(1) — identical speed.
"""

ITERATIONS = 100_000

set_time       = timeit.timeit("set(['Electronics','Books','Clothing','Home'])",
                               number=ITERATIONS)
frozenset_time = timeit.timeit("frozenset(['Electronics','Books','Clothing','Home'])",
                               number=ITERATIONS)

set_us       = (set_time       / ITERATIONS) * 1_000_000   # convert to µs
frozenset_us = (frozenset_time / ITERATIONS) * 1_000_000

"""
TYPICAL RESULTS (on an average machine):
  set creation       ≈ 0.15 – 0.25 µs per call
  frozenset creation ≈ 0.17 – 0.28 µs per call

frozenset is marginally slower to create (~5–15% overhead) because Python
hashes it immediately. However the cost is negligible.
Use frozenset for correctness (dict keys, set elements) not for speed.
"""

if __name__ == "__main__":

    print("=" * 60)
    print("         FROZENSET BUNDLE DISCOUNT SYSTEM")
    print("=" * 60)

    #Show all bundles
    print("\n🎁 AVAILABLE BUNDLE DEALS")
    print("-" * 60)
    for bundle, disc in bundle_discounts.items():
        cats = " + ".join(sorted(bundle))
        print(f"  {cats:<40} → {disc}% off")

    #Test carts
    test_carts = {
        "Cart A (Laptop + Clean Code)":
            {p1, p9},
        "Cart B (Laptop + Shoes + Book)":
            {p1, p5, p9},
        "Cart C (Laptop + Book + Lamp)":
            {p1, p9, p14},
        "Cart D (Shoes + Clock only)":
            {p5},
        "Cart E (Laptop + Book + Lamp + Shoes)":
            {p1, p9, p13, p5},
    }

    print("\n🛒 BUNDLE DISCOUNT CHECK")
    print("-" * 60)
    for label, cart in test_carts.items():
        discount, bundle = check_bundle_discount(cart)
        if discount:
            cats = " + ".join(sorted(bundle))
            print(f"  {label}")
            print(f"    Bundle match: [{cats}] → {discount}% discount\n")
        else:
            print(f"  {label}")
            print(f"    No bundle discount applicable\n")

    #Benchmark results
    print("\n⏱  PERFORMANCE BENCHMARK (100,000 iterations)")
    print("-" * 60)
    print(f"  set       creation: {set_time:.4f}s total  |  {set_us:.4f} µs per call")
    print(f"  frozenset creation: {frozenset_time:.4f}s total  |  {frozenset_us:.4f} µs per call")
    overhead = ((frozenset_us - set_us) / set_us) * 100
    print(f"  frozenset overhead: ~{overhead:.1f}%")
    print("\n  ℹ  Both have O(1) membership lookup — use frozenset for")
    print("     correctness (hashability), not for speed gains.")

    print("\n" + "=" * 60)
