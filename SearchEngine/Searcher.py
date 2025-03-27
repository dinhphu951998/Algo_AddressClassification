
class Searcher:
    def __init__(self, possible_provinces, possible_districts, possible_wards, province_trie, district_trie, ward_trie):
        self.possible_provinces = possible_provinces
        self.possible_districts = possible_districts
        self.possible_wards = possible_wards
        self.province_trie = province_trie
        self.district_trie = district_trie
        self.ward_trie = ward_trie

    def process(self):
        n = len(self.possible_provinces)

        district = ""
        ward = ""

        next_index, province = self.search_part(self.possible_provinces, self.province_trie, n - 1)

        if province:
            next_index, district = self.search_part(self.possible_districts, self.district_trie, next_index)

        if district:
            next_index, ward = self.search_part(self.possible_wards, self.ward_trie, next_index)

        return {
            "province": province,
            "district": district,
            "ward": ward
        }


    def search_part(self, possible_words, trie, i):
        while i >= 0:
            words_at_i = possible_words[i]
            if len(words_at_i) == 0:
                i -= 1
                continue

            words_at_i.sort(key=lambda x: len(x), reverse=True)
            candidates = trie.search_for_normalized_result(words_at_i[0])
            return i - len(words_at_i[0]) + 1, candidates[0][2]
        return 0, ""


