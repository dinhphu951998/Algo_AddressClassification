# Address Classification Problem - Analysis & Solution

## Problem Overview

Given:
- Three datasets: `list_ward.txt`, `list_district.txt`, `list_province.txt` containing the names of wards, districts, and provinces in Vietnam.
- An input string (possibly with misspellings, abbreviations, or inconsistent formatting).
- Some suggested libraries: `unicodedata`, `editdistance` and others with no machine learning/deep learning models inside.
- Be carefull with edge cases: E.g: Thanh Hoa and Thanh Hóa

**Goal:**  
Extract the correct `ward`, `district`, and `province` names from the input string. If a part cannot be found, return it as an empty string.

**Example:**  
Input: `'X. Thuận Thành, H. Cần Giuộc, T. Long An'`  
Output:  
```
ward: Thuận Thành
district: Cần Giuộc
province: Long An
```

## Challenges

- **Misspellings and Typos:** Input may have spelling errors or missing accents.
- **Abbreviations:** Prefixes like `X.`, `H.`, `T.`, `P.`, etc. may be used or omitted.
- **Order and Delimiters:** The order of address parts and delimiters (comma, space, etc.) are inconsistent.
- **Partial or Missing Information:** Some parts may be missing from the input.

## Data Reference

- The `public.json` file provides real-world test cases, with `text` as the input and `result` as the expected output.
- The datasets (`list_ward.txt`, etc.) are assumed to contain the canonical names for each administrative level.

## Solution Approach

### 1. **Data Preprocessing**

- **Normalization:**  
  - Convert all text to lowercase.
  - Remove or standardize diacritics (accents).
  - Remove extra spaces, punctuation, and unify delimiters.
  - Expand or standardize common abbreviations (e.g., `TP.` → `Thành phố`, `Q.` → `Quận`, `H.` → `Huyện`, `T.` → `Tỉnh`, `P.` → `Phường`, `X.` → `Xã`, etc.).

- **Dictionary Construction:**  
  - Build sets or tries for each of the three administrative levels using the provided lists.
  - Store both the original and normalized versions for robust matching.

### 2. **Efficient String Matching**

- **Trie Data Structure:**  
  - Use a trie for each administrative level to allow fast prefix and fuzzy matching.
  - Each trie node can store the original name and its normalized form.

- **Fuzzy Matching:**  
  - Use edit distance (Levenshtein or similar) to allow for minor typos or missing accents.
  - For each substring in the input, check if it matches any entry in the trie within a small edit distance threshold.

- **Dynamic Programming:**  
  - Use DP to segment the input string into possible address parts, maximizing the total match score (e.g., minimal edit distance).
  - This helps in cases where the boundaries between address parts are unclear.

### 3. **Parsing and Extraction**

- **Tokenization:**  
  - Split the normalized input into tokens using spaces and punctuation as delimiters.
  - Try to identify likely boundaries using known prefixes or common patterns.

- **Candidate Generation:**  
  - Generate all possible substrings (n-grams) up to a reasonable length.
  - For each substring, check for a match in the corresponding trie (ward, district, province).

- **Scoring and Selection:**  
  - For each candidate, compute a match score (e.g., edit distance, prefix match, etc.).
  - Select the best non-overlapping combination of ward, district, and province with the highest total score.

### 4. **Post-processing**

- **Disambiguation:**  
  - If multiple candidates have similar scores, use context (e.g., known province-district-ward hierarchies) to resolve ambiguities.
  - Prefer longer matches and those with lower edit distances.

- **Output Formatting:**  
  - Return the original (accented) names as found in the datasets.
  - If a part is not found, return an empty string for that part.

## Example Workflow

1. **Input:** `'X ThuanThanh H. Can Giuoc, Long An'`
2. **Normalization:** `'x thuanthanh h can giuoc long an'`
3. **Candidate Extraction:**  
   - Try to match `'thuanthanh'` to `'Thuận Thành'` (ward, edit distance 1).
   - Try to match `'can giuoc'` to `'Cần Giuộc'` (district, edit distance 1).
   - Try to match `'long an'` to `'Long An'` (province, exact match).
4. **Output:**  
   ```
   ward: Thuận Thành
   district: Cần Giuộc
   province: Long An
   ```

## Implementation Hints

- **Trie Construction:**  
  - Insert all normalized names into the trie.
  - Each node can store a list of possible completions for fuzzy matching.

- **Fuzzy Search:**  
  - For each substring, use a recursive or DP-based search in the trie allowing for a limited number of edits.

- **Dynamic Programming:**  
  - For the entire input, use DP to find the optimal segmentation into ward, district, and province.

- **Performance:**  
  - Limit the maximum substring length to avoid combinatorial explosion.
  - Cache results of expensive operations where possible.

## References

- [Levenshtein Distance](https://en.wikipedia.org/wiki/Levenshtein_distance)
- [Trie Data Structure](https://en.wikipedia.org/wiki/Trie)
- [Vietnamese Address Abbreviations](https://github.com/vietmap-company/vietmap-address-abbreviation)

---

## Summary Table

| Step                | Technique         | Purpose                                      |
|---------------------|------------------|----------------------------------------------|
| Normalization       | Text processing  | Handle case, accents, abbreviations          |
| Dictionary/Trie     | Data structure   | Fast and robust matching                     |
| Fuzzy Matching      | Edit distance    | Handle typos and misspellings                |
| Dynamic Programming | Segmentation     | Optimal extraction of address parts          |
| Post-processing     | Disambiguation   | Resolve ambiguities, format output           |

---

## Example Code Skeleton

```python
# Pseudocode outline

# 1. Load and normalize datasets
wards = load_and_normalize('list_ward.txt')
districts = load_and_normalize('list_district.txt')
provinces = load_and_normalize('list_province.txt')

# 2. Build tries for each level
ward_trie = build_trie(wards)
district_trie = build_trie(districts)
province_trie = build_trie(provinces)

# 3. Normalize input string
input_norm = normalize(input_string)

# 4. Extract candidates using fuzzy matching
ward = fuzzy_search(input_norm, ward_trie)
district = fuzzy_search(input_norm, district_trie)
province = fuzzy_search(input_norm, province_trie)

# 5. Return results
return {
    'ward': ward or '',
    'district': district or '',
    'province': province or ''
}
```

---

## Conclusion

This approach leverages normalization, trie-based search, fuzzy matching, and dynamic programming to robustly extract Vietnamese address components from noisy input. The provided `public.json` can be used for evaluation and further tuning of the solution. 