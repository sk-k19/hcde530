"""
Fetch app reviews from the HCDE 530 Week 4 API.

Documentation: https://brockcraft.github.io/docs/hcde530_api_documentation.html

The API exposes GET /reviews with pagination (offset, limit). Each review includes
'category' and 'helpful_votes'. This script pulls all pages, prints those fields,
and saves them to a CSV file next to this script.
"""

import csv
import json
import urllib.error
import urllib.request
from pathlib import Path


BASE_URL = "https://hcde530-week4-api.onrender.com"
REVIEWS_PATH = "/reviews"
PAGE_LIMIT = 100
OUTPUT_CSV = "reviews_category_helpful_votes.csv"


def fetch_page(offset: int, limit: int) -> dict:
    """Return parsed JSON for one GET /reviews page."""
    query = f"offset={offset}&limit={limit}"
    url = f"{BASE_URL}{REVIEWS_PATH}?{query}"
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as response:
        return json.loads(response.read().decode("utf-8"))


def main() -> None:
    out_path = Path(__file__).resolve().parent / OUTPUT_CSV
    rows: list[dict[str, object]] = []

    offset = 0
    total = None

    print(f"{'Category':<40} {'Helpful votes'}")
    print("-" * 55)

    while True:
        try:
            payload = fetch_page(offset=offset, limit=PAGE_LIMIT)
        except urllib.error.URLError as exc:
            raise SystemExit(f"Could not reach the API: {exc}") from exc
        except json.JSONDecodeError as exc:
            raise SystemExit(f"API did not return valid JSON: {exc}") from exc

        if total is None:
            total = int(payload["total"])

        batch = payload.get("reviews", [])
        returned = int(payload.get("returned", len(batch)))

        for review in batch:
            category = review.get("category", "")
            votes = review.get("helpful_votes", "")
            print(f"{str(category):<40} {votes}")
            rows.append({"category": category, "helpful_votes": votes})

        offset += returned
        if offset >= total or returned == 0:
            break

    fieldnames = ["category", "helpful_votes"]
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print()
    print(f"Wrote {len(rows)} rows to {out_path.name}")


if __name__ == "__main__":
    main()
