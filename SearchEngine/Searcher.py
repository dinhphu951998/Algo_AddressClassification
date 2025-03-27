from re import search

import editdistance

class Searcher:
    def __init__(self, possible_provinces, possible_districts, possible_wards, province_trie, district_trie, ward_trie):
        self.possible_provinces = possible_provinces
        self.possible_districts = possible_districts
        self.possible_wards = possible_wards
        self.province_trie = province_trie
        self.district_trie = district_trie
        self.ward_trie = ward_trie

    def process(self):
        final_province = self.search_part(self.possible_provinces, self.province_trie, "province")
        print(final_province)
        final_district = self.search_part(self.possible_districts, self.district_trie, "district")
        print(final_district)
        final_ward = self.search_part(self.possible_wards, self.ward_trie, "ward")
        print(final_ward)

        return {
            "province": final_province["best_candidate"],
            "district": final_district["best_candidate"],
            "ward": final_ward["best_candidate"]
        }

    part_possibilities = {
        "province": 1,
        "district": 2/3,
        "ward": 1/3
    }

    def search_part(self, possible_words, trie, type):
        result = []
        n = len(possible_words)

        for i, words_at_i in enumerate(possible_words):
            if len(words_at_i) == 0:
                continue
            calculator = self.search(words_at_i, trie)
            calculator["distance"] = calculator["distance"] * abs(i - self.part_possibilities[type] * n + 1) / n
            result.append(calculator)

        result.sort(key=lambda x: x["distance"])
        return result[0]


    def search(self, words, trie):
        words.sort(key=lambda x: len(x), reverse=True)
        all_candidates = []
        for word in words:
            candidates = trie.search_for_normalized_result(word)
            all_candidates = all_candidates + candidates
        if len(all_candidates) == 0:
            return {
                "best_candidate": "",
                "key": "",
                "distance": float("inf")
            }
        return self.find_best_candidates(words, all_candidates)

    def find_best_candidates(self, word, candidates):
        min_distance = float("inf")
        best_candidate = None
        for candidate in candidates:
            distance = editdistance.distance(word, candidate[0])
            if distance < min_distance:
                min_distance = distance
                best_candidate = candidate

        return {
            "best_candidate": best_candidate[2],
            "key": best_candidate[1],
            "distance": min_distance
        }

