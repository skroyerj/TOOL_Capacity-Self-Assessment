def sort_by_masters(df):

    df["Education"] = df["What master's programme do you follow?"]
    df.loc[df["What master's programme did you follow?"] == "I am still on my bachelor's", "Education"] = df["What bachelor's programme did you follow?"]
    sorted_df = df.sort_values(by="Education", key=lambda col: col.str.lower())

    return sorted_df



# To replace specific data: df.loc[RowNumber, 'ColumnName'] = Replacement




# df = sort_education.sort_by_masters(df)


# ---------------------------------------------
# How many on each master's programme?
# print(df["What master's programme did you follow?"].value_counts())

# print(df["What master's programme did you follow?"])
# ---------------------------------------------
