import time
import os
from Utils.Utils import *
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

    def insert_reversed(self, word, reference_id):
        current = self.root
        for char in reversed(word):
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

    def collect_candidates(self, reversed_search_key):
        node = self.root
        for char in reversed_search_key:
            if char not in node.children:
                return []  # No candidate matches this reversed prefix.
            node = node.children[char]

        candidates = []

        def dfs(current_node, path):
            # 'path' holds the accumulated reversed characters from the starting point.
            if current_node.isTerminal:
                # Do not reverse the path; keep the candidate in its reversed form.
                candidate = path
                candidates.append((candidate, current_node.references.copy()))
            for letter, child in current_node.children.items():
                dfs(child, path + letter)

        # Start DFS from the node corresponding to the reversed search key.
        dfs(node, reversed_search_key)
        return candidates


def generate_text_variants(raw_str):
    s = normalize_text(raw_str)
    tokens = s.split()
    n = len(tokens)

    if n == 2:
        t1, t2 = tokens
        variants = [
            # f"{t1} {t2}",
            # f"{t1[0]}{t2[0]}",
            f"{t1[0]}{t2}",
            # f"{t1}{t2[0]}",
            f"{t1}{t2}",
        ]

    elif n == 3:
        t1, t2, t3 = tokens
        variants = [
            # f"{t1} {t2} {t3}",
            f"{t1}{t2}{t3}",
            # f"{t1[0]}{t2[0]}{t3[0]}",
            # f"{t1} {t2}{t3}",
            # f"{t1}{t2} {t3}",
            # f"{t1[0]}{t2}{t3}",
            # f"{t1}{t2[0]}{t3}",
            # f"{t1}{t2}{t3[0]}",
        ]

    elif n == 4:
        t1, t2, t3, t4 = tokens
        variants = [
            # f"{t1} {t2} {t3} {t4}",
            f"{t1}{t2}{t3}{t4}",
            # f"{t1[0]}{t2[0]}{t3[0]}{t4[0]}",
            # f"{t1} {t2}{t3}{t4}",
            # f"{t1}{t2} {t3}{t4}",
            # f"{t1}{t2}{t3} {t4}",
            # f"{t1[0]}{t2}{t3}{t4}",
            # f"{t1}{t2[0]}{t3}{t4}",
        ]
    else:
        variants = [s]

    variants = list(set(variants))
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
    seen = set()
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            raw = line.strip()
            if raw and raw not in seen:
                seen.add(raw)
                id = current_id;
                current_id += 1

                locality_map[id] = {
                    "type": type,
                    "name": raw
                }

                if raw.isdigit():
                    numeric_vars = generate_numeric_variants(raw, type)
                    for variant in numeric_vars:
                        trie.insert(variant, id)
                else:
                    text_variants = generate_text_variants(raw)
                    for variant in text_variants:
                        trie.insert(variant, id)

def build_reversed_trie(file_path, trie, type):
    global current_id
    seen = set()
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            raw = line.strip()
            if raw and raw not in seen:
                seen.add(raw)
                id = current_id;
                current_id += 1

                locality_map[id] = {
                    "type": type,
                    "name": raw
                }

                if raw.isdigit():
                    numeric_vars = generate_numeric_variants(raw, type)
                    for variant in numeric_vars:
                        trie.insert_reversed(variant, id)
                else:
                    text_variants = generate_text_variants(raw)
                    for variant in text_variants:
                        trie.insert_reversed(variant, id)

def build_all_tries():
    trie_province = Trie()
    trie_district = Trie()
    trie_ward = Trie()

    trie_reversed_province = Trie()
    trie_reversed_district = Trie()
    trie_reversed_ward = Trie()

    current_dir = os.path.dirname(os.path.abspath(__file__))
    district_file = os.path.join(current_dir, "..", "list_district.txt")
    province_file = os.path.join(current_dir, "..", "list_province.txt")
    ward_file = os.path.join(current_dir, "..", "list_ward.txt")

    start = time.time()

    build_trie(province_file, trie_province, "province")
    build_trie(district_file, trie_district, "district")
    build_trie(ward_file, trie_ward, "ward")

    build_reversed_trie(province_file, trie_reversed_province, "province")
    build_reversed_trie(district_file, trie_reversed_district, "district")
    build_reversed_trie(ward_file, trie_reversed_ward, "ward")

    end = time.time()
    elapsed = end - start
    print(f"Building tries took {elapsed:.6f} seconds.")

    return trie_province, trie_district, trie_ward, trie_reversed_province, trie_reversed_district, trie_reversed_ward

def get_locality_mapper():
    return locality_map

