"""Campus shuttle timetable and fleet tracker.

Logs passenger counts per trip, works out average loads, flags
under-used routes and syncs the fleet data to a JSON file.
"""

import json
import secrets
from datetime import datetime

ROUTES = {"R1": {"name": "Main Gate - Library", "trips": []},
          "R2": {"name": "Hostel - Sports Complex", "trips": []},
          "R3": {"name": "Admin Block - Metro", "trips": []}}
MIN_CAPACITY = 10
DRIVERS = ["Prakash", "Leela", "Imran", "Tom"]


def add_trip_log(route_id, passenger_count, logs=None):
    """Record one trip's passenger count and append a log line.

    Raises ValueError for an unknown route or an invalid count.
    """
    if logs is None:
        logs = []
    if route_id not in ROUTES:
        raise ValueError(f"Unknown route: {route_id}")
    if (not isinstance(passenger_count, int)
            or isinstance(passenger_count, bool)
            or passenger_count < 0):
        raise ValueError(
            f"Invalid passenger count for {route_id}: {passenger_count!r}")
    ROUTES[route_id]["trips"].append(passenger_count)
    logs.append(f"{datetime.now()}: {route_id} carried {passenger_count}")
    return logs


def remove_route(route_id):
    """Remove a route if it exists. Returns True if it was removed."""
    return ROUTES.pop(route_id, None) is not None


def average_load(route_id):
    """Return the average passengers per trip, or None if no trips yet.

    Raises KeyError if the route does not exist.
    """
    trips = ROUTES[route_id]["trips"]
    if not trips:
        return None
    return sum(trips) / len(trips)


def underused_routes():
    """Return the routes whose average load is below MIN_CAPACITY."""
    flagged = []
    for route_id in ROUTES:
        avg = average_load(route_id)
        if avg is not None and avg < MIN_CAPACITY:
            flagged.append(route_id)
    return flagged


def assign_driver():
    """Pick a driver for a route using a secure random choice."""
    return secrets.choice(DRIVERS)


def sync_fleet_data(path="fleet.json"):
    """Write the fleet data to a JSON file and reload it from there."""
    with open(path, "w", encoding="utf-8") as fleet_file:
        json.dump(ROUTES, fleet_file)
    with open(path, encoding="utf-8") as fleet_file:
        data = json.load(fleet_file)
    ROUTES.clear()
    ROUTES.update(data)


def main():
    """Run a short demo of the shuttle tracker."""
    trips = [("R1", 32), ("R1", 28), ("R2", 4), ("R2", -6), ("R3", "full")]
    for route_id, count in trips:
        try:
            add_trip_log(route_id, count)
        except ValueError as err:
            print("Rejected:", err)
    print("Driver for R1:", assign_driver())
    print("Underused:", underused_routes())
    print("R1 average:", average_load("R1"))
    sync_fleet_data()
    remove_route("R3")
    choice = input("Route to look up (Enter for R2): ").strip() or "R2"
    if choice in ROUTES:
        print("Trips on", choice, ":", ROUTES[choice]["trips"])
    else:
        print("No such route:", choice)
    if "R3" in ROUTES:
        print("R3 average:", average_load("R3"))
    else:
        print("R3 has been removed, so it has no average.")


if __name__ == "__main__":
    main()
