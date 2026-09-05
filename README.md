# Flight History Analyzer

A Python project that analyzes Flighty flight history data from a CSV file and generates travel statistics and distance insights.

## Features

- Total number of flights
- Total flight time
- Total flight distance
- Longest flight
- Most used airline
- Most used route
- Most used aircraft
- Most visited airport
- Number of airports visited
- Number of countries/regions visited
- Flights grouped by month
- Automatic Flighty CSV detection
- Great-circle distance calculation between airports
- Travel distance equivalents:
  - Trips around Earth
  - Earth-to-Moon distances
  - Equivalent orbits around the Sun
- Future flights are automatically excluded
- Scheduled times are used when actual takeoff or landing times are unavailable

## How to Run

1. Clone the repository.

2. Install the required packages:

```bash
python -m pip install -r requirements.txt
```

3. Run the analyzer:

```bash
python main.py
```

If no Flighty export is found, the analyzer automatically uses the included `sample_flights.csv`.

## Using Your Own Flighty Export

Export your flight history as a CSV file from Flighty and place it in the project folder.

The analyzer automatically detects files named:

```text
FlightyExport-YYYY-MM-DD.csv
```

If multiple Flighty export files are present, the newest one is selected automatically.

Flighty export files are ignored through `.gitignore`, so personal flight history files are not uploaded to GitHub by default.

## Example Output

```text
FLIGHT HISTORY SUMMARY
----------------------
Total flights: 3
Total flight time: 36 hours
Total flight distance: 29,072 km
Airports visited: 4
Countries/regions visited: 3

TRAVEL EQUIVALENTS
------------------
Around Earth: 0.73 times
Earth to Moon: 0.08 times
Around the Sun: 0.000031 times

FLIGHT HIGHLIGHTS
-----------------
Most used airline: CPA
Most used route: YYZ -> HKG
Most used aircraft: Airbus A350-1000
Most visited airport: YYZ
Longest flight: 102 - 15.2 hours

FLIGHTS BY MONTH
----------------
2026-01: 1
2026-02: 1
2026-03: 1