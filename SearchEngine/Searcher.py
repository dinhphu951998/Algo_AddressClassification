from typing import Dict, Tuple, Optional

from IndexAnalyzer.IndexAnalyzer import Trie

def search_locations(tries: Dict[str, Trie], input_text: str) -> Tuple[Dict[str, Optional[str]], str]:
    """Searches the text using Tries and removes matched words."""
    results = {"ward": "", "district": "", "province": ""}
    matched_positions = set()
    remaining_chars = list(input_text)

    for category in ["province", "ward", "district"]:
        # print(category)
        trie = tries.get(category, None)

        if not trie:
            continue

        if category == "province":
            province = search_part_reversed(trie, input_text, matched_positions, remaining_chars)
            results["province"] = province

        if category == "ward":
            ward = search_part(trie, input_text, matched_positions, remaining_chars)
            results["ward"] = ward

        if category == "district":
            district = search_part(trie, input_text, matched_positions, remaining_chars)
            results["district"] = district

    normalized_remaining_text = "".join(remaining_chars).strip()
    return results, normalized_remaining_text

def search_part(trie, input_text, matched_positions, remaining_chars):
    for i in range(len(input_text)):
        if i in matched_positions:
            continue
        match = trie.search(input_text, i)
        if match and match[1] not in matched_positions and match[2] - 1 not in matched_positions:
            matched_positions.update(range(match[1], match[2]))
            for j in range(match[1], match[2]):
                remaining_chars[j] = ""
            return match[0] # normalized result
    return ""

def search_part_reversed(trie, input_text, matched_positions, remaining_chars):
    for i in range(len(input_text) - 1, -1, -1): # Reverse start at len - 1, end at -1 exclusive, step -1
        if i in matched_positions:
            continue
        match = trie.search(input_text, i)
        if match:
            matched_positions.update(range(match[1], match[2]))
            for j in range(match[1], match[2]):
                remaining_chars[j] = ""
            return match[0] # normalized result
    return ""