import json
from collections import defaultdict

class ContextualFiltering:
    def __init__(self, json_path='contextual_filtering_dataset.json'):
        self.province_to_district = defaultdict(set)
        self.district_to_ward = defaultdict(set)
        self.province_to_ward = defaultdict(set)
        self._load_context(json_path)

    def _load_context(self, json_path):
        with open(json_path, encoding='utf-8') as f:
            data = json.load(f)
        for province in data:
            p_name = province['FullName']
            for district in province.get('District', []):
                d_name = district['FullName']
                self.province_to_district[p_name].add(d_name)
                for ward in district.get('Ward', []):
                    w_name = ward['FullName']
                    self.district_to_ward[d_name].add(w_name)
                    self.province_to_ward[p_name].add(w_name)

    def is_valid(self, ward, district, province):
        """
        Returns True if the (ward, district, province) combination is valid.
        If any value is empty, that part is ignored in validation.
        """
        result = True
        if province and district:
            result &= district in self.province_to_district.get(province, set())

        if district and ward:
            result &= ward in self.district_to_ward.get(district, set())

        if not district and province and ward:
            result &= ward in self.province_to_ward.get(province, set())
        
        return result


# Example usage:
# cf = ContextualFiltering('contextual_filtering_dataset.json')
# print(cf.validate('Phúc Xá', 'Ba Đình', 'Hà Nội'))  # True
# print(cf.validate('', 'Ba Đình', 'Hà Nội'))         # True
# print(cf.validate('Phúc Xá', '', 'Hà Nội'))         # True
# print(cf.validate('Phúc Xá', '', ''))               # True 