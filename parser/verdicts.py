from enum import Enum


class Verdicts(Enum):
    FOUND = "FOUND: anchor + url"
    LINK_DELETED = "DELETED: anchor + url"
    ANCHOR_NOT_FOUND = "PARTIAL FOUND: wrong anchor"
    LINK_MISMATCH = "PARTIAL FOUND: wrong url"
    REDIRECT_DETECTED = "ERROR: page redirect"
    CAPTCHA_BLOCK = "BLOCKED: access forbidden from CF"
    NETWORK_ERROR = "ERROR: network issues"
    SERVER_ERROR = "ERROR: some server error"