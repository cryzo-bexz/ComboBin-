from flask import Flask, Response
import requests

app = Flask(__name__)

BASE_URL = "http://astro.wisp.uno:13462"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/127.0.0.0 Safari/537.36"
}

# Proxy any path
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def mirror(path):
    try:
        url = f"{BASE_URL}/{path}"
        resp = requests.get(url, headers=HEADERS, timeout=10)

        # Fix content type
        content_type = resp.headers.get("content-type", "text/html")

        return Response(resp.content, status=resp.status_code, content_type=content_type)
    except Exception as e:
        return Response(f"<h1>Error</h1><pre>{e}</pre>", status=500)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
