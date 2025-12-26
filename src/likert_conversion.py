def convert_likert_to_numeric(df, likert_columns, mapping):
    """
    Convert Likert scale text responses to numbers.
    """
    df_copy = df.copy()
    
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
