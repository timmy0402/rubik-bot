CREATE TRIGGER [dbo].[trg_IncreaseCommandCount]
ON [dbo].[CommandLog]
AFTER INSERT
AS 
BEGIN
    DECLARE @CurrentMonthYear CHAR(7);
    SET @CurrentMonthYear = FORMAT(GETDATE(),'MM-yyyy');
    -- Update usage count if command already used before
    UPDATE CommandTrack
    SET UsageCount = UsageCount + 1
    WHERE CommandName IN (SELECT CommandName FROM inserted)
        AND UsageMonth = @CurrentMonthYear;
    -- Insert new row if command haven't been used this month
    INSERT INTO CommandTrack(CommandName, UsageMonth, UsageCount)
    SELECT CommandName, @CurrentMonthYear, 1
    FROM inserted
    WHERE NOT EXISTS (
        SELECT 1
        FROM CommandTrack
        WHERE CommandName = inserted.CommandName
          AND UsageMonth = @CurrentMonthYear
    );
END;