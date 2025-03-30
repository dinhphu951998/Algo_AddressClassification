import re
from gettext import textdomain

import unicodedata
from numpy import character

SAFE_CASES = [
                #"TP.", "T.P", "F.", "Thành phố", "ThànhPhố", "TP ", " TP",
               "Tỉnh", " T ", #"Tỉn",  ",T ", "T.",
               #"Quận", "Q.", " Q ", ",Q ", -> quận 5 sau khi remove sẽ thành 5 và không tìm ra
               "Huyện", "hyện", #"H.", " H ", ",H ",
               # "Phường", "F",  "P.", " P ", ",P ",
               "Thị xã", "ThịXã", "Xã", # "X.", " X ", "X ", ",X ",
                "Thị trấn", "ThịTrấn", #"T.T",
                "khu phố", "KP", "KhuPhố", "Khu pho", "KhuPho", # -> KP5 bị nhầm thành P5
               ]

ALL_PREFIXES = ["TP.", "T.P", "F.", "Thành phố", "ThànhPhố", "TP ", " TP",
               "Tỉnh", "Tỉn","T.", " T ",  #",T ",
               "Quận", "Q.", " Q ", ",Q ",
               "Huyện", "hyện", "H.", " H ",  #",H ",
               "khu phố", "KP", "KhuPhố", "Khu pho", "KhuPho",  # KP. contains P.
               "Phường", "P.", "F", " P ",  #",P ",
               "X.", "Thị xã", "ThịXã", "Xã",  #" X ", "X ", ",X ",
                "Thị trấn", "ThịTrấn", "T.T",
               "-"
                ]

vietnamese_dict = {
    "a": ["à", "á", "ạ", "ả", "ã", "â", "ầ", "ấ", "ậ", "ẩ", "ẫ", "ă", "ằ", "ắ", "ặ", "ẳ", "ẵ"],
    "d": ["đ"],
    "e": ["è", "é", "ẹ", "ẻ", "ẽ", "ê", "ề", "ế", "ệ", "ể", "ễ"],
    "i": ["ì", "í", "ị", "ỉ", "ĩ"],
    "o": ["ò", "ó", "ọ", "ỏ", "õ", "ô", "ồ", "ố", "ộ", "ổ", "ỗ", "ơ", "ờ", "ớ", "ợ", "ở", "ỡ"],
    "u": ["ù", "ú", "ụ", "ủ", "ũ", "ư", "ừ", "ứ", "ự", "ử", "ữ"],
    "y": ["ỳ", "ý", "ỵ", "ỷ", "ỹ"],

}

reversed_vietnamese_dict = {}

wrong_accents = {
    "oà": "òa", "oá": "óa", "oạ": "ọa", "oã": "õa", "oả": "ỏa",
    "qui": "quy",
}

def common_normalize(text: str) -> str:
    text = text.lower()
    # text = text.replace(",", "")  # replace for T,â,n,B,ì,n,h Dĩ An Bình Dương
    # text = text.replace(".", "")
    for case in SAFE_CASES:
        text = re.sub(re.escape(case), ',', text, flags=re.IGNORECASE)
    return text

def normalize_text_and_remove_accent(text: str) -> str:
    """Normalize text by removing accents, spaces, and special cases."""
    text = common_normalize(text)
    text = unicodedata.normalize("NFKD", text)
    text = text.replace("đ", "d")
    text = "".join(c for c in text if not unicodedata.combining(c))  # Remove accents
    text = re.sub(r"\s+", "", text)  # Remove spaces
    return text

def normalize_text_but_keep_vietnamese_alphabet(text: str) -> str:
    text = common_normalize(text)
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

    text = "".join(c for c in text if not unicodedata.combining(c))  # Remove accents
    text = re.sub(r"\s+", "", text)  # Remove spaces
    return text

def normalize_text_but_keep_accent(text: str) -> str:
    """Normalize text by removing accents, spaces, and special cases."""
    text = common_normalize(text)
    text = unicodedata.normalize("NFKC", text)

    for wrong, correct in wrong_accents.items():
        text = text.replace(wrong, correct)

    # text = text.replace("oà", "òa")
    text = re.sub(r"\s+", "", text)  # Remove spaces

    return text

def segment_text(s, safe=True):
    text = s[:]

    prefixes = SAFE_CASES if safe else ALL_PREFIXES

    for p in prefixes:
        text = re.sub(re.escape(p), ',', text, flags=re.IGNORECASE)

    # Xử lý dấu "-" trong tên (ví dụ: "Ng-T-" -> "Ng T ")
    text = re.sub(r'[.\-]', ' ', text)

    # Tách cụm địa chỉ
    segments = [seg.strip() for seg in text.split(',') if seg.strip()]
    #
    # print()
    # print(f"'{s}'  -->  {segments}")
    return segments


# print(normalize_text_but_keep_accent("T18,Cẩm Bình, Cẩm Phả, Quảng Ninh"))
# print(normalize_text_but_keep_vietnamese("Thôn Đồng Lực Hoàng Lâu, Tam Dương, Vĩnh Phúc"))
# print(normalize_text_but_keep_vietnamese("Tam Đường, Tam Đường, Lai Châu"))

