import re

import unicodedata

SPECIAL_CASES = [
                "TP.", "T.P", "F.", "Thành phố", "ThànhPhố", "TP ", " TP",
               "Tỉnh", "Tỉn", #" T ", ",T ", "T.",
               #"Quận", "Q.", " Q ", ",Q ",
               "Huyện", "hyện", #"H.", " H ", ",H ",
               "Phường", "F", # "P.", " P ", ",P ",
               "Thị xã", "ThịXã", "Xã", # "X.", " X ", "X ", ",X ",
                "Thị trấn", "ThịTrấn", #"T.T",
                "khu phố", "KP", "KhuPhố", "Khu pho", "KhuPho",
               ]

vietnamese_dict = {
        "a": "áàạảã",
        "â": "ấầậẩẫ",
        "ă": "ắằặẳẵ",

        "e": "éèẹẻẽ",
        "ê": "ếềệểễ",

        "o": "óòọỏõ",
        "ô": "ôốồộổỗ",
        "ơ": "ớờợởỡ",

        "u": "úùụủũ",
        "ư": "ứừựửữ",
        "i": "íìịỉĩ",
        "y": "ýỳỵỷỹ",
    }

reversed_vietnamese_dict = {}

def normalize_text(text: str) -> str:
    """Normalize text by removing accents, spaces, and special cases."""
    for case in SPECIAL_CASES:
        text = re.sub(re.escape(case), ',', text, flags=re.IGNORECASE)

    text = text.replace(",", "")
    text = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in text if not unicodedata.combining(c))  # Remove accents
    text = re.sub(r"\s+", "", text)  # Remove spaces
    return text.lower()

def normalize_text_but_keep_vietnamese_alphabet(text: str) -> str:
    """Normalize text by removing accents, spaces, and special cases."""
    for case in SPECIAL_CASES:
        text = re.sub(re.escape(case), ',', text, flags=re.IGNORECASE)

    text = text.lower()
    text = text.replace(",", "") # replace for "T,â,n,B,ì,n,h Dĩ An Bình Dương
    # text = "".join(c for c in text if not unicodedata.combining(c))  # Remove accents

    for base_char, variations in vietnamese_dict.items():
        for char in variations:
            reversed_vietnamese_dict[char] = base_char

    result = []
    for char in text:
        if char in reversed_vietnamese_dict:
            result.append(reversed_vietnamese_dict[char])
        else:
            result.append(char)

    text = "".join(result)
    text = unicodedata.normalize("NFKC", text)
    text = re.sub(r"\s+", "", text)  # Remove spaces

    return text



print(normalize_text_but_keep_vietnamese_alphabet("Phố Đức Sơn, TT Bút Sơn, Hoằng Hoá, Thanh Hoá."))