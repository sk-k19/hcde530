"""
Analyze app reviews from the HCDE 530 Week 4 API.

Documentation: https://brockcraft.github.io/docs/hcde530_api_documentation.html

1. Calls the API base at https://hcde530-week4-api.onrender.com/ using GET /reviews.
2. Fetches all pages, then:
   - Filters reviews to those with rating >= 4 (simple, useful condition).
   - Counts how many filtered reviews fall in each category.
   - Finds the filtered review with the highest and lowest helpful_votes.
4. Saves a small summary CSV next to this script.
"""

import csv
import json
import urllib.error
import urllib.request
from collections import Counter
from pathlib import Path


BASE_URL = "https://hcde530-week4-api.onrender.com"
REVIEWS_PATH = "/reviews"
PAGE_LIMIT = 100
OUTPUT_CSV = "reviews_analysis_summary.csv"

# Simple filter you can change: keep only fairly positive reviews.
MIN_RATING = 4


def fetch_page(offset: int, limit: int) -> dict:
    """Return parsed JSON for one GET /reviews page."""
    query = f"offset={offset}&limit={limit}"
    url = f"{BASE_URL}{REVIEWS_PATH}?{query}"
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as response:
        return json.loads(response.read().decode("utf-8"))


def fetch_all_reviews() -> list[dict]:
    """Download every review using offset/limit pagination."""
    all_reviews: list[dict] = []
    offset = 0
    total = None

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
        all_reviews.extend(batch)

        offset += returned
        if offset >= total or returned == 0:
            break

    return all_reviews


def main() -> None:
    out_path = Path(__file__).resolve().parent / OUTPUT_CSV

    reviews = fetch_all_reviews()
    print(f"Fetched {len(reviews)} reviews (API total).")

    filtered = [r for r in reviews if int(r.get("rating", 0)) >= MIN_RATING]
    print(f"Filter: rating >= {MIN_RATING}  ->  {len(filtered)} reviews kept.\n")

    if not filtered:
        raise SystemExit("No reviews matched the filter; nothing to analyze.")

    category_counts = Counter(str(r.get("category", "")).strip() for r in filtered)

    top_by_votes = max(filtered, key=lambda r: int(r.get("helpful_votes", 0)))
    bottom_by_votes = min(filtered, key=lambda r: int(r.get("helpful_votes", 0)))

    print("Counts by category (filtered):")
    for category, count in sorted(category_counts.items(), key=lambda x: (-x[1], x[0])):
        print(f"  {count:>4}  {category}")

    print("\nHighest helpful_votes (within filtered set):")
    print(
        f"  id={top_by_votes.get('id')}  votes={top_by_votes.get('helpful_votes')}  "
        f"app={top_by_votes.get('app')}  category={top_by_votes.get('category')}"
    )
    print("\nLowest helpful_votes (within filtered set):")
    print(
        f"  id={bottom_by_votes.get('id')}  votes={bottom_by_votes.get('helpful_votes')}  "
        f"app={bottom_by_votes.get('app')}  category={bottom_by_votes.get('category')}"
    )

    summary_rows: list[dict[str, str]] = [
        {"row_type": "meta", "key": "filter", "value": f"rating>={MIN_RATING}"},
        {"row_type": "meta", "key": "total_fetched", "value": str(len(reviews))},
        {"row_type": "meta", "key": "filtered_count", "value": str(len(filtered))},
    ]

    for category, count in sorted(category_counts.items(), key=lambda x: (-x[1], x[0])):
        summary_rows.append(
            {"row_type": "category_count", "key": category, "value": str(count)}
        )

    summary_rows.extend(
        [
            {
                "row_type": "extreme",
                "key": "max_helpful_votes",
                "value": str(top_by_votes.get("helpful_votes", "")),
                "id": str(top_by_votes.get("id", "")),
                "app": str(top_by_votes.get("app", "")),
                "category": str(top_by_votes.get("category", "")),
            },
            {
                "row_type": "extreme",
                "key": "min_helpful_votes",
                "value": str(bottom_by_votes.get("helpful_votes", "")),
                "id": str(bottom_by_votes.get("id", "")),
                "app": str(bottom_by_votes.get("app", "")),
                "category": str(bottom_by_votes.get("category", "")),
            },
        ]
    )

    fieldnames = ["row_type", "key", "value", "id", "app", "category"]
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in summary_rows:
            writer.writerow(
                {
                    "row_type": row.get("row_type", ""),
                    "key": row.get("key", ""),
                    "value": row.get("value", ""),
                    "id": row.get("id", ""),
                    "app": row.get("app", ""),
                    "category": row.get("category", ""),
                }
            )

    print(f"\nWrote analysis summary to {out_path.name}")


if __name__ == "__main__":
    main()
