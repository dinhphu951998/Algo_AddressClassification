import unicodedata
import re
import json
from typing import List, Dict, Tuple, Optional

SPECIAL_CASES = ["xã", "x.", "huyện", "tỉnh", "t.", "tt", 
                 "tp", "thành phố", "thànhphố"]

def normalize_text(text: str) -> str:
    """Normalize text by removing accents, spaces, and special cases."""
    for case in SPECIAL_CASES:
        text = text.replace(case, "")
    
    text = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in text if not unicodedata.combining(c))  # Remove accents
    text = re.sub(r"\s+", "", text)  # Remove spaces
    return text.lower()

class TrieNode:
    """Trie Node for storing characters and mapping back to the original string."""
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False
        self.original_string: Optional[str] = None  # Store only original string

class Trie:
    """Trie Data Structure for efficient word lookup."""
    def __init__(self):
        self.root = TrieNode()
    
    def insert(self, original: str):
        """Inserts the normalized word into the trie with a reference to the original string."""
        normalized_word = normalize_text(original)
        node = self.root
        for char in normalized_word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True
        node.original_string = original  # Store original version
    
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
    """Load multiple database files into separate Tries."""
    tries = {}
    for category, filename in filenames.items():
        trie = Trie()
        try:
            with open(filename, "r", encoding="utf-8") as file:
                for line in file:
                    location_name = line.strip()
                    if location_name:
                        trie.insert(location_name)
            tries[category] = trie
        except FileNotFoundError:
            print(f"Warning: File {filename} not found!")
            tries[category] = Trie()  # Create an empty Trie if file is missing
    return tries

def search_locations(tries: Dict[str, Trie], input_text: str, original_text: str) -> Tuple[Dict[str, Optional[str]], str]:
    """Searches the text using Tries in sequence (ward -> district -> province) and removes matched words."""
    results = {"ward": None, "district": None, "province": None}
    matched_positions = set()
    remaining_text = original_text  # Work with original string

    for category in ["ward", "district", "province"]:  # Search order
        trie = tries.get(category, None)
        if trie:
            for i in range(len(input_text)):
                if i in matched_positions:  # Skip positions already matched
                    continue
                match = trie.search(input_text, i)
                if match:
                    results[category] = match[0]  # Save original string
                    matched_positions.update(range(match[1], match[2]))  # Mark as matched
                    
                    # **Remove the matched word from the original text**
                    remaining_text = re.sub(rf"\b{re.escape(match[0])}\b", "", remaining_text, count=1).strip()
                    break  # Only store one match per category
    
    return results, remaining_text

def load_input_texts(filename: str) -> List[Dict[str, str]]:
    """Load 'text' and 'result' fields from public.json."""
    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
            return [{"text": item["text"], "expected": item["result"]} for item in data if "text" in item and "result" in item]
    except FileNotFoundError:
        print(f"Error: {filename} not found!")
        return []

def validate_results(extracted_data: Dict[str, Optional[str]], expected_data: Dict[str, str]) -> Dict[str, str]:
    """Compares extracted results with expected results and marks mismatches as 'Wrong'."""
    validated_results = {}
    
    for key in ["ward", "district", "province"]:
        if extracted_data[key] == expected_data.get(key, None):
            validated_results[key] = extracted_data[key]
        else:
            validated_results[key] = "Wrong"
    
    return validated_results

def process_inputs(input_list: List[Dict[str, str]], tries: Dict[str, Trie]) -> List[Dict[str, str]]:
    """Processes input texts, extracts locations, validates them, and stores remaining text."""
    output = []
    
    for item in input_list:
        raw_text = item["text"]
        expected_result = item["expected"]  # Get expected values
        normalized_text = normalize_text(raw_text)  # Normalize input
        start_time = time.perf_counter_ns()
        extracted_data, remaining_text = search_locations(tries, normalized_text, raw_text)  # Extract from Trie
        end_time = time.perf_counter_ns()

        execution_time_ns = end_time - start_time
        execution_time_s = execution_time_ns / 1_000_000_000

        if execution_time_ns > 10_000_000:
            print(f"Warning: Segmentation took too long ({execution_time_s:.6f} s)!")
        validated_data = validate_results(extracted_data, expected_result)  # Validate against expected

        # Store results
        validated_data["original_string"] = raw_text
        validated_data["remaining_text"] = remaining_text
        validated_data["run_time"] = f"{execution_time_s:.6f}"
        output.append(validated_data)
    
    return output

# Example Usage
if __name__ == "__main__":
    db_filenames = {
        "province": "province_list.txt",
        "district": "district_list.txt",
        "ward": "ward_list.txt"
    }
    
    # Load data into Tries
    tries = load_databases(db_filenames)

    # Load input texts from public.json
    input_data = load_input_texts("public.json")

    # Process inputs
    results = process_inputs(input_data, tries)

    # Save results to JSON file
    with open("result_trie.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=4)

    # Print results
    print(json.dumps(results, ensure_ascii=False, indent=4))
