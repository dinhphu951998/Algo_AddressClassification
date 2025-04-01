from queue import Queue
from typing import Optional, Tuple, Dict, List

from Utils import *
locality_map = {}
current_id = 0

SPECIAL_CASES = ["xã", "x.", "huyện", "tỉnh", "t.",
                 "tp", "thành phố", "thànhphố"]

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

    def search_max_length(self, text: str, start: int) -> Optional[Tuple[str, int, int]]:
        """Finds the longest valid word from the given start index."""
        node = self.root
        longest_match = ""
        longest_length = 0
        for i in range(start, len(text)):
            char = text[i]
            if char not in node.children:
                break
            node = node.children[char]
            if node.is_end_of_word:
                current_length = i - start + 1
                if current_length > longest_length:
                    longest_length = current_length
                    longest_match = (node.original_string, start, i + 1)
        return longest_match

    def get_raw_text(self, normalized_text):
        return self.original_names.get(normalized_text, normalized_text)

def generate_prefixed_variations(location_name: str, category: str) -> Tuple[List[str], str]:
    """Generate prefixed variations ONLY for wards and districts, and store variations per category."""
    variations = []

    if category not in variation_map:
        variation_map[category] = {}

    normalized_name = normalize_text_but_keep_accent(location_name)

    if normalized_name.isdigit():  # Only generate prefixes for wards and districts
        variations = [prefix + normalized_name for prefix in DIGIT_CASES[category]]
    elif normalized_name in province_short_form:
        variations = [normalized_name, province_short_form[normalized_name]]
    else:
        variations = [normalized_name]

    non_accents_variations = [normalize_text_and_remove_accent(variation) for variation in variations]
    variations.extend(non_accents_variations)

    # Store variations per category
    variation_map[category][normalized_name] = variations
    return variations, normalized_name


def load_databases(filenames: Dict[str, str], tries) -> Dict[str, Trie]:
    """Load multiple database files into separate Tries with prefixed variations."""
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

    prefixed_variations, normalized_text = generate_prefixed_variations(location_name, category)

    for variant in prefixed_variations:
        trie.original_names[variant] = location_name
        trie.insert(variant)
