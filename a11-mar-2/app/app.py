from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.database import connect_to_mongo, close_mongo_connection
from app.minio_client import init_minio
from app.routers import readings, reports

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 1. Conectar a MongoDB
    await connect_to_mongo()
    # 2. Inicializar el bucket de MinIO si no existe
    init_minio()
    yield
    # 3. Cerrar conexiones al apagar
    await close_mongo_connection()

app = FastAPI(
    title="SensorHub IoT Platform",
    description="API para monitorización ambiental y generación de reportes CSV",
    version="1.0.0",
    lifespan=lifespan
)

# Endpoint de Healthcheck (Raíz o /health)
@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "ok", "service": "SensorHub API en funcionamiento"}

# Incluimos los routers que creamos antes
app.include_router(readings.router, prefix="/readings", tags=["Readings (Sensores)"])

# En reports.py metimos también el /export, así que lo incluimos aquí
app.include_router(reports.router, prefix="/reports", tags=["Reports & Export (MinIO)"])