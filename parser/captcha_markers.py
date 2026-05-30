class CaptchaMarkers:
    def __init__(self):
        self.markers = [
            "Server: cloudflare",
            "cf-ray",
            "Attention Required! | Cloudflare",
            "Checking your browser",
            "cf-challenge",
            "cf_challenge",
            "<div class='cf-turnstile'",
            "https://challenges.cloudflare.com"
        ]

    def take_markers(self):
        all_markers = []
        for marker in self.markers:
            all_markers.append(marker)
        return all_markers

def captcha_is_detected(html) -> bool:
    html_text = str(html).lower()
    for marker in CaptchaMarkers().take_markers():
        if marker.lower() in html_text:
            return True
    return False
