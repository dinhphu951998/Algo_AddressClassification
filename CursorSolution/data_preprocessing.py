import re
import unicodedata

# Vietnamese common abbreviations mapping (token form)
TOKEN_ABBREVIATIONS = {
    'tp': 'thành phố',
    'q': 'quận',
    'h': 'huyện', 
    't': 'tỉnh',
    'p': 'phường',
    'x': 'xã',
    'tx': 'thị xã',
    'tt': 'thị trấn',
    'đt': 'đường',
    'f': 'phường',
    'kdc': 'khu dân cư',
    'kcn': 'khu công nghiệp',
    'kdt': 'khu đô thị',
    'kp': 'khu phố',
}

def remove_diacritics(text):
    """Remove Vietnamese diacritics from text."""
    text = unicodedata.normalize('NFD', text)
    text = ''.join([c for c in text if unicodedata.category(c) != 'Mn'])
    return text


def standardize_abbreviations_tokens(text):
    """
    Expand common Vietnamese address abbreviations using token-based replacement.
    Only tokens that match known abbreviations are expanded, reducing over-replacement.
    """
    # Split by word boundaries, keep punctuation as separate tokens
    tokens = re.findall(r'\w+|[.,;:/\\\-]', text, re.UNICODE)
    new_tokens = []
    for token in tokens:
        token_lower = token.lower().strip('.')
        if token_lower in TOKEN_ABBREVIATIONS:
            new_tokens.append(TOKEN_ABBREVIATIONS[token_lower])
        else:
            new_tokens.append(token)
    return ' '.join(new_tokens)


def normalize_text(text):
    """
    Normalize Vietnamese address string:
    - Lowercase
    - Standardize abbreviations (token-based)
    - Remove diacritics
    - Remove extra spaces and punctuation
    Note: Do NOT perform typo correction here. Fuzzy matching should be done during the address matching step.
    """
    text = text.lower()
    text = standardize_abbreviations_tokens(text)
    text = remove_diacritics(text)
    # Replace punctuation with space
    text = re.sub(r'[.,;:/\\\-]', ' ', text)
    # Remove extra spaces
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# Example usage
if __name__ == "__main__":
    samples = [
        "X. Thuận Thành, H. Cần Giuộc, T. Long An",
        "T.huận Thành, H. Cần Giuộc, T. Long An",
        "TX. Mỹ Tho, T. Tiền Giang",
        "P. 1, Q. 3, TP. Hồ Chí Minh"
    ]
    for sample in samples:
        print("Original:", sample)
        print("Normalized:", normalize_text(sample))
        print()
