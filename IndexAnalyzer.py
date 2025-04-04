from queue import Queue
from typing import Optional, Tuple, Dict, List

from Utils import *
locality_map = {}
current_id = 0

SPECIAL_CASES = ["xã", "x.", "huyện", "tỉnh", "t.",
                 "tp","thành phố", "thànhphố"]

# Prefixes for wards and districts to expand possible matches
DIGIT_CASES = {
    "ward": ["p", "phường"],
    "district": ["q", "quận"],
}

# Dictionary to store generated variations for tracing back
variation_map: Dict[str, dict] = {}

province_short_form = {
    "hồchíminh":"hcm",
    "bàrịavũngtàu":"brvt",
}

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False
        self.original_string: Optional[str] = None


class Trie:

    def __init__(self):
        self.root = TrieNode()
        self.all_words = set()
        self.original_names: Dict[str, str] = {}

    def insert(self, normalized_word: str):
        """Insert a normalized word into the trie with a reference to the original."""
        node = self.root
        for i, char in enumerate(normalized_word):

            if char not in node.children:
                node.children[char] = TrieNode()

            node = node.children[char]

        node.is_end_of_word = True
        node.original_string = normalized_word

        self.all_words.add(normalized_word)

    def insert_reversed(self, normalized_word: str):
        node = self.root
        reversed_word = normalized_word[::-1]  # Đảo ngược chuỗi
        for char in reversed_word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]

        node.is_end_of_word = True
        node.original_string = normalized_word  # Lưu chuỗi gốc, không phải chuỗi đảo ngược.
        self.all_words.add(normalized_word)

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

    # def search_max_length(self, text: str, start: int) -> Optional[Tuple[str, int, int]]:
    #     """Finds the longest valid word from the given start index."""
    #     node = self.root
    #     longest_match = ""
    #     longest_length = 0
    #     result = []
    #     for i in range(start, len(text)):
    #         char = text[i]
    #         if char not in node.children:
    #             break
    #         node = node.children[char]
    #         if node.is_end_of_word:
    #             current_length = i - start + 1
    #             if current_length > longest_length:
    #                 longest_length = current_length
    #                 longest_match = (node.original_string, start, i + 1)
    #                 print(longest_match)
    #                 result.append(longest_match)
    #                 print(result)
    #     return result
    def search_max_length(self, text: str, start: int) -> List[Tuple[str, int, int]]:
        """Finds all valid words, including overlapping ones, without skipping characters."""
        result = []
        
        for i in range(start, len(text)):  # Start search at each position
            node = self.root
            for j in range(i, len(text)):  # Continue searching for words from `i`
                char = text[j]
                if char not in node.children:
                    break  # Stop if the character is not in the Trie
                
                node = node.children[char]

                if node.is_end_of_word:
                    match = (node.original_string, i, j + 1)  # (word, start index, end index)
                    result.append(match)  # Store all matches

        return result  # Return all matches


    
    def get_raw_text(self, normalized_text):
        return self.original_names.get(normalized_text, normalized_text)

    def collect_candidates(self, search_key: str) -> List[Tuple[str, Optional[str]]]:
        node = self.root
        for char in search_key:
            if char not in node.children:
                return []
            node = node.children[char]

        candidates = []

        def dfs(current_node: TrieNode, path: str):
            if current_node.is_end_of_word:
                candidates.append((path, current_node.original_string))
            for letter, child in current_node.children.items():
                dfs(child, path + letter)

        dfs(node, search_key)
        return candidates


def generate_prefixed_variations(location_name: str, category: str) -> Tuple[List[str], List[str], str]:
    """
    Generate basic prefixed variants and additional (acronym) variants.
    """
    variations = []
    if category not in variation_map:
        variation_map[category] = {}

    normalized_name = normalize_text_but_keep_accent(location_name)

    if normalized_name.isdigit():  # Only generate prefixes for wards and districts
        padded_name = normalized_name.zfill(2) if len(normalized_name) == 1 else normalized_name
        unpadded_name = str(int(normalized_name))  # "01" -> "1", keeps "11" as "11"
        
        all_number_forms = {padded_name, unpadded_name}  # Set ensures unique values

        variations = [prefix + num for num in all_number_forms for prefix in DIGIT_CASES[category]]
        # print(variations)
    elif normalized_name in province_short_form:
        variations = [normalized_name, province_short_form[normalized_name]]
    else:
        variations = [normalized_name]

    non_accents_variations = [normalize_text_and_remove_accent(v) for v in variations]
    variations.extend(non_accents_variations)
    variations = list(set(variations))

    # Process each acronym variant with the same logic as above.
    raw_acronym_variants = generate_text_variants(location_name)

    acronym_variants = []
    for av in raw_acronym_variants:
        if av.isdigit():
            new_vars = [prefix + av for prefix in DIGIT_CASES[category]]
        elif av in province_short_form:
            new_vars = [av, province_short_form[av]]
        else:
            new_vars = [av]
        new_vars_non_accent = [normalize_text_and_remove_accent(v) for v in new_vars]
        acronym_variants.extend(new_vars_non_accent)
    acronym_variants = list(set(acronym_variants))

    variation_map[category][normalized_name] = variations
    return variations, acronym_variants, normalized_name


def generate_text_variants(raw_str):
    # If there is no whitespace, just return the string itself.
    if " " not in raw_str:
        return [raw_str]

    tokens = raw_str.split()
    n = len(tokens)

    if n == 2:
        t1, t2 = tokens
        variants = [
            f"{t1[0]}{t2}",
            f"{t1}{t2}",
        ]
    elif n == 3:
        t1, t2, t3 = tokens
        variants = [
            f"{t1}{t2}{t3}",
        ]
    elif n == 4:
        t1, t2, t3, t4 = tokens
        variants = [
            f"{t1}{t2}{t3}{t4}",
        ]
    else:
        variants = [raw_str]

    return list(set(variants))


def load_databases(filenames: Dict[str, str],
                   tries: Dict[str, Trie],
                   reversed_tries: Dict[str, Trie]) -> Tuple[Dict[str, Trie], Dict[str, Trie]]:
    for category, filename in filenames.items():
        trie = Trie()
        reversed_trie = Trie()
        try:
            with open(filename, "r", encoding="utf-8") as file:
                for line in file:
                    load_line(line, trie, reversed_trie, category)
            tries[category] = trie
            reversed_tries[category] = reversed_trie
        except FileNotFoundError:
            print(f"Warning: File {filename} not found!")
            tries[category] = Trie()
            reversed_tries[category] = Trie()
    return tries, reversed_tries


def load_line(line, trie, reversed_trie, category):
    location_name = line.strip()
    if location_name == "":
        return

    # Generate the initial prefixed variants
    prefixed_variations, acronym_variants, normalized_text = generate_prefixed_variations(location_name, category)
    # Insert original prefixed_variations into the regular trie
    for variant in prefixed_variations:
        trie.original_names[variant] = location_name
        trie.insert(variant)

    all_variants = []
    for variant in prefixed_variations + acronym_variants:
        if variant not in all_variants:
            all_variants.append(variant)

    # Insert the combined variants into the reversed trie using insert_reversed
    for variant in all_variants:
        trie.original_names[variant] = location_name
        reversed_trie.insert_reversed(variant)
