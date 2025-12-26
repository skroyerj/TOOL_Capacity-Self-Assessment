
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

    ALL_Qs = MOTIVATION + CAPACITY + UNCERTAINTY

    include_in_df = INFO + EDU + ALL_Qs

    likert_6pt = {"Completely disagree": 1, "Mostly disagree": 2, "Slightly disagree": 3, "Slightly agree": 4, "Mostly agree": 5, "Completely agree": 6}

    likert_7pt_1 = {"None at all": 1, "Very little": 2, "Little": 3, "Some": 4, "Much": 5, "A great deal": 6, "Extreme amount": 7}

    likert_7pt_2 = {"Impossible": 1,"Very difficult": 2, "Difficult": 3, "Somewhat difficult": 4, "Somewhat easy": 5, "Easy": 6, "Very easy": 7}
    return PARTICIPANT_INFO_AGREEMENT, EDU, INFO, MOTIVATION, CAPACITY, UNCERTAINTY, include_in_df, likert_6pt, likert_7pt_1, likert_7pt_2

PARTICIPANT_INFO_AGREEMENT, EDU, INFO, MOTIVATION, CAPACITY, UNCERTAINTY, include_in_df, likert_6pt, likert_7pt_1, likert_7pt_2 = to_include()

LIKERTS = {
    "likert_6pt": likert_6pt,
    "likert_7pt_1": likert_7pt_1,
    "likert_7pt_2": likert_7pt_2
}

REV_LIKERTS = {
    "likert_6pt": {v: k for k, v in likert_6pt.items()},
    "likert_7pt_1": {v: k for k, v in likert_7pt_1.items()},
    "likert_7pt_2": {v: k for k, v in likert_7pt_2.items()}
}

# print("Reversed Likert Scales:\n", REV_LIKERTS)

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
    flat_data[key] = likert_conversion.convert_likert_to_numeric(flat_data[key], MOTIVATION + CAPACITY, LIKERTS["likert_6pt"])
    flat_data[key] = likert_conversion.convert_likert_to_numeric(flat_data[key], UNCERTAINTY[:2], LIKERTS["likert_7pt_1"])
    flat_data[key] = likert_conversion.convert_likert_to_numeric(flat_data[key], [UNCERTAINTY[2]], LIKERTS["likert_7pt_2"])

# Convert it
dataframes = visualisation.restructure_flat_dict(flat_data)



# Extract study lines and weeks from keys, count responses
data_dict = {}
for name, data in flat_data.items():
    parts = name.split("_")
    study_line = parts[0]  # 'arch', 'archeng', 'oth'
    week = parts[2]  # 'Week5', 'Week6', etc.
    
    # Count unique respondents
    response_count = data["Anon_ID"].nunique()
    
    # Store in nested dictionary
    if study_line not in data_dict:
        data_dict[study_line] = {}
    data_dict[study_line][week] = response_count

# Create dataframe from the nested dictionary
resp_df = pd.DataFrame.from_dict(data_dict, orient='index')

# Replace NaN with 0
resp_df = resp_df.fillna(0)

# Sort columns by week number
resp_df = resp_df.reindex(sorted(resp_df.columns, key=lambda x: int(x.replace('Week', ''))), axis=1)

# Add totals row
resp_df.loc['Total'] = resp_df.sum()

# print("Response Rates:\n", resp_df)


# Print response rates for each educational background for each week in ONE excel file
response_rates_dir = Path("figures/response_rates/")
response_rates_dir.mkdir(parents=True, exist_ok=True)

with pd.ExcelWriter(response_rates_dir / "response_rates_by_education.xlsx") as writer:
    resp_df.to_excel(writer, sheet_name="Response Rates", index=True)


"""
GUI Visualization Menu
"""
gui.show_visualization_menu(dataframes, MOTIVATION + CAPACITY + UNCERTAINTY, LIKERTS)

# --------------------------------
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




        

