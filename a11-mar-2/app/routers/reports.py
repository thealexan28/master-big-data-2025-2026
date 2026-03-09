from fastapi import APIRouter, HTTPException, Query, Response
from datetime import datetime, timedelta, timezone
from typing import Optional
import pandas as pd

from app.database import get_database
from app.services.analytics import generate_hourly_csv
from app.services.storage import upload_csv_to_minio, list_minio_reports, get_report_from_minio

router = APIRouter()

@router.post("/generate", status_code=201)
async def generate_report(
    hour: Optional[datetime] = Query(None, description="Hora a procesar en ISO. Ej: 2026-03-02T09:00:00Z")
):
    """Genera un reporte CSV horario, lo sube a MinIO y devuelve el enlace."""
    db = get_database()
    
    # Si no se pasa hora, usamos la actual
    target_time = hour or datetime.now(timezone.utc)
    
    # Truncamos a la hora exacta (ej: 09:34 -> 09:00)
    start_time = target_time.replace(minute=0, second=0, microsecond=0)
    end_time = start_time + timedelta(hours=1)
    
    # Buscamos en Mongo los datos de esa hora
    cursor = db["readings"].find({
        "timestamp": {
            "$gte": start_time,
            "$lt": end_time
        }
    })
    readings = await cursor.to_list(length=None)
    
    # Generamos el CSV en bytes (incluso si está vacío, generará cabeceras)
    csv_bytes = generate_hourly_csv(readings)
    
    # Creamos un nombre de archivo con la estructura: YYYY-MM-DD/HH00.csv
    folder = start_time.strftime("%Y-%m-%d")
    filename = start_time.strftime("%H00.csv")
    object_name = f"{folder}/{filename}"
    
    # Subimos a MinIO
    upload_csv_to_minio(object_name, csv_bytes)
    
    return {
        "message": "Reporte generado con éxito",
        "object_name": object_name,
        "download_url": f"/reports/{object_name}"
    }


@router.get("/")
async def list_reports():
    """Lista los reportes disponibles en MinIO."""
    reports = list_minio_reports()
    return reports


@router.get("/export")
async def export_raw_data():
    """Descarga todas las lecturas crudas en formato CSV."""
    db = get_database()
    cursor = db["readings"].find()
    readings = await cursor.to_list(length=None)
    
    if not readings:
        raise HTTPException(status_code=404, detail="No hay datos para exportar")
        
    df = pd.DataFrame(readings)
    # Eliminamos el _id de Mongo porque no es útil en el CSV
    if "_id" in df.columns:
        df = df.drop(columns=["_id"])
        
    # Convertimos a CSV directamente a un string
    csv_data = df.to_csv(index=False)
    
    return Response(
        content=csv_data,
        media_type="text/csv",
        headers={"Content-Disposition": 'attachment; filename="raw_readings.csv"'}
    )


@router.get("/{report_name:path}")
async def download_report(report_name: str):
    """
    Descarga un reporte concreto desde MinIO.
    El parámetro :path permite que el nombre incluya subdirectorios (ej: 2026-03-02/0900.csv).
    """
    try:
        csv_content = get_report_from_minio(report_name)
        
        # Devolvemos el CSV directamente como un archivo adjunto
        return Response(
            content=csv_content,
            media_type="text/csv",
            headers={"Content-Disposition": f'attachment; filename="{report_name.split("/")[-1]}"'}
        )
    except Exception as e:
        raise HTTPException(status_code=404, detail="Reporte no encontrado en MinIO")