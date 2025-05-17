import unicodedata
import re

# --- Normalization utilities (reuse from preprocessing) ---
def remove_diacritics(text):
    text = unicodedata.normalize('NFD', text)
    text = ''.join([c for c in text if unicodedata.category(c) != 'Mn'])
    return text

def normalize_name(text):
    text = text.lower()
    text = remove_diacritics(text)
    text = re.sub(r'[.,;:/\\\-]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# --- Dictionary construction ---
def load_and_normalize_list(filename):
    """
    Load a list of names from a file, normalize each, and return both original and normalized forms.
    Returns:
        - original_names: list of original names
        - normalized_to_original: dict mapping normalized name to list of original names
    """
    original_names = []
    normalized_to_original = {}
    with open(filename, encoding='utf-8') as f:
        for line in f:
            name = line.strip()
            if not name:
                continue
            norm = normalize_name(name)
            original_names.append(name)
            if norm not in normalized_to_original:
                normalized_to_original[norm] = []
            normalized_to_original[norm].append(name)
    return original_names, normalized_to_original

if __name__ == "__main__":
    # Example usage
    for level, fname in zip([
        'ward', 'district', 'province'],
        ['list_ward.txt', 'list_district.txt', 'list_province.txt']):
        try:
            orig, norm_map = load_and_normalize_list(fname)
            print(f"Loaded {len(orig)} {level}s from {fname}")
            print(f"Example normalized mapping: {list(norm_map.items())[:3]}")
        except FileNotFoundError:
            print(f"File {fname} not found. Please provide the dataset.") 