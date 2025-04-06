from typing import Dict, Tuple, Optional

from IndexAnalyzer import Trie
from Autocorrect import autocorrect
from Utils import *
from Utils import normalize_text_and_remove_accent, two_grams

def search_locations_in_trie(tries: Dict[str, Trie], input_text: str, results) -> Tuple[Dict[str, Optional[str]], str]:
    matched_positions = set()

    remaining_chars = list(input_text)

    for category, reverse in [("province", True), ("district", False), ("ward", False)]:
        if results[category] != "":
            continue
        match = search_part(tries[category], input_text, matched_positions, remaining_chars, reverse)
        res = match[0]
        if match and res:
            input_text = input_text[:match[1]] + "," + input_text[match[2]:]
        results[category] = res
        # print(input_text)
    # remaining_text = normalize_text_and_remove_accent(input_text)
    # for category, reverse in [("province", True), ("ward", False), ("district", False)]:
    #     if results[category] != "":
    #         continue
    #     match = search_part(tries[category], remaining_text, matched_positions, remaining_chars, reverse)
    #     res = match[0]
    #     if match and res:
    #         remaining_text = remaining_text[:match[1]] + "," + remaining_text[match[2]:]
    #         input_text = input_text[:match[1]] + "," + input_text[match[2]:]
    #     results[category] = res

    return results, input_text

def search_locations_in_segments(tries: Dict[str, Trie], segments: [], results) -> Tuple[Dict[str, Optional[str]], str]:
    for category, reverse in [("province", True), ("ward", False), ("district", False)]:
        if results[category] != "":
            continue

        res = search_in_segment(segments, tries[category], category, reverse)
        results[category] = res

    return results, segments

def search_in_trie(trie, input_text, matched_positions, remaining_chars, reverse):
    match = search_part(trie, input_text, matched_positions, remaining_chars, reverse)
    res = match[0]
    if match and res:
        input_text = input_text[:match[1]] + "," + input_text[match[2]:]
    return res, input_text

def search_in_segment(segments, trie, category, reverse=False):
    if reverse:
        segments.reverse()

    for seg in segments:
        word = autocorrect(seg, trie, category)
        if word == "":
            continue
        segments.remove(seg)
        return word

    if reverse:
        segments.reverse()

    return ""

def search_part(trie, input_text, matched_positions, remaining_chars, reversed=False):
    it_range = range(len(input_text))
    matched_intervals = []
    if reversed:
        it_range = it_range.__reversed__()
    for i in it_range:
        if i in matched_positions:
            continue
        matches = trie.search_max_length(input_text, i)

        if matches:
            best_match = max(matches, key=lambda x: (x[2], x[2] - x[1]))  # Prioritize the end and length
            # Check if the best match is actually the longest match covering the end of the string
            if any(match[1] <= len(input_text) - 1 <= match[2] for match in matches):
                best_match = max(matches, key=lambda x: (x[2], x[2] - x[1]))
            # print(best_match)
            # Ensure no overlap with previously matched regions
            start, end = best_match[1], best_match[2]
            if any(s <= start < e or s < end <= e for s, e in matched_intervals):
                continue  # Skip overlapping matches
            # Remove matched characters properly
            return best_match
    return "", None, None

