
# --------------------------------
# statement for agreeing in the survey
def to_include() -> str:

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
        "I feel like I can use my (priorly learned) skills in the course",
        "I feel like I am acquiring new skills every week with the Agile methodology",
        "The teacher",
        "The TA's",
        "Other students"
    ]

    UNCERTAINTY = [
        "How much uncertainty do you encounter in this course regarding the end goal at this point?",
        "How much uncertainty did you encounter in the Agile methodology from today?",
        "How easy or difficult would it be to make changes to your design at this stage?"
    ]
    '''What is relevant to include in the dataframe:'''
    INFO = ["Anon_ID"] + [PARTICIPANT_INFO_AGREEMENT]

    EDU = ["What bachelor's programme did you follow?", "What master's programme do you follow?"]

    ALL_Qs = MOTIVATION + CAPACITY

    include_in_df = INFO + EDU + ALL_Qs

    likert_6pt = ["Completely disagree", "Mostly disagree", "Slightly disagree", "Slightly agree", "Mostly agree", "Completely agree"]

    return PARTICIPANT_INFO_AGREEMENT, EDU, INFO, MOTIVATION, CAPACITY, include_in_df, likert_6pt

PARTICIPANT_INFO_AGREEMENT, EDU, INFO, MOTIVATION, CAPACITY, include_in_df, likert_6pt = to_include()


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

import sort_education
import plotting_data
import timeseries
import visualisation
import likert_conversion
import gui

def count_columns(df, columns_to_count, index):
    """ Count occurrences of answers in specified columns. """
    counted_df = pd.DataFrame()
    for col in columns_to_count:
        print(f"Counting column: {col}\n")
        counts = df[col].value_counts(dropna=False)
        counts = counts.reindex(index, fill_value=0)
        counted_df[col] = counts

    return counted_df


ANON_FILES = [
          Path("data/output_data/AGILE_5_anon.xlsx"),
          Path("data/output_data/AGILE_6_anon.xlsx"),
          Path("data/output_data/AGILE_7_anon.xlsx"),
          Path("data/output_data/AGILE_8_anon.xlsx"),
          Path("data/output_data/AGILE_9_anon.xlsx")]


def read_and_sort(files: list[Path], columns_to_include: str()) -> pd.DataFrame: # type: ignore
    """ Read and sort data files into a dictionary of dataframes."""

    dfs = {}
    week_list = []

    data = {}
    archeng = "archeng_students"
    arch = "arch_students"
    oth = "oth_students"

    for file in files:
        if not file.exists():
            print(f"File {file} does not exist, skipping...")
            continue
        else:
            print(f"TESTING {file}...")

            init_df = pd.read_excel(file)

            # Only include those who agreed to participate:
            df = init_df[init_df[PARTICIPANT_INFO_AGREEMENT] == "Yes"]

            week_name = "Week" + file.stem.split("_")[1]
            week_list.append(week_name)
            # df.set_index("Anon_ID", inplace=True)

            # Only include relevant columns:
            dfs[week_name] = init_df[include_in_df].copy() #dict of dataframes

            # Create education groups
            education_groups = sort_education.create_education_groups(dfs[week_name])

            # Store specific education program dataframes
            if education_groups.get('Architectural Engineering (any university)') is not None:
                data[f"{archeng}_{week_name}"] = education_groups['Architectural Engineering (any university)']

            if education_groups.get('Architecture (any university)') is not None:
                data[f"{arch}_{week_name}"] = education_groups['Architecture (any university)']

            if education_groups.get('Other') is not None:
                data[f"{oth}_{week_name}"] = education_groups['Other']
            
            # # View all programs
            # print(list(education_groups.keys()))

            # # Check sizes
            # for program, program_df in education_groups.items():
            #     print(f"{program}: {len(program_df)} students")

            # for i, col in enumerate(dfs[week_name].columns):
            #     print(f"{i}: '{col}'")

    return data

dfs = read_and_sort(ANON_FILES, include_in_df)

# Flat dictionary
flat_data = dfs

# Convert all your dataframes
for key in flat_data:
    flat_data[key] = likert_conversion.convert_likert_to_numeric(flat_data[key], MOTIVATION + CAPACITY)


# Convert it
dataframes = visualisation.restructure_flat_dict(flat_data)

gui.show_visualization_menu(dataframes, MOTIVATION + CAPACITY)

# Now use the visualization functions as normal
# fig1 = visualisation.plot_question_over_time(dataframes, 'I am interested in the methodology of this course')
# plt.show()

# fig2 = visualisation.plot_stacked_distribution(dataframes, 'I felt confident in working with the methodology today',5)
# plt.show()

# fig3 = visualisation.plot_heatmap_all_questions(dataframes, CAPACITY, 5)
# plt.show()

# fig4 = visualisation.create_summary_report(dataframes, MOTIVATION + CAPACITY)
# plt.show()


# TEST = count_columns(dfs["Week5"],["This course is relevant for me in my future"], likert_6pt)
# print("Value count test:\n", TEST)

    
# count_week_5 = count_columns(dfs["Week5"], MOTIVATION, likert_6pt)

# fig, ax = plotting_data.butterfly(TEST2.transpose())
# plt.show()


# timeseries = timeseries.time_series_df(dfs, "I felt confident in working with the methodology today", "Anon_ID",False)

# plotting_data.stacked_area(timeseries, "I felt confident in working with the methodology today")

"""
count_timeseries = count_columns(timeseries, week_list, likert_6pt)
print("Timeseries:\n", timeseries)
print("Counted timeseries:\n", count_timeseries)

fig2 = plotting_data.stacked_area(count_timeseries, "I felt confident in working with the methodology today")
"""




        

