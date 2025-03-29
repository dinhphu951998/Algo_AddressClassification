from SearchAnalyzer.Segment import segment_text
from SearchEngine.Autocorrect import autocorrect


class Searcher:
    def __init__(self, raw_text, possible_provinces, possible_districts, possible_wards, province_trie, district_trie, ward_trie):
        self.raw_text = raw_text
        self.possible_provinces = possible_provinces
        self.possible_districts = possible_districts
        self.possible_wards = possible_wards
        self.province_trie = province_trie
        self.district_trie = district_trie
        self.ward_trie = ward_trie
        self.n = len(possible_provinces)

    def process(self):
        segments = segment_text(self.raw_text)
        j, province = self.search_part_reversed(self.possible_provinces, self.province_trie)

        if province == "":
            for seg in reversed(segments):
                _, province = autocorrect(seg, trie=self.province_trie)
                if province:
                    segments.remove(seg)
                    break

        i, ward = self.search_part(self.possible_wards, self.ward_trie)
        if ward == "":
            for seg in segments:
                _, ward = autocorrect(seg, trie=self.ward_trie)
                if ward:
                    segments.remove(seg)
                    break

        (index, district) = self.search_part(self.possible_districts, self.district_trie)
        if district == "":
            for seg in segments:
                _, district = autocorrect(seg, trie=self.district_trie)
                if district:
                    segments.remove(seg)
                    break

        return {
            "province": province,
            "district": district,
            "ward": ward
        }

    def search_part_reversed(self, possible_words, trie):
        for words_at_i in reversed(possible_words.copy()):
            if len(words_at_i) == 0:
                continue
            words_at_i.sort(key=lambda x: len(x), reverse=True)
            candidates = trie.search_for_normalized_result(words_at_i[0])
            return possible_words.index(words_at_i), candidates[0][2]
        return self.n, ""

    def search_part(self, possible_words, trie):
        for words_at_i in possible_words:
            if len(words_at_i) == 0:
                continue
            words_at_i.sort(key=lambda x: len(x), reverse=True)
            candidates = trie.search_for_normalized_result(words_at_i[0])
            return possible_words.index(words_at_i), candidates[0][2]
        return 0, ""

    def search_part_range(self, possible_words, trie, i, j):
        if i + 1 > j - 1:
            return ""
        for index in range(i + 1, j - 1):
            words_at_i = possible_words[index]
            if len(words_at_i) == 0:
                continue
            words_at_i.sort(key=lambda x: len(x), reverse=True)
            candidates = trie.search_for_normalized_result(words_at_i[0])
            return candidates[0][2]
        return ""

        # while i >= 0:
            # words_at_i = possible_words[i]
            # if len(words_at_i) == 0:
            #     i -= 1
            #     continue
            #
            # words_at_i.sort(key=lambda x: len(x), reverse=True)
            # candidates = trie.search_for_normalized_result(words_at_i[0])
            # return i - len(words_at_i[0]) + 1, candidates[0][2]
        # return 0, ""