# def search_by_character(trie, last_results, missing_results, remaining_text):
#     # Kết hợp các phần tử trong remaining_text thành chuỗi, sau đó đảo ngược chuỗi và tách thành danh sách các ký tự.
#     combined_string = ''.join(remaining_text)
#     split_char_segment = list(combined_string[::-1])
#
#     keys_order = ['province', 'district', 'ward']
#     results = {}
#
#     for key in keys_order:
#         if key in missing_results:
#             merged_token = ""
#             best_result = None
#             best_distance = float('inf')
#             used_count = 0  # Số token đã merge cho key hiện tại
#             best_used_count = 0  # Số token tạo ra candidate tốt nhất
#             candidate_array = []  # Lưu trữ các candidate thu được ở từng bước merge
#
#             # Duyệt qua các token theo thứ tự reversed (từ phải qua trái ban đầu)
#             for token in split_char_segment:
#                 # Nối token mới vào cuối merged_token (vì split_char_segment đã là reversed)
#                 merged_token = merged_token + token if merged_token != "" else token
#                 used_count += 1
#
#                 search_key = merged_token
#
#                 # Lấy danh sách candidate từ reversed trie theo key
#                 candidates = trie[key].collect_candidates(search_key)
#
#                 # best_candidate_by_distance trả về (current_candidate, candidate_ids, distance)
#                 current_candidate, candidate_ids, distance = best_candidate_by_distance(search_key, candidates)
#
#                 candidate_array.append((current_candidate, candidate_ids, distance, used_count))
#
#                 # So sánh các candidate đã thu thập để chọn ra candidate tốt nhất hiện tại cho key này.
#                 best_candidate_current = None
#                 best_candidate_ids_current = None
#                 best_distance_current = float('inf')
#                 best_used_count_current = 0
#
#                 for cand, cand_ids, cand_dist, cand_used in candidate_array:
#                     if cand is not None:
#                         d = levenshtein_distance(search_key, cand)
#                         if d < best_distance_current or (
#                                 d == best_distance_current and cand_used > best_used_count_current):
#                             best_candidate_current = cand
#                             best_candidate_ids_current = cand_ids
#                             best_distance_current = d
#                             best_used_count_current = cand_used
#
#                 # Cập nhật kết quả tốt nhất nếu có candidate hợp lệ
#                 if best_candidate_ids_current:
#                     if best_result is None or best_distance_current < best_distance or (
#                             best_distance_current == best_distance and used_count > best_used_count):
#                         best_result = best_candidate_ids_current
#                         best_distance = best_distance_current
#                         best_used_count = used_count
#
#             # Nếu có kết quả cho key hiện tại, cập nhật vào results
#             if best_result is not None:
#                 # Nếu best_result là tập hợp và chứa nhiều hơn 1 phần tử thì chỉ lấy một giá trị
#                 if isinstance(best_result, set) and len(best_result) > 0:
#                     best_result = next(iter(best_result))
#                 results[key] = best_result
#                 # Loại bỏ các token đã sử dụng (theo số lượng best_used_count) khỏi split_char_segment
#                 split_char_segment = split_char_segment[best_used_count:]
#
#     # Merge kết quả mới vào last_results
#     if last_results is None:
#         last_results = {}
#     last_results.update(results)
#     return last_results


def search_by_character(trie, last_results, missing_results, remaining_text):
    # Kết hợp các phần tử trong remaining_text thành chuỗi, sau đó
    # đảo ngược chuỗi và tách thành danh sách các ký tự.
    combined_string = ''.join(remaining_text)
    split_char_segment = list(combined_string[::-1])

    keys_order = ['province', 'district', 'ward']
    results = {}

    for key in keys_order:
        if key in missing_results:
            merged_token = ""
            best_result = None        # Sẽ lưu "reference" tốt nhất
            best_used_count = 0       # Ưu tiên token dài hơn khi distance=0
            candidate_array = []      # Lưu mọi candidate tìm được

            # Duyệt qua các token (đã bị đảo ngược)
            for token in split_char_segment:
                merged_token = merged_token + token if merged_token else token
                used_count = len(merged_token)
                search_key = merged_token

                # Gọi hàm collect_candidates() để lấy list (candidate, reference)
                candidates = trie[key].collect_candidates(search_key)

                # Giờ best_candidate_by_distance trả về list dict:
                # [ { "candidate": c, "reference": r, "distance": d }, ... ]
                list_of_candidates = best_candidate_by_distance(search_key, candidates)

                # Ta nối (extend) vào candidate_array, mỗi phần tử bổ sung cột used_count
                for item in list_of_candidates:
                    candidate_array.append((
                        item["candidate"],
                        item["reference"],
                        item["distance"],
                        used_count
                    ))

                # Kiểm tra xem có candidate nào distance=0 hay không
                # Nếu có, lấy candidate có used_count lớn nhất
                for cand, ref, dist, used in candidate_array:
                    d = levenshtein_distance(search_key, cand)
                    if d <= 1:  # Levenshtein distance thường là số nguyên, nên dist < 1 nghĩa là dist == 0
                        if best_result is None or used > best_used_count:
                            best_result = ref
                            best_used_count = used

            # Nếu đã tìm được best_result cho key hiện tại, cập nhật vào results
            if best_result is not None:
                # Nếu best_result là một tập hợp và chứa >1 phần tử, lấy tạm 1 phần tử
                if isinstance(best_result, set) and len(best_result) > 0:
                    best_result = next(iter(best_result))

                results[key] = best_result

                # Cắt bỏ best_used_count ký tự (đã dùng) khỏi split_char_segment
                split_char_segment = split_char_segment[best_used_count:]

    # Cập nhật last_results (nếu cần)
    if last_results is None:
        last_results = {}
    last_results.update(results)
    return last_results
