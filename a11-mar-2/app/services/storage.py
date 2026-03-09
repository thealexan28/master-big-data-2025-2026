import io
from minio.error import S3Error
from app.minio_client import minio_client
from app.config import settings

def upload_csv_to_minio(object_name: str, csv_content: bytes) -> str:
    """
    Sube un archivo CSV (en formato bytes) al bucket de MinIO.
    Devuelve el nombre del objeto subido.
    """
    # MinIO necesita un "stream" (flujo de datos) y su longitud
    csv_stream = io.BytesIO(csv_content)
    length = len(csv_content)
    
    minio_client.put_object(
        bucket_name=settings.MINIO_BUCKET_NAME,
        object_name=object_name,
        data=csv_stream,
        length=length,
        content_type="text/csv"
    )
    return object_name

def list_minio_reports() -> list[dict]:
    """
    Lista todos los reportes CSV disponibles en el bucket.
    """
    try:
        # recursive=True permite listar dentro de subcarpetas (ej: 2026-03-02/0900.csv)
        objects = minio_client.list_objects(settings.MINIO_BUCKET_NAME, recursive=True)
        reports = []
        for obj in objects:
            reports.append({
                "name": obj.object_name,
                "size": obj.size, # En bytes
                "last_modified": obj.last_modified
            })
        return reports
    except S3Error as e:
        print(f"Error listando objetos: {e}")
        return []

def get_report_from_minio(object_name: str) -> bytes:
    """
    Descarga el contenido de un reporte CSV desde MinIO.
    """
    try:
        response = minio_client.get_object(settings.MINIO_BUCKET_NAME, object_name)
        content = response.read()
        return content
    finally:
        # Es muy importante cerrar la conexión HTTP de MinIO
        if 'response' in locals():
            response.close()
            response.release_conn()