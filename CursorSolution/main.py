from dictionary_construction import load_and_normalize_list, normalize_name
from trie import Trie
from address_candidate_extraction import extract_candidates
from address_selection import select_best_combination
from contextual_filter import ContextualFilter

def build_trie_from_norm_map(norm_map):
    """Build a Trie from a normalized-to-original mapping."""
    trie = Trie()
    for norm, originals in norm_map.items():
        for orig in originals:
            trie.insert(norm, orig)
    return trie

def load_address_tries():
    """Load datasets and build tries for ward, district, and province."""
    ward_names, ward_norm_map = load_and_normalize_list('list_ward.txt')
    district_names, district_norm_map = load_and_normalize_list('list_district.txt')
    province_names, province_norm_map = load_and_normalize_list('list_province.txt')
    ward_trie = build_trie_from_norm_map(ward_norm_map)
    district_trie = build_trie_from_norm_map(district_norm_map)
    province_trie = build_trie_from_norm_map(province_norm_map)
    return ward_trie, district_trie, province_trie

def print_candidates(candidates):
    """Nicely print extracted address candidates."""
    if not candidates:
        print("No candidates found.")
        return
    print("Candidates:")
    for c in candidates:
        print(f"  [{c['type']}] {c['original']} (ngram: '{c['ngram']}', tokens {c['start']}-{c['end']})")

def test(input_str):
    # Load tries
    ward_trie, district_trie, province_trie = load_address_tries()

    # Input string
    print(f"Input: {input_str}")

    # Normalize input
    normalized_input = normalize_name(input_str)
    print(f"Normalized: {normalized_input}")

    # Extract candidates
    candidates = extract_candidates(normalized_input, ward_trie, district_trie, province_trie)
    print_candidates(candidates)

    cf = ContextualFilter('real_dataset_filter.json')
    
    # Select best combination
    best = select_best_combination(candidates, cf)
    print("Best selection:")
    print(f"  ward: {best['ward']}")
    print(f"  district: {best['district']}")
    print(f"  province: {best['province']}")
    print("--------------------------------")

# test("X ThuanThanh H. Can Giuoc, Long An")
# test("Thuận Thanh, HCần Giuộc, Tlong An")
# test("Thuận Thành, H Cần Giuộc T. Long An")

# Additional real-world tests from public.json
# 1. Abbreviated, noisy, and with diacritics
# test("TT T,â,n B,ì,n,h Huyện Yên Sơn, Tuyên Quang")
# # 2. Abbreviated, no district/ward found
# test("357/28,Ng-T- Thuật,P1,Q3,TP.HồChíMinh.")
# # 3. Numeric ward, province abbreviation
# test("284DBis Ng Văn Giáo, P3, Mỹ Tho, T.Giang.")
# # 4. Noisy, missing accents
# test("Nà Làng Phú Bình, Chiêm Hoá, Tuyên Quang")
# # 5. District as number, ward with diacritics
# test("59/12 Ng-B-Khiêm, Đa Kao Quận 1, TP. Hồ Chí Minh")
# # 6. Ward and district repeated, province with diacritics
# test("46/8F Trung Chánh 2 Trung Chánh, Hóc Môn, TP. Hồ Chí Minh")
# # 7. Province with diacritics, ward and district with diacritics
# test("T18,Cẩm Bình, Cẩm Phả, Quảng Ninh.")
# # 8. Noisy, missing accents, no abbreviations
# test("Thanh Long, Yên Mỹ Hưng Yên")
# # 9. Ward and district with diacritics, province with diacritics
# test("D2, Thạnh Lợi, Vĩnh Thạnh Cần Thơ")
# # 10. Ward and district with diacritics, province with diacritics
# test("Cổ Lũy Hải Ba, Hải Lăng, Quảng Trị")

# test("Khu phố 4 Thị trấn, Dương Minh Châu, Tây Ninh")
test("Khu phố 3, Trảng Dài, Thành phố Biên Hòa, Đồng Nai.")
# test("Số Nhà 38, Tổ 9 Tô Hiệu, Thành phố Sơn La, Sơn La.")
# test("CH F1614-HH2-Khu ĐTM Dương Nội Yên NghĩahàdônghyàNội")
# test("Khu 3 Suối Hoa, Thành phố Bắc Ninh, Bắc Ninh")
# test("X.Nga Thanh hyện Nga son TỉnhThanhQ Hóa")
# test("Phường Phú Mỹ, Thà6nh phố Thủ Dầu Một, TBình Dương")
