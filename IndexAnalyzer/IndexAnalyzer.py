from typing import Optional, Tuple, Dict, List

from Utils.Utils import *
locality_map = {}
current_id = 0

SPECIAL_CASES = ["xã", "x.", "huyện", "tỉnh", "t.",
                 "tp", "thành phố", "thànhphố"]

# Prefixes for wards and districts to expand possible matches
WARD_CASES = ["p", "phường", "phương", "phuong"]
DISTRICT_CASES = ["q", "quân", "quan"]

# Dictionary to store generated variations for tracing back
variation_map: Dict[str, List[str]] = {}
original_names: Dict[str, str] = {}


class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False
        self.original_string: Optional[str] = None


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, original: str):
        """Insert a normalized word into the trie with a reference to the original."""
        normalized_word = original
        # normalized_word = normalize_text(original)
        node = self.root
        for char in normalized_word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True
        node.original_string = normalized_word

    def search(self, text: str, start: int) -> Optional[Tuple[str, int, int]]:
        """Finds the first valid word from the given start index."""
        node = self.root
        for i in range(start, len(text)):
            char = text[i]
            if char not in node.children:
                break
            node = node.children[char]
            if node.is_end_of_word:
                return (node.original_string, start, i + 1)
        return None

def generate_prefixed_variations(normalized_name: str, category: str) -> List[str]:
    """Generate prefixed variations ONLY for wards and districts, and store variations per category."""
    variations = []

    if category not in variation_map:
        variation_map[category] = {}

    if category not in original_names:
        original_names[category] = {}

    if normalized_name.isdigit():  # Only generate prefixes for wards and districts
        if category == "ward":
            variations = [prefix + normalized_name for prefix in WARD_CASES]
        elif category == "district":
            variations = [prefix + normalized_name for prefix in DISTRICT_CASES]
    else:
        variations.append(normalized_name)

    # Store variations per category
    variation_map[category][normalized_name] = variations
    return variations


def load_databases(filenames: Dict[str, str]) -> Dict[str, Trie]:
    """Load multiple database files into separate Tries with prefixed variations."""
    tries = {}
    for category, filename in filenames.items():
        trie = Trie()
        try:
            with open(filename, "r", encoding="utf-8") as file:
                for line in file:
                    location_name = line.strip()
                    if location_name:

                        normalized_name_but_keep_alphabet = normalize_text_but_keep_vietnamese_alphabet(location_name)
                        normalized_name = normalize_text(location_name)

                        prefixed_variations = list(set(generate_prefixed_variations(normalized_name, category) + generate_prefixed_variations(normalized_name_but_keep_alphabet, category)))

                        for variant in prefixed_variations:
                            # Store the original form under the correct category
                            original_names[category][variant] = location_name
                            trie.insert(variant)
            tries[category] = trie
        except FileNotFoundError:
            print(f"Warning: File {filename} not found!")
            tries[category] = Trie()
    return tries

