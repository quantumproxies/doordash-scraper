"""Popular dishes of a city's DoorDash restaurants, one row per dish.

    python popular_items.py "Chicago, IL" --cuisine mexican

Flattens the popular menu items of every restaurant (up to 8 each) into one
row per dish with the restaurant, its cuisine and rating, the dish name,
description and price, and prints the median dish price per cuisine.
"""

import argparse
from collections import defaultdict
from statistics import median

from quanticdata_doordash_scraper import DoorDashScraper, write


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("location", help='US city and state, e.g. "Chicago, IL"')
    parser.add_argument("--cuisine", help='one cuisine, e.g. "mexican"')
    parser.add_argument("--max-results", type=int, default=50, help="restaurants to read (max 50)")
    parser.add_argument("--out", default="popular_items.csv")
    args = parser.parse_args()

    doordash = DoorDashScraper()
    run = doordash.restaurants(args.location, cuisine=args.cuisine, max_results=args.max_results)
    dishes = []
    by_cuisine = defaultdict(list)
    for r in run:
        for item in r.get("popular_items") or []:
            dishes.append({
                "restaurant_id": r.get("id"),
                "restaurant": r["name"],
                "cuisine": r.get("cuisine"),
                "restaurant_rating": r.get("rating"),
                "dish": item.get("name"),
                "description": item.get("description"),
                "price": item.get("price"),
                "currency": item.get("currency"),
            })
            if item.get("price"):
                by_cuisine[r.get("cuisine") or "other"].append(item["price"])

    for cuisine, prices in sorted(by_cuisine.items(), key=lambda c: -len(c[1])):
        print(f"{cuisine:<20} {len(prices):>4} dishes  median {median(prices):.2f}")
    write(dishes, args.out)
    print(f"{len(dishes)} dishes from {len(run)} restaurants written to {args.out}")


if __name__ == "__main__":
    main()
