import json
from collections import defaultdict

# Contextual filter loader and lookup
class ContextualFilter:
    def __init__(self, json_path):
        self.province_to_districts = defaultdict(set)
        self.district_to_wards = defaultdict(set)
        self.ward_to_district_province = dict()
        self.district_to_province = dict()
        self.province_names = set()
        self.district_names = set()
        self.ward_names = set()
        self._load(json_path)

    def _load(self, json_path):
        with open(json_path, encoding='utf-8') as f:
            data = json.load(f)
        for province in data:
            pname = province['FullName']
            self.province_names.add(pname)
            for district in province.get('District', []):
                dname = district['FullName']
                self.district_names.add(dname)
                self.province_to_districts[pname].add(dname)
                self.district_to_province[dname] = pname
                for ward in district.get('Ward', []):
                    wname = ward['FullName']
                    self.ward_names.add(wname)
                    self.district_to_wards[dname].add(wname)
                    self.ward_to_district_province[wname] = (dname, pname)

    def is_ward_in_district(self, ward, district):
        return ward in self.district_to_wards.get(district, set())

    def is_district_in_province(self, district, province):
        return district in self.province_to_districts.get(province, set())

    def get_districts_of_province(self, province):
        return list(self.province_to_districts.get(province, []))

    def get_wards_of_district(self, district):
        return list(self.district_to_wards.get(district, []))

    def get_district_province_of_ward(self, ward):
        return self.ward_to_district_province.get(ward, (None, None))

# Example usage:
# cf = ContextualFilter('real_dataset_filter.json')
# print(cf.is_ward_in_district('Phường Phúc Xá', 'Quận Ba Đình'))
# print(cf.is_district_in_province('Quận Ba Đình', 'Thành phố Hà Nội'))
# print(cf.get_district_province_of_ward('Phường Phúc Xá')) 