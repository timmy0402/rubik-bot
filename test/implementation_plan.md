# Rubik-Bot Feature Implementation Plan

This document outlines the roadmap for upgrading the Rubik-Bot with advanced cubing features. The goal is to transform the bot from a simple timer into a comprehensive competitive and educational tool.


## Phase 1: Knowledge Base (Algorithm Reference)
**Objective:** Add educational tools for learning OLL/PLL algorithms.

1.  **Data Structure (`src/data/algorithms.json`)**
    *   **Task:** Create a knowledge base.
    *   **Format:**
        ```json
        {
          "pll": {
            "T": {
              "name": "T Perm",
              "alg": "R U R' U' R' F R2 U' R' U' R U R' F'",
              "image_url": "..."
            }
          }
        }
        ```

2.  **Command Implementation**
    *   **Action:** Create `/alg [set] [case]` (e.g., `/alg pll T`).
    *   **Logic:** Look up key in JSON. Return Embed with Algorithm Notation and Image.

---

## Phase 2: WCA Integration
**Objective:** Link Discord users to their World Cube Association profiles.

1.  **Link Command**
    *   **Action:** Create `/wca link [wca_id]`.
    *   **Logic:** Update `Users` table `WCA_ID` column.

2.  **Profile Command**
    *   **Action:** Create `/wca profile [user]`.
    *   **Logic:**
        *   Fetch WCA ID from DB.
        *   Call `https://www.worldcubeassociation.org/api/v0/persons/{WCA_ID}`.
        *   Display Embed with: National Rank (NR), Continental Rank (CR), World Rank (WR), and Medal Count.

---
## Phase 3: Core Data & Statistics (Foundation)
**Objective:** Upgrade database schema and internal logic to support Puzzle Types, Averages (Ao5/Ao12), and Personal Bests (PB).

1.  **Database Migration (`src/DB_Manager.py` & `src/main.py`)**
    *   **Task:** Update `SolveTimes` table schema.
    *   **Action:** Add `PuzzleType` column (TEXT, Default '3x3').
    *   **Action:** Add `WCA_ID` column to `Users` table (TEXT, nullable).
    *   **Note:** Since SQLite doesn't support easy column alterations in all versions, script a migration: Rename old table -> Create new table -> Copy data -> Drop old table.

2.  **Update Stopwatch Context (`src/main.py` & `src/timer.py`)**
    *   **Task:** Pass puzzle context to the timer.
    *   **Action:** Update `/stopwatch` command to accept an optional `puzzle` argument (enum choices identical to `/scramble`).
    *   **Action:** Pass this `puzzle` type into `TimerView`.
    *   **Action:** Ensure `TimerView` passes this `puzzle` type to the DB insert function upon completion.

3.  **Math Logic (`src/utils.py`)**
    *   **Task:** Implement WCA-standard averaging.
    *   **Action:** Create `calculate_ao5(times_list)`:
        *   Remove best and worst time.
        *   Average the remaining 3.
    *   **Action:** Create `calculate_ao12(times_list)`:
        *   Remove best and worst time.
        *   Average the remaining 10.

4.  **Stats Command (`src/main.py`)**
    *   **Task:** Display advanced stats.
    *   **Action:** Create `/stats [puzzle]` command.
    *   **Logic:** Query DB for:
        *   **Single PB:** `SELECT MIN(SolveTime) ... WHERE PuzzleType=?`
        *   **Averages:** Fetch last 5 and 12 records, run through `utils.py` functions.
        *   **Count:** Total solve count for that puzzle.

---


## Phase 4: Battle / Race Mode (Multiplayer)
**Objective:** Real-time competitive solving.

1.  **State Management (`src/battle.py`)**
    *   **Task:** Manage lobby state.
    *   **Class:** `BattleLobby`
    *   **Attributes:** `host_id`, `puzzle_type`, `scramble`, `players: {id: status}`, `state` (JOINING, RACING, FINISHED).

2.  **Battle View**
    *   **Task:** UI for joining and starting.
    *   **Buttons:** `Join Race`, `Start (Host only)`, `Forfeit`.

3.  **Race Logic**
    *   **Command:** `/race [puzzle]`.
    *   **Flow:**
        1.  Bot generates **one** scramble for the lobby.
        2.  Users join.
        3.  Host starts -> Bot sends countdown.
        4.  Users get a button "Stop Timer".
        5.  Bot updates a "Live Leaderboard" message as users finish.
