from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, Path
from sqlalchemy.orm import Session
import shutil
import os
import pandas as pd

from db.session import get_db
from models.datasets import Dataset
from models.dataset_metadata import DatasetMetadata

from api.auth import get_current_user

from services.metric_detector import detect_business_metrics
from services.correlation_engine import detect_correlations
from services.insight_engine import generate_insights
from services.metadata_engine import generate_metadata
from services.data_quality_engine import analyze_data_quality
from services.kpi_engine import calculate_kpis

router = APIRouter(prefix="/datasets", tags=["Datasets"])

UPLOAD_FOLDER = "uploads"

# ----------------------------
# Upload Dataset
# ----------------------------
@router.post("/upload")
def upload_dataset(
    file: UploadFile = File(...),
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files allowed")

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    # Save file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Save dataset record
    new_dataset = Dataset(
        filename=file.filename,
        file_path=file_path
    )

    db.add(new_dataset)
    db.commit()
    db.refresh(new_dataset)

    # Generate metadata
    df = pd.read_csv(file_path)

    metadata = generate_metadata(df)

    new_metadata = DatasetMetadata(
        dataset_id=new_dataset.id,
        numeric_columns=",".join(metadata["numeric_columns"]),
        date_column=metadata["date_column"],
        detected_metrics=""
    )

    db.add(new_metadata)
    db.commit()

    return {
        "message": "File uploaded successfully",
        "dataset_id": new_dataset.id
    }


# ----------------------------
# Dataset Summary
# ----------------------------
@router.get("/{dataset_id}/summary")
def dataset_summary(
    dataset_id: int = Path(...),
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    dataset = db.query(Dataset).filter(Dataset.id == dataset_id).first()

    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")

    df = pd.read_csv(dataset.file_path)

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

        if pd.api.types.is_numeric_dtype(df[col]):
            column_info.update({
                "mean": float(df[col].mean()),
                "min": float(df[col].min()),
                "max": float(df[col].max())
            })

        summary["column_details"].append(column_info)

    return summary


# ----------------------------
# KPI Calculation
# ----------------------------
@router.get("/{dataset_id}/kpis")
def dataset_kpis(
    dataset_id: int,
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    dataset = db.query(Dataset).filter(Dataset.id == dataset_id).first()

    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")

    df = pd.read_csv(dataset.file_path)

    kpis = calculate_kpis(df)

    return {
        "kpis": kpis
    }


# ----------------------------
# Metric Detection
# ----------------------------
@router.get("/{dataset_id}/metrics")
def detect_metrics(
    dataset_id: int,
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    dataset = db.query(Dataset).filter(Dataset.id == dataset_id).first()

    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")

    df = pd.read_csv(dataset.file_path)

    detected = detect_business_metrics(df.columns)

    return {
        "detected_metrics": detected
    }


# ----------------------------
# Correlation Analysis
# ----------------------------
@router.get("/{dataset_id}/correlations")
def dataset_correlations(
    dataset_id: int,
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    dataset = db.query(Dataset).filter(Dataset.id == dataset_id).first()

    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")

    df = pd.read_csv(dataset.file_path)

    correlations = detect_correlations(df)

    return {
        "correlations": correlations
    }


# ----------------------------
# Insight Generation
# ----------------------------
@router.get("/{dataset_id}/insights")
def dataset_insights(
    dataset_id: int,
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    dataset = db.query(Dataset).filter(Dataset.id == dataset_id).first()

    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")

    df = pd.read_csv(dataset.file_path)

    correlations = detect_correlations(df)

    growth_metrics = {}
    anomalies = {}

    insights = generate_insights(growth_metrics, correlations, anomalies)

    return {
        "insights": insights
    }


# ----------------------------
# Data Quality Analysis
# ----------------------------
@router.get("/{dataset_id}/quality")
def dataset_quality(
    dataset_id: int,
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    dataset = db.query(Dataset).filter(Dataset.id == dataset_id).first()

    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")

    df = pd.read_csv(dataset.file_path)

    quality_report = analyze_data_quality(df)

    return {
        "data_quality": quality_report
    }