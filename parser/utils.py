

def url_normalise(url: str):
    if url is None:
        return ""
    corrected_url = url.strip()
    if corrected_url[-1] == "/" and len(corrected_url) > 1:
        corrected_url = corrected_url[:-1]
    return corrected_url
