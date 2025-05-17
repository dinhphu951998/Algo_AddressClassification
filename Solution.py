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

    def print_candidates(self, candidates):
        """Nicely print extracted address candidates."""
        if not candidates:
            print("No candidates found.")
            return
        print("Candidates:")
        for c in candidates:
            print(f"  [{c['type']}] {c['original']} (ngram: '{c['ngram']}', tokens {c['start']}-{c['end']}, {c['ngram_type']}, {c['match_type']})")

    def process(self, s: str):
        # Preprocess
        s_copy = s[:]
        input_text = normalize_text_v2(s)

        # Start searching
        candidates = extract_candidates(input_text, self.tries["ward"], self.tries["district"], self.tries["province"])

        best = select_best_combination(candidates)
        
        result =  {
            "ward": best["ward"],
            "district": best["district"],
            "province": best["province"],
        }

        if self.debug:
            print()
            print(f"Original: {s_copy}")
            print("Normalized: ", input_text)
            self.print_candidates(candidates)
            print(f"Result: {result}")

        return result
    
    
    
s = Solution()
s.debug = 0


# exit()


# print(s.process("Khu phố 3, Trảng Dài, Thành phố Biên Hòa, Đồng Nai."))
# print(s.process("357/28,Ng-T- Thuật,P1,Q3,TP.HồChíMinh."))
# print(s.process("284DBis Ng Văn Giáo, P3, Mỹ Tho, T.Giang."))
# print(s.process("TT T,â,n B,ì,n,h Huyện Yên Sơn, Tuyên Quang"))

# print(s.process("46/8F Trung Chánh 2 Trung Chánh, Hóc Môn, TP. Hồ Chí Minh"))
# print(s.process("T18,Cẩm Bình, Cẩm Phả, Quảng Ninh"))
# print(s.process("Thanh Long, Yên Mỹ Hưng Yên"))
# print(s.process("D2, Thạnh Lợi, Vĩnh Thạnh Cần Thơ"))
# print(s.process("Cổ Lũy Hải Ba, Hải Lăng, Quảng Trị"))
# print(s.process("Phú Lộc Phú Thạnh, Phú Tân, An Giang"))
# print(s.process("Nguyễn Khuyến Thị trấn Vĩnh Trụ, Lý Nhân, Hà Nam"))
# print(s.process("Nam chính Tiền hải, Thái bình"))
# print(s.process("Đá Hàng Hiệp Thạnh, Gò Dầu, Tây Ninh"))
# print(s.process("371/11 Thoại Ngọc Hầu Hiệp Tân, Tân Phú, TP. Hồ Chí Minh"))
# print(s.process("Số 93, khu phố 9, thị trấn Hai Riêng, Sông Hinh, Phú Yên"))
# print(s.process("Tổ Dân Phố 3 Thị trấn Chư Prông, Chư Prông, Gia Lai"))
# print(s.process("Xã Minh Đạo, Huyện Tiên Du, Tỉnh Bắc Ninh"))
# print(s.process("Xã Bồng Khê Huyện Con Cuông, Nghệ An"))
# print(s.process("Thôn 16 Cư Prông, Ea Kar, Đắk Lắk"))
# print(s.process("Số 259/54/8, Tổ 28, KP1, Long Bình Tân, Biên Hòa, Đồng Nai."))
# print(s.process("Pháp Ngỡ, Vĩnh Hòa Vĩnh Lộc, Thanh Hóa"))
# print(s.process("Thôn Chua Bình Minh, Thanh Oai, Hà Nội"))

# print(s.process("Tiểu khu 3, thị trấn Ba Hàng, huyện Phổ Yên, tỉnh Thái Nguyên"))
# print(s.process("Xóm 2, Hưng Mỹ, Hưng Nguyên, Nghệ An"))
# print(s.process("Bương Hạ Nam, Quỳnh Ngọc Quỳnh Phụ, Thái Bình"))
# print(s.process("Nậm Cha Sìn Hổ, Lai Châu"))
# print(s.process("TDP Hạ 10, Tây Tựu Bắc Từ Liêm, Hà Nội"))
# print(s.process("P. Nghi Hương Thị xã Cửa Lò, Nghệ An"))
# print(s.process("Hoằng Anh Thành phố Thanh Hóa, Thanh Hóa"))
# print(s.process("Ấp Phú Hữu Hữu Định, Châu Thành, Bến Tre"))
# print(s.process("Phường Yên Thanh, thành phố Uông Bí, tỉnh Quảng Ninh"))
# print(s.process("Khóm 1 TT Càng Long, Càng Long, Trà Vinh"))
# print(s.process("Khu 3, Tân Bình, Hồ Chí Minh"))
# print(s.process("Khu 1, Tân Bình, Hồ Chí Minh"))
# print(s.process("Khu 1, Tân Bình, Hồ Chí Minh"))
# print(s.process("Khóm 1 TT Càng Long, Càng Long, Trà Vinh"))


# Not solved yet
# print(s.process("Khu 3 Suối Hoa, Thành phố Bắc Ninh, Bắc Ninh"))



