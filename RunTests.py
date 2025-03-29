import json
import time
import pandas as pd
from datetime import datetime

from Solution import Solution


# CORRECT TESTS
groups_province = {}
groups_district = {'hòa bình': ['Hoà Bình', 'Hòa Bình'], 'kbang': ['Kbang', 'KBang'], 'quy nhơn': ['Qui Nhơn', 'Quy Nhơn']}
groups_ward = {'ái nghĩa': ['ái Nghĩa', 'Ái Nghĩa'], 'ái quốc': ['ái Quốc', 'Ái Quốc'], 'ái thượng': ['ái Thượng', 'Ái Thượng'], 'ái tử': ['ái Tử', 'Ái Tử'], 'ấm hạ': ['ấm Hạ', 'Ấm Hạ'], 'an ấp': ['An ấp', 'An Ấp'], 'ẳng cang': ['ẳng Cang', 'Ẳng Cang'], 'ẳng nưa': ['ẳng Nưa', 'Ẳng Nưa'], 'ẳng tở': ['ẳng Tở', 'Ẳng Tở'], 'an hòa': ['An Hoà', 'An Hòa'], 'ayun': ['Ayun', 'AYun'], 'bắc ái': ['Bắc ái', 'Bắc Ái'], 'bảo ái': ['Bảo ái', 'Bảo Ái'], 'bình hòa': ['Bình Hoà', 'Bình Hòa'], 'châu ổ': ['Châu ổ', 'Châu Ổ'], 'chư á': ['Chư á', 'Chư Á'], 'chư rcăm': ['Chư Rcăm', 'Chư RCăm'], 'cộng hòa': ['Cộng Hoà', 'Cộng Hòa'], 'cò nòi': ['Cò  Nòi', 'Cò Nòi'], 'đại ân 2': ['Đại Ân  2', 'Đại Ân 2'], 'đak ơ': ['Đak ơ', 'Đak Ơ'], "đạ m'ri": ["Đạ M'ri", "Đạ M'Ri"], 'đông hòa': ['Đông Hoà', 'Đông Hòa'], 'đồng ích': ['Đồng ích', 'Đồng Ích'], 'hải châu i': ['Hải Châu  I', 'Hải Châu I'], 'hải hòa': ['Hải Hoà', 'Hải Hòa'], 'hành tín đông': ['Hành Tín  Đông', 'Hành Tín Đông'], 'hiệp hòa': ['Hiệp Hoà', 'Hiệp Hòa'], 'hòa bắc': ['Hoà Bắc', 'Hòa Bắc'], 'hòa bình': ['Hoà Bình', 'Hòa Bình'], 'hòa châu': ['Hoà Châu', 'Hòa Châu'], 'hòa hải': ['Hoà Hải', 'Hòa Hải'], 'hòa hiệp trung': ['Hoà Hiệp Trung', 'Hòa Hiệp Trung'], 'hòa liên': ['Hoà Liên', 'Hòa Liên'], 'hòa lộc': ['Hoà Lộc', 'Hòa Lộc'], 'hòa lợi': ['Hoà Lợi', 'Hòa Lợi'], 'hòa long': ['Hoà Long', 'Hòa Long'], 'hòa mạc': ['Hoà Mạc', 'Hòa Mạc'], 'hòa minh': ['Hoà Minh', 'Hòa Minh'], 'hòa mỹ': ['Hoà Mỹ', 'Hòa Mỹ'], 'hòa phát': ['Hoà Phát', 'Hòa Phát'], 'hòa phong': ['Hoà Phong', 'Hòa Phong'], 'hòa phú': ['Hoà Phú', 'Hòa Phú'], 'hòa phước': ['Hoà Phước', 'Hòa Phước'], 'hòa sơn': ['Hoà Sơn', 'Hòa Sơn'], 'hòa tân': ['Hoà Tân', 'Hòa Tân'], 'hòa thuận': ['Hoà Thuận', 'Hòa Thuận'], 'hòa tiến': ['Hoà Tiến', 'Hòa Tiến'], 'hòa trạch': ['Hoà Trạch', 'Hòa Trạch'], 'hòa vinh': ['Hoà Vinh', 'Hòa Vinh'], 'hương hòa': ['Hương Hoà', 'Hương Hòa'], 'ích hậu': ['ích Hậu', 'Ích Hậu'], 'ít ong': ['ít Ong', 'Ít Ong'], 'khánh hòa': ['Khánh Hoà', 'Khánh Hòa'], 'krông á': ['Krông Á', 'KRông á'], 'lộc hòa': ['Lộc Hoà', 'Lộc Hòa'], 'minh hòa': ['Minh Hoà', 'Minh Hòa'], 'mường ải': ['Mường ải', 'Mường Ải'], 'mường ẳng': ['Mường ẳng', 'Mường Ẳng'], 'nậm ét': ['Nậm ét', 'Nậm Ét'], 'nam hòa': ['Nam Hoà', 'Nam Hòa'], 'na ư': ['Na ư', 'Na Ư'], 'ngã sáu': ['Ngã sáu', 'Ngã Sáu'], 'nghi hòa': ['Nghi Hoà', 'Nghi Hòa'], 'nguyễn úy': ['Nguyễn Uý', 'Nguyễn úy', 'Nguyễn Úy'], 'nhân hòa': ['Nhân Hoà', 'Nhân Hòa'], 'nhơn hòa': ['Nhơn Hoà', 'Nhơn Hòa'], 'nhơn nghĩa a': ['Nhơn nghĩa A', 'Nhơn Nghĩa A'], 'phúc ứng': ['Phúc ứng', 'Phúc Ứng'], 'phước hòa': ['Phước Hoà', 'Phước Hòa'], 'sơn hóa': ['Sơn Hoá', 'Sơn Hóa'], 'tạ an khương đông': ['Tạ An Khương  Đông', 'Tạ An Khương Đông'], 'tạ an khương nam': ['Tạ An Khương  Nam', 'Tạ An Khương Nam'], 'tăng hòa': ['Tăng Hoà', 'Tăng Hòa'], 'tân hòa': ['Tân Hoà', 'Tân Hòa'], 'tân hòa thành': ['Tân Hòa  Thành', 'Tân Hòa Thành'], 'tân khánh trung': ['Tân  Khánh Trung', 'Tân Khánh Trung'], 'tân lợi': ['Tân lợi', 'Tân Lợi'], 'thái hòa': ['Thái Hoà', 'Thái Hòa'], 'thiết ống': ['Thiết ống', 'Thiết Ống'], 'thuận hòa': ['Thuận Hoà', 'Thuận Hòa'], 'thượng ấm': ['Thượng ấm', 'Thượng Ấm'], 'thụy hương': ['Thuỵ Hương', 'Thụy Hương'], 'thủy xuân': ['Thuỷ Xuân', 'Thủy Xuân'], 'tịnh ấn đông': ['Tịnh ấn Đông', 'Tịnh Ấn Đông'], 'tịnh ấn tây': ['Tịnh ấn Tây', 'Tịnh Ấn Tây'], 'triệu ái': ['Triệu ái', 'Triệu Ái'], 'triệu ẩu': ['Triệu ẩu', 'Triệu Ẩu'], 'trung hòa': ['Trung Hoà', 'Trung Hòa'], 'trung ý': ['Trung ý', 'Trung Ý'], 'tùng ảnh': ['Tùng ảnh', 'Tùng Ảnh'], 'úc kỳ': ['úc Kỳ', 'Úc Kỳ'], 'ứng hòe': ['ứng Hoè', 'Ứng Hoè'], 'vĩnh hòa': ['Vĩnh Hoà', 'Vĩnh Hòa'], 'vũ hòa': ['Vũ Hoà', 'Vũ Hòa'], 'xuân ái': ['Xuân ái', 'Xuân Ái'], 'xuân áng': ['Xuân áng', 'Xuân Áng'], 'xuân hòa': ['Xuân Hoà', 'Xuân Hòa'], 'xuất hóa': ['Xuất Hoá', 'Xuất Hóa'], 'ỷ la': ['ỷ La', 'Ỷ La']}
groups_ward.update({1: ['1', '01'], 2: ['2', '02'], 3: ['3', '03'], 4: ['4', '04'], 5: ['5', '05'], 6: ['6', '06'], 7: ['7', '07'], 8: ['8', '08'], 9: ['9', '09']})
def to_same(groups):
    same = {ele: k for k, v in groups.items() for ele in v}
    return same
