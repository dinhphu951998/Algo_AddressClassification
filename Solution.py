from IndexAnalyzer import load_databases, variation_map
from Searcher import search_locations_in_trie, search_locations_in_segments
from Utils import normalize_text_but_keep_vietnamese_alphabet, normalize_text_but_keep_accent, \
    normalize_text_and_remove_accent, segment_text


class Solution:

    debug=False

    def __init__(self):
        # list provice, district, ward for private test, do not change for any reason (these file will be provided later with this exact name)

        self.province_path = 'list_province.txt'
        self.district_path = 'list_district.txt'
        self.ward_path = 'list_ward.txt'

        self.tries = {}
        load_databases({
            "province": self.province_path,
            "district": self.district_path,
            "ward": self.ward_path
        }, self.tries)

        self.variation_map = variation_map
        pass

    def process(self, s: str):
        # Preprocess
        s_copy = s[:]

        segments = segment_text(s)
        input_text = normalize_text_but_keep_accent(",".join(segments))

        # Start searching
        results = {"ward": "", "district": "", "province": ""}

        # Search with accents
        result, remaining_text = search_locations_in_trie(self.tries, input_text, results)

        # If the province/district/ward not found, search without accents
        # remaining_text = normalize_text_and_remove_accent(remaining_text)
        # result, remaining_text = search_locations_in_trie(self.tries, remaining_text, results)

        # If the province/district/ward not found, search by segments
        segments = segment_text(remaining_text, False)
        result, remaining_text = search_locations_in_segments(self.tries, segments, results)

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

runner.process("Diên Thạnh,,T Khabnh Hòa")


# Not able to solve yet
# runner.process(" T.P Phan Rang-Tháp lhàm  Ninh Thuận")
# runner.process("Điên Hải, Đông Hải, T bạc Liêu")