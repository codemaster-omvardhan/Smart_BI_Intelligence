import pandas as pd

def detect_correlations(df):

    # detect numeric columns
    numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns.tolist()

    if len(numeric_cols) < 2:
        return []

    corr_matrix = df[numeric_cols].corr()

    correlations = []

    for col1 in numeric_cols:
        for col2 in numeric_cols:

            if col1 == col2:
                continue

            corr_value = corr_matrix.loc[col1, col2]

            if abs(corr_value) > 0.7:
                correlations.append({
                    "metric_1": col1,
                    "metric_2": col2,
                    "correlation": round(float(corr_value), 2)
                })

    return correlations