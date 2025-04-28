import pandas as pd
import random
import os

# Create output directory
output_dir = "4"
os.makedirs(output_dir, exist_ok=True)

# Load and rename columns
df = pd.read_csv("NYPD_Arrest_Data_2023.csv")
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
    'Y_COORD_CD': 'Y_Coordinate',
    'Latitude': 'Latitude',
    'Longitude': 'Longitude'
})

# Drop null rows
df = df.dropna()

# Sample 1000 rows
sample_df = df.sample(1000, random_state=1)

# Generate Age from Age_Group
def age_from_group(group):
    if group == "<18":
        return random.randint(12, 17)
    elif group == "18-24":
        return random.randint(18, 24)
    elif group == "25-44":
        return random.randint(25, 44)
    elif group == "45-64":
        return random.randint(45, 64)
    elif group == "65+":
        return random.randint(65, 90)
    else:
        return None

# Prepare individual tables
arrests = sample_df[['Arrest_ID', 'Arrest_Date', 'Law_Code', 'Offense_Level']].drop_duplicates()
offense_types = sample_df[['Offense_Code', 'Offense_Desc', 'Category_Code', 'Category_Desc']].drop_duplicates()
arrest_offenses = sample_df[['Arrest_ID', 'Offense_Code']].drop_duplicates()

perpetrators = sample_df[['Arrest_ID', 'Age_Group', 'Sex', 'Race']].drop_duplicates()
perpetrators['Age'] = perpetrators['Age_Group'].apply(age_from_group)
perpetrators = perpetrators[['Arrest_ID', 'Age', 'Sex', 'Race']]

arrest_details = sample_df[['Arrest_ID', 'Arrest_Borough', 'Arrest_Precinct', 'Jurisdiction', 'X_Coordinate', 'Y_Coordinate', 'Latitude', 'Longitude']]

# Save to CSV
arrests.to_csv(f"{output_dir}/Arrests.csv", index=False)
offense_types.to_csv(f"{output_dir}/Offense_Types.csv", index=False)
arrest_offenses.to_csv(f"{output_dir}/Arrest_Offenses.csv", index=False)
perpetrators.to_csv(f"{output_dir}/Perpetrators.csv", index=False)
arrest_details.to_csv(f"{output_dir}/Arrest_Details.csv", index=False)

print("All CSV files created successfully in the '4/' directory.")
