# a13 — Redis: introducción práctica

**Fecha:** 20 de abril de 2025  
**Duración:** ~40 minutos (un tercio de la clase)

---

## ¿Qué es Redis?

Redis es una base de datos **en memoria**, extremadamente rápida, que almacena datos como pares **clave → valor**. A diferencia de MongoDB (documentos) o PostgreSQL (tablas), Redis mantiene los datos en RAM, lo que le permite alcanzar cientos de miles de operaciones por segundo.

No es un sustituto de una base de datos tradicional. Es una capa que vive **al lado** de tu sistema para casos donde la velocidad es crítica:

- **Caché** — guardar resultados costosos para no recalcularlos
- **Sesiones de usuario** — almacenar tokens con expiración automática
- **Contadores en tiempo real** — visitas, likes, peticiones por IP
- **Rankings y leaderboards** — gracias a los Sorted Sets
- **Colas ligeras** — alternativa simple a RabbitMQ para tareas básicas

## Setup

```bash
# Levantar Redis con Docker
docker compose up -d

# Instalar el cliente Python
pip install redis

# Verificar que Redis está activo
docker compose exec redis redis-cli ping
# → PONG
```

## Notebook

Abre `redis.ipynb` y ejecútalo celda a celda. Cada sección introduce un tipo de dato con ejemplos interactivos.

| Sección | Tipo de dato | Caso de uso |
|---------|-------------|-------------|
| 1 | Strings | Contadores, caché, TTL |
| 2 | Hashes | Perfiles, configuración |
| 3 | Lists | Historial, colas de tareas |
| 4 | Sorted Sets | Rankings, leaderboards |

## Recursos

- [Redis documentation](https://redis.io/docs/latest/)
- [redis-py (cliente Python)](https://redis-py.readthedocs.io/)
- [Redis commands reference](https://redis.io/commands/)
- [Try Redis online (sin instalar nada)](https://try.redis.io/)
