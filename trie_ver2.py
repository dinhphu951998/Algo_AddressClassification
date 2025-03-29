import unicodedata
import re
import json
import time
from typing import List, Dict, Tuple, Optional

SPECIAL_CASES = ["xã", "x.", "huyện", "tỉnh", "t.", 
                 "tp", "thành phố", "thànhphố"]

# Prefixes for wards and districts to expand possible matches
WARD_CASES = ["p", "phường"]
DISTRICT_CASES = ["q", "quận"]

# Dictionary to store generated variations for tracing back
variation_map: Dict[str, List[str]] = {}
original_names: Dict[str, str] = {}

def normalize_text(text: str) -> str:
    """Normalize text by removing accents, spaces, and special cases."""
    for case in SPECIAL_CASES:
        text = text.replace(case, "")
    
    text = text.replace(",", "")
    text = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in text if not unicodedata.combining(c))  # Remove accents
    text = re.sub(r"\s+", "", text)  # Remove spaces
    return text.lower()

def generate_prefixed_variations(name: str, category: str) -> List[str]:
    """Generate prefixed variations ONLY for wards and districts, and store variations per category."""
    variations = []
    normalized_name = normalize_text(name)

    if category not in variation_map:
        variation_map[category] = {}

    if category not in original_names:
        original_names[category] = {}

    # Store the original form under the correct category
    original_names[category][normalized_name] = name  

    if name.isdigit():  # Only generate prefixes for wards and districts
        if category == "ward":
            variations = [prefix + name for prefix in WARD_CASES]
        elif category == "district":
            variations = [prefix + name for prefix in DISTRICT_CASES]
    else:
        variations.append(normalized_name)

    # Store variations per category
    variation_map[category][normalized_name] = variations
    return variations

def reverse_lookup(normalized_name: str, category: str) -> str:
    """Find the original form of a normalized name using the correct category."""
    if not normalized_name:
        return ""

    # Check direct matches in the category's variation map
    if category in variation_map:
        for key, variations in variation_map[category].items():
            if normalized_name in variations:
                return original_names[category].get(key, key)

    # Handle prefixed cases (e.g., "q1" → "1", "phuong3" → "3")
    if category == "ward":
        stripped_name = re.sub(r"^(p|phuong)", "", normalized_name)
    elif category == "district":
        stripped_name = re.sub(r"^(q|quan)", "", normalized_name)
    else:
        stripped_name = normalized_name  # No prefix removal for provinces

    return original_names[category].get(stripped_name, stripped_name)

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
        normalized_word = normalize_text(original)
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

def load_databases(filenames: Dict[str, str]) -> Dict[str, Trie]:
    """Load multiple database files into separate Tries with prefixed variations."""
    tries = {}
    for category, filename in filenames.items():
        trie = Trie()
        try:
            with open(filename, "r", encoding="utf-8") as file:
                # print(file)
                for line in file:
                    location_name = line.strip()
                    # print(location_name)
                    if location_name:
                        prefixed_variations = generate_prefixed_variations(location_name, category)
                        for variant in prefixed_variations:
                            trie.insert(variant)
            tries[category] = trie
        except FileNotFoundError:
            print(f"Warning: File {filename} not found!")
            tries[category] = Trie()
    return tries

def search_locations(tries: Dict[str, Trie], input_text: str) -> Tuple[Dict[str, Optional[str]], str]:
    """Searches the text using Tries and removes matched words."""
    results = {"ward": None, "district": None, "province": None}
    matched_positions = set()
    remaining_chars = list(input_text)

    for category in ["ward", "district", "province"]:
        # print(category)
        trie = tries.get(category, None)
        if trie:
            for i in range(len(input_text)):
                if i in matched_positions:
                    continue
                match = trie.search(input_text, i)
                if match:
                    results[category] = match[0]  # Save normalized result
                    # print(results)
                    matched_positions.update(range(match[1], match[2]))
                    for j in range(match[1], match[2]):
                        remaining_chars[j] = ""
                    break
    
    normalized_remaining_text = "".join(remaining_chars).strip()
    return results, normalized_remaining_text

def unnormalize_results(extracted_data: Dict[str, Optional[str]]) -> Dict[str, Optional[str]]:
    """Maps back extracted normalized values to their original forms based on categories."""
    return {
        "ward": reverse_lookup(extracted_data["ward"], "ward") if extracted_data["ward"] else "",
        "district": reverse_lookup(extracted_data["district"], "district") if extracted_data["district"] else "",
        "province": reverse_lookup(extracted_data["province"], "province") if extracted_data["province"] else "",
    }

def process_inputs(input_list: List[Dict[str, str]], tries: Dict[str, Trie]) -> List[Dict[str, str]]:
    """Processes input texts and restores original dictionary structure."""
    output = []
    
    for item in input_list:
        raw_text = item["text"]
        normalized_text = normalize_text(raw_text)
        start_time = time.perf_counter_ns()
        extracted_data, remaining_text = search_locations(tries, normalized_text)
        end_time = time.perf_counter_ns()

        execution_time_s = (end_time - start_time) / 1_000_000_000
        final_results = unnormalize_results(extracted_data)

        processed_item = {"text": raw_text}
        processed_item.update(final_results)
        # print(final_results)
        processed_item["remaining_text"] = remaining_text
        processed_item["run_time"] = f"{execution_time_s:.6f}"
 
        if "result" in item:
            expected_result = item["result"]
            for key in ["ward", "district", "province"]:
                if final_results.get(key, "") != expected_result.get(key, ""):
                    processed_item[key] = "wrong"
        
        output.append(processed_item)

    return output

if __name__ == "__main__":
    db_filenames = {
        "province": "province_list.txt",
        "district": "district_list.txt",
        "ward": "ward_list.txt"
    }
    tries = load_databases(db_filenames)
    input_data = json.load(open("public.json", "r", encoding="utf-8"))
    results = process_inputs(input_data, tries)
    json.dump(results, open("result_trie.json", "w", encoding="utf-8"), ensure_ascii=False, indent=4)
    print(json.dumps(results, ensure_ascii=False, indent=4))
