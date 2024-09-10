from terminal_app.curlify import Curlify

from requests import Request

req = Request(method="GET", url="http://localhost:7773/1:jazzXR/status").prepare()

curl = Curlify(req).to_curl()
print(curl)
