# Lab 5 – Issues Found and Fixed (`shuttle_system.py`)

Line numbers refer to the **original** starter file. "Priority" is my judgement of impact (Bandit itself rated both of its findings Low severity, High confidence).

| # | Issue | Type | Tool / Code | Priority | Line(s) | Description | Fix Approach |
|---|-------|------|-------------|----------|---------|-------------|--------------|
| 1 | Bare `except: pass` | Bug / Security | Bandit B110, Pylint W0702, Flake8 E722 | High | 26–30 | Every error inside `underused_routes()` is silently swallowed. It hid two real bugs: `ZeroDivisionError` for routes with no trips, and `TypeError` for the bad `"full"` entry in R3. | Removed the `try/except`. `average_load()` now returns `None` when a route has no trips, and `underused_routes()` skips `None`. |
| 2 | No input validation on passenger count | Bug (logic) | Not flagged by any tool (found by running) | High | 11–12, 49–50 | `-6` and `"full"` were accepted as passenger counts. The negative count dragged R2's average down; the string poisoned R3 so its average could never be computed. | `add_trip_log()` now raises `ValueError` unless the count is a non-negative `int` (and not `bool`). `main()` catches it and prints "Rejected: …". |
| 3 | Crash on removed / unknown route | Bug (logic) | Not flagged by any tool (found by running) | High | 55–58 | R3 is deleted, then `average_load("R3")` is called → `KeyError` crash. Typing an unknown route at the prompt also crashes with `KeyError`. | `main()` checks `if route in ROUTES` before using it and prints a friendly message. `remove_route()` uses `pop(route_id, None)` so removing a missing route is safe. |
| 4 | Mutable default argument | Bug | Pylint W0102 | Medium | 11 | `logs=[]` is created once when the function is defined, so every call without `logs` shares and keeps growing the same list. | Default changed to `None`; a new list is created inside the function. |
| 5 | Insecure pseudo-random generator | Security | Bandit B311 | Low | 35 | `random.choice` is predictable and not meant for security-sensitive choices. | Replaced with `secrets.choice`. |
| 6 | Files opened without `with` / encoding | Bug (resource leak) | Pylint R1732, W1514 | Medium | 39, 42 | The second file handle is never closed; encoding depends on the OS default. | Used `with open(..., encoding="utf-8")` and `json.dump` / `json.load`. |
| 7 | `global` statement | Code quality | Pylint W0603 | Medium | 38 | Reassigning the module-level `routes` via `global` makes state hard to track. | Kept one dict (`ROUTES`) and updated it in place with `clear()` / `update()`. |
| 8 | Unused argument + non-snake_case name | Code quality | Pylint W0613, C0103 | Low | 33 | `assignDriver(route_id)` never uses `route_id` and breaks PEP 8 naming. | Renamed to `assign_driver()` and removed the unused parameter. Driver list moved to a module constant. |
| 9 | Old `%` string formatting | Style | Pylint C0209; Flake8 E501 | Low | 13 | `%` formatting, and the line is 82 chars (> 79). | Rewrote as an f-string, which also fixes the line length. |
| 10 | Missing docstrings | Style | Pylint C0114, C0116 | Low | 1, 11, 16, 19, 23, 33, 37, 45 | No module or function docstrings. | Added a docstring to the module and every function. |
| 11 | Blank-line formatting | Style | Flake8 E302, E305 | Low | 11, 16, 19, 23, 33, 37, 45, 60 | PEP 8 needs 2 blank lines around top-level functions. | Added the blank lines. |
| 12 | Script runs on import | Code quality | (good practice) | Low | 60 | `main()` runs whenever the file is imported. | Wrapped it in `if __name__ == "__main__":`. |

## Results

| Tool | Before | After |
|------|--------|-------|
| Pylint | 6.25 / 10 | 10.00 / 10 |
| Bandit | 2 issues (B110, B311 – Low) | No issues identified |
| Flake8 | 10 issues | 0 issues |
