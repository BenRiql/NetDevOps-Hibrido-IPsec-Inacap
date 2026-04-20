# Automatización de Redes con Python, Docker y GNS3

## Descripción
Este proyecto automatiza la configuración de una topologia hibrida en GNS3 para la asignatura Redes Avanzadas I. Implementa NrtDevOps para configurar:
- **Cisco IOSv**: Via SSH/Telnet (Netmiko) para enrutamiento e IPsec.
- **MikroTik CHR (R3)**: Vía API REST (Requests) con payload JSON.
- **Seguridad**: Túnel VPN IPsec entre R1 y R3.

## Requisitos
- GNS3 con los nodos configurados según la tabla de direccionamiento.
- Docker instalado para la ejecución del nodo de automatización.
- Python 3.11+.

## Instalación

### 1. Clonar repositorio
git clone https://github.com/TU_USUARIO/PROYECTO_V1.git
cd PROYECTO_V1


### 2. Construir imagen Docker
docker build -t netdevops-app .

### 3. Ejecutar contenedor
docker run --network gns3-oob-net netdevops-app`

## Estructura del Proyecto
App.py
src/
├── routers.py       # Conexión a routers
├── api_rest.py      # Consumo de API REST (MikroTik) y parseo JSON.
└── requirements.txt # Dependencias del proyecto (netmiko, requests).
## Autores
- Benjamin Sebastian Riquelme Landero
- David Fernando Pradenas Leiva

