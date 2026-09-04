# Flight History Analyzer

A small Python project that analyzes flight history data from a CSV file.

## Current Features

- Total number of flights
- Total flight time
- Longest flight
- Most used airline
- Most used route

## How to Run

1. Clone the repository.

2. Install the required packages:
    
    ```bash
    python -m pip install -r requirements.txt

3. Run the analyzer with the included sample data:

    python main.py

The project includes `sample_flights.csv` for testing.

## Using Your Own Flighty Export

Export your flight history as a CSV file from Flighty.

Place the CSV file in the project folder, then update the filename passed to `load_flights()` in `main.py`.

For example:

```python
flights = load_flights("FlightyExport-2026-09-04.csv")

Flighty export files are ignored by Git through .gitignore, so your personal flight history will not be uploaded to GitHub by default.