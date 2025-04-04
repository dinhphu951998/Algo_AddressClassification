import re
from gettext import textdomain

import unicodedata
from numpy import character

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


def two_grams(segments):
    if not segments:
        return []

    result = []
    n = len(segments)
    for i in range(n):
        for j in range(i + 1, n):
            result.append(segments[i] + segments[j])
    return result

def best_candidate_by_distance(search_key, candidates):
    best_distance = float('inf')
    best_candidate = None
    best_reference = None  # Giờ đây chỉ lưu một chuỗi hoặc None

    for candidate, reference in candidates:
        d = levenshtein_distance(candidate, search_key)
        if d < best_distance:
            best_distance = d
            best_candidate = candidate
            best_reference = reference
        elif d == best_distance:
            # Nếu có nhiều candidate với cùng khoảng cách, bạn có thể quyết định cách chọn:
            # Ví dụ, nếu best_reference khác candidate hiện tại, bạn có thể lưu cả hai trong một tập hợp
            if best_reference is None:
                best_reference = reference
            elif best_reference != reference:
                # Nếu cần lưu tất cả, bạn có thể chuyển thành tập hợp
                if isinstance(best_reference, set):
                    best_reference.add(reference)
                else:
                    best_reference = {best_reference, reference}
    return best_candidate, best_reference, best_distance


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


# print(normalize_text_but_keep_accent("T18,Cẩm Bình, Cẩm Phả, Quảng Ninh"))
# print(normalize_text_but_keep_vietnamese("Thôn Đồng Lực Hoàng Lâu, Tam Dương, Vĩnh Phúc"))
# print(normalize_text_but_keep_vietnamese("Tam Đường, Tam Đường, Lai Châu"))

