from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.request
import json

HOST = "localhost"
PORT = 8000

def fetch_latest_stories():
    try:
        # fetch the JSON feed that Time.com uses internally for the Latest Stories section
        url = "https://time.com/index.json"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode("utf-8", errors="ignore"))

        stories = []
        for item in data.get("latest", [])[:6]:
            stories.append({
                "title": item.get("headline", "").strip(),
                "link": item.get("url", "").strip()
            })

        return stories
    except Exception as e:
        print("ERROR:", e)
        return []


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path != "/getTimeStories":
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Invalid endpoint")
            return

        stories = fetch_latest_stories()

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(stories, indent=2).encode("utf-8"))


if __name__ == "__main__":
    server = HTTPServer((HOST, PORT), RequestHandler)
    print(f"Server running on http://{HOST}:{PORT}/getTimeStories")
    server.serve_forever()
