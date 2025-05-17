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

def normalize_text_v2(text: str) -> str:
    # Bước 1: Chuyển về chữ thường
    text = text.lower()
    
    # Bước 2: Chuẩn hóa các từ viết tắt
    tokens = re.findall(r'\w+|[.,;:/\\\-]', text, re.UNICODE)
    new_tokens = []
    for token in tokens:
        token_lower = token.lower().strip('.')
        if token_lower in TOKEN_ABBREVIATIONS:
            new_tokens.append(TOKEN_ABBREVIATIONS[token_lower])
        else:
            new_tokens.append(token)
    text = ' '.join(new_tokens)
    
    # Bước 3: Bỏ dấu tiếng Việt
    text = unicodedata.normalize('NFD', text)
    text = ''.join([c for c in text if unicodedata.category(c) != 'Mn'])
    
    # Bước 4: Thay thế dấu câu bằng khoảng trắng
    text = re.sub(r'[.,;:/\\\-]', ' ', text)
    
    # Bước 5: Chuẩn hóa khoảng trắng
    text = re.sub(r'\s+', ' ', text).strip()
    
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
