from IndexAnalyzer.IndexAnalyzer import build_all_tries, get_locality_mapper
from Utils.Utils import *
import time
import json


def map_results(search_result, mapper):
    mapped = {}
    # Define the region types you expect
    region_types = ["province", "district", "ward"]

    for region_type in region_types:
        id_set = search_result.get(region_type, set())
        names = set()
        for id in id_set:
            if id in mapper and "name" in mapper[id]:
                names.add(mapper[id]["name"])
        if not names:
            mapped[region_type] = ""
        elif len(names) == 1:
            mapped[region_type] = names.pop()
        else:
            mapped[region_type] = ", ".join(sorted(names))

    return mapped


def compare_and_export_results(records, output_file):
    # Write the updated records to the output file.
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=4)
    print(f"Comparison complete. Results written to {output_file}.")

def levenshtein_distance(s, t):
    m, n = len(s), len(t)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            cost = 0 if s[i - 1] == t[j - 1] else 1
            dp[i][j] = min(
                dp[i - 1][j] + 1,  # deletion
                dp[i][j - 1] + 1,  # insertion
                dp[i - 1][j - 1] + cost  # substitution
            )
    return dp[m][n]

def best_candidate_by_distance(search_key, candidates):
    best_distance = float('inf')
    best_candidate = None
    best_references = set()

    for candidate, references in candidates:
        d = levenshtein_distance(candidate, search_key)
        if d < best_distance:
            best_distance = d
            best_candidate = candidate
            if isinstance(references, set):
                best_references = references.copy()
            else:
                best_references = set([references])
        elif d == best_distance:
            if isinstance(references, set):
                best_references |= references
            else:
                best_references.add(references)

    return best_candidate, best_references, best_distance

def search_with_merging(search_tokens, trie_sequence):
    results = {}
    tokens_remaining = search_tokens[:]  # Make a copy; these tokens will be reduced level by level.

    for trie_name, current_trie in trie_sequence:
        if not tokens_remaining:
            break  # No tokens left to process

        merged_token = ""
        best_result = None
        best_distance = float('inf')
        used_count = 0  # Number of tokens merged so far at this level.
        best_used_count = 0  # Number of tokens that produced the best result.

        # Iterate from the rightmost token of tokens_remaining.
        for i in range(len(tokens_remaining) - 1, -1, -1):
            token = tokens_remaining[i]
            merged_token = token if merged_token == "" else token + merged_token
            used_count += 1

            # Reverse the merged token because the trie is built backward.
            search_key = merged_token[::-1]
            # Collect candidates from the trie.
            print("Search Key: ", search_key)
            candidates = current_trie.collect_candidates(search_key)
            print("Candidates", candidates)
            # Evaluate candidates using Levenshtein distance.
            best_candidate, candidate_ids, distance = best_candidate_by_distance(search_key, candidates)
            print("Best Candidates: ", best_candidate)
            print("Best Candidates IDs: ", candidate_ids)
            print("Distance: ", distance)

            if candidate_ids:
                if best_result is None or distance <= best_distance:
                    best_result = candidate_ids
                    best_distance = distance
                    best_used_count = used_count
                else:
                    # Stop merging if adding this token does not improve the distance.
                    break

        if best_result is not None:
            results[trie_name] = best_result

        # Remove the tokens that were used for this level.
        tokens_remaining = tokens_remaining[:len(tokens_remaining) - best_used_count]

    return results


def main():
    # Build all tries and retrieve the locality mapper.
    province_trie, district_trie, ward_trie = build_all_tries()
    trie_sequence = [
        ("province", province_trie),
        ("district", district_trie),
        ("ward", ward_trie)
    ]
    locality_mapper = get_locality_mapper()

    input_file = 'public.json'
    output_file = 'results.json'

    # Load the JSON file.
    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Process each record from the JSON.
    for record in data:
        # Use the "text" field as the search input.
        search_text = record.get("text", "")
        search_tokens = tokenize_search_term(search_text)
        record_start = time.time()
        results = search_with_merging(search_tokens, trie_sequence)
        record_end = time.time()
        computed_time = record_end - record_start
        mapped_result = map_results(results, locality_mapper)
        record["computed_result"] = mapped_result
        record["computed_time"] = computed_time

        # Compare with the expected result.
        expected = record.get("result", {})
        record["isValid"] = (mapped_result == expected)

    # Write the updated records to a new JSON file.
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    print(f"Comparison complete. Results written to {output_file}.")


if __name__ == "__main__":
    main()
