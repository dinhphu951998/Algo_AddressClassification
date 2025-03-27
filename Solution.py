from IndexAnalyzer.IndexAnalyzer import Trie, build_trie
import time
from SearchAnalyzer.SearchAnalyzer import SearchAnalyzer
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
        print(f"Search took {elapsed:.6f} seconds.")

        pass

    def process(self, str):
        # Search Analyzer
        str = normalize_text(str)
        print("Original: ", str)

        # find matching words
        search_analyzer = SearchAnalyzer()
        possible_provinces = search_analyzer.find_matching_words(str, self.trie_province)
        possible_districts = search_analyzer.find_matching_words(str, self.trie_district)
        possible_wards = search_analyzer.find_matching_words(str, self.trie_ward)

        # find best candidates
        searcher = Searcher(possible_provinces, possible_districts, possible_wards, self.trie_province, self.trie_district, self.trie_ward)
        result = searcher.process()

        # print("Possible provinces: ", possible_provinces)
        # print("Possible districts: ", possible_districts)
        # print("Possible wards: ", possible_wards)
        # print("Result: ", result)

        print()

        return result

# Test
runner = Solution()
runner.process("284DBis Ng Văn Giáo, P3, Mỹ Tho, T.Giang.")
runner.process("Tiểu khu 3, thị trấn Ba Hàng, huyện Phổ Yên, tỉnh Thái Nguyên.")
# runner.process("357/28,Ng-T- Thuật,P1,Q3,TP.HồChíMinh.")
# runner.process("Khu phố 4 Thị trấn, Dương Minh Châu, Tây Ninh")
# runner.process("A:12A.21BlockA C/c BCA,P.AnKhánh,TP.Thủ Đức, TP. HCM")
# runner.process("Hải Ba  Hải Lăng ")
