import csv
from datetime import date, datetime
from zoneinfo import ZoneInfo
import airportsdata
from pathlib import Path
from math import radians, sin, cos, sqrt, atan2

BASE_DIR = Path(__file__).resolve().parent

AIRPORTS = airportsdata.load("IATA")
EARTH_RADIUS_KM = 6371
EARTH_CIRCUMFERENCE_KM = 40075
MOON_DISTANCE_KM = 384400
EARTH_ORBIT_KM = 939886000


def calculate_distance(from_airport, to_airport):
    lat1 = radians(AIRPORTS[from_airport]["lat"])
    lon1 = radians(AIRPORTS[from_airport]["lon"])

    lat2 = radians(AIRPORTS[to_airport]["lat"])
    lon2 = radians(AIRPORTS[to_airport]["lon"])

    lat_difference = lat2 - lat1
    lon_difference = lon2 - lon1

    a = (
        sin(lat_difference / 2) ** 2
        + cos(lat1)
        * cos(lat2)
        * sin(lon_difference / 2) ** 2
    )

    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return EARTH_RADIUS_KM * c


def load_flights(filename):
    flights = []

    with open(filename, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        required_columns = {
            "Date",
            "Airline",
            "Flight",
            "From",
            "To",
            "Aircraft Type Name",
            "Take off (Actual)",
            "Landing (Actual)",
            "Take off (Scheduled)",
            "Landing (Scheduled)"
        }
        if not required_columns.issubset(reader.fieldnames):
            raise ValueError(
                "CSV format not recognized. Please use a Flighty export CSV.")

        for row in reader:
            flight_date = date.fromisoformat(row["Date"])
            if flight_date > date.today():
                continue
            takeoff_text = row["Take off (Actual)"]
            landing_text = row["Landing (Actual)"]

            if not takeoff_text or not landing_text:
                takeoff_text = row["Take off (Scheduled)"]
                landing_text = row["Landing (Scheduled)"]

            duration = None

            if takeoff_text and landing_text:
                from_airport = row["From"]
                to_airport = row["To"]

                takeoff = datetime.fromisoformat(takeoff_text)
                landing = datetime.fromisoformat(landing_text)

                takeoff = takeoff.replace(
                    tzinfo=ZoneInfo(AIRPORTS[from_airport]["tz"])
                )

                landing = landing.replace(
                    tzinfo=ZoneInfo(AIRPORTS[to_airport]["tz"])
                )

                duration = (landing - takeoff).total_seconds() / 3600
            flight = {
                "date": row["Date"],
                "airline": row["Airline"],
                "flight": row["Flight"],
                "from": row["From"],
                "to": row["To"],
                "aircraft": row["Aircraft Type Name"],
                "takeoff": row["Take off (Actual)"],
                "landing": row["Landing (Actual)"],
                "duration": duration,
            }
            flights.append(flight)

    return flights


def analyze_flights(flights):
    flight_count = 0
    airline_count = {}
    route_count = {}
    aircraft_count = {}
    airport_count = {}
    total_duration = 0.0
    longest_duration = 0.0
    longest_flight = ""
    month_count = {}
    total_distance = 0.0
    unique_airports = set()
    unique_countries = set()
    for row in flights:
        flight_count += 1

        airline = row["airline"]
        airline_count[airline] = airline_count.get(airline, 0) + 1

        route = row['from'] + " -> " + row['to']

        route = row["from"] + " -> " + row["to"]
        route_count[route] = route_count.get(route, 0) + 1

        aircraft = row["aircraft"]
        aircraft_count[aircraft] = aircraft_count.get(aircraft, 0) + 1

        for airport in [row["from"], row["to"]]:
            unique_airports.add(airport)
            country = AIRPORTS[airport]["country"]
            unique_countries.add(country)
            airport_count[airport] = airport_count.get(airport, 0) + 1

        current_duration = row["duration"]

        if current_duration is not None:
            total_duration += current_duration

            if current_duration > longest_duration:
                longest_duration = current_duration
                longest_flight = row["flight"]

        month = row["date"][:7]
        month_count[month] = month_count.get(month, 0) + 1

        current_distance = calculate_distance(row["from"], row["to"])
        total_distance += current_distance

    earth_laps = total_distance / EARTH_CIRCUMFERENCE_KM
    moon_trips = total_distance / MOON_DISTANCE_KM
    sun_orbits = total_distance / EARTH_ORBIT_KM

    return {
        "flight_count": flight_count,
        "airline_count": airline_count,
        "route_count": route_count,
        "aircraft_count": aircraft_count,
        "airport_count": airport_count,
        "total_duration": total_duration,
        "longest_duration": longest_duration,
        "longest_flight": longest_flight,
        "month_count": month_count,
        "total_distance": total_distance,
        "earth_laps": earth_laps,
        "moon_trips": moon_trips,
        "sun_orbits": sun_orbits,
        "unique_airports": len(unique_airports),
        "unique_countries": len(unique_countries)
    }


def format_sun_orbits(value):
    if value >= 1:
        return f"{value:.1f}"
    elif value >= 0.1:
        return f"{value:.2f}"
    elif value >= 0.01:
        return f"{value:.3f}"
    elif value >= 0.001:
        return f"{value:.4f}"
    else:
        return f"{value:.6f}"


def print_report(results):
    most_used_airline = max(
        results["airline_count"],
        key=results["airline_count"].get
    )

    most_used_route = max(
        results["route_count"],
        key=results["route_count"].get
    )

    most_used_aircraft = max(
        results["aircraft_count"],
        key=results["aircraft_count"].get
    )

    most_visited_airport = max(
        results["airport_count"],
        key=results["airport_count"].get
    )

    print()
    print("FLIGHT HISTORY SUMMARY")
    print("----------------------")
    print(f"Total flights: {results['flight_count']}")
    print(f"Total flight time: {round(results['total_duration'])} hours")
    print(f"Total flight distance: {round(results['total_distance']):,} km")
    print(f"Airports visited: {results['unique_airports']}")
    print(f"Countries/regions visited: {results['unique_countries']}")

    print()
    print("TRAVEL EQUIVALENTS")
    print("------------------")
    print(f"Around Earth: {results['earth_laps']:.2f} times")
    print(f"Earth to Moon: {results['moon_trips']:.2f} times")
    print(
        f"Around the Sun: "
        f"{format_sun_orbits(results['sun_orbits'])} times"
    )

    print()
    print("FLIGHT HIGHLIGHTS")
    print("-----------------")
    print(f"Most used airline: {most_used_airline}")
    print(f"Most used route: {most_used_route}")
    print(f"Most used aircraft: {most_used_aircraft}")
    print(f"Most visited airport: {most_visited_airport}")
    print(
        f"Longest flight: {results['longest_flight']} - "
        f"{results['longest_duration']:.1f} hours"
    )

    print()
    print("FLIGHTS BY MONTH")
    print("----------------")
    for month in sorted(results["month_count"]):
        print(f"{month}: {results['month_count'][month]}")


def find_csv_file():
    csv_files = sorted(
        BASE_DIR.glob("FlightyExport-*.csv"),
        reverse=True
    )

    if csv_files:
        return csv_files[0]

    return BASE_DIR / "sample_flights.csv"


def main():
    filename = find_csv_file()

    print(f"Loading: {filename.name}")

    flights = load_flights(filename)
    results = analyze_flights(flights)
    print_report(results)


if __name__ == "__main__":
    main()
