from flask import Flask, Response, request
import requests

app = Flask(__name__)

BASE_URL = "http://astro.wisp.uno:13462"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/127.0.0.0 Safari/537.36",
    "Accept": "*/*",
}

@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def mirror(path):
    target = f"{BASE_URL}/{path}" if path else f"{BASE_URL}/"

    # Append query params if present
    if request.query_string:
        target += "?" + request.query_string.decode("utf-8")

    try:
        resp = requests.get(target, headers=HEADERS, timeout=15)
        return Response(
            resp.content,
            status=resp.status_code,
            content_type=resp.headers.get("content-type", "application/octet-stream"),
        )
    except Exception as e:
        return Response(f"<h1>Proxy error</h1><pre>{e}</pre>", status=500)

def handler(request, *args, **kwargs):
    with app.request_context(request.environ):
        return app.full_dispatch_request()
