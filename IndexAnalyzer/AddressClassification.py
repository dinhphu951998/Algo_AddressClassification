import re
import time
import unicodedata

locality_map = {}
current_id = 0


class TrieNode:
    def __init__(self):
        self.children = {}
        self.isTerminal = False
        self.references = set()


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word, reference_id):
        current = self.root
        for char in word:
            if char not in current.children:
                current.children[char] = TrieNode()
            current = current.children[char]
        current.isTerminal = True
        current.references.add(reference_id)

    def search(self, word):
        current = self.root
        for char in word:
            if char not in current.children:
                return None
            current = current.children[char]
        if current.isTerminal:
            return current.references
        return None


def remove_vietnamese_accents(text):
    text = unicodedata.normalize('NFD', text)
    text = ''.join(ch for ch in text if unicodedata.category(ch) != 'Mn')
    return text


def generate_text_variants(raw_str):
    s = remove_vietnamese_accents(raw_str).lower()

    s = re.sub(r'[^a-z0-9\s]', ' ', s)

    s = re.sub(r'\s+', ' ', s).strip()

    tokens = s.split()
    n = len(tokens)

    if n == 2:
        t1, t2 = tokens
        variants = [
            f"{t1} {t2}",
            f"{t1[0]}{t2[0]}",
            f"{t1[0]}{t2}",
            f"{t1}{t2[0]}",
            f"{t1}{t2}",
        ]

    elif n == 3:
        t1, t2, t3 = tokens
        variants = [
            f"{t1} {t2} {t3}",
            f"{t1}{t2}{t3}",
            f"{t1[0]}{t2[0]}{t3[0]}",
            f"{t1} {t2}{t3}",
            f"{t1}{t2} {t3}",
            f"{t1[0]}{t2}{t3}",
            f"{t1}{t2[0]}{t3}",
            f"{t1}{t2}{t3[0]}",
        ]

    elif n == 4:
        t1, t2, t3, t4 = tokens
        variants = [
            f"{t1} {t2} {t3} {t4}",
            f"{t1}{t2}{t3}{t4}",
            f"{t1[0]}{t2[0]}{t3[0]}{t4[0]}",
            f"{t1} {t2}{t3}{t4}",
            f"{t1}{t2} {t3}{t4}",
            f"{t1}{t2}{t3} {t4}",
            f"{t1[0]}{t2}{t3}{t4}",
            f"{t1}{t2[0]}{t3}{t4}",
        ]
    else:
        variants = [s]

    variants = list(set(variants))

    print(variants)
    return variants


numbers_1_to_30 = {
    1: "mot", 2: "hai", 3: "ba", 4: "bon",
    5: "nam", 6: "sau", 7: "bay", 8: "tam",
    9: "chin", 10: "muoi",
    11: "muoi mot", 12: "muoi hai", 13: "muoi ba", 14: "muoi bon",
    15: "muoi lam", 16: "muoi sau", 17: "muoi bay", 18: "muoi tam",
    19: "muoi chin",
    20: "hai muoi",
    21: "hai muoi mot", 22: "hai muoi hai", 23: "hai muoi ba",
    24: "hai muoi bon", 25: "hai muoi lam", 26: "hai muoi sau",
    27: "hai muoi bay", 28: "hai muoi tam", 29: "hai muoi chin",
    30: "ba muoi"
}


def generate_numeric_variants(num_str, place_type):
    if place_type not in ("district", "ward"):
        return [num_str]

    if place_type == "district":
        prefixShort = "q"
        prefixLong = "quan"
    else:  # ward
        prefixShort = "p"
        prefixLong = "phuong"

    try:
        n = int(num_str)
    except ValueError:
        return [num_str]

    if 1 <= n <= 30:
        digit_word = numbers_1_to_30[n]
        digit_word_no_space = digit_word.replace(" ", "")

        zero_num = ""
        if n < 10:
            zero_num = f"0{num_str}"

        variants = []

        variants.append(f"{prefixShort}{num_str}")
        variants.append(f"{prefixLong}{num_str}")
        variants.append(f"{prefixShort}{digit_word}")
        variants.append(f"{prefixLong}{digit_word}")

        if zero_num:
            variants.append(f"{prefixShort}{zero_num}")
            variants.append(f"{prefixLong}{zero_num}")

        variants.append(num_str)

        if zero_num:
            variants.append(zero_num)

        variants.append(digit_word)

        variants.append(f"{prefixLong} {num_str}")

        if zero_num:
            variants.append(f"{prefixShort} {zero_num}")

        variants.append(f"{prefixShort} {num_str}")

        variants.append(f"{prefixShort}{digit_word_no_space}")
        variants.append(f"{prefixLong}{digit_word_no_space}")

        variants.append(f"{prefixShort} {digit_word_no_space}")
        variants.append(f"{prefixLong} {digit_word_no_space}")

        variants.append(f"{prefixShort} {digit_word}")
        variants.append(f"{prefixLong} {digit_word}")

        variants = list(set(variants))
        return variants
    else:
        return [num_str]


def build_trie(file_path, trie, type):
    global current_id
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            raw = line.strip()
            if raw:
                id = current_id;
                current_id += 1

                locality_map[id] = {
                    "type": type,
                    "name": raw
                }

                if raw.isdigit():
                    numeric_vars = generate_numeric_variants(raw, type)
                    print(numeric_vars)
                    for variant in numeric_vars:
                        trie.insert(variant, id)
                else:
                    text_variants = generate_text_variants(raw)
                    for variant in text_variants:
                        trie.insert(variant, id)
trie_province = Trie()
trie_district = Trie()
trie_ward = Trie()

start = time.time()  # current time in seconds
build_trie("../list_province.txt", trie_province, "province")
build_trie("../list_district.txt", trie_district, "district")
build_trie("../list_ward.txt", trie_ward, "ward")
end = time.time()

elapsed = end - start
print(f"Search took {elapsed:.6f} seconds.")

