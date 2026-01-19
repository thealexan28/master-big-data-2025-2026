# 19 de Enero - Comandos Linux Básicos

Introducción a comandos de Linux y usar la terminal.

## Opciones para practicar

### Opción 1: WSL (Windows Subsystem for Linux) - Recomendado

Como todos teneis ya Docker instalado, podeis abrir WSL:

1. Abre el menú inicio y busca "Ubuntu" o "WSL"
2. O abre PowerShell/CMD y escribe: `wsl`

**Nota:** En WSL entrarás con tu usuario normal (no root).

### Opción 2: Docker (alternativa si WSL no funciona)

Si WSL no te funciona, usa Docker:

```bash
docker run -it --rm ubuntu bash
```

**Nota:** Con Docker entrarás como `root` (superusuario) en el directorio `/root`.

Con un solo comando ya estás dentro de Linux. Si necesitas instalar herramientas (nano, tree, etc.), puedes hacerlo con `apt-get install`.