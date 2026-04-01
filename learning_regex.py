import re


str_ = "Order 1234 costs 20000 naira and size is 50ml"
txt = "Afnan Modest Deux EDP for Men 100ml"

def normalize_words(text):
    ignore = {"edp", "parfum", "perfume", "extrait", "de", "eau"}
    weak = {"for", "men", "women", "unisex"}

    words = re.sub(r"[^a-z0-9]", "", text.lower()).split()

    # core = [w for w in words if w not in ignore and w not in weak and not w.isdigit()]
    return words


def learning_regex(text):
    all_numbers = re.findall(r"\d+", text.lower())
    size_num = re.search(r"\d+\s*ml", text.lower())
    all_words = re.sub(r"[^a-z\s*]", "", text.lower()).split()
    print(all_numbers, all_words, size_num.group())


print(learning_regex(str_))
