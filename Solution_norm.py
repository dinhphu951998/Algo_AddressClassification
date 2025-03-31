import unicodedata
import re
import json
import time
import editdistance
from collections import Counter
import math
from typing import List, Dict, Tuple, Optional

SPECIAL_CASES = ["xã", "x.", "huyện", "tỉnh", "t.", "số nhà", "thị trấn", "ấp",
                 "h.", "khu phố","tp", "thành phố", "thànhphố"]

# Prefixes for wards and districts to expand possible matches
WARD_CASES = ["p", "p.", "phường"]
DISTRICT_CASES = ["q", "q.", "quận"]

# Dictionary to store generated variations for tracing back
variation_map: Dict[str, List[str]] = {}
original_names: Dict[str, str] = {}

def normalize_text(text: str) -> str:
    """Normalize text by removing accents, spaces, and special cases."""
    text = text.rstrip('.')
    for case in SPECIAL_CASES:
        text = text.replace(case, "")
    
    text = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in text if not unicodedata.combining(c))  # Remove accents
    text = re.sub(r"\s+", "", text)  # Remove spaces
    return text.lower()

def generate_prefixed_variations(name: str, category: str) -> List[str]:
    """Generate prefixed variations ONLY for wards and districts, but exclude the raw number from the Trie."""
    variations = []
    normalized_name = normalize_text(name)

    if category not in variation_map:
        variation_map[category] = {}

    if category not in original_names:
        original_names[category] = {}

    # Store the original form under the correct category
    original_names[category][normalized_name] = name  

    if name.isdigit():  # Ensure districts and wards with numbers are handled correctly
        if category == "ward":
            variations = [normalize_text(prefix + name) for prefix in WARD_CASES]
        elif category == "district":
            variations = [normalize_text(prefix + name) for prefix in DISTRICT_CASES]

        variation_map[category][normalized_name] = variations
    else:
        variations.append(normalized_name)
        variation_map[category][normalized_name] = variations  # Store normally

    return variations  # Return prefixed variations only


def reverse_lookup(normalized_name: str, category: str) -> str:
    """Find the original form of a normalized name using variation mapping."""
    if not normalized_name or category not in variation_map:
        return normalized_name  # Return as is if no match found

    # Check if the normalized name exists as a key
    if normalized_name in original_names[category]:
        return original_names[category][normalized_name]

    # Look for the normalized name in variations
    for key, variations in variation_map[category].items():
        if normalized_name in variations:
            return original_names[category].get(key, key)  # Get original form

    return normalized_name  # Return as is if no match found

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
        """Finds the longest valid word from the given start index."""
        node = self.root
        longest_match = None
        match_end = start

        for i in range(start, len(text)):
            char = text[i]
            if char not in node.children:
                break
            node = node.children[char]

            # Update longest match if this is a valid end of word
            if node.is_end_of_word:
                longest_match = (node.original_string, start, i + 1)
                match_end = i + 1

        return longest_match  # Return the longest match found


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
                            # print(variant)
                            trie.insert(variant)
            tries[category] = trie
        except FileNotFoundError:
            print(f"Warning: File {filename} not found!")
            tries[category] = Trie()
    return tries

def calculate_edit_distance(s1: str, s2: str) -> float:
    """Calculate the normalized edit distance between two strings."""
    distance = editdistance.eval(s1, s2)
    max_len = max(len(s1), len(s2))
    return 1 - (distance / max_len)  # Normalize to a similarity score between 0 and 1

def calculate_cosine_similarity(s1: str, s2: str) -> float:
    """Calculate the cosine similarity between two strings."""
    # Tokenize the strings into characters
    tokens1 = list(s1)
    tokens2 = list(s2)

    # Count the frequency of each character
    freq1 = Counter(tokens1)
    freq2 = Counter(tokens2)

    # Calculate dot product
    dot_product = sum(freq1[char] * freq2[char] for char in set(tokens1) & set(tokens2))

    # Calculate magnitudes
    magnitude1 = math.sqrt(sum(freq1[char] ** 2 for char in freq1))
    magnitude2 = math.sqrt(sum(freq2[char] ** 2 for char in freq2))

    # Calculate cosine similarity
    if magnitude1 == 0 or magnitude2 == 0:
        return 0.0
    return dot_product / (magnitude1 * magnitude2)

def find_best_match_with_similarity(remaining_text: str, category: str, cosine_threshold: float = 0.7) -> Optional[str]:
    """Find the best match using edit distance and cosine similarity with a threshold."""
    best_match = None
    best_score = 0.0

    for original_name, variations in variation_map[category].items():
        for variation in variations:
            edit_distance_score = calculate_edit_distance(remaining_text, variation)
            cosine_similarity_score = calculate_cosine_similarity(remaining_text, variation)

            # Apply cosine similarity threshold
            if cosine_similarity_score < cosine_threshold:
                continue

            combined_score = (edit_distance_score + cosine_similarity_score) / 2

            if combined_score > best_score:
                best_score = combined_score
                best_match = original_names[category][original_name]

    return best_match

