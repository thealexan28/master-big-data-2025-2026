import pandas as pd
import numpy as np
import io

def calculate_device_stats(readings: list[dict]) -> list[dict]:
    """
    Calcula estadísticas agrupadas por dispositivo:
    número de lecturas, temperatura (media y std), humedad (media), CO2 (media y max).
    """
    if not readings:
        return []
    
    # Cargamos la lista de diccionarios en un DataFrame
    df = pd.DataFrame(readings)
    
    # Agrupamos y calculamos las agregaciones
    stats = df.groupby('device_id').agg(
        num_readings=('device_id', 'count'),
        temp_mean=('temperature', 'mean'),
        temp_std=('temperature', 'std'),
        hum_mean=('humidity', 'mean'),
        co2_mean=('co2', 'mean'),
        co2_max=('co2', 'max')
    ).reset_index()
    
    # pandas pone NaN en la desviación típica si solo hay 1 lectura. 
    # Lo cambiamos a None (null en JSON) para que la API no falle.
    stats = stats.replace({np.nan: None})
    
    # Devolvemos una lista de diccionarios
    return stats.to_dict(orient='records')


def generate_hourly_csv(readings: list[dict]) -> bytes:
    """
    Agrega los datos por dispositivo y ubicación, y devuelve el contenido CSV en bytes.
    """
    if not readings:
        # Si no hay datos en esa hora, devolvemos un CSV vacío solo con cabeceras
        df = pd.DataFrame(columns=['device_id', 'location', 'temp_mean', 'hum_mean', 'co2_mean', 'readings_count'])
    else:
        df = pd.DataFrame(readings)
        # Agregamos por dispositivo y ubicación
        df = df.groupby(['device_id', 'location']).agg(
            temp_mean=('temperature', 'mean'),
            hum_mean=('humidity', 'mean'),
            co2_mean=('co2', 'mean'),
            readings_count=('device_id', 'count')
        ).reset_index()
        
        # Redondeamos a 2 decimales para que el CSV quede limpio
        df = df.round(2)
        
    # Usamos StringIO para generar el CSV en memoria sin tocar el disco duro
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)
    
    # Lo pasamos a bytes, que es lo que necesita MinIO
    return csv_buffer.getvalue().encode('utf-8')