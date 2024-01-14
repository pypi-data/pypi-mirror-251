from typing import Iterable
from . import consts
import fnmatch


def contains_only(string: str, charset: Iterable[str]) -> bool:
    for char in string:
        if char not in charset:
            return False
    return True


def is_base64(string: str) -> bool:
    return contains_only(string, consts.BASE64_DIGITS_WITH_EQUALS)


def is_base64_no_equals(string: str) -> bool:
    return contains_only(string, consts.BASE64_DIGITS)


def is_octal(string: str) -> bool:
    return contains_only(string, consts.OCTAL_DIGITS)


def is_numerical(string: str) -> bool:
    return contains_only(string, consts.ASCII_DIGITS)


def is_hex(string: str) -> bool:
    return contains_only(string, consts.HEX_DIGITS)


def is_hex_upper(string: str) -> bool:
    return contains_only(string, consts.HEX_DIGITS_UPPER)


def is_hex_lower(string: str) -> bool:
    return contains_only(string, consts.HEX_DIGITS_LOWER)


def is_whitespace(string: str) -> bool:
    return contains_only(string, consts.WHITESPACE)


def is_lowercase(string: str) -> bool:
    return string == string.lower()


def is_uppercase(string: str) -> bool:
    return string == string.upper()


def is_fully_lowercase(string: str) -> bool:
    return contains_only(string, consts.ASCII_LOWERCASE)


def is_fully_uppercase(string: str) -> bool:
    return contains_only(string, consts.ASCII_UPPERCASE)


def is_ascii_letters(string: str) -> bool:
    return contains_only(string, consts.ASCII_LETTERS)


def is_ascii_punctuation(string: str) -> bool:
    return contains_only(string, consts.ASCII_PUNCTUATION)


def is_ascii_printable(string: str) -> bool:
    return contains_only(string, consts.ASCII_PRINTABLE)


def is_ascii_control(string: str) -> bool:
    return contains_only(string, consts.ASCII_CONTROL)


def is_ascii(string: str) -> bool:
    return contains_only(string, consts.ASCII_ALL)


def is_ansi(string: str) -> bool:
    return contains_only(string, consts.ANSI_ALL)


def is_anagram(string1: str, string2: str) -> bool:
    return sorted(string1) == sorted(string2)


def is_palindrome(string: str) -> bool:
    return "".join(reversed(string)) == string


def is_substring(source: str, sub: str) -> bool:
    return sub in source


def is_prefix(source: str, prefix: str) -> bool:
    return source.startswith(prefix)


def is_suffix(source: str, suffix: str) -> bool:
    return source.endswith(suffix)


def wildcard(string: str, pattern: str) -> bool:
    return fnmatch.fnmatchcase(string, pattern)
