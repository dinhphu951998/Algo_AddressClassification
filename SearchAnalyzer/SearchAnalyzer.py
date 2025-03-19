from VietnameseHelper import VietnameseHelper


class SearchAnalyzer:
    def __init__(self):
        pass

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False

    # add a word to the trie
    def add_word(self, word):
        node = self
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True

    # search a word in the trie
    def search_word(self, word):
        node = self
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end

class Trie:
    def __init__(self):
        self.root = TrieNode()

    # add a word to the trie
    def add_word(self, word):
        self.root.add_word(word)

    # search a word in the trie
    def search_word(self, word):
        return self.root.search_word(word)

    def split_words(self, str):
        n = len(str)
        words = [[]] * (n + 1)
        for i in range(n):
            node = self.root
            for j in range(i, n):
                c = str[j]
                if c not in node.children:
                    break
                node = node.children[c]
                if node.is_end and len(words[j + 1]) == 0:
                    words[j + 1] = words[i] + [str[i:j + 1]]

        return [item for possible_words in words for item in possible_words]

ward_trie = Trie()
ward_trie.add_word("3")
ward_trie.add_word("p3")
ward_trie.add_word("p1")
ward_trie.add_word("1")
ward_trie.add_word("an khanh")
ward_trie.add_word("an")
ward_trie.add_word("khanh")

province_trie = Trie()
province_trie.add_word("tien giang")
province_trie.add_word("tien")
province_trie.add_word("giang")
province_trie.add_word("tgiang")
province_trie.add_word("tay ninh")
province_trie.add_word("tay")
province_trie.add_word("ninh")
province_trie.add_word("ho chi minh")
province_trie.add_word("ho chi")
province_trie.add_word("chi minh")
province_trie.add_word("ho")
province_trie.add_word("chi")
province_trie.add_word("minh")
province_trie.add_word("hcm")

district_trie = Trie()
district_trie.add_word("thu duc")
district_trie.add_word("thu")
district_trie.add_word("duc")
district_trie.add_word("my tho")
district_trie.add_word("my")
district_trie.add_word("tho")
district_trie.add_word("duong minh chau")
district_trie.add_word("duong minh")
district_trie.add_word("minh chau")
district_trie.add_word("duong")
district_trie.add_word("minh")
district_trie.add_word("chau")
district_trie.add_word("q3")
district_trie.add_word("3")

helper = VietnameseHelper()

def test(str):
    print("original: " + str)
    str = str.lower()
    str = helper.remove_vietnamese_signs(str).lower()
    str = helper.remove_special_characters(str)
    print("preprocessed: " + str)
    print("province: ")
    print(province_trie.split_words(str))
    print("district: ")
    print(district_trie.split_words(str))
    print("ward: ")
    print(ward_trie.split_words(str))
    print()

print()
test("284DBis Ng Văn Giáo, P3, Mỹ Tho, T.Giang.")
test("357/28,Ng-T- Thuật,P1,Q3,TP.HồChíMinh.")
test("Khu phố 4 Thị trấn, Dương Minh Châu, Tây Ninh")
test("A:12A.21BlockA C/c BCA,P.AnKhánh,TP.Thủ Đức, TP. HCM")

# original: 284DBis Ng Văn Giáo, P3, Mỹ Tho, T.Giang.
# preprocessed: 284dbis ng van giao p3 my tho tgiang
# province:
# ['ho', 'tgiang'] => Match whole words with max length
# district:
# ['3', 'my', 'my tho']
# ward:
# ['an', 'p3', 'an'] => Create trie should contain concate to contain p3

# original: 357/28,Ng-T- Thuật,P1,Q3,TP.HồChíMinh.
# preprocessed: 35728ngt thuatp1q3tphochiminh
# province:
# ['ho', 'ho', 'chi', 'ho', 'chi', 'minh'] => if not match whole words, n-gram should match whole words
# district:
# ['3', 'thu', 'q3', 'minh'] => Create trie should contain q3
# ward:
# ['3', 'p1', '3'] => Match whole words with max length

# original: Khu phố 4 Thị trấn, Dương Minh Châu, Tây Ninh
# preprocessed: khu pho 4 thi tran duong minh chau tay ninh
# province:
# ['ho', 'minh', 'tay', 'tay ninh']
# district:
# ['duong', 'duong minh', 'duong minh chau']
# ward:
# ['an'] => return null if not match whole words or not match n-gram

# original: A:12A.21BlockA C/c BCA,P.AnKhánh,TP.Thủ Đức, TP. HCM
# preprocessed: a12a21blocka cc bcapankhanhtpthu duc tp hcm
# province:
# ['hcm']
# district:
# ['thu', 'thu duc']
# ward:
# ['1', '1', 'an', 'an', 'an', 'khanh'] => Match n-gram will create 'an khanh'
