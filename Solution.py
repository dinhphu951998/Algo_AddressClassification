from CursorSolution.address_candidate_extraction import extract_candidates
from CursorSolution.address_selection import select_best_combination
from IndexAnalyzer import load_databases, variation_map
from Searcher import search_locations_in_trie, search_locations_in_segments
from Utils import normalize_text_v2, normalize_text_but_keep_accent, segment_text

class Solution:

    debug = False

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
        input_text = normalize_text_v2(",".join(segments))

        # Start searching
        candidates = extract_candidates(input_text, self.tries["ward"], self.tries["district"], self.tries["province"])

        best = select_best_combination(candidates)
        
        result =  {
            "province": best['province'],
            "district": best['district'],
            "ward": best['ward'],
        }

        if self.debug:
            print()
            # print(f"Original: {s_copy}")
            # print(f"Normalized: {normalize_text_but_keep_accent(s_copy)}")
            print(f"Result: {result}")

        return result

    # def process(self, s: str):
    #     # Preprocess
    #     s_copy = s[:]

    #     segments = segment_text(s)
    #     input_text = normalize_text_but_keep_accent(",".join(segments))

    #     # Start searching
    #     results = {"ward": "", "district": "", "province": ""}

    #     # Search with accents
    #     result, remaining_text = search_locations_in_trie(self.tries, input_text, results)

    #     segments = segment_text(remaining_text, False)
    #     result, remaining_text = search_locations_in_segments(self.tries, segments, results)

    #     result =  {
    #         "province": self.tries["province"].get_raw_text(result["province"]),
    #         "district": self.tries["district"].get_raw_text(result["district"]),
    #         "ward": self.tries["ward"].get_raw_text(result["ward"]),
    #     }

    #     if self.debug:
    #         print()
    #         print(f"Original: {s_copy}")
    #         print(f"Normalized: {normalize_text_but_keep_accent(s_copy)}")
    #         print(f"Result: {result}")

    #     return result
