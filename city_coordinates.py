import json
from urllib.error import URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
USER_AGENT = "city-coordinate-lookup/1.0"


def find_city_coordinates(city: str) -> tuple[float, float] | None:
    """Return a city's latitude and longitude, or None if it isn't found."""
    query = urlencode({"q": city, "format": "jsonv2", "limit": 1})
    request = Request(
        f"{NOMINATIM_URL}?{query}",
        headers={"User-Agent": USER_AGENT},
    )

    try:
        with urlopen(request, timeout=10) as response:
            results = json.load(response)
    except (URLError, TimeoutError, json.JSONDecodeError) as error:
        raise RuntimeError(f"Could not look up the city: {error}") from error

    if not results:
        return None

    return float(results[0]["lat"]), float(results[0]["lon"])


def main() -> None:
    city = input("Enter a city: ").strip()
    if not city:
        print("Please enter a city name.")
        return

    try:
        coordinates = find_city_coordinates(city)
    except (RuntimeError, KeyError, ValueError) as error:
        print(error)
        return

    if coordinates is None:
        print(f"No results found for {city!r}.")
        return

    latitude, longitude = coordinates
    print(f"{city}: latitude {latitude:.6f}, longitude {longitude:.6f}")


if __name__ == "__main__":
    main()
