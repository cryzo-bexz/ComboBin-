from flask import Flask, Response
import requests

app = Flask(__name__)

BASE_URL = "http://astro.wisp.uno:13462"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive",
}

NOT_FOUND_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>404</title>
<style>
body { background:#000; color:#fff; font-family:monospace; }
.copy-container { text-align:center; margin-top:20%; }
p { font-size:24px; }
</style>
</head>
<body>
  <div class="copy-container">
    <p>404, page not found.</p>
  </div>
</body>
</html>
"""

@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def mirror(path):
    allowed_paths = ["", "about", "create", "pastebins"]

    if path in allowed_paths or len(path) == 8 or (len(path.split("/")[0]) == 8 and path.endswith("/raw")):
        url = f"{BASE_URL}/{path}"
        try:
            resp = requests.get(url, headers=HEADERS, timeout=5)
            return Response(resp.content,
                            status=resp.status_code,
                            content_type=resp.headers.get("content-type", "text/html"))
        except Exception as e:
            return Response(f"<h1>Error</h1><pre>{e}</pre>", status=500)
    else:
        return Response(NOT_FOUND_HTML, status=404, mimetype="text/html")

# 👇 Expose to Vercel as handler
def handler(request, *args, **kwargs):
    with app.request_context(request.environ):
        response = app.full_dispatch_request()
        return response
