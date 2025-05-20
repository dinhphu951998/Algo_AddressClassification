from ContextualFiltering import ContextualFiltering
from CursorSolution.address_candidate_extraction import extract_candidates
from CursorSolution.address_selection import select_best_combination, select_best_combination_dp
from IndexAnalyzer import load_databases
from Utils import normalize_text_v2
import time
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

        self.contextual_filter = ContextualFiltering()
        self.contextual_filter.load_context('contextual_filtering_dataset.json')

        self.total_extract_time = 0
        self.total_select_time = 0
        self.process_count = 0
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
        self.process_count += 1

        # Preprocess
        s_copy = s[:]
        input_text = normalize_text_v2(s)
        
        start_time = time.time()
        candidates, total_fuzzy_search_time, total_fuzzy_search_count = extract_candidates(input_text, self.tries["ward"], self.tries["district"], self.tries["province"])
        extract_time = time.time() - start_time
        self.total_extract_time += extract_time

        start_time = time.time()
        best = select_best_combination(candidates, self.contextual_filter)
        select_time = time.time() - start_time
        self.total_select_time += select_time

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
            # print(best)
            print(f"Extract time: {extract_time:.4f}s")
            print(f"    Fuzzy search (fuzzy/extract): {total_fuzzy_search_time/extract_time:.4f}")
            print(f"Select time: {select_time:.4f}s")
            print("--------------------------------")

        return result
    

if __name__ == "__main__":
    s = Solution()
    s.debug = 1
    # print(s.process("P. Nghi Hương Thị xã Cửa Lò, Nghệ An"))
    # print(s.process("7/3/4/16 Thành Thái Phường 14, Quận 10, TP. Hồ Chí Minh"))
    # print(s.process("Khu 3 Suối Hoa, Thành phố Bắc Ninh, Bắc Ninh"))
    # print(s.process("CH F1614-HH2-Khu ĐTM Dương Nội Yên NghĩahàdônghyàNội"))
    # print(s.process("TT T,â,n B,ì,n,h Huyện Yên Sơn, Tuyên Quang"))
    print(s.process("X. Sơn Hv HSơn Hoa Tỉnh Phú Yên"))

    # exit()


    # s.process("Khu phố 3, Trảng Dài, Thành phố Biên Hòa, Đồng Nai.")
    # s.process("357/28,Ng-T- Thuật,P1,Q3,TP.HồChíMinh.")
    # s.process("284DBis Ng Văn Giáo, P3, Mỹ Tho, T.Giang.")
    # s.process("TT T,â,n B,ì,n,h Huyện Yên Sơn, Tuyên Quang")

    # s.process("46/8F Trung Chánh 2 Trung Chánh, Hóc Môn, TP. Hồ Chí Minh")
    # s.process("T18,Cẩm Bình, Cẩm Phả, Quảng Ninh")
    # s.process("Thanh Long, Yên Mỹ Hưng Yên")
    # s.process("D2, Thạnh Lợi, Vĩnh Thạnh Cần Thơ")
    # s.process("Cổ Lũy Hải Ba, Hải Lăng, Quảng Trị")
    # s.process("Phú Lộc Phú Thạnh, Phú Tân, An Giang")
    # s.process("Nguyễn Khuyến Thị trấn Vĩnh Trụ, Lý Nhân, Hà Nam")
    # s.process("Nam chính Tiền hải, Thái bình")
    # s.process("Đá Hàng Hiệp Thạnh, Gò Dầu, Tây Ninh")
    # s.process("371/11 Thoại Ngọc Hầu Hiệp Tân, Tân Phú, TP. Hồ Chí Minh")
    # s.process("Số 93, khu phố 9, thị trấn Hai Riêng, Sông Hinh, Phú Yên")
    # s.process("Tổ Dân Phố 3 Thị trấn Chư Prông, Chư Prông, Gia Lai")
    # s.process("Xã Minh Đạo, Huyện Tiên Du, Tỉnh Bắc Ninh")
    # s.process("Xã Bồng Khê Huyện Con Cuông, Nghệ An")
    # s.process("Thôn 16 Cư Prông, Ea Kar, Đắk Lắk")
    # s.process("Số 259/54/8, Tổ 28, KP1, Long Bình Tân, Biên Hòa, Đồng Nai.")
    # s.process("Pháp Ngỡ, Vĩnh Hòa Vĩnh Lộc, Thanh Hóa")
    # s.process("Thôn Chua Bình Minh, Thanh Oai, Hà Nội")
    # s.process("Tiểu khu 3, thị trấn Ba Hàng, huyện Phổ Yên, tỉnh Thái Nguyên")
    # s.process("Xóm 2, Hưng Mỹ, Hưng Nguyên, Nghệ An")
    # s.process("Bương Hạ Nam, Quỳnh Ngọc Quỳnh Phụ, Thái Bình")
    # s.process("Nậm Cha Sìn Hổ, Lai Châu")
    # s.process("TDP Hạ 10, Tây Tựu Bắc Từ Liêm, Hà Nội")
    # s.process("P. Nghi Hương Thị xã Cửa Lò, Nghệ An")
    # s.process("Hoằng Anh Thành phố Thanh Hóa, Thanh Hóa")
    # s.process("Ấp Phú Hữu Hữu Định, Châu Thành, Bến Tre")
    # s.process("Phường Yên Thanh, thành phố Uông Bí, tỉnh Quảng Ninh")
    # s.process("Khóm 1 TT Càng Long, Càng Long, Trà Vinh")
    # s.process("Khu 3, Tân Bình, Hồ Chí Minh")
    # s.process("Khu 1, Tân Bình, Hồ Chí Minh")
    # s.process("Khu 1, Tân Bình, Hồ Chí Minh")
    # s.process("Khóm 1 TT Càng Long, Càng Long, Trà Vinh")
    # s.process("Số Nhà 38, Tổ 9 Tô Hiệu, Thành phố Sơn La, Sơn La")
    # s.process("Khu 3 Suối Hoa, Thành phố Bắc Ninh, Bắc Ninh")


    # print(f"Average extract time: {s.total_extract_time / s.process_count:.4f}s")
    # print(f"Average select time: {s.total_select_time / s.process_count:.4f}s")
    # print(f"Average process time: {(s.total_extract_time + s.total_select_time) / s.process_count:.4f}s")


    # Not solved yet
    # print(s.process("CH F1614-HH2-Khu ĐTM Dương Nội Yên NghĩahàdônghyàNội"))




