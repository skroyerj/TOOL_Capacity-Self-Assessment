
# --------------------------------
# statement for agreeing in the survey
PARTICIPANT_INFO_AGREEMENT = "I have read the participant information and consent to my data being collected and used in anonymised form for this study."


import pandas as pd
from pathlib import Path


ANON_FILES = [
          Path("data/output_data/AGILE_5_anon.xlsx"),
          Path("data/output_data/AGILE_6_anon.xlsx"),
          Path("data/output_data/AGILE_7_anon.xlsx"),
          Path("data/output_data/AGILE_8_anon.xlsx"),
          Path("data/output_data/AGILE_9_anon.xlsx"),
          Path("data/output_data/AGILE_10_anon.xlsx"),
          Path("data/output_data/AGILE_11_anon.xlsx"),
          Path("data/output_data/AGILE_12_anon.xlsx"),
          Path("data/output_data/AGILE_13_anon.xlsx")]

cols_to_remove = ()

def columns_to_remove(dataframe):
    all_cols = list(df.columns)

    cols_to_remove = all_cols[0:6] # Remove first 7 columns
    cols_to_remove += [col for col in all_cols if "Point" in col]
    cols_to_remove += [col for col in all_cols if "Feedback –" in col]

    return cols_to_remove

# Clean up data
for file in ANON_FILES:
    if not file.exists():
        print("file not found")
    else:
        df = pd.read_excel(file)

        # Have columns to remove already been identified?
        if not cols_to_remove:
            cols_to_remove = list(columns_to_remove(df))
            # print(f"Columns to remove: {cols_to_remove}")
        else:
            continue

        # Remove unwanted columns from each dataframe
        for col in cols_to_remove:
            # print(f"Removing column: {col}")
            df = df.drop(columns=col)

        # print(f"Remaining columns: {df.columns}")


        # Only include those who agreed to participate:
        df = df[df[PARTICIPANT_INFO_AGREEMENT] == "Yes"]

        

