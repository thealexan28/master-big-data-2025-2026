from minio import Minio
from minio.error import S3Error
from app.config import settings

# Inicializamos el cliente de MinIO usando la configuración
minio_client = Minio(
    endpoint=settings.MINIO_ENDPOINT,
    access_key=settings.MINIO_ACCESS_KEY,    
    secret_key=settings.MINIO_SECRET_KEY,    
    secure=settings.MINIO_SECURE
)

def init_minio():
    """
    Verifica si el bucket de reportes existe. Si no existe, lo crea.
    """
    bucket_name = settings.MINIO_BUCKET_NAME
    try:
        print(f"Verificando bucket de MinIO: '{bucket_name}'...")
        if not minio_client.bucket_exists(bucket_name):
            minio_client.make_bucket(bucket_name)
            print(f"Bucket '{bucket_name}' creado exitosamente.")
        else:
            print(f"El bucket '{bucket_name}' ya existe. Todo listo.")
    except S3Error as e:
        print(f"Error al conectar con MinIO o crear el bucket: {e}")
        raise e