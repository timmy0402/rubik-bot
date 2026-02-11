from database import DatabaseManager

def update_user_pbs(db_manager: DatabaseManager, user_id: int, puzzle_type: str, new_time: float) -> bool:
    # Fetch current PB for the user and puzzle type
    db_manager.cursor.execute(
        "SELECT BestSingle FROM UserStats WHERE UserID=? AND PuzzleType=?", (user_id, puzzle_type))
    current_pb = db_manager.cursor.fetchval()
    if current_pb is None or new_time < current_pb:
        # Update PB if new time is better or if no PB exists
        if current_pb is None:
            db_manager.cursor.execute(
                "INSERT INTO UserStats(UserID, PuzzleType, BestSingle) VALUES(?, ?, ?)",
                (user_id, puzzle_type, new_time),
            )
        else:
            db_manager.cursor.execute(
                "UPDATE UserStats SET BestSingle=? WHERE UserID=? AND PuzzleType=?",
                (new_time, user_id, puzzle_type),
            )
        db_manager.connection.commit()
        return True
    return False

def calculate_wca_avg(times, count):
    if len(times) < count:
        return None
    subset = sorted(times[:count])
    trimmed = subset[1:-1]
    return sum(trimmed) / len(trimmed)

def update_user_average_best(db_manager: DatabaseManager, user_id: int, puzzle_type: str, new_ao5: float, new_ao12: float) -> tuple[bool, bool]:
    # Fetch current average best for the user and puzzle type
    db_manager.cursor.execute(
        "SELECT BestAo5, BestAo12 FROM UserStats WHERE UserID=? AND PuzzleType=?", (user_id, puzzle_type))
    row = db_manager.cursor.fetchone()
    
    current_ao5 = row[0] if row else None
    current_ao12 = row[1] if row else None

    updated_ao5 = False
    if new_ao5 is not None and (current_ao5 is None or new_ao5 < current_ao5):
        if row is None:
             db_manager.cursor.execute(
                "INSERT INTO UserStats(UserID, PuzzleType, BestAo5) VALUES(?, ?, ?)",
                (user_id, puzzle_type, new_ao5),
            )
        else:
            db_manager.cursor.execute(
                "UPDATE UserStats SET BestAo5=? WHERE UserID=? AND PuzzleType=?",
                (new_ao5, user_id, puzzle_type),
            )
        updated_ao5 = True

    updated_ao12 = False
    if new_ao12 is not None and (current_ao12 is None or new_ao12 < current_ao12):
        # We check if we need to insert or update again in case row was None and we didn't insert in Ao5 block
        db_manager.cursor.execute(
            "SELECT 1 FROM UserStats WHERE UserID=? AND PuzzleType=?", (user_id, puzzle_type))
        if not db_manager.cursor.fetchone():
            db_manager.cursor.execute(
                "INSERT INTO UserStats(UserID, PuzzleType, BestAo12) VALUES(?, ?, ?)",
                (user_id, puzzle_type, new_ao12),
            )
        else:
            db_manager.cursor.execute(
                "UPDATE UserStats SET BestAo12=? WHERE UserID=? AND PuzzleType=?",
                (new_ao12, user_id, puzzle_type),
            )
        updated_ao12 = True

    db_manager.connection.commit()
    return (updated_ao5, updated_ao12)

def get_user_pbs(db_manager: DatabaseManager, user_id: int, puzzle_type: str = "3x3") -> dict:
    # Fetch PBs for the user for a specific puzzle type
    db_manager.cursor.execute(
        "SELECT BestSingle, BestAo5, BestAo12 FROM UserStats WHERE UserID=? AND PuzzleType=?", (user_id, puzzle_type))
    row = db_manager.cursor.fetchone()
    
    if not row:
        return {
            "BestSingle": None,
            "BestAo5": None,
            "BestAo12": None,
        }
        
    return {
        "BestSingle": float(row[0]) if row[0] is not None else None,
        "BestAo5": float(row[1]) if row[1] is not None else None,
        "BestAo12": float(row[2]) if row[2] is not None else None,
    }