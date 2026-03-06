import pandas as pd


def generate_metadata(df):

    numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns.tolist()

    date_col = None

    for col in df.columns:
        try:
            parsed = pd.to_datetime(df[col], errors="coerce")
            if parsed.notna().sum() > len(df) * 0.6:
                date_col = col
                break
        except:
            continue

    return {
        "numeric_columns": numeric_cols,
        "date_column": date_col
    }