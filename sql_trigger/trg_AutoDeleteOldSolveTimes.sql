ALTER TRIGGER trg_AutoDeleteOldSolveTimes
ON SolveTimes
AFTER INSERT
AS
BEGIN
    WITH CTE AS (
        SELECT
            TimeID,
            UserID,
            PuzzleType,
            ROW_NUMBER() OVER (
                PARTITION BY UserID, PuzzleType
                ORDER BY SolveAt DESC
            ) AS RowNum
        FROM SolveTimes
    )
    DELETE FROM SolveTimes
    WHERE TimeID IN (
        SELECT TimeID
        FROM CTE
        WHERE RowNum > 15
    );
END;
