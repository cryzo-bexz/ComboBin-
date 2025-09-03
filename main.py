from flask import Flask, request, Response
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
@import url('https://fonts.googleapis.com/css?family=Roboto+Mono');
.center-xy { top: 50%; left: 50%; transform: translate(-50%,-50%); position: absolute; }
html, body { font-family: 'Roboto Mono', monospace; font-size: 16px; background:#000; color:#fff; }
.container { width:100%; }
.copy-container { text-align:center; }
p { font-size:24px; margin:0; }
.handle { background:#ffe500; width:14px; height:30px; position:absolute; margin-top:1px; }
#cb-replay { fill:#666; width:20px; margin:15px; right:0; bottom:0; position:absolute; cursor:pointer; }
#cb-replay:hover { fill:#888; }
</style>
</head>
<body>
<div class="container">
  <div class="copy-container center-xy">
    <p>404, page not found.</p>
    <span class="handle"></span>
  </div>
</div>
<svg version="1.1" id="cb-replay" xmlns="http://www.w3.org/2000/svg" 
     viewBox="0 0 279.9 297.3"><g>
     <path d="M269.4,162.6c-2.7,66.5-55.6,120.1-121.8,123.9c-77,4.4-141.3-60-136.8-136.9C14.7,81.7,71,27.8,140,27.8c1.8,0,3.5,0,5.3,0.1c0.3,0,0.5,0.2,0.5,0.5v15c0,1.5,1.6,2.4,2.9,1.7l35.9-20.7c1.3-0.7,1.3-2.6,0-3.3L148.6,0.3c-1.3-0.7-2.9,0.2-2.9,1.7v15c0,0.3-0.2,0.5-0.5,0.5c-1.7-0.1-3.5-0.1-5.2-0.1C63.3,17.3,1,78.9,0,155.4C-1,233.8,63.4,298.3,141.9,297.3c74.6-1,135.1-60.2,138-134.3c0.1-3-2.3-5.4-5.3-5.4l0,0C271.8,157.6,269.5,159.8,269.4,162.6z"/>
</g></svg>
</body>
</html>
"""

@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def mirror(path):
    allowed_paths = ["", "about", "create", "pastebins"]

    # valid if root, allowed paths, or /<hwid>, /<hwid>/raw
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
