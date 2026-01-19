# Comandos Básicos de Linux

## Instalación de Paquetes

- `apt-get update` - Actualiza lista de paquetes disponibles
- `apt-get install` - Instala paquetes (`apt-get install tree nano htop`)
- `apt-get remove` - Desinstala paquetes

## Navegación

- `pwd` - Muestra el directorio actual
- `ls` - Lista archivos (`-l` detalles, `-a` ocultos, `-h` tamaño legible)
- `cd` - Cambia de directorio

## Ubicaciones Importantes en Linux

- **`/`** - Raíz del sistema (todo parte de aquí)
- **`/home`** - Directorios de usuarios (`/home/usuario`)
- **`/root`** - Home del usuario root
- **`~`** - Atajo a tu directorio home
- **`/etc`** - Archivos de configuración del sistema
- **`/tmp`** - Archivos temporales (se borran al reiniciar)
- **`/usr`** - Programas y librerías del sistema
- **`/bin`** - Comandos binarios esenciales
- **`/opt`** - Software adicional instalado

### Entender permisos con ls -l

Cuando haces `ls -l` ves algo como: `drwxr-x---+`

**Las tres categorías de permisos:**
1. **Usuario (owner)**: El propietario del archivo
2. **Grupo (group)**: Usuarios que pertenecen al mismo grupo
3. **Otros (others)**: Todos los demás usuarios del sistema

Ejemplo: Si un archivo es `rwxr-x---` y pertenece al grupo "desarrollo":
- El propietario puede leer, escribir y ejecutar
- Los usuarios del grupo "desarrollo" pueden leer y ejecutar
- El resto de usuarios no pueden acceder

**Permisos:**
- `r` (read) = 4 - Leer
- `w` (write) = 2 - Escribir
- `x` (execute) = 1 - Ejecutar

**Ejemplos:**
- `rwx` = 7 (todos los permisos)
- `r-x` = 5 (leer y ejecutar)
- `r--` = 4 (solo leer)
- `---` = 0 (ninguno)

**Permisos comunes con chmod:**
- `chmod 755 script.sh` = `rwxr-xr-x` (dueño: todo, otros: leer/ejecutar) - típico para scripts
- `chmod 644 archivo.txt` = `rw-r--r--` (dueño: leer/escribir, otros: solo leer) - típico para archivos
- `chmod 777 archivo` = `rwxrwxrwx` (todos: todo) - PELIGROSO, evitar
- `chmod 600 clave.txt` = `rw-------` (solo dueño puede leer/escribir) - para archivos privados

**Importante:** El usuario `root` puede acceder a CUALQUIER archivo independientemente de los permisos. Los permisos solo aplican a usuarios normales.

**Símbolos al final:**
- `+` - ACLs extendidas (permisos adicionales)
- `@` - Atributos extendidos (metadatos, común en macOS)

## Archivos

- `cat` - Muestra contenido de archivo
- `head` / `tail` - Primeras/últimas líneas (`-n 20`, `-f` seguir)
- `less` - Ver archivo (navegable, `q` salir)
- `touch` - Crea archivo vacío
- `cp` - Copia archivos/carpetas
- `mv` - Mueve o renombra
- `rm` - Elimina (`-r` directorios, `-f` forzar)
- `mkdir` - Crea directorio (`-p` con subdirectorios)

## Editores de Texto

- `nano` - Editor simple (Ctrl+O guardar, Ctrl+X salir)
- `vi` / `vim` - Editor avanzado (`:wq` guardar y salir, `:q!` salir sin guardar)

## Búsqueda

- `find` - Busca archivos (`find . -name "*.txt"`)
- `grep` - Busca texto en archivos (`-r` recursivo, `-i` ignora mayúsculas)
- `which` - Muestra ruta de un comando

## Sistema

- `whoami` - Usuario actual
- `df -h` - Espacio en disco
- `top` / `htop` - Monitor de procesos

## Permisos y Superusuario

- **`sudo comando`** - Ejecuta comando como superusuario (administrador)
- **Usuario normal vs root**:
  - Usuario normal: Permisos limitados, no puede modificar el sistema
  - root: Superusuario, puede hacer cualquier cosa
- **Cuándo usar sudo**:
  - Instalar/desinstalar software: `sudo apt-get install`
  - Modificar archivos del sistema: `sudo nano /etc/archivo`
  - Gestionar servicios: `sudo systemctl restart servicio`
- `sudo su` - Cambiar a usuario root (no recomendado, mejor usar sudo)
- `sudo !!` - Repite último comando con sudo

**Cuidado:** Con sudo puedes romper el sistema. Úsalo solo cuando sea necesario.

### El comando más peligroso de Linux

```bash
sudo rm -rf /
```

**¿Qué hace cada parte?**
- `sudo` - Ejecuta como superusuario (permisos totales)
- `rm` - Remove (eliminar)
- `-r` - Recursivo (entra en todos los subdirectorios)
- `-f` - Force (sin preguntar confirmación)
- `/` - Desde la raíz (TODO el sistema)

**Protección moderna:** Desde 2013, Linux tiene protección y da error. Para que realmente funcione habría que añadir `--no-preserve-root`, pero NUNCA lo hagas.

**Resultado si se ejecuta:** Borra todo el sistema operativo completo. El ordenador queda inutilizable.

## Utilidades

