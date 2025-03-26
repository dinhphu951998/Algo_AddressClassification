

class SearchAnalyzer:
    def __init__(self):
        pass

    def find_matching_words(self, str, trie):
        return trie.split_words(str)

# print()
# test("284DBis Ng Văn Giáo, P3, Mỹ Tho, T.Giang.")
# test("357/28,Ng-T- Thuật,P1,Q3,TP.HồChíMinh.")
# test("Khu phố 4 Thị trấn, Dương Minh Châu, Tây Ninh")
# test("A:12A.21BlockA C/c BCA,P.AnKhánh,TP.Thủ Đức, TP. HCM")

# original: 284DBis Ng Văn Giáo, P3, Mỹ Tho, T.Giang.
# preprocessed: 284dbis ng van giao p3 my tho tgiang
# province:
# ['ho', 'tgiang'] => Match whole words with max length
# district:
# ['3', 'my', 'my tho']
# ward:
# ['an', 'p3', 'an'] => Create trie should have the combination p3

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
