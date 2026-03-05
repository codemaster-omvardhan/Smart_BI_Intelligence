from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, Path
from sqlalchemy.orm import Session
import shutil
import os

from db.session import get_db
from models.datasets import Dataset
from api.auth import get_current_user
import pandas as pd
import numpy as np


router = APIRouter(prefix="/datasets", tags=["Datasets"])

UPLOAD_FOLDER = "uploads"

@router.post("/upload")
def upload_dataset(
    file: UploadFile = File(...),
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files allowed")

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    new_dataset = Dataset(
        filename=file.filename,
        file_path=file_path
    )

    db.add(new_dataset)
    db.commit()
    db.refresh(new_dataset)

    return {
        "message": "File uploaded successfully",
        "dataset_id": new_dataset.id
    }


@router.get("/{dataset_id}/summary")
def dataset_summary(
    dataset_id: int = Path(...),
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    dataset = db.query(Dataset).filter(Dataset.id == dataset_id).first()

    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")

    try:
        df = pd.read_csv(dataset.file_path)
    except Exception:
        raise HTTPException(status_code=400, detail="Error reading CSV file")

    summary = {
        "rows": len(df),
        "columns": len(df.columns),
        "column_details": []
    }

    for col in df.columns:
        column_info = {
            "name": col,
            "dtype": str(df[col].dtype),
            "missing_values": int(df[col].isnull().sum())
        }

        # Numeric stats
        if pd.api.types.is_numeric_dtype(df[col]):
            column_info.update({
                "mean": float(df[col].mean()),
                "min": float(df[col].min()),
                "max": float(df[col].max())
            })

        summary["column_details"].append(column_info)

    return summary

@router.get("/{dataset_id}/kpis")
def dataset_kpis(
    dataset_id: int,
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    dataset = db.query(Dataset).filter(Dataset.id == dataset_id).first()

    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")

    try:
        df = pd.read_csv(dataset.file_path)
    except Exception:
        raise HTTPException(status_code=400, detail="Error reading CSV")

    # --------- Detect Date Columns First ---------
    date_cols = []

    for col in df.columns:
        try:
            df[col] = pd.to_datetime(df[col])
            date_cols.append(col)
        except:
            continue

    # --------- Detect Pure Numeric Columns ---------
    numeric_cols = []

    for col in df.columns:
        if (
            pd.api.types.is_numeric_dtype(df[col])
            and not pd.api.types.is_datetime64_any_dtype(df[col])
        ):
            numeric_cols.append(col)

    if not numeric_cols:
        return {"message": "No numeric columns found"}

    # --------- KPI Calculations ---------
    kpi_results = {}

    for col in numeric_cols:
        kpi_results[col] = {
            "total": float(df[col].sum()),
            "average": float(df[col].mean())
        }

    # --------- Monthly Trend ---------
    monthly_trend = {}

    if date_cols:
        date_col = date_cols[0]

        df["month"] = df[date_col].dt.to_period("M")

        for col in numeric_cols:
            grouped = df.groupby("month")[col].sum()

            monthly_trend[col] = {
                str(month): float(value)
                for month, value in grouped.items()
            }

    # --------- Growth Metrics ---------
    growth_metrics = {}

    for col, month_data in monthly_trend.items():
        months = sorted(month_data.keys())
        growth_metrics[col] = {}

        for i in range(1, len(months)):
            prev_month = months[i - 1]
            curr_month = months[i]

            prev_value = month_data[prev_month]
            curr_value = month_data[curr_month]

            if prev_value == 0:
                growth = None
            else:
                growth = ((curr_value - prev_value) / prev_value) * 100

            growth_metrics[col][curr_month] = round(growth, 2) if growth is not None else None

    # --------- Anomaly Detection ---------

    anomalies = {}

    for col in numeric_cols:
        series = df[col]

        mean = series.mean()
        std = series.std()

        anomaly_points = []

        if std != 0:
            for idx, value in series.items():
                z_score = (value - mean) / std
                if abs(z_score) > 3:  # threshold
                    anomaly_points.append({
                        "row": int(idx),
                        "value": float(value),
                        "z_score": round(z_score, 2)
                    })

        anomalies[col] = anomaly_points

    return {
        "numeric_columns": numeric_cols,
        "kpis": kpi_results,
        "monthly_trend": monthly_trend,
        "growth_metrics": growth_metrics,
        "anomalies": anomalies
    }