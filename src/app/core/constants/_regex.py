# -*- coding: utf-8 -*-

# Valid characters:
ALPHANUM_REGEX = r"^[0-9a-zA-Z]+$"
ALPHANUM_SPACE_REGEX = r"^[0-9a-zA-Z ]+$"
ALPHANUM_HYPHEN_REGEX = r"^[0-9a-zA-Z_\-]+$"
ALPHANUM_HOST_REGEX = r"^[0-9a-zA-Z_\-.]+$"
ALPHANUM_EXTEND_REGEX = r"^[0-9a-zA-Z_\-. ]+$"
ALPHANUM_PATH_REGEX = r"^[0-9a-zA-Z_\-. \\\/]+$"

ALPHANUM_KR_REGEX = r"^[0-9a-zA-Z가-힣]+$"
ALPHANUM_KR_SPACE_REGEX = r"^[0-9a-zA-Z가-힣 ]+$"
ALPHANUM_KR_HYPHEN_REGEX = r"^[0-9a-zA-Z가-힣_\-]+$"
ALPHANUM_KR_HOST_REGEX = r"^[0-9a-zA-Z가-힣_\-.]+$"
ALPHANUM_KR_EXTEND_REGEX = r"^[0-9a-zA-Z가-힣_\-. ]+$"
ALPHANUM_KR_PATH_REGEX = r"^[0-9a-zA-Z가-힣_\-. \\\/]+$"

ALPHANUM_KR_MN_REGEX = r"^[0-9a-zA-Z가-힣А-яҮүӨөЁё]+$"
ALPHANUM_KR_MN_SPACE_REGEX = r"^[0-9a-zA-Z가-힣А-яҮүӨөЁё ]+$"
ALPHANUM_KR_MN_HYPHEN_REGEX = r"^[0-9a-zA-Z가-힣А-яҮүӨөЁё_\-]+$"
ALPHANUM_KR_MN_HOST_REGEX = r"^[0-9a-zA-Z가-힣А-яҮүӨөЁё_\-.]+$"
ALPHANUM_KR_MN_EXTEND_REGEX = r"^[0-9a-zA-Z가-힣А-яҮүӨөЁё_\-. ]+$"
ALPHANUM_KR_MN_PATH_REGEX = r"^[0-9a-zA-Z가-힣А-яҮүӨөЁё_\-. \\\/]+$"

KR_NUM_REGEX = r"^[0-9가-힣]+$"
KR_NUM_SPACE_REGEX = r"^[0-9가-힣 ]+$"
KR_NUM_HYPHEN_REGEX = r"^[0-9가-힣_\-]+$"
KR_NUM_HOST_REGEX = r"^[0-9가-힣_\-.]+$"
KR_NUM_EXTEND_REGEX = r"^[0-9가-힣_\-. ]+$"
KR_NUM_PATH_REGEX = r"^[0-9가-힣_\-. \\\/]+$"

REQUEST_ID_REGEX = (
    r"\b[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}\b|"
    r"\b[0-9a-fA-F]{32}\b"
)


# Invalid characters:
SPECIAL_CHARS_REGEX = r"[&'\"<>]"
SPECIAL_CHARS_BASE_REGEX = r"[&'\"<>\\\/]"
SPECIAL_CHARS_LOW_REGEX = r"[&'\"<>\\\/`{}|]"
SPECIAL_CHARS_MEDIUM_REGEX = r"[&'\"<>\\\/`{}|()\[\]]"
SPECIAL_CHARS_HIGH_REGEX = r"[&'\"<>\\\/`{}|()\[\]!@#$%^*;:?]"
SPECIAL_CHARS_STRICT_REGEX = r"[&'\"<>\\\/`{}|()\[\]~!@#$%^*_=\-+;:,.?\t\n ]"


__all__ = [
    "ALPHANUM_REGEX",
    "ALPHANUM_SPACE_REGEX",
    "ALPHANUM_HYPHEN_REGEX",
    "ALPHANUM_HOST_REGEX",
    "ALPHANUM_EXTEND_REGEX",
    "ALPHANUM_PATH_REGEX",
    "ALPHANUM_KR_REGEX",
    "ALPHANUM_KR_SPACE_REGEX",
    "ALPHANUM_KR_HYPHEN_REGEX",
    "ALPHANUM_KR_HOST_REGEX",
    "ALPHANUM_KR_EXTEND_REGEX",
    "ALPHANUM_KR_PATH_REGEX",
    "ALPHANUM_KR_MN_REGEX",
    "ALPHANUM_KR_MN_SPACE_REGEX",
    "ALPHANUM_KR_MN_HYPHEN_REGEX",
    "ALPHANUM_KR_MN_HOST_REGEX",
    "ALPHANUM_KR_MN_EXTEND_REGEX",
    "ALPHANUM_KR_MN_PATH_REGEX",
    "KR_NUM_REGEX",
    "KR_NUM_SPACE_REGEX",
    "KR_NUM_HYPHEN_REGEX",
    "KR_NUM_HOST_REGEX",
    "KR_NUM_EXTEND_REGEX",
    "KR_NUM_PATH_REGEX",
    "REQUEST_ID_REGEX",
    "SPECIAL_CHARS_REGEX",
    "SPECIAL_CHARS_BASE_REGEX",
    "SPECIAL_CHARS_LOW_REGEX",
    "SPECIAL_CHARS_MEDIUM_REGEX",
    "SPECIAL_CHARS_HIGH_REGEX",
    "SPECIAL_CHARS_STRICT_REGEX",
]
