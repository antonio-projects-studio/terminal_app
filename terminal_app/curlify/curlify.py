from requests import PreparedRequest


class Curlify:
    def __init__(self, request: PreparedRequest, compressed=False, verify=True):
        self.request = request
        self.compressed = compressed
        self.verify = verify

    def headers(self) -> str:
        """organize headers

        Returns:
            str: return string of set headers
        """
        headers = [f'"{k}: {v}"' for k, v in self.request.headers.items()]

        return " -H ".join(headers)

    def body(self) -> str | None:
        return (
            self.request.body
            if isinstance(self.request.body, str | None)
            else str(self.request.body, "utf-8")
        )

    def to_curl(self) -> str:
        """build curl command

        Returns:
            str: string represents curl command
        """
        curl = f"curl -X {self.request.method}{f" -H {self.headers()}" if self.headers() else ""}{f" -d '{self.body()}'" if self.body() else ""} {self.request.url}"

        if self.compressed:
            curl += " --compressed"
        if not self.verify:
            curl += " --insecure"

        return curl
