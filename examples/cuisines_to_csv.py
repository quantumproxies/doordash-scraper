"""DoorDash restaurants of one city across several cuisines, in one CSV.

    python cuisines_to_csv.py "Austin, TX" mexican pizza sushi thai burgers

Runs the city once per cuisine (each cuisine has its own list on DoorDash) and
writes every restaurant once, matched by its DoorDash store id, with the
cuisine search it first came from. With no cuisine given it runs the city's
main list only.
"""

import argparse

from quanticdata_doordash_scraper import DoorDashScraper, write


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("location", help='US city and state, e.g. "Austin, TX"')
    parser.add_argument("cuisines", nargs="*", help='cuisines, e.g. mexican pizza sushi')
    parser.add_argument("--out", default="doordash_restaurants.csv")
    args = parser.parse_args()

    doordash = DoorDashScraper()
    rows, seen = [], set()
    for cuisine in args.cuisines or [None]:
        run = doordash.restaurants(args.location, cuisine=cuisine, max_results=50)
        added = 0
        for r in run:
            key = r.get("id") or r.get("url")
            if key in seen:
                continue
            seen.add(key)
            rows.append({"searched_cuisine": cuisine or "", **r})
            added += 1
        print(f"{cuisine or 'all'}: {len(run)} restaurants, {added} new")

    write(rows, args.out)
    print(f"{len(rows)} restaurants written to {args.out}")


if __name__ == "__main__":
    main()
