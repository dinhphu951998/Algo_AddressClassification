from typing import List, Dict

def select_best_combination(candidates: List[Dict], contextual_filter=None) -> Dict[str, str]:
    """
    Given a list of candidates (with type, start, end, original, ngram),
    select the best non-overlapping combination for ward, district, and province.
    Preference is given to longer matches (more tokens), and to non-overlapping spans.
    If contextual_filter is provided, only allow valid (ward, district, province) hierarchies.
    Returns a dict: {'ward': ..., 'district': ..., 'province': ...}
    """
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
    for ward in by_type['ward'] or [None]:
        for district in by_type['district'] or [None]:
            for province in by_type['province'] or [None]:
                spans = []
                score = 0
                if province:
                    spans.append((province['start'], province['end']))
                    score += province['end'] - province['start'] + 1
                if district:
                    spans.append((district['start'], district['end']))
                    score += district['end'] - district['start'] + 1
                if ward:
                    spans.append((ward['start'], ward['end']))
                    score += ward['end'] - ward['start'] + 1
                
                # Check for overlap
                spans = sorted(spans)
                overlap = any(spans[i][1] >= spans[i+1][0] for i in range(len(spans)-1))

                if not overlap:
                    if district and ward and not contextual_filter.is_ward_in_district(ward['original'], district['original']):
                        score -= ward['end'] - ward['start'] + 1
                    if province and district and not contextual_filter.is_district_in_province(district['original'], province['original']):
                        score -= district['end'] - district['start'] + 1

                if score > best_score:
                    best_score = score
                    w = ward['original'] if ward else ''
                    d = district['original'] if district else ''
                    p = province['original'] if province else ''
                    if d and p and not contextual_filter.is_district_in_province(d, p):
                        d = ''
                    if w and d and not contextual_filter.is_ward_in_district(w, d):
                        w = ''
                    best['ward'] = w
                    best['district'] = d
                    best['province'] = p

    return best

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