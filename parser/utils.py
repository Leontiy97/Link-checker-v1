from html import unescape
from urllib.parse import urlsplit, urlunsplit


def url_normalise(url: str):
    if url is None:
        return ""
    corrected_url = decode_url(url).strip()
    if not corrected_url:
        return ""
    if corrected_url[-1] == "/" and len(corrected_url) > 1:
        corrected_url = corrected_url[:-1]
    return corrected_url

def decode_url(url: str):
    split_url = urlsplit(url)
    if "xn--" in split_url.netloc:
        corrected_host = split_url.netloc.encode('ascii').decode('idna')
        split_url = split_url._replace(netloc=corrected_host)
        return urlunsplit(split_url)
    else:
        return url

def normalise_anchor(anchor: str) -> str:
    # Decode HTML (&rsquo; -> ', &#8217; -> ')
    anchor = unescape(anchor)
    replacements = {
        "\u2018": "'",  # ' -> '
        "\u2019": "'",  # ' -> '
        "\u201C": '"',  # " -> "
        "\u201D": '"',  # " -> "
        "\u2013": "-",  # – -> -
        "\u2014": "-",  # — -> -
        "\xa0": " ",  # non-breaking space -> regular space
    }
    for unicode_char, ascii_char in replacements.items():
        anchor = anchor.replace(unicode_char, ascii_char)

    return "".join(anchor.strip())