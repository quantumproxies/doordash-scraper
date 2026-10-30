"""Row types of each command, for editors and type checkers (rows are plain dicts)."""

from typing import Any, Dict, List, Optional

try:  # Python 3.8+
    from typing import TypedDict
except ImportError:  # pragma: no cover
    from typing_extensions import TypedDict  # type: ignore


class DoordashRestaurantsRow(TypedDict, total=False):
    """One row of `doordash-scraper restaurants` (doordash_restaurants v1.1.2)."""

    rank: int
    """Position in DoorDash's order for this city."""
    id: Optional[str]
    """DoorDash store id."""
    name: str
    """Restaurant name."""
    rating: Optional[float]
    """Average rating out of 5. Null on stores with too few ratings."""
    reviews: Optional[int]
    """Exact review count."""
    cuisine: Optional[str]
    """Primary cuisine."""
    price_range: Optional[str]
    """Price band ($ to $$$$)."""
    street: Optional[str]
    """Street address."""
    city: Optional[str]
    """City."""
    state: Optional[str]
    """State code."""
    postal_code: Optional[str]
    """ZIP code."""
    country: Optional[str]
    """Country."""
    image: Optional[str]
    """Store photo URL."""
    url: Optional[str]
    """Store page URL."""
    address: Optional[str]
    """Full address on one line as DoorDash prints it, ZIP included."""
    latitude: Optional[float]
    """Store latitude."""
    longitude: Optional[float]
    """Store longitude."""
    categories: Optional[List[str]]
    """Every cuisine/category tag on the store; `cuisine` is the primary one."""
    delivery_fee: Optional[str]
    """Delivery fee as displayed, e.g. "$0 delivery fee"."""
    distance: Optional[str]
    """Distance from the city centre, as displayed ("0.5 mi", "800 ft")."""
    eta_minutes: Optional[int]
    """Estimated delivery time in minutes when DoorDash shows one."""
    promotions: Optional[List[str]]
    """Promotion and highlight tags on the card, e.g. "$5 off on $35+", "Newly Added"."""
    popular_items: Optional[List[Dict[str, Any]]]
    """Up to 8 popular menu items: name, description, price, currency, image."""
    offers_pickup: Optional[bool]
    """True when the store offers pickup."""
    sponsored: Optional[bool]
    """True when the card is a sponsored placement."""