same_province = to_same(groups_province)
same_district = to_same(groups_district)
same_ward = to_same(groups_ward)
def normalize(text, same_dict):
    return same_dict.get(text, text)

def get_formatted_datetime():
  now = datetime.now()
  formatted_datetime = now.strftime("%Y%m%d_%H%M%S")
  return formatted_datetime

#
TEAM_NAME = f'TestResults/DEFAULT_NAME_{get_formatted_datetime()}'  # This should be your team name
EXCEL_FILE = f'{TEAM_NAME}.xlsx'
TEST_FILE = 'public.json'
with open(TEST_FILE, encoding='utf-8') as f:
    data = json.load(f)

summary_only = True
df = []
solution = Solution()
timer = []
correct = 0
for test_idx, data_point in enumerate(data):
    address = data_point["text"]

    ok = 0
    try:
        answer = data_point["result"]
        answer["province_normalized"] = normalize(answer["province"], same_province)
        answer["district_normalized"] = normalize(answer["district"], same_district)
        answer["ward_normalized"] = normalize(answer["ward"], same_ward)

        start = time.perf_counter_ns()
        result = solution.process(address)
        finish = time.perf_counter_ns()
        timer.append(finish - start)
        result["province_normalized"] = normalize(result["province"], same_province)
        result["district_normalized"] = normalize(result["district"], same_district)
        result["ward_normalized"] = normalize(result["ward"], same_ward)

        province_correct = int(answer["province_normalized"] == result["province_normalized"])
        district_correct = int(answer["district_normalized"] == result["district_normalized"])
        ward_correct = int(answer["ward_normalized"] == result["ward_normalized"])
        ok = province_correct + district_correct + ward_correct

        df.append([
            test_idx,
            address,
            answer["province"],
            result["province"],
            answer["province_normalized"],
            result["province_normalized"],
            province_correct,
            answer["district"],
            result["district"],
            answer["district_normalized"],
            result["district_normalized"],
            district_correct,
            answer["ward"],
            result["ward"],
            answer["ward_normalized"],
            result["ward_normalized"],
            ward_correct,
            ok,
            timer[-1] / 1_000_000_000,
        ])
        if not ok or not province_correct or not district_correct or not ward_correct:
            raise ValueError()
    except Exception as e:
        print()
        print("Original: " + address)
        print(f"{answer = }")
        print(f"{result = }")
        df.append([
            test_idx,
            address,
            answer["province"],
            "EXCEPTION",
            answer["province_normalized"],
            "EXCEPTION",
            0,
            answer["district"],
            "EXCEPTION",
            answer["district_normalized"],
            "EXCEPTION",
            0,
            answer["ward"],
            "EXCEPTION",
            answer["ward_normalized"],
            "EXCEPTION",
            0,
            0,
            0,
        ])
        # any failure count as a zero correct
        pass
    correct += ok

    if not summary_only:
        # responsive stuff
        print(f"Test {test_idx:5d}/{len(data):5d}")
        print(f"Correct: {ok}/3")
        print(f"Time Executed: {timer[-1] / 1_000_000_000:.4f}")

