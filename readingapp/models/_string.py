import re
import unicodedata


def calculate_check_digit_10(isbn_10):
    x = 0
    for i, c in enumerate(isbn_10[:9]):
        x += (10 - i) * int(c)
    return -x % 11


def check_ISBN10(isbn_10):
    if not isbn_10[:9].isdigit():
        return False

    if isbn_10[9].isdigit():
        check_digit = int(isbn_10[-1])
    elif isbn_10[9] == 'X':
        check_digit = 10
    else:
        return False

    if check_digit == calculate_check_digit_10(isbn_10):
        return True
    else:
        return False


def calculate_check_digit_13(isbn_13):
    x = 0
    w = 1
    for c in isbn_13[:12]:
        x += w * int(c)
        w = 1 if w == 3 else 3
    return -x % 10


def check_ISBN13(isbn_13):
    if not isbn_13.isdigit():
        return False
    
    check_digit = int(isbn_13[12])
    if check_digit == calculate_check_digit_13(isbn_13):
        return True
    else:
        return False


def translate_ISBN10_to_ISBN13(isbn_10):
    string = '978' + isbn_10[:9] + '0'
    check_digit = calculate_check_digit_13(string)
    return string[:-1] + str(check_digit)


def canonicalize_ISBN(code):
    code = code.upper()
    code = ''.join(re.findall('[0-9X]', code))
    isbn_13 = None
    if len(code) == 10:
        if check_ISBN10(code):
            isbn_13 = translate_ISBN10_to_ISBN13(code)
    elif len(code) == 13:
        if check_ISBN13(code):
            isbn_13 = code
    
    return isbn_13


def get_width(string: str):
    """半角文字幅1, 全角文字幅2"""
    width = 0
    for char in string:
        if unicodedata.east_asian_width(char) in 'FWA':
            width += 2
        else:
            width += 1
    return width


def validate_username(username: str):
    """文字幅16, 半角英数"""
    if not re.fullmatch('[0x20-0x7e]+', username):
        return 1
    
    if not len(username) <= 16:
        return 2

def validate_email(email: str):
    """文字幅16, 半角英数"""
    if not re.fullmatch('[0x20-0x7e]+', email):
        return 1
    
    if not len(email) <= 32:
        return 2###############