def convert_likert_to_numeric(df, likert_columns, mapping=None):
    """
    Convert Likert scale text responses to numbers.
    """
    df_copy = df.copy()
    
    if mapping is None:
        mapping = {
            'Completely disagree': 1,
            'Mostly disagree': 2,
            'Slightly disagree': 3,
            'Slightly agree': 4,
            'Mostly agree': 5,
            'Completely agree': 6
        }
    
    for col in likert_columns:
        if col in df_copy.columns:
            df_copy[col] = (
                df_copy[col]
                .astype(str)
                .str.strip()
                .str.replace(r"\s+", " ", regex=True)
                .map(mapping)
                )
    
    return df_copy
