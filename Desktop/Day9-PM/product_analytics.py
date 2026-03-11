from collections import namedtuple

Product = namedtuple("Product", ["id", "name", "category", "price"])

# TASK 2 — Product Catalog (15+ products across 4 categories)

# Electronics
p1  = Product(1,  "Laptop",            "Electronics", 75000)
p2  = Product(2,  "Smartphone",        "Electronics", 45000)
p3  = Product(3,  "Wireless Earbuds",  "Electronics",  3500)
p4  = Product(4,  "Smart Watch",       "Electronics", 12000)

# Clothing
p5  = Product(5,  "Running Shoes",     "Clothing",     3000)
p6  = Product(6,  "Denim Jacket",      "Clothing",     2500)
p7  = Product(7,  "Cotton T-Shirt",    "Clothing",      800)
p8  = Product(8,  "Winter Hoodie",     "Clothing",     1800)

# Books
p9  = Product(9,  "Clean Code",        "Books",         700)
p10 = Product(10, "Python Crash Course","Books",        600)
p11 = Product(11, "Atomic Habits",     "Books",         500)
p12 = Product(12, "The Pragmatic Programmer", "Books",  750)

# Home
p13 = Product(13, "Air Purifier",      "Home",        8000)
p14 = Product(14, "Desk Lamp",         "Home",        1200)
p15 = Product(15, "Coffee Maker",      "Home",        3500)
p16 = Product(16, "Wall Clock",        "Home",         900)


catalog = (p1, p2, p3, p4, p5, p6, p7, p8, p9,
           p10, p11, p12, p13, p14, p15, p16)

# TASK 3 — Customer Cart Sets

customer_1_cart = {p1, p2, p9, p13, p5}
customer_2_cart = {p2, p3, p9, p14, p7}
customer_3_cart = {p1, p2, p9, p10, p15}
customer_4_cart = {p2, p6, p9, p11, p13}
customer_5_cart = {p2, p4, p9, p12, p16}

all_carts = [customer_1_cart, customer_2_cart,
             customer_3_cart, customer_4_cart, customer_5_cart]


# TASK 4 — Analyze Shopping Behaviour

# (a) Bestsellers — products appearing in ALL carts (set intersection)
bestsellers = customer_1_cart.intersection(*all_carts[1:])

# (b) Catalog Reach — products appearing in ANY cart (set union)
catalog_reach = customer_1_cart.union(*all_carts[1:])

# (c) Exclusive Purchases — products ONLY customer_1 bought (set difference)
other_carts_union = customer_2_cart | customer_3_cart | customer_4_cart | customer_5_cart
exclusive_customer_1 = customer_1_cart - other_carts_union

# TASK 5 — Product Recommendation Function

def recommend_products(customer_cart, all_carts):
    others_bought = set()
    for cart in all_carts:
        if cart is not customer_cart:          # skip the current customer
            others_bought = others_bought | cart

    # Recommend = what others bought MINUS what this customer already has
    recommendations = others_bought - customer_cart
    return recommendations

# TASK 6 — Category Summary Function

def category_summary():
    
    categories = {product.category for product in catalog}  
    summary = {
        cat: {product.name for product in catalog if product.category == cat}
        for cat in categories
    }
    return summary

if __name__ == "__main__":

    print("=" * 60)
    print("        E-COMMERCE PRODUCT ANALYTICS TOOL")
    print("=" * 60)

    # Catalog
    print("\n📦 PRODUCT CATALOG")
    print("-" * 60)
    for p in catalog:
        print(f"  [{p.id:>2}] {p.name:<30} | {p.category:<12} | ₹{p.price:,}")

    # Customer Carts
    print("\n🛒 CUSTOMER CARTS")
    print("-" * 60)
    for i, cart in enumerate(all_carts, 1):
        names = ", ".join(p.name for p in cart)
        print(f"  Customer {i}: {names}")

    #Task 4a: Bestsellers
    print("\n🏆 BESTSELLERS (in ALL carts — intersection)")
    print("-" * 60)
    for p in bestsellers:
        print(f"  • {p.name} (₹{p.price:,})")

    #Task 4b: Catalog Reach 
    print("\n🌍 CATALOG REACH (in ANY cart — union)")
    print("-" * 60)
    for p in sorted(catalog_reach, key=lambda x: x.id):
        print(f"  • {p.name}")

    #Task 4c: Exclusive Purchases
    print("\n🔒 EXCLUSIVE PURCHASES by Customer 1 (difference)")
    print("-" * 60)
    if exclusive_customer_1:
        for p in exclusive_customer_1:
            print(f"  • {p.name}")
    else:
        print("  None — all products were also bought by someone else.")

    #Task 5: Recommendations
    print("\n💡 PRODUCT RECOMMENDATIONS for Customer 1")
    print("-" * 60)
    recs = recommend_products(customer_1_cart, all_carts)
    for p in sorted(recs, key=lambda x: x.id):
        print(f"  • {p.name} ({p.category}, ₹{p.price:,})")

    #Task 6: Category Summary
    print("\n📊 CATEGORY SUMMARY")
    print("-" * 60)
    summary = category_summary()
    for cat, names in sorted(summary.items()):
        print(f"  {cat}:")
        for name in sorted(names):
            print(f"    - {name}")

    print("\n" + "=" * 60)
