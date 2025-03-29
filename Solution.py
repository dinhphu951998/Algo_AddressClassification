from IndexAnalyzer.IndexAnalyzer import load_databases, variation_map, original_names
from SearchEngine.Searcher import search_locations
from Utils.Utils import normalize_text, normalize_text_but_keep_vietnamese_alphabet


class Solution:

    debug=False

    def __init__(self):
        # list provice, district, ward for private test, do not change for any reason (these file will be provided later with this exact name)

        self.province_path = 'list_province.txt'
        self.district_path = 'list_district.txt'
        self.ward_path = 'list_ward.txt'

        self.files = {
            "province": self.province_path,
            "district": self.district_path,
            "ward": self.ward_path
        }

        self.tries = load_databases(self.files)
        self.variation_map = variation_map
        self.original_names = original_names
        pass

    def process(self, s: str):
        # write your process string here
        s_copy = s[:]

        normalized_text = normalize_text_but_keep_vietnamese_alphabet(s)
        result, remaining_text = search_locations(self.tries, normalized_text)

        result =  {
            "province": original_names["province"].get(result["province"], result["province"]),
            "district": original_names["district"].get(result["district"], result["district"]),
            "ward": original_names["ward"].get(result["ward"], result["ward"])
        }

        if self.debug:
            print()
            print(f"Original: {s_copy}")
            print(f"Normalized: {normalized_text}")
            print(f"Result: {result}")
            print("Remaining Text: ", remaining_text)

        return result

# runner = Solution()
# runner.debug = True
# runner.process("489/24A/18 Huỳnh Văn Bánh Phường 13, Phú Nhuận, TP. Hồ Chí Minh")
# runner.process("Số 259/54/8, Tổ 28, KP1, Long Bình Tân, Biên Hòa, Đồng Nai.")
# runner.process("285 B/1A Bình Gĩa Phường 8,Vũng Tàu,Bà Rịa - Vũng Tàu")
# runner.process("290 Tùng Thiện- Vương,P.13, Quận 8, TP. Hồ Chí Minh.")
# runner.process("8 Trịnh Văn Cấn P.C-Ô-Lãnh, Q.1, TP. Hồ Chí Minh")
# runner.process("Khu phố Nam Tân, TT Thuận Nam, Hàm Thuận Bắc, Bình Thuận.")
# runner.process("H.Hoài ân,TBình Dịnh")
# runner.process("Mường La,  sơn La")
# runner.process("x. Văn Cẩs HuyệnHung Hà Tthái Bình")
# runner.process("Duy Phú,  Duy Xuyen,  Quang Nam")
# runner.process("X. Bản Nguyen,HuyệnLâm Thao,")
# runner.process("X.Mỹ Thạnh, HuyệnGiong Trôm, TỉnhBến Tre")
# runner.process("")