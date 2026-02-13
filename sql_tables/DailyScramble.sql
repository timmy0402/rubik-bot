CREATE TABLE DailyScramble(
    ScrambleID INTEGER IDENTITY(1,1) PRIMARY KEY,
    ScrambleText NVARCHAR(255) NOT NULL,
    ScrambleDate DATE NOT NULL,
    PulzzleType NVARCHAR(20) NOT NULL
)
