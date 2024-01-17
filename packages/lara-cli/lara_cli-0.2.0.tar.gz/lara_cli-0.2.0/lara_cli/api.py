from requests import Session
from urllib.parse import urljoin


class APISession(Session):
    def __init__(self, base_url=None, token=None):
        super().__init__()
        self.token = token
        self.base_url = base_url

    def request(self, method, url, *args, **kwargs):
        headers = kwargs.get("headers", {})
        headers.setdefault(
            "User-Agent",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        )

        if self.token:
            headers.setdefault("Authorization", "Bearer " + self.token)

        kwargs["headers"] = headers

        joined_url = urljoin(self.base_url, url)

        return super().request(method, joined_url, *args, **kwargs)
