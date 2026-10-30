"""DoorDash Scraper API: DoorDash scraper for Python and the command line: restaurants delivering in a US city, with rating, exact review count, cuisine, price band, address, delivery fee, delivery time, promotions and popular menu items with prices, as JSON or CSV. Free and open source; sign in with your QuanticData account, no proxies or headless browser to run.

    from quanticdata_doordash_scraper import DoorDashScraper

    scraper = DoorDashScraper()   # saved login (`doordash-scraper login`) or QUANTICDATA_API_KEY
    run = scraper.restaurants(...)   # DoorDash restaurants delivering in a US city
"""

from typing import Any, Dict, Optional, Sequence, Union

from ._qd.client import Client, Run
from ._qd.errors import (APIError, AuthError, InsufficientCredit, InvalidInput, JobFailed, JobTimeout,
                         QuanticDataError, RateLimited)
from ._qd.output import write

__version__ = "0.1.0"
__all__ = ["DoorDashScraper", "Run", "write", "APIError", "AuthError", "InsufficientCredit", "InvalidInput",
           "JobFailed", "JobTimeout", "QuanticDataError", "RateLimited", "__version__"]


def _as_list(value: Any) -> Any:
    if value is None or isinstance(value, (list, tuple)):
        return list(value) if value is not None else None
    return [value]


class DoorDashScraper:
    """DoorDash Scraper API on the QuanticData Data API.

    Every method runs one collector and returns a :class:`Run`: iterate it for the
    rows (plain dicts, typed in ``types``), or save it with ``to_csv()``,
    ``to_json()``, ``to_jsonl()`` or ``to_dataframe()``.
    """

    def __init__(self, api_key: Optional[str] = None, *, timeout: float = 180.0) -> None:
        self.client = Client(api_key, user_agent="doordash-scraper/0.1.0 (+https://github.com/quantumproxies/doordash-scraper)", timeout=timeout)

    def restaurants(
        self, location: str,
        *,
        cuisine: Optional[str] = None,
        country: Optional[str] = None,
        max_results: Optional[int] = None,
        wait: bool = True,
        timeout: float = 900.0,
    ) -> Run:
        """Restaurants delivering in a US city — rating, exact review count, cuisine, address.

        Args:
            location: US city and state, e.g. "Austin, TX".
            cuisine: Narrow to one cuisine, e.g. "mexican" or "sushi". Each cuisine has its own list for the city, so running several cuisines covers more restaurants.
            country: Country to run the request from, as an ISO 3166-1 alpha-2 code (us, gb, de...).
            max_results: How many restaurants to deliver at most (1–50). You pay only for delivered restaurants.
            wait: False starts the run in the background and returns its id at once.
            timeout: seconds to wait for a background run before giving up.

        Returns up to 50 rows, one per restaurant: see ``types.DoordashRestaurantsRow``.
        """
        payload = {
            "location": location,
            "cuisine": cuisine,
            "country": country,
            "max_results": max_results,
        }
        return self.client.run_collector("doordash_restaurants", payload, wait=wait, timeout=timeout)
