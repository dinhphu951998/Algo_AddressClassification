class VietnameseHelper:
    vietnamese_dict = {
        "a": "áàạảãâấầậẩẫăắằặẳẵ",
        "A": "ÁÀẠẢÃÂẤẦẬẨẪĂẮẰẶẲẴ",
        "e": "éèẹẻẽêếềệểễ",
        "E": "ÉÈẸẺẼÊẾỀỆỂỄ",
        "o": "óòọỏõôốồộổỗơớờợởỡ",
        "O": "ÓÒỌỎÕÔỐỒỘỔỖƠỚỜỢỞỠ",
        "u": "úùụủũưứừựửữ",
        "U": "ÚÙỤỦŨƯỨỪỰỬỮ",
        "i": "íìịỉĩ",
        "I": "ÍÌỊỈĨ",
        "d": "đ",
        "D": "Đ",
        "y": "ýỳỵỷỹ",
        "Y": "ÝỲỴỶỸ"
    }
    reversed_vietnamese_dict = {}
    special_characters = ["!", "\"", "#", "$", "%", "&", "'", "(", ")", "*", "+", ",", "-", ".", "/", ":", ";", "<",
                          "=", ">", "?", "@", "[", "\\", "]", "^", "_", "`", "{", "|", "}", "~"]

    def __init__(self):
        for base_char, variations in self.vietnamese_dict.items():
            for char in variations:
                self.reversed_vietnamese_dict[char] = base_char

    def remove_vietnamese_signs(self, s: str):
        result = []
        for char in s:
            if char in self.reversed_vietnamese_dict:
                result.append(self.reversed_vietnamese_dict[char])
            else:
                result.append(char)
        return "".join(result)

    def remove_special_characters(self, s: str):
        result = []
        for char in s:
            if char not in self.special_characters:
                result.append(char)
        return "".join(result).strip()