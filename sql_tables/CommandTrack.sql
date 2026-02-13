CREATE TABLE CommandTrack(
    CommandName PRIMARY KEY NVARCHAR(225) NOT NULL,
    UsageMonth PRIMARY KEY CHAR(7) NOT NULL, -- Format: YYYY-MM
    UsageCount INTEGER NOT NULL
)