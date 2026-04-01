import json
import re
import difflib


'''
This package does a search (shopify stores) against all the products in the store
it creates two files, matches.json and filtered.json for the matches and products not found respectively
it is useful for bulk searches without cloudflare blocks
'''


def extract_size(text):
    '''
    uses regex to extract sizes (in ml) from a perfume title
    '''
    match = re.search(r'(\d+)\s*ml', text.lower())
    return match.group(1) if match else None


def normalize_words(text):
    '''
    gets the core words from a perfume title
    '''
    ignore = {"edp", "parfum", "perfume", "extrait", "de", "eau"}
    weak = {"for", "men", "women", "unisex"}

    words = re.sub(r"[^a-z0-9 ]", "", text.lower()).split()

    core = [w for w in words if w not in ignore and w not in weak and not w.isdigit()]
    return core


# compares two strings (quite flexibly)
def strong_match(a, b):
    size_a = extract_size(a)
    size_b = extract_size(b)

    # SIZE CHECK (strict)
    if size_a and size_b and size_a != size_b:
        return False

    words_a = normalize_words(a)
    words_b = normalize_words(b)

    if not words_a or not words_b:
        return False

    set_a = set(words_a)
    set_b = set(words_b)

    common = set_a & set_b

    ratio = len(common) / max(len(set_a), len(set_b))

    # must match enough
    if ratio < 0.6:
        return False

    # detect conflicting unique words
    unique_a = set_a - set_b
    unique_b = set_b - set_a

    # if both sides have strong unique words → reject
    if unique_a and unique_b:
        return False
    return True


matches = []
not_existing_prod = []

with open("all_products.json", "r") as f:
    all_products = json.load(f)

with open("products.json", "r") as f:
    compare = json.load(f)

all_products_flat = [product for page in all_products for product in page]
product_comparer = []

# turning an object with lists into a flat list
for product_list in compare.values():
    for p in product_list:
        product_comparer.append(p)


# Search Starts
for prodct in product_comparer:
    found = False
    for p in all_products_flat:
        if strong_match(prodct, p["title"]):
            print(f'found a match - {prodct} and {p["title"]} ❌ ')
            matches.append(f'{prodct} - {p["title"]}')
            found = True
            break
    if not found:
        not_existing_prod.append(prodct)
    print(f"product - {prodct} added>> ✅ ")

# creates json file for products not found
with open("filtered.json", "w") as f:
    json.dump(not_existing_prod, f, indent=4)

# creates a json file for matches found
with open("matches.json", "w") as f:
    json.dump(matches, f, indent=4)
