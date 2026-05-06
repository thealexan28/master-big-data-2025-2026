# Clase 14 · Kubernetes

Primeras sesiones de Kubernetes del master. A lo largo de varias clases vamos a:

1. Entender por que necesitamos un orquestador (no nos vale docker-compose).
2. Conocer los recursos basicos de Kubernetes: **Pod, Deployment, Service, ConfigMap, Secret, PersistentVolumeClaim, Namespace, Ingress**.
3. Montar un cluster local con **k3d** (Kubernetes encima de Docker).
4. Desplegar nginx, **MinIO** y **Postgres** sobre ese cluster, sin docker-compose.
5. Manejar el cluster con tres herramientas: `kubectl` (CLI estandar), **k9s** (TUI) y **Lens** / Freelens (GUI).

## Que necesitais traer instalado

Solo una cosa:

- **Docker Desktop** para Windows, con el backend **WSL2** activado (Settings → General → "Use the WSL 2 based engine").

El resto (`k3d`, `kubectl`, `k9s`, Lens) lo instalamos juntos en clase. Si quereis adelantar:

```powershell
winget install k3d-io.k3d
winget install Derailed.k9s
winget install Mutagen.Lens
```

Alternativas si winget no os va:
- **Scoop**: `scoop install k3d k9s` y Lens descargado de https://k8slens.dev.
- **Freelens** (fork de Lens sin login): https://github.com/freelensapp/freelens/releases.

`kubectl` viene con Docker Desktop, no hace falta instalarlo aparte.

## Verificar antes de clase

```powershell
docker version
kubectl version --client
```

Si las dos devuelven version, estais listos.

## Estructura del repo

```
a14-may-6/
├── README.md          # este archivo
└── manifests/         # los YAML que aplicamos en clase
```

## Recursos para repasar despues

- Documentacion oficial: https://kubernetes.io/docs/home/
- learnk8s (diagramas): https://learnk8s.io/troubleshooting-deployments
- Curso libre en español: https://pabpereza.dev/docs/cursos/kubernetes
