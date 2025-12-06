# Time Latest Stories API

This project contains a custom API service that returns the **latest 3 news stories from Time.com** by parsing the homepage using a **basic string-based approach** (no external parsing libraries), as required in the assignment.

---

## Features
- Fetches homepage of **https://time.com**
- Extracts **latest 3 story titles + links**
- Uses **only core Python modules**
- No HTML parsing libraries (BeautifulSoup, lxml, etc.)
- JSON API response format
- Accessible locally at: `http://localhost:8000/getTimeStories`

---

## Endpoint

| Method | URL |
|--------|-----|
| **GET** | `http://localhost:8000/getTimeStories` |

### Example Response
```json
[
  {
    "title": "Story Title Example",
    "link": "https://time.com/123456/example"
  },
  {
    "title": "Another Example Title",
    "link": "https://time.com/654321/another-example"
  }
]
