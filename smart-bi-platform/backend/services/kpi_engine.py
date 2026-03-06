import pandas as pd


def calculate_kpis(df):

    numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns.tolist()

    kpi_results = {}

    for col in numeric_cols:

        kpi_results[col] = {
            "total": float(df[col].sum()),
            "average": float(df[col].mean())
        }

    return kpi_results