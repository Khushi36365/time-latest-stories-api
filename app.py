from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.request
import json
import re

HOST = "localhost"
PORT = 8000

def fetch_latest_stories():
    try:
        url = "https://time.com"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req) as response:
            html = response.read().decode("utf-8", errors="ignore")

        stories = []
        seen_links = set()

        # Find all href=" /6142390/... " style article links
        pos = 0
        while len(stories) < 6:
            href_pos = html.find('href="', pos)
            if href_pos == -1:
                break
            href_pos += len('href="')
            href_end = html.find('"', href_pos)
            link = html[href_pos:href_end]

            # only real Time.com articles contain "/6142..."
            if re.search(r'/\d+/', link) and link not in seen_links:
                full_link = link if link.startswith("http") else "https://time.com" + link
                seen_links.add(link)

                # extract title text near the link
                title_end = html.find("</a>", href_end)
                title_start = html.rfind(">", 0, title_end)
                title = html[title_start+1:title_end].strip()

                if title:
                    stories.append({"title": title, "link": full_link})

            pos = href_end

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
