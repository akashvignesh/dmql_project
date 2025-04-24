import pandas as pd
import psycopg2
from psycopg2 import Error
import random

# Database connection parameters for AWS RDS
db_params = {
    "host": "dmqlproject.ccv00icswcgq.us-east-1.rds.amazonaws.com",
    "database": "postgres",
    "user": "dmqlRdsLogin",
    "password": "dmqlRdsPassword",
    "port": "5432"
}

# Function to connect to PostgreSQL
def connect_to_db():
    try:
        connection = psycopg2.connect(**db_params)
        return connection
    except Error as e:
        print(f"Error connecting to PostgreSQL: {e}")
        return None

# Function to create tables in BCNF with renamed columns
def create_tables(connection):
    try:
        cursor = connection.cursor()

        # Table 1: Arrests
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Arrests (
                Arrest_ID VARCHAR(20) PRIMARY KEY,
                Arrest_Date DATE,
                Law_Code VARCHAR(10),
                Offense_Level CHAR(1)
            );
        """)

        # Table 2: Offense_Types
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Offense_Types (
                Offense_Code INT PRIMARY KEY,
                Offense_Desc VARCHAR(100),
                Category_Code FLOAT,
                Category_Desc VARCHAR(100)
            );
        """)

        # Table 3: Arrest_Offenses
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Arrest_Offenses (
                Arrest_ID VARCHAR(20),
                Offense_Code INT,
                PRIMARY KEY (Arrest_ID, Offense_Code),
                FOREIGN KEY (Arrest_ID) REFERENCES Arrests(Arrest_ID),
                FOREIGN KEY (Offense_Code) REFERENCES Offense_Types(Offense_Code)
            );
        """)

        # Table 4: Perpetrators
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Perpetrators (
                Arrest_ID VARCHAR(20) PRIMARY KEY,
                Age INT,
                Sex CHAR(1),
                Race VARCHAR(50),
                FOREIGN KEY (Arrest_ID) REFERENCES Arrests(Arrest_ID)
            );
        """)

        # Table 5: Arrest_Details
        cursor.execute("""
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
        """)

        connection.commit()
        print("Five tables created successfully in BCNF form with renamed columns.")
    except Error as e:
        print(f"Error creating tables: {e}")
    finally:
        cursor.close()

# Function to generate random age based on Age_Group
def get_random_age(age_group):
    if age_group == "<18":
        return random.randint(12, 17)
    elif age_group == "18-24":
        return random.randint(18, 24)
    elif age_group == "25-44":
        return random.randint(25, 44)
    elif age_group == "45-64":
        return random.randint(45, 64)
    elif age_group == "65+":
        return random.randint(65, 90)
    else:
        return None

# Function to insert data into tables with renamed columns
def insert_data(connection, df):
    try:
        cursor = connection.cursor()
        inserted_rows = 0

        for index, row in df.iterrows():
            # Skip rows with any null or empty values
            if row.isnull().any() or any(str(val).strip() == "" for val in row):
                continue

            # Generate random age from Age_Group
            age = get_random_age(row['Age_Group'])
            if age is None:
                continue

            # Insert into Arrests table
            cursor.execute("""
                INSERT INTO Arrests (Arrest_ID, Arrest_Date, Law_Code, Offense_Level)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (Arrest_ID) DO NOTHING;
            """, (row['Arrest_ID'], row['Arrest_Date'], row['Law_Code'], row['Offense_Level']))

            # Insert into Offense_Types table
            cursor.execute("""
                INSERT INTO Offense_Types (Offense_Code, Offense_Desc, Category_Code, Category_Desc)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (Offense_Code) DO NOTHING;
            """, (row['Offense_Code'], row['Offense_Desc'], row['Category_Code'], row['Category_Desc']))

            # Insert into Arrest_Offenses table
            cursor.execute("""
                INSERT INTO Arrest_Offenses (Arrest_ID, Offense_Code)
                VALUES (%s, %s)
                ON CONFLICT (Arrest_ID, Offense_Code) DO NOTHING;
            """, (row['Arrest_ID'], row['Offense_Code']))

            # Insert into Perpetrators table
            cursor.execute("""
                INSERT INTO Perpetrators (Arrest_ID, Age, Sex, Race)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (Arrest_ID) DO NOTHING;
            """, (row['Arrest_ID'], age, row['Sex'], row['Race']))

            # Insert into Arrest_Details table
            cursor.execute("""
                INSERT INTO Arrest_Details (Arrest_ID, Arrest_Borough, Arrest_Precinct, Jurisdiction, 
                                           X_Coordinate, Y_Coordinate, Latitude, Longitude)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (Arrest_ID) DO NOTHING;
            """, (row['Arrest_ID'], row['Arrest_Borough'], row['Arrest_Precinct'], row['Jurisdiction'],
                  row['X_Coordinate'], row['Y_Coordinate'], row['Latitude'], row['Longitude']))

            inserted_rows += 1
            if inserted_rows >= 10000:
                break

        connection.commit()
        print(f"Inserted {inserted_rows} rows successfully across five tables.")
    except Error as e:
        print(f"Error inserting data: {e}")
    finally:
        cursor.close()

# Main execution
if __name__ == "__main__":
    # Load CSV file and rename columns
    try:
        df = pd.read_csv("NYPD_Arrest_Data_2023.csv")
        # Rename columns to match the new schema
        df = df.rename(columns={
            'ARREST_KEY': 'Arrest_ID',
            'ARREST_DATE': 'Arrest_Date',
            'PD_CD': 'Offense_Code',
            'PD_DESC': 'Offense_Desc',
            'KY_CD': 'Category_Code',
            'OFNS_DESC': 'Category_Desc',
            'LAW_CODE': 'Law_Code',
            'LAW_CAT_CD': 'Offense_Level',
            'ARREST_BORO': 'Arrest_Borough',
            'ARREST_PRECINCT': 'Arrest_Precinct',
            'JURISDICTION_CODE': 'Jurisdiction',
            'AGE_GROUP': 'Age_Group',
            'PERP_SEX': 'Sex',
            'PERP_RACE': 'Race',
            'X_COORD_CD': 'X_Coordinate',
            'Y_COORD_CD': 'Y_Coordinate'
        })
        print("CSV file loaded and columns renamed successfully.")
    except Exception as e:
        print(f"Error loading CSV: {e}")
        exit()

    # Convert Arrest_Date to proper date format
    df['Arrest_Date'] = pd.to_datetime(df['Arrest_Date'], errors='coerce')

    # Connect to database
    connection = connect_to_db()
    if connection is None:
        exit()

    # Create tables in BCNF
    create_tables(connection)

    # Insert data into tables
    insert_data(connection, df)

    # Close connection
    connection.close()
    print("Database connection closed.")