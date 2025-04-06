import re
import unicodedata

SAFE_CASES = [
                "TP.", "TP","Thành phố", "ThànhPhố", # "T.P", "F.", "TP ", " TP",
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
                #"KP", # KP. contains P.
               "khu phố",  "KhuPhố", "Khu pho", "KhuPho",
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
    text = re.sub(r"\s{2,}", ",", text)  # Remove spaces
    text = text.replace(" ", "")
    return text

def normalize_text_and_remove_accent(text: str) -> str:
    """Normalize text by removing accents, spaces, and special cases."""
    text = common_normalize(text)
    text = unicodedata.normalize("NFKD", text)
    text = text.replace("đ", "d")
    text = "".join(c for c in text if not unicodedata.combining(c))  # Remove accents
    # text = re.sub(r"\s+", "", text)  # Remove spaces
    return text

def normalize_text_but_keep_accent(text: str) -> str:
    """Normalize text by removing accents, spaces, and special cases."""
    text = common_normalize(text)
    text = unicodedata.normalize("NFKC", text)

    for wrong, correct in wrong_accents.items():
        text = text.replace(wrong, correct)

    return text

def segment_text(s, safe=True):
    text = s[:]

    prefixes = SAFE_CASES if safe else ALL_PREFIXES

    for p in prefixes:
        text = re.sub(re.escape(p), ',', text, flags=re.IGNORECASE)

    # Xử lý dấu "-" trong tên (ví dụ: "Ng-T-" -> "Ng T ")
    text = re.sub(r'[.]', ' ', text)

    # Tách cụm địa chỉ
    segments = [seg.strip() for seg in text.split(',') if seg.strip()]
    #
    # print()
    # print(f"'{s}'  -->  {segments}")
    return segments
