import csv


def load_flights():
    flights = []

    with open('flights.csv', 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)

        for row in reader:
            flights.append(row)

    return flights


def analyze_flights(flights):
    flight_count = 0
    total_duration = 0.0
    longest_duration = 0.0
    longest_flight = ""
    airline_count = {}
    route_count = {}
    for row in flights:
        flight_count += 1
        current_duration = float(row['duration'])
        total_duration += current_duration
        if current_duration > longest_duration:
            longest_duration = current_duration
            longest_flight = row['flight']

        if row['airline'] in airline_count:
            airline_count[row["airline"]] += 1
        else:
            airline_count[row['airline']] = 1

        route = row['from'] + " -> " + row['to']

        if route in route_count:
            route_count[route] += 1
        else:
            route_count[route] = 1
    return {
        "flight_count": flight_count,
        "total_duration": total_duration,
        "longest_duration": longest_duration,
        "longest_flight": longest_flight,
        "airline_count": airline_count,
        "route_count": route_count
    }


def print_report(results):
    print(f"Total flights: {results['flight_count']}")
    print(f"Total flight time: {results['total_duration']} hours")
    print(
        f"Longest flight: {results['longest_flight']} - {results['longest_duration']} hours")
    most_used_airline = max(
        results['airline_count'], key=results['airline_count'].get)
    print(f"Most used airline: {most_used_airline}")
    most_used_route = max(results['route_count'],
                          key=results['route_count'].get)
    print(f"Most used route: {most_used_route}")


def main():
    flights = load_flights()
    results = analyze_flights(flights)
    print_report(results)


if __name__ == "__main__":
    main()