- `echo` - Imprime texto
- `clear` - Limpia pantalla
- `history` - Historial de comandos
- `|` - Pipe: conecta salida con entrada (`ls | grep txt`)
- `>` - Redirige salida sobrescribiendo (`ls > archivo.txt`)
- `>>` - Redirige salida añadiendo (`echo "hola" >> archivo.txt`)
- `&&` - Ejecuta segundo comando SOLO si primero tiene éxito (`apt-get update && apt-get install python3`)
- `||` - Ejecuta segundo comando SOLO si primero falla (`rm archivo.txt || echo "Error al borrar"`)
- `wget` / `curl` - Descarga archivos
- `chmod +x` - Hace archivo ejecutable

## Atajos de Teclado

- `Ctrl + C` - Cancela comando
- `Ctrl + L` - Limpia pantalla
- `Ctrl + R` - Busca en historial de comandos
- `Tab` - Autocompletar
- `↑` / `↓` - Navegar historial

## Variables de Entorno

- `echo $VARIABLE` - Muestra el valor de una variable (`echo $HOME`, `echo $PATH`)
- `export VARIABLE=valor` - Crea/modifica variable de entorno
- `env` - Lista todas las variables de entorno
- Variables comunes:
  - `$HOME` - Directorio home del usuario
  - `$USER` - Nombre del usuario
  - `$PATH` - Rutas donde busca comandos
  - `$PWD` - Directorio actual

## Shell y Configuración

- **Shell**: El intérprete de comandos (bash, zsh)

**¿Qué shell estoy usando?**
```bash
echo $SHELL
```
- Si dice `/bin/bash` → usas bash → edita `.bashrc`
- Si dice `/bin/zsh` → usas zsh → edita `.zshrc`

**Archivos de configuración (en tu home):**
- **`.bashrc`** - Configuración de bash (Linux)
- **`.bash_profile`** - Configuración de bash en login (macOS usa este en vez de .bashrc)
- **`.zshrc`** - Configuración de zsh (shell moderno, por defecto en macOS desde 2019)

### Añadir al PATH (permanente)

El PATH es donde el sistema busca comandos. Para añadir un directorio de forma PERMANENTE:

**Paso 1: Edita tu archivo de configuración**
```bash
nano ~/.bashrc      # Si usas bash (Linux)
nano ~/.zshrc       # Si usas zsh
```

**Paso 2: Añade al final del archivo**
```bash
export PATH="$PATH:/home/usuario/mis_scripts"
```

**Paso 3: Guarda y cierra** (Ctrl+O, Enter, Ctrl+X en nano)

**Paso 4: Recarga la configuración**
```bash
source ~/.bashrc    # Para bash
source ~/.zshrc     # Para zsh
```

O simplemente cierra y abre la terminal.

**Ejemplo típico (añadir Python local):**
```bash
export PATH="$HOME/.local/bin:$PATH"
```

**Diferencia temporal vs permanente:**
- Si solo haces `export PATH="..."` en la terminal → TEMPORAL (solo en esta sesión)
- Si lo añades al archivo `.bashrc`/`.zshrc` → PERMANENTE (cada vez que abras terminal)

**Nota:** 
- `$PATH` al final: añade tu directorio al final
- `:$PATH` al principio: tu directorio tiene prioridad

## Conexión Remota y Transferencia de Archivos

### ssh - Conectar a servidores remotos

```bash
ssh usuario@servidor.com              # Conectar a servidor
ssh usuario@192.168.1.100            # Conectar por IP
```

**Ejemplo real:**
```bash
ssh admin@miservidor.com
```

### scp - Copiar archivos entre máquinas

```bash
# Copiar archivo local a servidor remoto
scp archivo.txt usuario@servidor:/ruta/destino/

# Copiar archivo de servidor a local
scp usuario@servidor:/ruta/archivo.txt ./

# Copiar directorio completo (recursivo)
scp -r carpeta/ usuario@servidor:/ruta/destino/
```

### ping - Comprobar conectividad

```bash
ping google.com                       # Comprobar si hay conexión
ping 8.8.8.8
```

## Desconectar y Background (trabajar con servidores)

Cuando trabajas en un servidor remoto, necesitas que los procesos sigan corriendo al desconectarte.

### Ejecutar en background

```bash
comando &                             # Ejecuta en background desde el inicio
python script.py &                    # Ejemplo: script en background
```

### screen - Sesiones persistentes

**screen** (más simple):
```bash
screen                                # Inicia sesión
Ctrl+A, D                            # Desconectar (detach)
screen -r                            # Reconectar
screen -ls                           # Listar sesiones
```

Otras opciones son nohup o tmux

**Caso de uso:** Empiezas un entrenamiento de ML en el servidor, te desconectas con screen/tmux, y sigue corriendo.

## Comandos en Dockerfiles (contexto profesional)

Comandos Linux que verás en Dockerfiles y entornos de desarrollo:

**Instalación de paquetes:**
```bash
apt-get update && apt-get install -y paquete
```

**Crear directorios:**
```bash
mkdir -p /app/logs
```

**Cambiar permisos:**
```bash
chmod 755 script.sh          # rwxr-xr-x (ejecutable)
chmod 644 config.txt         # rw-r--r-- (solo lectura)
chown usuario:grupo archivo  # Cambiar propietario
```

**Comandos múltiples en una línea:**
```bash
apt-get update && \
apt-get install -y python3 && \
rm -rf /var/lib/apt/lists/*
```
El `\` permite dividir comandos largos en varias líneas
El último comando limpia la cache de apt (reduce tamaño de imagen)

**Ejemplo real de Dockerfile:**
```dockerfile
RUN apt-get update && \
    apt-get install -y python3 pip && \
    mkdir -p /app/logs && \
    chmod 755 /app/entrypoint.sh && \
    rm -rf /var/lib/apt/lists/*
```

## Ayuda

- `man comando` - Manual completo
- `comando --help` - Ayuda rápida
