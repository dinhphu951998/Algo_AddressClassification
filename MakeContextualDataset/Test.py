import json
import re

new_file = "contextual_filtering_dataset_2.json"

def read_file(filename):
    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data

def write_file(data, filename):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)

        
def remove_prefix(name):
    prefix = ["Huyện ", "Thị xã ", "Thành phố ", "Xã ", "Phường ", "Thị trấn ", "Tỉnh ", "Quận "]
    for prefix_item in prefix:
        if name.lower().startswith(prefix_item.lower()):
            name = name.replace(prefix_item, "")
    return re.sub(r'\s+', ' ', name).strip()

def append_name(name, arr):
    if '-' in name:
        name_parts = [part.strip() for part in name.split('-')]
        arr.append(' '.join(name_parts))
    arr.append(name)
    return arr


def parse_wards(data):
    ward_names = []
    if len(data) == 0:
        return []
    for key, value in data.items():
        for ward in value[0]:
            norm_ward = remove_prefix(ward)
            append_name(norm_ward, ward_names)
    
    return [{"FullName": ward} for ward in set(ward_names)]

def parse_districts(data):
    result =[]
    for key, value in data.items():
        district_names = []
        wards = parse_wards(value[1])
        for district in value[0]:
            norm_district_name = remove_prefix(district)
            append_name(norm_district_name, district_names)

        result.extend([{"FullName": name, "Ward": wards} for name in set(district_names)])

    return result


# This function is to read and transform file tree.json
def parse_province(data): 
    result = []
    for key, value in data.items():
        # Get just the value from each key-value pair
        province_names = []
        districts = parse_districts(value[1])
        for province in value[0]:
            norm_province_name = remove_prefix(province)
            append_name(norm_province_name, province_names)

        result.extend([{"FullName": name, "District": districts} for name in set(province_names)])

    return result

def transform_data():
    data = read_file("tree.json")
    provinces = parse_province(data)
    write_file(provinces, new_file)

transform_data()