print(f"-" * 30)
total = len(data) * 3
score_scale_10 = round(correct / total * 10, 2)
if len(timer) == 0:
    timer = [0]
max_time_sec = round(max(timer) / 1_000_000_000, 4)
avg_time_sec = round((sum(timer) / len(timer)) / 1_000_000_000, 4)

df2 = pd.DataFrame(
    [[correct, total, score_scale_10, max_time_sec, avg_time_sec]],
    columns=['correct', 'total', 'score / 10', 'max_time_sec', 'avg_time_sec', ],
)

columns = [
    'ID',
    'text',
    'province',
    'province_student',
    'province_normalized',
    'province_student_normalized',
    'province_correct',
    'district',
    'district_student',
    'district_normalized',
    'district_student_normalized',
    'district_correct',
    'ward',
    'ward_student',
    'ward_normalized',
    'ward_student_normalized',
    'ward_correct',
    'total_correct',
    'time_sec',
]

df = pd.DataFrame(df)
df.columns = columns

print(df2)

# print(f'{TEAM_NAME = }')
# print(f'{EXCEL_FILE = }')
# writer = pd.ExcelWriter(EXCEL_FILE, engine='xlsxwriter')
# df2.to_excel(writer, index=False, sheet_name='summary')
# df.to_excel(writer, index=False, sheet_name='details')
# writer.close()