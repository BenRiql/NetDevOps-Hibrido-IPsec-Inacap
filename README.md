####Automatización de Red con IPsec (Cisco + MikroTik + Docker)####

Este proyecto implementa la automatización de configuración de una red utilizando Python, Docker, Netmiko (SSH) y la API REST de MikroTik.

El objetivo es desplegar y configurar automáticamente:
Router R2 (ISP)
Router R1 (Sede Central)
Router R3 (MikroTik)
Incluyendo la creación de un túnel IPsec funcional entre Cisco (R1) y MikroTik (R3), validado con tráfico real.

Tecnologías utilizadas:
Python 3.11
Docker
Netmiko (automatización SSH para Cisco)
Requests (API REST MikroTik)
GNS3 (topología de red)
Cisco IOSv
MikroTik RouterOS v7
Topología de red

### 1. Clonar repositorio
git clone https://github.com/BenRiql/automatizacion-redes.git
cd automatizacion-redes

### 2. Construir Imagen
docker build -t automatizacion-redes .

### 3. Ejecutar contenedor
docker run --rm automatizacion-redes

### Red implementada:
R1 (Cisco)
LAN: 192.168.10.0/24
Enlace a ISP: 200.1.12.1/30
Enlace a R3: 200.1.13.1/30
R2 (ISP)
200.1.12.2/30 ↔ R1
200.1.23.1/30 ↔ R3
R3 (MikroTik)
LAN: 192.168.30.0/24
Enlace a ISP: 200.1.23.2/30
Enlace a R1: 200.1.13.2/30

### El túnel IPsec conecta:
192.168.10.0/24  <----IPsec---->  192.168.30.0/24
Funcionalidades
Configuración automática de interfaces en R1 y R2
Creación de rutas estáticas
Configuración de IPsec en Cisco (ISAKMP + transform-set + crypto map)
Configuración de IPsec en MikroTik mediante API REST:
Peer
Identity
Policy
Ejecución dentro de contenedor Docker
Logs de ejecución para verificación

### Configuración previa

Antes de ejecutar el script:
En Cisco (R1 y R2)

Debe estar habilitado SSH:
conf t
hostname R1
ip domain-name lab.local
username admin privilege 15 secret cisco123
crypto key generate rsa
ip ssh version 2
line vty 0 4
 login local
 transport input ssh
end
wr


### Habilitar API REST en MIKROTIK:
/ip service enable www

Credenciales usadas:
Usuario: admin
Password: inacap2030
Ejecución con Docker

El script realiza:
Espera inicial para que los routers levanten
Configuración de R2 (ISP)
Configuración de R1 (VPN + rutas)
Configuración de MikroTik vía API REST
Finalización
Validación

### 1. Verificar interfaces

En R1:
show ip interface brief
### 2. Verificar IPsec
show crypto isakmp sa
show crypto ipsec sa

Estado esperado:
QM_IDLE
Paquetes cifrados y descifrados > 0

### 3. Prueba de conectividad
ping 192.168.30.1 source 192.168.10.1
Resultado esperado:
Success rate is 100%

### 4. Verificación en MikroTik
/ip ipsec installed-sa print
Debe mostrar SAs en estado mature.
Logs del contenedor

Para revisar ejecución:
docker logs <container_id>
Ejemplo esperado:

[INFO] Conectando a R1...
[OK] Conectado a R1
[OK] Peer creado
[OK] Identity creada
[OK] Policy creada
Consideraciones importantes
El script está diseñado para ejecutarse en un entorno limpio
Si se ejecuta múltiples veces, pueden aparecer errores como:
Name can't repeat
Peer already exists
Estos errores no afectan si la configuración ya está aplicada
Problemas encontrados y soluciones
SSH Cisco incompatible con algoritmos modernos
Solución: permitir diffie-hellman-group14-sha1 y ssh-rsa
Contenedor terminaba inmediatamente
Solución: ejecutar el script como proceso principal
API MikroTik devolvía 401
Solución: corregir credenciales
Error "Peer not set"
Solución: crear correctamente peer antes de policy
Resultado final
Túnel IPsec operativo ✔
Conectividad entre redes privadas ✔
Automatización completa ✔
Integración Cisco + MikroTik ✔

Autor
Benjamin Sebastian Riquelme Landero.