#
# def generate_text_variants(raw_str):
#     s = normalize_text(raw_str)
#     tokens = s.split()
#     n = len(tokens)
#
#     if n == 2:
#         t1, t2 = tokens
#         variants = [
#             f"{t1} {t2}",
#             f"{t1[0]}{t2[0]}",
#             f"{t1[0]}{t2}",
#             f"{t1}{t2[0]}",
#             f"{t1}{t2}",
#         ]
#
#     elif n == 3:
#         t1, t2, t3 = tokens
#         variants = [
#             f"{t1} {t2} {t3}",
#             f"{t1}{t2}{t3}",
#             f"{t1[0]}{t2[0]}{t3[0]}",
#             f"{t1} {t2}{t3}",
#             f"{t1}{t2} {t3}",
#             f"{t1[0]}{t2}{t3}",
#             f"{t1}{t2[0]}{t3}",
#             f"{t1}{t2}{t3[0]}",
#         ]
#
#     elif n == 4:
#         t1, t2, t3, t4 = tokens
#         variants = [
#             f"{t1} {t2} {t3} {t4}",
#             f"{t1}{t2}{t3}{t4}",
#             f"{t1[0]}{t2[0]}{t3[0]}{t4[0]}",
#             f"{t1} {t2}{t3}{t4}",
#             f"{t1}{t2} {t3}{t4}",
#             f"{t1}{t2}{t3} {t4}",
#             f"{t1[0]}{t2}{t3}{t4}",
#             f"{t1}{t2[0]}{t3}{t4}",
#         ]
#     else:
#         variants = [s]
#
#     variants = list(set(variants))
#     print(variants)
#     return variants
#
#
# numbers_1_to_30 = {
#     1: "mot", 2: "hai", 3: "ba", 4: "bon",
#     5: "nam", 6: "sau", 7: "bay", 8: "tam",
#     9: "chin", 10: "muoi",
#     11: "muoi mot", 12: "muoi hai", 13: "muoi ba", 14: "muoi bon",
#     15: "muoi lam", 16: "muoi sau", 17: "muoi bay", 18: "muoi tam",
#     19: "muoi chin",
#     20: "hai muoi",
#     21: "hai muoi mot", 22: "hai muoi hai", 23: "hai muoi ba",
#     24: "hai muoi bon", 25: "hai muoi lam", 26: "hai muoi sau",
#     27: "hai muoi bay", 28: "hai muoi tam", 29: "hai muoi chin",
#     30: "ba muoi"
# }
#
#
# def generate_numeric_variants(num_str, place_type):
#     if place_type not in ("district", "ward"):
#         return [num_str]
#
#     if place_type == "district":
#         prefixShort = "q"
#         prefixLong = "quan"
#     else:  # ward
#         prefixShort = "p"
#         prefixLong = "phuong"
#
#     try:
#         n = int(num_str)
#     except ValueError:
#         return [num_str]
#
#     if 1 <= n <= 30:
#         digit_word = numbers_1_to_30[n]
#         digit_word_no_space = digit_word.replace(" ", "")
#
#         zero_num = ""
#         if n < 10:
#             zero_num = f"0{num_str}"
#
#         variants = []
#
#         variants.append(f"{prefixShort}{num_str}")
#         variants.append(f"{prefixLong}{num_str}")
#         variants.append(f"{prefixShort}{digit_word}")
#         variants.append(f"{prefixLong}{digit_word}")
#
#         if zero_num:
#             variants.append(f"{prefixShort}{zero_num}")
#             variants.append(f"{prefixLong}{zero_num}")
#
#         variants.append(num_str)
#
#         if zero_num:
#             variants.append(zero_num)
#
#         variants.append(digit_word)
#
#         variants.append(f"{prefixLong} {num_str}")
#
#         if zero_num:
#             variants.append(f"{prefixShort} {zero_num}")
#
#         variants.append(f"{prefixShort} {num_str}")
#
#         variants.append(f"{prefixShort}{digit_word_no_space}")
#         variants.append(f"{prefixLong}{digit_word_no_space}")
#
#         variants.append(f"{prefixShort} {digit_word_no_space}")
#         variants.append(f"{prefixLong} {digit_word_no_space}")
#
#         variants.append(f"{prefixShort} {digit_word}")
#         variants.append(f"{prefixLong} {digit_word}")
#
#         variants = list(set(variants))
#         return variants
#     else:
#         return [num_str]
#
#
# def build_trie(file_path, trie, type):
#     global current_id
#     seen = set()
#     with open(file_path, 'r', encoding='utf-8') as f:
#         for line in f:
#             raw = line.strip()
#             if raw and raw not in seen:
#                 seen.add(raw)
#                 id = current_id;
#                 current_id += 1
#
#                 locality_map[id] = {
#                     "type": type,
#                     "name": raw
#                 }
#
#                 if raw.isdigit():
#                     numeric_vars = generate_numeric_variants(raw, type)
#                     for variant in numeric_vars:
#                         trie.insert(variant, id)
#                 else:
#                     text_variants = generate_text_variants(raw)
#                     for variant in text_variants:
#                         trie.insert(variant, id)
#
# def build_reversed_trie(file_path, trie, type):
#     global current_id
#     seen = set()
#     with open(file_path, 'r', encoding='utf-8') as f:
#         for line in f:
#             raw = line.strip()
#             if raw and raw not in seen:
#                 seen.add(raw)
#                 id = current_id;
#                 current_id += 1
#
#                 locality_map[id] = {
#                     "type": type,
#                     "name": raw
#                 }
#
#                 if raw.isdigit():
#                     numeric_vars = generate_numeric_variants(raw, type)
#                     for variant in numeric_vars:
#                         trie.insert_reversed(variant, id)
#                 else:
#                     text_variants = generate_text_variants(raw)
#                     for variant in text_variants:
#                         trie.insert_reversed(variant, id)
#
# def build_all_tries():
#     trie_province = Trie()
#     trie_district = Trie()
#     trie_ward = Trie()
#
#     trie_reversed_province = Trie()
#     trie_reversed_district = Trie()
#     trie_reversed_ward = Trie()
#
#     current_dir = os.path.dirname(os.path.abspath(__file__))
#     district_file = os.path.join(current_dir, "..", "list_district.txt")
#     province_file = os.path.join(current_dir, "..", "list_province.txt")
#     ward_file = os.path.join(current_dir, "..", "list_ward.txt")
#
#     start = time.time()
#
#     build_trie(province_file, trie_province, "province")
#     build_trie(district_file, trie_district, "district")
#     build_trie(ward_file, trie_ward, "ward")
#
#     build_reversed_trie(province_file, trie_reversed_province, "province")
#     build_reversed_trie(district_file, trie_reversed_district, "district")
#     build_reversed_trie(ward_file, trie_reversed_ward, "ward")
#
#     end = time.time()
#     elapsed = end - start
#     print(f"Building tries took {elapsed:.6f} seconds.")
#
#     return trie_province, trie_district, trie_ward, trie_reversed_province, trie_reversed_district, trie_reversed_ward
#
# def get_locality_mapper():
#     return locality_map

