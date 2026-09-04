import csv
from datetime import date
from datetime import datetime
from zoneinfo import ZoneInfo
import airportsdata

AIRPORTS = airportsdata.load("IATA")


def load_flights(filename):
    flights = []

    with open(filename, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)

        for row in reader:
            flight_date = date.fromisoformat(row["Date"])
            if flight_date > date.today():
                continue
            takeoff_text = row["Take off (Actual)"]
            landing_text = row["Landing (Actual)"]

            duration_source = "actual"

            if not takeoff_text or not landing_text:
                takeoff_text = row["Take off (Scheduled)"]
                landing_text = row["Landing (Scheduled)"]
                duration_source = "scheduled"

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
                "duration_source": duration_source
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
    for row in flights:
        flight_count += 1

        if row['airline'] in airline_count:
            airline_count[row["airline"]] += 1
        else:
            airline_count[row['airline']] = 1

        route = row['from'] + " -> " + row['to']

        if route in route_count:
            route_count[route] += 1
        else:
            route_count[route] = 1

        aircraft = row['aircraft']
        if aircraft in aircraft_count:
            aircraft_count[aircraft] += 1
        else:
            aircraft_count[aircraft] = 1

        for airport in [row["from"], row["to"]]:
            if airport in airport_count:
                airport_count[airport] += 1
            else:
                airport_count[airport] = 1

        current_duration = row["duration"]

        if current_duration is not None:
            total_duration += current_duration

            if current_duration > longest_duration:
                longest_duration = current_duration
                longest_flight = row["flight"]

        month = row["date"][:7]
        if month in month_count:
            month_count[month] += 1
        else:
            month_count[month] = 1

    return {
        "flight_count": flight_count,
        "airline_count": airline_count,
        "route_count": route_count,
        "aircraft_count": aircraft_count,
        "airport_count": airport_count,
        "total_duration": total_duration,
        "longest_duration": longest_duration,
        "longest_flight": longest_flight,
        "month_count": month_count
    }


def print_report(results):
    print(f"Total flights: {results['flight_count']}")
    most_used_airline = max(
        results['airline_count'], key=results['airline_count'].get)
    print(f"Most used airline: {most_used_airline}")
    most_used_route = max(
        results['route_count'], key=results['route_count'].get)
    print(f"Most used route: {most_used_route}")
    most_used_aircraft = max(
        results['aircraft_count'], key=results['aircraft_count'].get)
    print(f"Most used aircraft: {most_used_aircraft}")
    most_visited_airport = max(
        results['airport_count'], key=results['airport_count'].get)
    print(f"Most visited airport: {most_visited_airport}")
    print(f"Total flight time: {round(results['total_duration'])} hours")
    print(f"Longest flight: {results['longest_flight']} - "
          f"{round(results['longest_duration'], 1)} hours")
    print("Flights by month:")
    for month in sorted(results["month_count"]):
        print(f"{month}: {results['month_count'][month]}")


def main():
    flights = load_flights("sample_flights.csv")
    results = analyze_flights(flights)
    print_report(results)


if __name__ == "__main__":
    main()
