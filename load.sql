
CREATE TABLE IF NOT EXISTS Arrests (
    Arrest_ID VARCHAR(20) PRIMARY KEY,
    Arrest_Date DATE,
    Law_Code VARCHAR(10),
    Offense_Level CHAR(1)
);

CREATE TABLE IF NOT EXISTS Offense_Types (
    Offense_Code INT PRIMARY KEY,
    Offense_Desc VARCHAR(100),
    Category_Code FLOAT,
    Category_Desc VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS Arrest_Offenses (
    Arrest_ID VARCHAR(20),
    Offense_Code INT,
    PRIMARY KEY (Arrest_ID, Offense_Code),
    FOREIGN KEY (Arrest_ID) REFERENCES Arrests(Arrest_ID),
    FOREIGN KEY (Offense_Code) REFERENCES Offense_Types(Offense_Code)
);

CREATE TABLE IF NOT EXISTS Perpetrators (
    Arrest_ID VARCHAR(20) PRIMARY KEY,
    Age INT,
    Sex CHAR(1),
    Race VARCHAR(50),
    FOREIGN KEY (Arrest_ID) REFERENCES Arrests(Arrest_ID)
);

CREATE TABLE IF NOT EXISTS Arrest_Details (
    Arrest_ID VARCHAR(20) PRIMARY KEY,
    Arrest_Borough CHAR(1),
    Arrest_Precinct INT,
    Jurisdiction INT,
    X_Coordinate INT,
    Y_Coordinate INT,
    Latitude FLOAT,
    Longitude FLOAT,
    FOREIGN KEY (Arrest_ID) REFERENCES Arrests(Arrest_ID)
);
