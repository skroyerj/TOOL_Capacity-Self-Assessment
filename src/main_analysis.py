
# --------------------------------
# statement for agreeing in the survey
PARTICIPANT_INFO_AGREEMENT = "I have read the participant information and consent to my data being collected and used in anonymised form for this study."


# --------------------------------
# Questions to include in the analysis:
MOTIVATION = [
    "I felt confident in working with the methodology today",
    "I am interested in the methodology of this course",
    "This course is relevant for me in my future",
    "I want to gain practical knowledge",
    "I want to gain theoretical knowledge",
    "I feel like I know more than I did last week",
    "I feel that I have influence and responsibility in my group, and that my inclusion and opinions are valued"
]

CAPACITY = [
    "I feel like I can use my (priorly learned) skills in the course..",
    "I feel like I am acquiring new skills every week with the Agile methodology. .",
    "To perform the tasks today, I felt like seeking support from....The teacher",
    "To perform the tasks today, I felt like seeking support from....The TA's",
    "To perform the tasks today, I felt like seeking support from....Other students"
]

UNCERTAINTY = [
    "How much uncertainty do you encounter in this course regarding the end goal at this point? .",
    "How much uncertainty did you encounter in the Agile methodology from today? .",
    "How easy or difficult would it be to make changes to your design at this stage? ."
]

likert_6pt = ["Completely disagree", "Mostly disagree", "Slightly disagree", "Slightly agree", "Mostly agree", "Completely agree"]

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

import sort_education
import plotting_data

def count_columns(df, columns_to_count):
    counted_df = pd.DataFrame()
    for col in columns_to_count:
        counts = df[col].value_counts(dropna=False)
        counts = counts.reindex(likert_6pt, fill_value=0)
        counted_df[col] = counts

    return counted_df


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
    all_cols = list(dataframe.columns)

    cols_to_remove = all_cols[0:5] # Remove first 5 columns
    cols_to_remove += [col for col in all_cols if "Point" in col]
    cols_to_remove += [col for col in all_cols if "Feedback –" in col]

    return cols_to_remove

# Get columns to remove from the first file (assuming all files have the same structure)
cols_to_remove = list(columns_to_remove(pd.read_excel(ANON_FILES[0])))

# Clean up data
for file in ANON_FILES:
    if not file.exists():
        continue
    else:
        df = pd.read_excel(file)

        # df.set_index("Anon_ID", inplace=True)

        # Remove unwanted columns from each dataframe
        for col in cols_to_remove:
            # print(f"Removing column: {col}")
            df = df.drop(columns=col)

        # print(f"Remaining columns: {df.columns}")


        print(f"TESTING {file}...")
        print(df.columns)
    
        # Only include those who agreed to participate:
        df = df[[PARTICIPANT_INFO_AGREEMENT]] == "Yes"

        # df = sort_education.sort_by_masters(df)


        # ---------------------------------------------
        # How many on each master's programme?
        # print(df["What master's programme did you follow?"].value_counts())

        # print(df["What master's programme did you follow?"])
        # ---------------------------------------------

        # TEST = df["This course is relevant for me in my future"].value_counts()
        
        # TEST = TEST.reindex(["Completely agree", "Mostly agree", "Slightly agree", "Slightly disagree", "Mostly disagree", "Completely disagree"], fill_value=0)
        # # print("Efter sortering", TEST)
        
        columns_to_count = MOTIVATION + CAPACITY + UNCERTAINTY

        

        TEST2 = count_columns(df, columns_to_count)

        TEST2 = count_columns(df, MOTIVATION)
        print("TEST2:")
            
    print(TEST2.transpose())

# fig, ax = plotting_data.butterfly(TEST2.transpose())
# plt.show()

import test

timeseries = test.time_series_df(TEST2, "I felt confident in working with the methodology today.")

print(timeseries)





        

