from Utils import normalize_text_v2


def tokenize(text):
    """Tokenize the normalized input into words."""
    return text.split()


def generate_word_ngrams(normalized_text, min_n=1, max_n=5):
    """
    Generate all possible word n-gram substrings from the token list.
    Returns: list of (start_idx, end_idx, ngram_str, 'word')
    """
    tokens = tokenize(normalized_text)

    if max_n is None:
        max_n = len(tokens)
    ngrams = set()
    for n in range(min_n, max_n + 1):
        for i in range(len(tokens) - n + 1):
            ngram = ' '.join(tokens[i:i + n])
            # Find start and end character positions in original text
            start_char = normalized_text.find(ngram)
            end_char = start_char + len(ngram) - 1
            ngrams.add((start_char, end_char, ngram, 'word'))
    return ngrams


def generate_char_ngrams(text, min_n=6, max_n=20):
    """
    Generate all possible character n-gram substrings from the text.
    Returns: list of (start_idx, end_idx, ngram_str, 'char')
    """
    ngrams = set()
    length = len(text)
    for n in range(min_n, min(max_n, length) + 1):
        for i in range(length - n + 1):
            ngram = text[i:i + n]
            ngrams.add((i, i + n - 1, ngram, 'char'))
    return ngrams


def extract_candidates(normalized_text, ward_trie, district_trie, province_trie):
    """
    For a normalized input string, generate all word and char n-grams and check for matches in each trie.
    Returns: list of candidate dicts (start, end, original_name, type, ngram, ngram_type)
    """
    word_ngrams = generate_word_ngrams(normalized_text, min_n=1, max_n=5)
    char_ngrams = generate_char_ngrams(normalized_text, min_n=5, max_n=20)
    ngrams = [*word_ngrams, *char_ngrams]
    candidates = []
    for start, end, ngram, ngram_type in ngrams:
        norm_ngram = ngram
        for trie, typ in [
            (ward_trie, 'ward'),
            (district_trie, 'district'),
            (province_trie, 'province')
        ]:
            matches = trie.search(norm_ngram)
            if not matches:
                continue
            if not matches:
                matches = trie.fuzzy_search(norm_ngram)
            for match in matches:
                candidates.append({
                    'type': typ,
                    'start': start,
                    'end': end,
                    'original': match,
                    'ngram': ngram,
                    'ngram_type': ngram_type
                })
    return candidates

# Example usage
if __name__ == "__main__":
    from trie import Trie
    ward_trie = Trie(); district_trie = Trie(); province_trie = Trie()
    ward_trie.insert("thuan thanh", "Thuận Thành")
    district_trie.insert("can giuoc", "Cần Giuộc")
    province_trie.insert("long an", "Long An")

    normalized = "x thuan thanh hcan giuoc tlong an"
    candidates = extract_candidates(normalized, ward_trie, district_trie, province_trie)
    for c in candidates:
        print(c) 