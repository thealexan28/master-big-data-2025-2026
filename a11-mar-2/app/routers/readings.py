from fastapi import APIRouter, HTTPException, Query, Depends
from pydantic import BaseModel, Field
from datetime import datetime, timezone
from typing import Optional

from app.database import get_database
from app.services.analytics import calculate_device_stats

router = APIRouter()

# --- MODELOS PYDANTIC (Para Swagger) ---
class ReadingCreate(BaseModel):
    device_id: str = Field(..., example="sensor-001")
    location: str = Field(..., example="Sala de reuniones A")
    temperature: float = Field(..., example=22.5)
    humidity: float = Field(..., example=45.2)
    co2: float = Field(..., example=420.0)
    # Si no nos envían timestamp, Pydantic usa la hora UTC actual por defecto
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

# --- ENDPOINTS ---

@router.post("/", status_code=201)
async def create_reading(reading: ReadingCreate):
    """Guarda una nueva lectura de un sensor en MongoDB."""
    db = get_database()
    
    # Convertimos el modelo a un diccionario
    reading_dict = reading.model_dump()
    
    # Insertamos en la colección 'readings'
    result = await db["readings"].insert_one(reading_dict)
    
    return {"message": "Lectura guardada", "id": str(result.inserted_id)}


@router.get("/")
async def get_readings(
    device_id: Optional[str] = Query(None, description="Filtrar por ID de dispositivo"),
    limit: int = Query(100, ge=1, le=1000, description="Límite de resultados")
):
    """Lista las lecturas guardadas. Permite filtrar y limitar resultados."""
    db = get_database()
    query = {}
    if device_id:
        query["device_id"] = device_id
        
    cursor = db["readings"].find(query).limit(limit).sort("timestamp", -1)
    readings = await cursor.to_list(length=limit)
    
    # MongoDB devuelve el _id como ObjectId, que no es serializable en JSON directamente.
    # Lo convertimos a string.
    for r in readings:
        r["_id"] = str(r["_id"])
        
    return readings


@router.get("/stats")
async def get_readings_stats():
    """Devuelve estadísticas agregadas usando pandas y numpy."""
    db = get_database()
    # Para las stats, sacamos todas las lecturas (en producción se acotaría por tiempo)
    cursor = db["readings"].find()
    readings = await cursor.to_list(length=None)
    
    if not readings:
        return []
        
    # Usamos nuestro servicio de analytics
    stats = calculate_device_stats(readings)
    return stats