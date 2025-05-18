import time
import re
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from IndexAnalyzer import Trie


def tokenize(text):
    """Tokenize the normalized input into words."""
    return text.split()


def tokenize_with_indices(text):
    tokens = []
    for match in re.finditer(r'\S+', text):
        tokens.append((match.group(), match.start(), match.end()))
    return tokens


def generate_word_ngrams(normalized_text, min_n=1, max_n=4):
    """
    Generate all possible word n-gram substrings from the token list.
    Returns: list of (start_idx, end_idx, ngram_str, 'word')
    """
    tokens = tokenize_with_indices(normalized_text)

    max_n = min(max_n, len(tokens))
    ngrams = set()

    for token in tokens:
        if len(token[0]) <= 10:
            continue
        ngrams.update(generate_char_ngrams(token[0], base_index=token[1]))

    for n in range(min_n, max_n + 1):
        for i in range(len(tokens) - n + 1):
            ngram_tokens = tokens[i:i+n]
            ngram_str = ' '.join([t[0] for t in ngram_tokens])
            start_char = ngram_tokens[0][1]
            end_char = ngram_tokens[-1][2] - 1
            ngrams.add((start_char, end_char, ngram_str, 'word'))
    return ngrams


def generate_char_ngrams(word, min_n=6, max_n=10, base_index=0):
    """
    Generate all possible character n-gram substrings from the text.
    Returns: list of (start_idx, end_idx, ngram_str, 'char')
    """
    ngrams = set()
    length = len(word)
    for n in range(min_n, min(max_n, length) + 1):
        for i in range(length - n + 1):
            ngram = word[i:i + n]
            # Find start and end character positions in normalized text
            start_char = base_index + i
            end_char = start_char + n - 1
            ngrams.add((start_char, end_char, ngram, 'char'))
    return ngrams


total_fuzzy_search_time = 0
total_fuzzy_search_count = 0

def extract_candidates(normalized_text: str, ward_trie: Trie, district_trie: Trie, province_trie: Trie):
    """
    For a normalized input string, generate all word and char n-grams and check for matches in each trie.
    Returns: list of candidate dicts (start, end, original_name, type, ngram, ngram_type)
    """
    global total_fuzzy_search_time, total_fuzzy_search_count

    ngrams = generate_word_ngrams(normalized_text, min_n=1, max_n=4)
    candidates = []
    for start, end, ngram, ngram_type in ngrams:
        norm_ngram = ngram
        for trie, typ in [
            (ward_trie, 'ward'),
            (district_trie, 'district'),
            (province_trie, 'province')
        ]:
            match_type = 'exact'
            matches = trie.search(norm_ngram)
            if not matches:
                match_type = 'fuzzy'

                timer = time.time()

                matches = trie.fuzzy_search_with_ratio(norm_ngram)
                # matches = trie.fuzzy_search_with_ratio_bktree(norm_ngram)

                total_fuzzy_search_time += time.time() - timer
                total_fuzzy_search_count += 1

            for match in matches:
                candidates.append({
                    'type': typ,
                    'start': start,
                    'end': end,
                    'original': match,
                    'ngram': ngram,
                    'ngram_type': ngram_type,
                    'match_type': match_type
                })
    return candidates, total_fuzzy_search_time, total_fuzzy_search_count
    

# Example usage
if __name__ == "__main__":
    # from trie import Trie
    # ward_trie = Trie(); district_trie = Trie(); province_trie = Trie()
    # ward_trie.insert("thuan thanh", "Thuận Thành")
    # district_trie.insert("can giuoc", "Cần Giuộc")
    # province_trie.insert("long an", "Long An")

    # normalized = "x thuan thanh hcan giuoc tlong an"
    # candidates = extract_candidates(normalized, ward_trie, district_trie, province_trie)
    # for c in candidates:
    #     print(c) 

    s = "ch 1614 hh2 khu dtm duong noi yen nghiahadonghyanoi"
    print(generate_word_ngrams(s))