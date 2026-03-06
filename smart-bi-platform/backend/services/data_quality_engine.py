import pandas as pd


def analyze_data_quality(df):

    # Missing values
    missing_values = int(df.isnull().sum().sum())

    # Duplicate rows
    duplicate_rows = int(df.duplicated().sum())

    # Detect numeric columns
    numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns.tolist()

    outliers = 0

    for col in numeric_cols:

        series = df[col]

        mean = series.mean()
        std = series.std()

        if std == 0:
            continue

        for value in series:
            z_score = (value - mean) / std

            if abs(z_score) > 3:
                outliers += 1

    return {
        "rows": len(df),
        "missing_values": missing_values,
        "duplicate_rows": duplicate_rows,
        "outliers_detected": outliers
    }