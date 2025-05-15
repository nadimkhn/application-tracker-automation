import pandas as pd

def clean_column_names(df):
    cleaned_columns = []
    for col in df.columns:
        clean_col = col.lower().strip().replace(' ', '_')
        cleaned_columns.append(clean_col)
    df.columns = cleaned_columns
    return df.head()