from enum import Enum


class Verdicts(Enum):
    FOUND = "FOUND: anchor + url"
    ANCHOR_MISMATCH = "PARTIAL FOUND: wrong anchor"
    REDIRECT_DETECTED = "ERROR: page redirect"
    LINK_MISMATCH = "PARTIAL FOUND: wrong url"
    LINK_DELETED = "DELETED: anchor + url"
    CAPTCHA_BLOCK = "BLOCKED: access forbidden from CF"
    NETWORK_ERROR = "ERROR: network issues"
    SERVER_ERROR = "ERROR: some server error"
    FALLBACK_NEEDED = "Rechecking by Playwright"