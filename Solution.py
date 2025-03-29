from IndexAnalyzer.IndexAnalyzer import Trie, build_trie
import time
from SearchAnalyzer.SearchAnalyzer import SearchAnalyzer
from SearchAnalyzer.Segment import segment_text
from SearchEngine.Searcher import Searcher
from Utils.Utils import normalize_text
from Utils.VietnameseHelper import VietnameseHelper


class Solution:
    trie_province = Trie()
    trie_district = Trie()
    trie_ward = Trie()
    helper = VietnameseHelper()

    def __init__(self):
        # list province, district, ward for private test, do not change for any reason (these file will be provided later with this exact name)
        # self.province_path = 'vietnamese-provinces-database/list_province.txt'
        # self.district_path = 'vietnamese-provinces-database/list_district.txt'
        # self.ward_path = 'vietnamese-provinces-database/list_ward.txt'

        self.province_path = 'list_province.txt'
        self.district_path = 'list_district.txt'
        self.ward_path = 'list_ward.txt'

        # Index Analyzer
        start = time.time()  # current time in seconds

        build_trie(self.province_path, self.trie_province, "province")
        build_trie(self.district_path, self.trie_district, "district")
        build_trie(self.ward_path, self.trie_ward, "ward")

        end = time.time()

        elapsed = end - start
        # print(f"Search took {elapsed:.6f} seconds.")

        pass

    def process(self, raw_text):
        # Search Analyzer
        str = normalize_text(raw_text[:])

        # find matching words
        search_analyzer = SearchAnalyzer()
        possible_provinces = search_analyzer.find_matching_words(str, self.trie_province)
        possible_districts = search_analyzer.find_matching_words(str, self.trie_district)
        possible_wards = search_analyzer.find_matching_words(str, self.trie_ward)

        # find best candidates
        searcher = Searcher(raw_text, possible_provinces, possible_districts, possible_wards, self.trie_province, self.trie_district, self.trie_ward)
        result = searcher.process()

        print("Original: ", str)
        # print("Possible provinces: ", possible_provinces)
        # print("Possible districts: ", possible_districts)
        # print("Possible wards: ", possible_wards)
        print("Result: ", result)

        print()

        return result

# Test
runner = Solution()
# runner.process("X. Trà Sơn,Huyện Trà Bồng,T.Quảng mNgãi")
# runner.process("357/28,Ng-T- Thuật,P1,Q3,TP.HồChíMinh.")
# runner.process("Khu phố 4 Thị trấn, Dương Minh Châu, Tây Ninh")
# runner.process("A:12A.21BlockA C/c BCA,P.AnKhánh,TP.Thủ Đức, TP. HCM")
# runner.process("Hải Ba  Hải Lăng ")
# runner.process("ftanbinhdian")
# runner.process("Xã Thanh Hòa, Huyện Cai Lậy, Tỉnh Tiền Giang")
runner.process(",Lệ Thủy,T quảng BìnKh")

runner.process("284DBis Ng Văn Giáo, P3, Mỹ Tho, T.Giang.")
runner.process("CH F1614-HH2-Khu ĐTM Dương Nội Yên NghĩahàdônghyàNội")
runner.process("A:12A.21BlockA C/c BCA,P.AnKhánh,TP.Thủ Đức, TP. HCM")
runner.process("14.5 Block A2, The Mansion, ĐS 7,KDC 13E,Ấp 5,PP,BC,TP.HCM")
runner.process("X. Trà Sơn,Huyện Trà Bồng,T.Quảng mNgãi")
runner.process("X.Thài Phìn Tủng, Huyện ĐồGg Van,  Hà Gxiang")
runner.process(", H Nam Trực, Nam Đị8nh")
runner.process("  Đông Giang T Quảyg Nm")
runner.process("XGia Hội,h.Văn Chấn,TỉnhYênKBái")
runner.process("X. HoDng Quỳ,,9hanh Hóa")
runner.process("FHim Lam   Điện Biê")
runner.process(" TP Biên Hòa TỉnhĐyng Nai")
runner.process("X. Trà DVưong Bắc Trà My TQuảg Nam")
runner.process(", Huyện Cẩm Thủy, T.Thanh Hóca")
runner.process(" Cộng Hòa,,TỉnhHaOi Dương")
runner.process(" Hải An  Hải Lăng TQdung trị")
runner.process("X.Chê La,,T.Hà GianZ")
runner.process("XãChiềng Mu5ng  T.stn la")
runner.process("Fmễ Trì, Nam Từ Liêm, Thành phố HN")
runner.process("F. Trần Hưng Đao,Phủ Ly,TỉnhH  Nam")
runner.process(" Chi Lăng,H Chi Lăng,Tỉnh Lạng5 Sơn")
runner.process(" Huyệntân biên T.TDy Ninh")
runner.process(" Hướng Hiệp  Đa Krông T Quảng TrZ")
runner.process("P Ea Tam T.P Buôn Ma Thuột TỉnĐắk Llk")
runner.process("X Bình Hi, , T.Quảcg Nam")
runner.process(", Đông Hòa,Tỉnh Phú yn")
runner.process("F.LoWng Binh, TpThủ Đưc, TPHCM")
runner.process("X. Hải Minh,,N5am Định")
runner.process("Bạch Lưu, H.Song Lô, Vĩnh PGhúc")
runner.process("Nghi Sơ6n, T.X. Nghi Sơn, Thhanh Hóa")
runner.process("Quách Phẩm Bắc, , Cà Mzu")
runner.process("xã Vạn Kim, HuyệnMỹ Đức, T.P HNội")
runner.process("X Phu Mãn   HN")
runner.process("X Mường Lèo H Sốp Cộp T Sơn ma")
runner.process("X. Bok Tới H Hoài Ân  Bìh Định")
runner.process("  Quỳ Châu T.NSghệ An")
runner.process(" H.Văn Giang Tỉnh Hưng Yê0")
runner.process(" eăn Tiến, Yên Lạc, vĩnh P0húc")
runner.process("X.Cẩm Hoàng,,T. Hải Dươnwg")
runner.process("Diên Thạnh,,T Khabnh Hòa")
runner.process("Đứ Lợi,H Mộ Đức,TỉnhQuản Ngãi")
runner.process("Xã Kiên Thành H Trấn Yên T.yên Bi")
runner.process(" Quận 1 T.P H.C.Minh")
runner.process(", Tân Phươc, Tin GJiang")
runner.process("XTrung Kiên,,Tỉnh Vĩnh Phuúc")
runner.process(" Thái Ha, HBa Vì, T.pHNội")
runner.process(", Nam Đông,T. T.T.H")
runner.process(",H.Hoài ân,TBình Dịnh")
runner.process("  Bắc Trà My TỉnhQuảng NaHm")
runner.process("P Thủy Châu,T.X. hươngThủy,Thừa.t.Huế")
runner.process("X.Nga Thanh hyện Nga son TỉnhThanhQ Hóa")
runner.process(",Lệ Thủy,T quảng BìnKh")
runner.process("XãCôn Lôn,H Na Hang,TỉnhC Tuyên.Quang")

