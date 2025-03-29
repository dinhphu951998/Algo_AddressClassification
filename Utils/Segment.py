import re


def segment_text(s):
    text = s[:]

    prefix = [ "TP.", "T.P", "F.", "Thành phố", "ThànhPhố", "TP ", " TP",
               "Tỉnh", "Tỉn","T.", " T ", ",T ",
               "Quận", "Q.", " Q ", ",Q ",
               "Huyện", "hyện", "H.", " H ", ",H ",
               "Phường", "P.", "F", " P ", ",P ",
               "X.", "Thị xã", "ThịXã", "Xã", " X ", "X ", ",X ",
                "Thị trấn", "ThịTrấn", "T.T"
               "-"
    ]
    for p in prefix:
        text = re.sub(re.escape(p), ',', text, flags=re.IGNORECASE)

    # Xử lý dấu "-" trong tên (ví dụ: "Ng-T-" -> "Ng T ")
    text = re.sub(r'[.\-]', ' ', text)

    # Tách cụm địa chỉ
    segments = [seg.strip() for seg in text.split(',') if seg.strip()]
    #
    # print()
    print(f"'{s}'  -->  {segments}")
    return segments

