# DoorDash Scraper API

[![ci](https://github.com/quantumproxies/doordash-scraper/actions/workflows/ci.yml/badge.svg)](https://github.com/quantumproxies/doordash-scraper/actions/workflows/ci.yml) ![python](https://img.shields.io/badge/python-3.9%2B-blue) ![license](https://img.shields.io/badge/license-MIT-green) ![dependencies](https://img.shields.io/badge/dependencies-none-brightgreen)

Scrape DoorDash restaurants from Python or the command line: the restaurants that deliver in a US city, with rating, exact review count, cuisine and category tags, price band, address and coordinates, delivery fee, delivery time, promotions and up to 8 popular menu items with their prices, as JSON or CSV. The code is free and open source (MIT). It runs on the QuanticData Data API, so there are no proxies to rotate and no headless browser to keep alive: sign in once and run a command.

```bash
pip install git+https://github.com/quantumproxies/doordash-scraper
doordash-scraper login
doordash-scraper restaurants "Austin, TX" --max-results 50 -o austin.csv
```

`login` opens the QuanticData sign-in page in your browser. New accounts get $2 of free usage every month, no card required: [create one](https://app.quanticdata.io/register?utm_source=github&utm_medium=readme&utm_campaign=doordash-scraper).

## What it scrapes

| Command | Input | Returns | Per run |
|---|---|---|---|
| `doordash-scraper restaurants` | US city and state, optional cuisine | Rating, exact review count, cuisine, address, 25 fields per row ([fields and price](https://quanticdata.io/collectors/doordash-scraper-api/?utm_source=github&utm_medium=readme&utm_campaign=doordash-scraper)) | up to 50 |

A location is a US city and state, e.g. "Austin, TX". One run returns up to 50 restaurants for that city; add `--cuisine mexican`, `--cuisine sushi` and so on to collect each cuisine's own list. Every row carries the exact review count, the delivery fee and delivery time as DoorDash shows them, promotion tags and up to 8 popular menu items with name, description, price and image.

## Sample output

A real row from `doordash-scraper restaurants "Austin, TX" --max-results 3` (2026-10-23):

```json
{
  "id": "24726613",
  "url": "https://www.doordash.com/store/pardon-my-cheesesteak-austin-24726613/",
  "city": "Austin",
  "name": "Pardon My Cheesesteak",
  "rank": 1,
  "image": "https://img.cdn4dd.com/cdn-cgi/image/fit=contain,format=auto/https://doordash-static.s3.amazonaws.com/media/store/header/6da5bbe5-dae0-4186-9660-ca8acade860b.png",
  "state": "TX",
  "rating": 3.8,
  "street": "707 East Cesar Chavez Street",
  "address": "707 E Cesar Chavez St, Austin, TX 78701, USA",
  "country": "United States",
  "cuisine": "American",
  "reviews": 368,
  "distance": "0.5 mi",
  "latitude": 30.261007,
  "longitude": -97.737341,
  "sponsored": false,
  "categories": [
    "American",
    "Fast Food"
  ],
  "promotions": [
    "$5 off on $35+"
  ],
  "eta_minutes": 29,
  "postal_code": "78701",
  "price_range": "$$",
  "delivery_fee": "$0 delivery fee",
  "offers_pickup": false,
  "popular_items": [
    {
      "name": "Cheesesteak",
      "image": "https://img.cdn4dd.com/cdn-cgi/image/fit=contain,format=auto/https://doordash-static.s3.amazonaws.com/media/photosV2/5c87a61e-2c67-4486-a5ec-38dbd001ccb7-779cfa7a-35a4-43e5-9504-83e339cabe52-retina-large.JPG",
      "price": 16.53,
      "currency": "USD",
      "description": "Thinly sliced steak with melted provolone, cheese sauce & caramelized onions on a toasted hoagie roll."
    },
    {
      "name": "Chipotle Cheesesteak",
      "image": "https://img.cdn4dd.com/cdn-cgi/image/fit=contain,format=auto/https://doordash-static.s3.amazonaws.com/media/photosV2/cd1acb07-728f-4fe4-b4d4-4e34313d3390-e71dfdcd-06c0-43da-8040-a49e4f894a35-retina-large.JPG",
      "price": 17.14,
      "currency": "USD",
      "description": "Thinly sliced steak with melted provolone, cheese sauce & caramelized onions, doused with chipotle sauce on a toasted hoagie roll."
    }
  ]
}
```

## Python

```python
from quanticdata_doordash_scraper import DoorDashScraper

doordash = DoorDashScraper()  # saved login, or QUANTICDATA_API_KEY

austin = doordash.restaurants("Austin, TX", max_results=50)
for r in austin:
    print(r["name"], r["cuisine"], r["rating"], r["reviews"], r["delivery_fee"], r["eta_minutes"])
austin.to_csv("austin.csv")

mexican = doordash.restaurants("Chicago, IL", cuisine="mexican", max_results=50)
for r in mexican:
    for item in r["popular_items"] or []:
        print(r["name"], item["name"], item["price"])
```

Each call returns a `Run`: iterate it for the rows (plain dicts), take `len()`, or save it with `to_csv()`, `to_json()`, `to_jsonl()` or `to_dataframe()` (pandas). Errors are specific: `InsufficientCredit`, `RateLimited`, `InvalidInput`, `JobFailed`, `AuthError`.

## Examples

- **Restaurants by cuisine**: Run one city across several cuisines and get one deduplicated CSV of restaurants with rating, review count, address and delivery details. See [`examples/cuisines_to_csv.py`](examples/cuisines_to_csv.py).
- **Popular dish prices**: Turn the popular items of a city's restaurants into one row per dish with its price, and see the median dish price per cuisine. See [`examples/popular_items.py`](examples/popular_items.py).
- **City comparison**: Compare several cities by restaurant count, median rating, median delivery time, share with a promotion and the most common cuisines. See [`examples/cities_report.py`](examples/cities_report.py).

## Command line

Results print as a table; `-o file.csv`, `-o file.json` or `-o file.jsonl` writes a file. List inputs take `a b c`, `a,b,c`, `@file.txt` (one per line) or `-` (stdin). `--no-wait` starts a long run in the background and prints its id; `doordash-scraper run <id> -o out.csv` collects it later.

### `doordash-scraper restaurants`

Restaurants delivering in a US city — rating, exact review count, cuisine, address.

```
doordash-scraper restaurants LOCATION [options]
```

| Option | Type | Default | Description |
|---|---|---|---|
| `LOCATION` | string |  | US city and state, e.g. "Austin, TX". |
| `--cuisine` | string |  | Narrow to one cuisine, e.g. "mexican" or "sushi". Each cuisine has its own list for the city, so running several cuisines covers more restaurants. |
| `--country` | string |  | Country to run the request from, as an ISO 3166-1 alpha-2 code (us, gb, de...). |
| `--max-results` | integer | `50` | How many restaurants to deliver at most (1–50). You pay only for delivered restaurants. |

## Output fields

<details><summary><code>doordash-scraper restaurants</code>: 25 fields</summary>

| Field | Type | Description |
|---|---|---|
| `rank` | integer | Position in DoorDash's order for this city. |
| `id` | string or null | DoorDash store id. |
| `name` | string | Restaurant name. |
| `rating` | number or null | Average rating out of 5. Null on stores with too few ratings. |
| `reviews` | integer or null | Exact review count. |
| `cuisine` | string or null | Primary cuisine. |
| `price_range` | string or null | Price band ($ to $$$$). |
| `street` | string or null | Street address. |
| `city` | string or null | City. |
| `state` | string or null | State code. |
| `postal_code` | string or null | ZIP code. |
| `country` | string or null | Country. |
| `image` | string or null | Store photo URL. |
| `url` | string or null | Store page URL. |
| `address` | string or null | Full address on one line as DoorDash prints it, ZIP included. |
| `latitude` | number or null | Store latitude. |
| `longitude` | number or null | Store longitude. |
| `categories` | string[] or null | Every cuisine/category tag on the store; `cuisine` is the primary one. |
| `delivery_fee` | string or null | Delivery fee as displayed, e.g. "$0 delivery fee". |
| `distance` | string or null | Distance from the city centre, as displayed ("0.5 mi", "800 ft"). |
| `eta_minutes` | integer or null | Estimated delivery time in minutes when DoorDash shows one. |
| `promotions` | string[] or null | Promotion and highlight tags on the card, e.g. "$5 off on $35+", "Newly Added". |
| `popular_items` | object[] or null | Up to 8 popular menu items: name, description, price, currency, image. |
| `offers_pickup` | boolean or null | True when the store offers pickup. |
| `sponsored` | boolean or null | True when the card is a sponsored placement. |

</details>

## Sign-in and API keys

- `doordash-scraper login` signs you in with OAuth 2.1 and PKCE in the browser. The token is stored in `~/.config/quanticdata/credentials.json` (readable only by you) and refreshed automatically. One login serves every QuanticData tool on the machine.
- No browser on the machine (SSH, Docker, Colab): run `doordash-scraper login --no-browser`, open the link anywhere, then paste back the address the browser ends on.
- Scripts and CI: set `QUANTICDATA_API_KEY` to a key from the dashboard, or store one with `doordash-scraper login --api-key`.
- `doordash-scraper logout` revokes the token. The connection is listed under API keys in the dashboard as "API · QuanticData CLI"; deleting that key disconnects every machine that uses it.

## Pricing

The code is free and MIT-licensed. Runs are billed to your QuanticData account per delivered row, at the price shown on each collector page linked above; $2 of usage is free every month and failed runs are never billed. Plans with higher limits: [pricing](https://quanticdata.io/pricing/?utm_source=github&utm_medium=readme&utm_campaign=doordash-scraper).

## Other ways to call it

The same data over plain HTTP:

```bash
curl -X POST https://api.quanticdata.io/v1/scraper/collectors/doordash_restaurants/run \
  -H "Authorization: Bearer $QUANTICDATA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"input": {"location": "Austin, TX", "max_results": 3}}'
```

- [API reference](https://quanticdata.io/docs/?utm_source=github&utm_medium=readme&utm_campaign=doordash-scraper) with Python, Node, PHP and curl examples.
- [MCP server](https://quanticdata.io/mcp-server/?utm_source=github&utm_medium=readme&utm_campaign=doordash-scraper) to give Claude, Cursor or any MCP client the same tools.
- [n8n node](https://github.com/quantumproxies/n8n-nodes-quanticdata) for no-code workflows.

## FAQ

**Is this DoorDash scraper free?**

The code is free and MIT-licensed. Scraping runs on your QuanticData account: $2 of usage is free every month with no card, then you pay per delivered row at the price shown on each collector page. Failed runs are never billed.

**Do I need proxies or a headless browser?**

No. You send a US city and, if you want, a cuisine, and get rows back; the requests run on QuanticData's side. It reads public city pages only; you are responsible for respecting DoorDash's terms.

**Does it return menu items?**

Each restaurant row carries up to 8 popular menu items with name, description, price, currency and image, as DoorDash shows them for the restaurant on the city page.

**How many restaurants can one run return?**

Up to 50 restaurants per run; ask for fewer with --max-results and you pay only for what is delivered. Add --cuisine to collect each cuisine's own list for the same city.

**Can I export to CSV or Excel?**

Add -o restaurants.csv (or .json, .jsonl). Category and promotion tags are joined with '; ' and the popular items are written as JSON text in one cell, so the CSV opens cleanly in Excel or Google Sheets.

**Can I run it on a schedule?**

Yes. Set QUANTICDATA_API_KEY in the environment and call the CLI or examples/cities_report.py from cron, GitHub Actions or any scheduler.

## Related scrapers

- [Google Maps Scraper](https://github.com/quantumproxies/google-maps-scraper): Google Maps scraper for Python and the command line.
- [Trustpilot Scraper](https://github.com/quantumproxies/trustpilot-scraper): Trustpilot scraper for Python and the command line.

## License

MIT. Built and maintained by [QuanticData](https://quanticdata.io/?utm_source=github&utm_medium=readme&utm_campaign=doordash-scraper).
