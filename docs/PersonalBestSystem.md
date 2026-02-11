# Personal Best System Documentation

The Personal Best (PB) system tracks individual user performance across different puzzle types (e.g., 3x3, 2x2). it calculates WCA-style averages (Ao5 and Ao12) and maintains a record of the fastest single solves and averages in the `UserStats` database table.

## Components Overview

### 1. Database Schema
**Table:** `UserStats`
- `StatID` (PK): Unique identifier.
- `UserID` (FK): Links to the `Users` table.
- `PuzzleType`: String identifier for the puzzle (e.g., '3x3').
- `BestSingle`: Fastest single solve time.
- `BestAo5`: Fastest Average of 5 (WCA trimmed).
- `BestAo12`: Fastest Average of 12 (WCA trimmed).

### 2. Logic Implementation
**File:** `src/stats/personal_best.py`

#### `calculate_wca_avg(times, count)`
Calculates the trimmed average according to WCA standards.
- **Logic**: Takes the `count` most recent solves, sorts them, removes the fastest and slowest times, and averages the remaining values.
- **Returns**: `float` (average) or `None` if insufficient solves exist.

#### `update_user_pbs(db_manager, user_id, puzzle_type, new_time)`
Checks if a new solve is a "Personal Best Single".
- **Returns**: `bool` (True if a new PB was set).

#### `update_user_average_best(db_manager, user_id, puzzle_type, new_ao5, new_ao12)`
Updates the cached Best Ao5 and Best Ao12 in the database.
- **Returns**: `tuple[bool, bool]` (New Ao5 PB status, New Ao12 PB status).

## Integration with Timer

**File:** `src/views/timer.py`

When a user stops the timer, the `TimerView` performs the following sequence:
1.  **Save Solve**: Inserts the new time into `SolveTimes`.
2.  **Check Single PB**: Calls `update_user_pbs`.
3.  **Calculate Session Stats**: Fetches the last 15 solves from the database to compute the current Ao5 and Ao12.
4.  **Update Average PBs**: Calls `update_user_average_best` with the calculated averages.
5.  **UI Feedback**: Updates the Discord embed with specialized congratulations messages and emojis for each record broken.