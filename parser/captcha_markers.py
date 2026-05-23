class CaptchaMarkers:
    def __init__(self):
        self.markers = [
            "Server: cloudflare",
            "cf-ray",
            "Attention Required! | Cloudflare",
            "Checking your browser",
            "cf-challenge",
            "cf_challenge",
            "<div class='cf-turnstile'"
        ]

    def take_markers(self):
        all_markers = []
        for marker in self.markers:
            all_markers.append(marker)
        return all_markers
