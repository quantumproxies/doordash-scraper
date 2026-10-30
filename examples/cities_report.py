"""Compare US cities by their DoorDash restaurants.

    python cities_report.py "Austin, TX" "Chicago, IL" "Denver, CO"

For each city it reads the restaurants DoorDash lists and writes the number of
restaurants, the median rating and review count, the median delivery time, the
share of restaurants with a promotion tag, the share offering pickup and the
five most common cuisines.
"""

import argparse
from collections import Counter
from statistics import median

from quanticdata_doordash_scraper import DoorDashScraper, write


def med(values):
    values = [v for v in values if v is not None]
    return median(values) if values else None


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("cities", nargs="+", help='US cities with state, e.g. "Austin, TX"')
    parser.add_argument("--out", default="cities_report.csv")
    args = parser.parse_args()

    doordash = DoorDashScraper()
    rows = []
    for city in args.cities:
        run = doordash.restaurants(city, max_results=50)
        n = len(run)
        if not n:
            print(f"{city}: no restaurants returned")
            continue
        cuisines = Counter(r["cuisine"] for r in run if r.get("cuisine"))
        rows.append({
            "city": city,
            "restaurants": n,
            "median_rating": med(r.get("rating") for r in run),
            "median_reviews": med(r.get("reviews") for r in run),
            "median_eta_minutes": med(r.get("eta_minutes") for r in run),
            "share_with_promotion": round(sum(1 for r in run if r.get("promotions")) / n, 2),
            "share_with_pickup": round(sum(1 for r in run if r.get("offers_pickup")) / n, 2),
            "top_cuisines": ", ".join(c for c, _ in cuisines.most_common(5)),
        })
        print(f"{city}: {n} restaurants, median rating {rows[-1]['median_rating']}, "
              f"median delivery {rows[-1]['median_eta_minutes']} min, top {rows[-1]['top_cuisines']}")

    write(rows, args.out)
    print(f"{len(rows)} cities written to {args.out}")


if __name__ == "__main__":
    main()
