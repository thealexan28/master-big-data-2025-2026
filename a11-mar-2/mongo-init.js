// Nos cambiamos a la base de datos 'sensorhub'
// (Si no existe, MongoDB la creará en cuanto insertemos algo)
db = db.getSiblingDB('sensorhub');

print("=== INICIANDO CONFIGURACIÓN DE MONGODB ===");

// Creamos un usuario específico para que la API se conecte
db.createUser({
  user: "sensor_admin",
  pwd: "secretpassword", // Esta es la que pondremos en el .env
  roles: [
    {
      role: "readWrite",
      db: "sensorhub"
    }
  ]
});

// Creamos la colección explícitamente (opcional en Mongo, pero buena práctica)
db.createCollection("readings");

print("=== BASE DE DATOS INICIALIZADA CON ÉXITO ===");