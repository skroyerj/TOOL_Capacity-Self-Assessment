def sort_by_masters(df):

    sorted_df = df.sort_values(by="What master's programme did you follow?", key=lambda col: col.str.lower())
    
    return sorted_df



# To replace specific data: df.loc[RowNumber, 'ColumnName'] = Replacement