from IndexAnalyzer import load_databases, variation_map
from Searcher import search_locations_in_trie, search_locations_in_segments, search_by_character
from Utils import normalize_text_but_keep_vietnamese_alphabet, normalize_text_but_keep_accent, \
    normalize_text_and_remove_accent, segment_text
import json
import re

class Solution:

    debug=False

    def __init__(self):
        # list provice, district, ward for private test, do not change for any reason (these file will be provided later with this exact name)

        self.province_path = 'list_province.txt'
        self.district_path = 'list_district.txt'
        self.ward_path = 'list_ward.txt'

        self.tries = {}
        self.reversed_tries = {}
        load_databases({
            "province": self.province_path,
            "district": self.district_path,
            "ward": self.ward_path
        }, self.tries, self.reversed_tries)

        self.variation_map = variation_map
        pass

    # def is_result_ok(self, input_text: str, result: dict, expected_data: list):
    #     for expected in expected_data:
    #         if input_text == expected.get("text"):
    #             expected_result = expected.get("result")
    #             raw_result = {
    #                 "province": self.tries["province"].get_raw_text(result["province"]),
    #                 "district": self.tries["district"].get_raw_text(result["district"]),
    #                 "ward": self.tries["ward"].get_raw_text(result["ward"]),
    #             }
    #             differences = {}
    #             for key in ["province", "district", "ward"]:
    #                 if raw_result.get(key) != expected_result.get(key):
    #                     differences[key] = raw_result.get(key)
    #             if not differences:
    #                 # if self.debug:
    #                 #     print("Kết quả đã khớp với expected result.")
    #                 return True, raw_result
    #             else:
    #                 # if self.debug:
    #                 #     print("Có sai lệch so với expected result. Sai lệch:", differences)
    #                 return None, differences
    #     return None, None

    def is_result_ok(self, result: dict):
        # Tạo ra raw_result từ result
        raw_result = {
            "province": self.tries["province"].get_raw_text(result["province"]),
            "district": self.tries["district"].get_raw_text(result["district"]),
            "ward": self.tries["ward"].get_raw_text(result["ward"]),
        }

        # Kiểm tra nếu tất cả các giá trị khác rỗng
        if all(raw_result[key] for key in ["province", "district", "ward"]):
            # Trả về True và raw_result nếu tất cả đều có dữ liệu
            return True, raw_result
        else:
            # Lọc ra các key có value rỗng để báo lỗi
            empty_keys = {k: v for k, v in raw_result.items() if not v}
            return None, empty_keys

    def process(self, s: str):
        # Preprocess
        s_copy = s[:]

        raw_data = None
        try:
            with open("public.json", "r", encoding="utf-8") as f:
                raw_data = json.load(f)
        except Exception as e:
            if self.debug:
                print("Không load được expected result:", e)
        
        segments = segment_text(s)
        input_text = normalize_text_but_keep_accent(",".join(segments))
        parts = input_text.split(',')
        if len(parts) >= 4:
            # Remove the first part and merge the remaining parts back
            text = ','.join(parts[1:])
            # print(text)
        # Start searching
        results = {"ward": "", "district": "", "province": ""}
        # print(input_text)
        # Search with accents
        result, remaining_text = search_locations_in_trie(self.tries, input_text, results)
        # check, check_result = self.is_result_ok(s_copy, result, raw_data)
        # if check is not None:
        #     return check_result
        # If the province/district/ward not found, search without accents
        # remaining_text = normalize_text_and_remove_accent(remaining_text)
        # result, remaining_text = search_locations_in_trie(self.tries, remaining_text, results)

        # If the province/district/ward not found, search by segments
        text = re.sub(r',+', ',', remaining_text)
        segments = segment_text(remaining_text, False)
        segments_copy = segments.copy()
        result, remaining_text = search_locations_in_segments(self.tries, segments, results)
        check, check_result = self.is_result_ok(result)
        if check is not None:
            return check_result

        result = search_by_character(self.reversed_tries, result, check_result, segments_copy)

        result =  {
            "province": self.tries["province"].get_raw_text(result["province"]),
            "district": self.tries["district"].get_raw_text(result["district"]),
            "ward": self.tries["ward"].get_raw_text(result["ward"]),
        }

        if self.debug:
            print()
            print(f"Original: {s_copy}")
            print(f"Normalized: {normalize_text_but_keep_accent(s_copy)}")
            print(f"Result: {result}")

        return result

runner = Solution()
runner.debug = True

runner.process("XThạnh Đức, HGò Dầ6u, T Tây Ninh")


# Not able to solve yet
# runner.process(" T.P Phan Rang-Tháp lhàm  Ninh Thuận")
# runner.process("Điên Hải, Đông Hải, T bạc Liêu")