from typing import Optional, Tuple, Dict, List
from Utils import *

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
        self.all_norm_names = set()
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

        self.all_norm_names.add(normalized_word)

    def insert_reversed(self, normalized_word: str):
        node = self.root
        reversed_word = normalized_word[::-1]  # Đảo ngược chuỗi
        for char in reversed_word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]

        node.is_end_of_word = True
        node.original_string = normalized_word  # Lưu chuỗi gốc, không phải chuỗi đảo ngược.
        self.all_norm_names.add(normalized_word)

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

    normalized_name = normalize_text_v2(location_name)

    if normalized_name.isdigit():  # Only generate prefixes for wards and districts
        padded_name = normalized_name.zfill(2) if len(normalized_name) == 1 else normalized_name
        unpadded_name = str(int(normalized_name))  # "01" -> "1", keeps "11" as "11"
        
        all_number_forms = {padded_name, unpadded_name}  # Set ensures unique values

        variations = [prefix + num for num in all_number_forms for prefix in DIGIT_CASES[category]]
    else:
        variations = [normalized_name]

    # non_accents_variations = [normalize_text_and_remove_accent(v) for v in variations]
    # variations.extend(non_accents_variations)
    variations = list(set(variations))

   
    variation_map[category][normalized_name] = variations
    return variations, normalized_name


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
                   tries: Dict[str, Trie]) -> Tuple[Dict[str, Trie], Dict[str, Trie]]:
    for category, filename in filenames.items():
        trie = Trie()
        try:
            with open(filename, "r", encoding="utf-8") as file:
                for line in file:
                    load_line(line, trie, category)
            tries[category] = trie
        except FileNotFoundError:
            print(f"Warning: File {filename} not found!")
            tries[category] = Trie()
    return tries


def load_line(line, trie, category):
    location_name = line.strip()
    if location_name == "":
        return

    # Generate the initial prefixed variants
    prefixed_variations, normalized_text = generate_prefixed_variations(location_name, category)
    # Insert original prefixed_variations into the regular trie
    for variant in prefixed_variations:
        trie.original_names[variant] = location_name
        trie.insert(variant)
