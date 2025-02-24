CREATE TABLE IF NOT EXISTS dev1.matchScouting (
        id INT AUTO_INCREMENT NOT NULL,
        BAeventID VARCHAR(20) NOT NULL,
        matchID INT NOT NULL,
        matchNum INT NULL,
        scouterID INT NULL,
        scoutingStatus INT NULL,
        team VARCHAR(10) NOT NULL,
        teamMatchNum INT NULL,
        scoutingRoleID INT NULL,
        preStartPos TINYINT NULL,
        /* add Level 1 columns here */
        /* add Level 2 columns here. Note that these columns must match those of the level2 DB table */
        PRIMARY KEY (id),
        FOREIGN KEY (BAeventID) REFERENCES events (BAeventID) ON DELETE CASCADE,
        FOREIGN KEY (matchID) REFERENCES matches (id) ON DELETE CASCADE,
        FOREIGN KEY (scouterID) REFERENCES scouters (id) ON DELETE CASCADE,
        FOREIGN KEY (team) REFERENCES teams (team) ON DELETE CASCADE,
        FOREIGN KEY (scoutingRoleID) REFERENCES scoutingRoles (id) ON DELETE CASCADE
) Engine = InnoDB;