def search_locations(tries: Dict[str, Trie], input_text: str) -> Tuple[Dict[str, Optional[str]], str]:
    """Searches the text using Tries and selects the latest valid match for each category."""
    results = {"ward": None, "district": None, "province": None}
    matched_intervals = []
    remaining_chars = list(input_text)

    for category in ["province", "district", "ward"]:
        trie = tries.get(category, None)
        if trie:
            matches = []
            i = 0
            while i < len(remaining_chars):
                match = trie.search("".join(remaining_chars), i)
                if match:
                    matches.append(match)
                    i += 1  # Move past the matched part
                else:
                    i += 1  # Continue searching

            if matches:
                print("".join(remaining_chars).strip())
                # if category == "ward":
                #      # Find the match that contains the end of the string and has the longest length
                #     best_match = max(matches, key=lambda x: (x[2], x[2] - x[1]))  # Prioritize the end and length
                #     # Check if the best match is actually the longest match covering the end of the string
                #     if any(match[1] <= len(input_text) - 1 <= match[2] for match in matches):
                #         best_match = max(matches, key=lambda x: (x[2], x[2] - x[1]))
                # else:
                #     best_match = matches[-1]  # For other categories, take the latest (last) match
                best_match = max(matches, key=lambda x: (x[2], x[2] - x[1]))  # Prioritize the end and length
                # Check if the best match is actually the longest match covering the end of the string
                if any(match[1] <= len(input_text) - 1 <= match[2] for match in matches):
                    best_match = max(matches, key=lambda x: (x[2], x[2] - x[1]))
                print(matches)
                # Ensure no overlap with previously matched regions
                start, end = best_match[1], best_match[2]
                if any(s <= start < e or s < end <= e for s, e in matched_intervals):
                    continue  # Skip overlapping matches

                # Store results and update matched ranges
                results[category] = best_match[0]
                matched_intervals.append((start, end))

                # Remove matched characters properly
                for j in range(start, end):
                    remaining_chars[j] = ""  # Clear matched characters
    normalized_remaining_text = "".join(remaining_chars).strip()

    # Use edit distance and cosine similarity for unmatched categories
    for category in results:
        if results[category] is None:
            best_match = find_best_match_with_similarity(normalized_remaining_text, category)
            if best_match:
                results[category] = normalize_text(best_match)
                
    normalized_remaining_text = "".join(remaining_chars).strip()
    return results, normalized_remaining_text

def unnormalize_results(extracted_data: Dict[str, Optional[str]]) -> Dict[str, Optional[str]]:
    """Maps back extracted normalized values to their original forms based on categories."""
    return {
        "ward": reverse_lookup(extracted_data["ward"], "ward") if extracted_data["ward"] else "",
        "district": reverse_lookup(extracted_data["district"], "district") if extracted_data["district"] else "",
        "province": reverse_lookup(extracted_data["province"], "province") if extracted_data["province"] else "",
    }

def process_input(item: Dict[str, str], tries: Dict[str, Trie]) -> Dict[str, str]:
    """Processes a single input text and restores original dictionary structure."""
    raw_text = item["text"]
    normalized_text = normalize_text(raw_text.lower())
    print(normalized_text)
    start_time = time.perf_counter_ns()
    extracted_data, remaining_text = search_locations(tries, normalized_text)
    end_time = time.perf_counter_ns()

    execution_time_s = (end_time - start_time) / 1_000_000_000
    final_results = unnormalize_results(extracted_data)

    processed_item = {"text": raw_text}
    processed_item.update(final_results)
    processed_item["remaining_text"] = remaining_text
    processed_item["run_time"] = f"{execution_time_s:.6f}"
    
    return processed_item

if __name__ == "__main__":
    db_filenames = {
        "province": "province_list.txt",
        "district": "district_list.txt",
        "ward": "ward_list.txt"
    }
    tries = load_databases(db_filenames)
    input_data = json.load(open("public.json", "r", encoding="utf-8"))
    results = []  # Initialize a list to store results
    for item in input_data:
        result = process_input(item, tries)
        results.append(result)  # Append each result to the list
    
    # Save all results to a JSON file
    json.dump(results, open("result_trie.json", "w", encoding="utf-8"), ensure_ascii=False, indent=4)
    print(json.dumps(results, ensure_ascii=False, indent=4))
