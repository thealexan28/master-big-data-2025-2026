from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings

class DataBase:
    client: AsyncIOMotorClient = None

db = DataBase()

async def connect_to_mongo():
    """Abre la conexión con MongoDB. Se llama al arrancar la API."""
    print("Conectando a MongoDB...")
    db.client = AsyncIOMotorClient(settings.MONGO_URI)
    print("Conectado a MongoDB exitosamente.")

async def close_mongo_connection():
    """Cierra la conexión con MongoDB. Se llama al apagar la API."""
    if db.client:
        print("Cerrando conexión a MongoDB...")
        db.client.close()
        print("Conexión cerrada.")

def get_database():
    """Devuelve la instancia de la base de datos para usarla en los endpoints."""
    return db.client[settings.MONGO_DB]