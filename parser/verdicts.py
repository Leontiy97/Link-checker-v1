from enum import Enum


class verdicts(Enum):
    FOUND: "anchor + url found"
    LINK_DELETED: "anchor + url not found"
    ANCHOR_NOT_FOUND: "wrong anchor"
    LINK_MISMATCH: "anchor found, wrong url"
    REDIRECT_DETECTED: "page redirect"
    CAPTCHA_BLOCK: "access forbidden from CF"
    NETWORK_ERROR: "network error"
    SERVER_ERROR: "error during load page"