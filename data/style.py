from enum import Enum


class Style(Enum):
    RESET_STYLE = '\033[0m'
    ERR_STYLE = '\033[37;5;41m'
    INFO_STYLE = '\033[30;42m'
    BG_HIGHLIGHT = '\033[43m'
    TXT_ERR_STYLE = '\033[31m'
    TXT_HIGHLIGHT = '\033[33m'
