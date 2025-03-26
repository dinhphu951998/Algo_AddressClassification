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
        n = len(self.possible_provinces)
        final_province = ""
        final_district = ""
        final_ward = ""
        i = n - 1
        while i >= 0:
            provinces_at_i = self.possible_provinces[i]
            districts_at_i = self.possible_districts[i]
            wards_at_i = self.possible_wards[i]

            pro_calculator = self.search(provinces_at_i, self.province_trie)
            dis_calculator = self.search(districts_at_i, self.district_trie)
            wa_calculator = self.search(wards_at_i, self.ward_trie)

            length = 0
            if final_province is "" and pro_calculator["distance"] == min(pro_calculator["distance"], dis_calculator["distance"], wa_calculator["distance"]):
                final_province = pro_calculator["best_candidate"]
                length = len(pro_calculator["key"])
            elif final_district is "" and dis_calculator["distance"] == min(pro_calculator["distance"], dis_calculator["distance"], wa_calculator["distance"]):
                final_district = dis_calculator["best_candidate"]
                length = len(dis_calculator["key"])
            elif final_ward is "" and wa_calculator["distance"] == min(pro_calculator["distance"], dis_calculator["distance"], wa_calculator["distance"]):
                final_ward = wa_calculator["best_candidate"]
                length = len(wa_calculator["key"])

            if final_province != "" and final_district != "" and final_ward != "":
                break

            i = i - max(length, 2) + 1

        return {
            "province": final_province,
            "district": final_district,
            "ward": final_ward
        }


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

