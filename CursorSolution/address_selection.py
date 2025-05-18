from typing import List, Dict

def select_best_combination(candidates: List[Dict], cf=None) -> Dict[str, str]:
    """
    Given a list of candidates (with type, start, end, original, ngram),
    select the best non-overlapping combination for ward, district, and province.
    Preference is given to longer matches (more tokens), and to non-overlapping spans.
    If contextual_filter is provided, only allow valid (ward, district, province) hierarchies.
    Returns a dict: {'ward': ..., 'district': ..., 'province': ...}
    """

    SCORE_FOR_EXACT_MATCH = 0.3
    SCORE_FOR_FUZZY_MATCH = 0

    # Group candidates by type
    by_type = {'ward': [], 'district': [], 'province': []}
    for c in candidates:
        by_type[c['type']].append(c)

    # Sort each group by (-length, start) so longer matches come first
    for typ in by_type:
        by_type[typ].sort(key=lambda c: (-(c['end'] - c['start'] + 1), c['start']))

    # Try to select the best non-overlapping combination
    best = {'ward': '', 'district': '', 'province': ''}
    best_score = -1
    # Try all combinations (usually only a few candidates per type)
    for ward in [None] + (by_type['ward'] or []):
        for district in [None] + (by_type['district'] or []):
            for province in [None] + (by_type['province'] or []):
                spans = []
                score = 0
                added_percentage = 0
                
                if ward:
                    spans.append((ward['start'], ward['end']))
                    score += (ward['end'] - ward['start'] + 1)# * (2 if ward['match_type'] == 'exact' else 1)
                    added_percentage += SCORE_FOR_EXACT_MATCH if ward['match_type'] == 'exact' else SCORE_FOR_FUZZY_MATCH

                if district:
                    spans.append((district['start'], district['end']))
                    score += (district['end'] - district['start'] + 1)# * (2 if district['match_type'] == 'exact' else 1)
                    added_percentage += SCORE_FOR_EXACT_MATCH if district['match_type'] == 'exact' else SCORE_FOR_FUZZY_MATCH
                    
                if province:
                    spans.append((province['start'], province['end']))
                    score += (province['end'] - province['start'] + 1)# * (2 if province['match_type'] == 'exact' else 1)
                    added_percentage += SCORE_FOR_EXACT_MATCH if province['match_type'] == 'exact' else SCORE_FOR_FUZZY_MATCH

                # Check if any consecutive spans overlap of ward, district, province
                overlap = any(spans[i][1] >= spans[i+1][0] for i in range(len(spans)-1))
                if overlap:
                    continue

                if cf and not cf.is_valid(ward['original'] if ward else '', 
                                          district['original'] if district else '', 
                                          province['original'] if province else ''):
                    continue

                score = score * (1 + added_percentage)

                if score > best_score:
                    best_score = score
                    best['ward'] = ward['original'] if ward else ''
                    best['district'] = district['original'] if district else ''
                    best['province'] = province['original'] if province else ''
                    best['ward_candidate'] = ward
                    best['district_candidate'] = district
                    best['province_candidate'] = province
                    best['score'] = score
                    best['added_percentage'] = added_percentage

    return best

def select_best_combination_dp(candidates: List[Dict], cf=None) -> Dict[str, str]:
    """
    DP-based selection of the best non-overlapping combination for ward, district, and province.
    Returns a dict: {'ward': ..., 'district': ..., 'province': ...}
    """
    SCORE_FOR_EXACT_MATCH = 0.3
    SCORE_FOR_FUZZY_MATCH = 0
    types = ['ward', 'district', 'province']
    type_to_bit = {'ward': 0, 'district': 1, 'province': 2}

    # Sort candidates by end position for DP
    candidates_sorted = sorted(candidates, key=lambda c: (c['end'], c['start']))
    n = len(candidates_sorted)
    # dp[i][mask] = (score, path)
    dp = [{} for _ in range(n+1)]
    dp[0][0] = (0, [])

    for i in range(1, n+1):
        cand = candidates_sorted[i-1]
        typ = cand['type']
        typ_idx = type_to_bit[typ]
        for mask, (score, path) in dp[i-1].items():
            # Option 1: skip this candidate
            if mask not in dp[i] or dp[i][mask][0] < score:
                dp[i][mask] = (score, path)
            # Option 2: take this candidate if type not used and no overlap
            new_mask = mask | (1 << typ_idx)
            if (mask & (1 << typ_idx)) == 0:
                # Check overlap
                overlap = False
                for prev_cand in path:
                    if not (cand['end'] < prev_cand['start'] or cand['start'] > prev_cand['end']):
                        overlap = True
                        break
                if overlap:
                    continue
                # Contextual filter
                if cf:
                    ward = cand['original'] if typ == 'ward' else next((c['original'] for c in path if c['type'] == 'ward'), '')
                    district = cand['original'] if typ == 'district' else next((c['original'] for c in path if c['type'] == 'district'), '')
                    province = cand['original'] if typ == 'province' else next((c['original'] for c in path if c['type'] == 'province'), '')
                    if not cf.is_valid(ward, district, province):
                        continue
                # Score
                added_percentage = SCORE_FOR_EXACT_MATCH if cand.get('match_type') == 'exact' else SCORE_FOR_FUZZY_MATCH
                new_score = score + (cand['end'] - cand['start'] + 1) * (1 + added_percentage)
                new_path = path + [cand]
                if new_mask not in dp[i] or dp[i][new_mask][0] < new_score:
                    dp[i][new_mask] = (new_score, new_path)

    # Find the best among all dp[n][mask]
    best_score = -1
    best_path = []
    best_mask = 0
    for mask, (score, path) in dp[n].items():
        if score > best_score:
            best_score = score
            best_path = path
            best_mask = mask

    # Build result dict
    result = {'ward': '', 'district': '', 'province': ''}
    for cand in best_path:
        result[cand['type']] = cand['original']
        result[cand['type'] + '_candidate'] = cand
    result['score'] = best_score
    return result

# Example usage
if __name__ == "__main__":
    # Example candidates
    candidates = [
        {'type': 'ward', 'start': 1, 'end': 2, 'original': 'Thuận Thành', 'ngram': 'thuan thanh'},
        {'type': 'district', 'start': 4, 'end': 5, 'original': 'Cần Giuộc', 'ngram': 'can giuoc'},
        {'type': 'province', 'start': 7, 'end': 8, 'original': 'Long An', 'ngram': 'long an'},
    ]
    result = select_best_combination(candidates)
    print(result) 