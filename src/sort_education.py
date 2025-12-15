import pandas as pd

def create_education_groups(df):
    """
    Creates a dictionary of dataframes grouped by education program.
    For bachelor students, uses their bachelor program.
    For others, uses their master's program.
    """
    
    # Make a copy to avoid SettingWithCopyWarning
    df_copy = df.copy()

    # Create a new column that determines the grouping key
    def get_program(row):
        masters_col = "What master's programme do you follow?"
        bachelors_col = "What bachelor's programme did you follow?"
        
        if row[masters_col] == "I am still on my bachelor's":
            return row[bachelors_col]
        else:
            return row[masters_col]
    
    df_copy['_education_group'] = df_copy.apply(get_program, axis=1)
    
    # Create dictionary of dataframes grouped by education program
    education_dict = {}
    for program in df_copy['_education_group'].unique():
        education_dict[program] = df_copy[df_copy['_education_group'] == program].copy()
        # Remove the temporary grouping column from each dataframe
        education_dict[program] = education_dict[program].drop('_education_group', axis=1)
    
    return education_dict















































# def sort_by_masters(dfs: pd.DataFrame) -> pd.DataFrame:
#     """ Sort by education (current master's programme or not-yet-completed bachelor's programme)."""
#     sorted_dfs = {}
    
#     for df in dfs:
#         df["Education"]
#         print("Master's: ",df["What master's programme do you follow?"])
#         df.loc[df["What master's programme did you follow?"] == "I am still on my bachelor's", "Education"] = df["What bachelor's programme did you follow?"]
#         sorted_df = df.sort_values(by="Education", key=lambda col: col.str.lower())

#         sorted_dfs[df.name] = sorted_df

#     return sorted_df



# # To replace specific data: df.loc[RowNumber, 'ColumnName'] = Replacement




# # df = sort_education.sort_by_masters(df)


# ---------------------------------------------
# How many on each master's programme?
# print(df["What master's programme did you follow?"].value_counts())

# print(df["What master's programme did you follow?"])
# ---------------------------------------------
