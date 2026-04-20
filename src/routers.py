from netmiko import ConnectHandler
import time

class RouterManager:
    def __init__(self, nodos_config):
        self.config = nodos_config

    def _conectar(self, nombre_nodo):
        """Establece conexión con un nodo Cisco usando los datos de config.py"""
        nodo = self.config[nombre_nodo]
        device = {
            'device_type': nodo['device_type'],
            'host': nodo['host'],
            'username': nodo['auth']['username'],
            'password': nodo['auth']['password'],
        }
        return ConnectHandler(**device)

    def configurar_r2(self):
        """R2 es el ISP: Solo necesita rutas estáticas para unir R1 y R3 [cite: 35]"""
        print(">>> Configurando R2 (Router de Tránsito)...")
        try:
            with self._conectar("R2") as net_connect:
                comandos = [
                    "ip route 200.1.13.0 255.255.255.252 200.1.12.1", # Hacia R1
                    "ip route 200.1.13.0 255.255.255.252 200.1.23.2", # Hacia R3
                ]
                output = net_connect.send_config_set(comandos)
                print(output)
                print("[OK] R2 configurado.")
        except Exception as e:
            print(f"[!] Error en R2: {e}")

    def configurar_r1(self):
        """R1 es Sede Central: Configura IPs, Rutas e IPsec [cite: 18, 36]"""
        print(">>> Configurando R1 (Sede Central)...")
        try:
            with self._conectar("R1") as net_connect:
                # Configuración de interfaces y rutas base [cite: 19, 29]
                config_base = [
                    "interface Gi0/1",
                    "ip address 200.1.12.1 255.255.255.252",
                    "no shutdown",
                    "interface Gi0/2",
                    "ip address 200.1.13.1 255.255.255.252",
                    "no shutdown",
                    "interface Loopback10",
                    "ip address 192.168.10.1 255.255.255.0",
                    "ip route 192.168.30.0 255.255.255.0 200.1.13.2" # Ruta hacia LAN de R3
                ]
                
                # Configuración IPsec Fase 1 y 2 [cite: 36]
                config_vpn = [
                    "crypto isakmp policy 10",
                    "encryption aes",
                    "authentication pre-share",
                    "group 2",
                    "crypto isakmp key cisco123 address 200.1.13.2",
                    "crypto ipsec transform-set TSET esp-aes esp-sha-hmac",
                    "mode tunnel",
                    "crypto map CMAP 10 ipsec-isakmp",
                    "set peer 200.1.13.2",
                    "set transform-set TSET",
                    "match address 100",
                    "access-list 100 permit ip 192.168.10.0 0.0.0.255 192.168.30.0 0.0.0.255",
                    "interface Gi0/2",
                    "crypto map CMAP"
                ]
                
                net_connect.send_config_set(config_base)
                output = net_connect.send_config_set(config_vpn)
                print(output)
                print("[OK] R1 y VPN IPsec configurados.")
        except Exception as e:
            print(f"[!] Error en R1: {e}")