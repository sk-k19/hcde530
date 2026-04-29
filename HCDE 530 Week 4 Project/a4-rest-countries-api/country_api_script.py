import csv
from pathlib import Path

import requests


# This script uses the REST Countries API to collect country level data
# This is the API address I am asking for data from
# The "/ all" endpoint returns country records from the REST Countries API
API_URL = "https://restcountries.com/v3.1/all"

# The REST Countries "all" endpoint requires a fields parameter.
# I am using the fields parameter so the API only sends back the country details I need
# This keeps the response focused instead of downloading every possible key.
PARAMS = {
    "fields": "name,cca2,region,subregion,population,languages,currencies,timezones"
}

OUTPUT_FILE = Path("countries_localization_data.csv")


def format_languages(languages):
    """Turn the API's languages dictionary into a readable text string."""
    if not languages:
        return "Not listed"

    # The API returns languages as a dictionary, such as {"eng": "English"}.
    # For the CSV, only the language names are easier to read.
    return "; ".join(sorted(languages.values()))


def format_currencies(currencies):
    """Turn the API's currencies dictionary into a readable text string."""
    if not currencies:
        return "Not listed"

    readable_currencies = []

    # The API returns currencies as nested dictionaries.
    # Example: {"USD": {"name": "United States dollar", "symbol": "$"}}
    # So I pull out the name, code, and symbol for each currency. This makes it easier to read in one CSV cell
    for currency_code, currency_info in currencies.items():
        currency_name = currency_info.get("name", "Unknown currency")
        currency_symbol = currency_info.get("symbol", "")

        if currency_symbol:
            readable_currencies.append(f"{currency_name} ({currency_code}, {currency_symbol})")
        else:
            readable_currencies.append(f"{currency_name} ({currency_code})")

    return "; ".join(sorted(readable_currencies))


def main():
    # This sends my request to the API
    # The URL says which API endpoint to call, and PARAMS tells the API which fields we want back
    response = requests.get(API_URL, params=PARAMS, timeout=20)

    # If the API call fails, this stops the script and prints a useful error.
    response.raise_for_status()

    # The API returns JSON, which is structured data from the web
    # This line turns that JSON into Python data I can loop through
    countries = response.json()

 # I expect the API response to be a list, where each item is one country.
    # This check helps catch unexpected API responses before the script tries to process them.
    if not isinstance(countries, list):
        raise ValueError("Expected the API response to be a list of countries.")

    rows = []

    for country in countries:
        name_info = country.get("name", {})
        languages = country.get("languages", {})
        currencies = country.get("currencies", {})
        timezones = country.get("timezones", [])

    # This is the data that is being extracted from the API.
    # This is the data I am choosing to extract from each country record.
        row = {
            "country_name": name_info.get("common", "Unknown"),
            "official_name": name_info.get("official", "Unknown"),
            "country_code": country.get("cca2", "Unknown"),
            "region": country.get("region", "Not listed"),
            "subregion": country.get("subregion", "Not listed"),
            "population": country.get("population", 0),
            "languages": format_languages(languages),
            "language_count": len(languages),
            "currencies": format_currencies(currencies),
            "currency_count": len(currencies),
            "timezones": "; ".join(timezones) if timezones else "Not listed",
            "timezone_count": len(timezones),
        }

        rows.append(row)

    # Sorting alphabetically makes the CSV easier for a reviewer to scan.
    rows.sort(key=lambda item: item["country_name"])

    # This saves the structured API data into a readable CSV file.
    with OUTPUT_FILE.open("w", newline="", encoding="utf-8") as csv_file:
        fieldnames = [
            "country_name",
            "official_name",
            "country_code",
            "region",
            "subregion",
            "population",
            "languages",
            "language_count",
            "currencies",
            "currency_count",
            "timezones",
            "timezone_count",
        ]

        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Saved {len(rows)} country records to {OUTPUT_FILE}")
# This prints a small preview so I can quickly check that the script worked without having to open the whole CSV file first
    print("\nSample records:")
    for row in rows[:5]:
        print(
            f"{row['country_name']} | "
            f"Region: {row['region']} | "
            f"Languages: {row['languages']} | "
            f"Time zones: {row['timezone_count']}"
        )


if __name__ == "__main__":
    main()
