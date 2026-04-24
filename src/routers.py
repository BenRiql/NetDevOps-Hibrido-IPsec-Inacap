from netmiko import ConnectHandler
import time

class RouterManager:
    def __init__(self, config):
        self.config = config

    def _connect(self, name):
        nodo = self.config[name]

        for intento in range(5):
            try:
                print(f"[INFO] Conectando a {name} ({nodo['host']})...")

                device = {
                    "device_type": nodo["device_type"],
                    "host": nodo["host"],
                    "username": nodo["auth"]["username"],
                    "password": nodo["auth"]["password"],
                    "secret": nodo["auth"]["password"],

                    # estabilidad
                    "fast_cli": False,
                    "conn_timeout": 20,
                    "auth_timeout": 20,
                    "banner_timeout": 30,
                }

                conn = ConnectHandler(**device)
                conn.enable()

                print(f"[OK] Conectado a {name}")
                return conn

            except Exception as e:
                print(f"[REINTENTO {intento+1}] {name} no disponible: {e}")
                time.sleep(10)

        raise Exception(f"No se pudo conectar a {name}")

    def configurar_r2(self):
        print(">>> Configurando R2 (ISP)...")

        try:
            conn = self._connect("R2")

            comandos = [
                "interface g0/1",
                "ip address 200.1.12.2 255.255.255.252",
                "no shutdown",

                "interface g0/2",
                "ip address 200.1.23.1 255.255.255.252",
                "no shutdown",

                # rutas
                "ip route 200.1.13.0 255.255.255.252 200.1.23.2",
                "ip route 200.1.12.0 255.255.255.252 200.1.12.1"
            ]

            output = conn.send_config_set(comandos)
            print(output)

            conn.disconnect()

        except Exception as e:
            print(f"[ERROR R2] {e}")

    def configurar_r1(self):
        print(">>> Configurando R1 (Sede Central)...")

        try:
            conn = self._connect("R1")

            config = [
                "interface g0/1",
                "ip address 200.1.12.1 255.255.255.252",
                "no shutdown",

                "interface g0/2",
                "ip address 200.1.13.1 255.255.255.252",
                "no shutdown",

                "interface loopback10",
                "ip address 192.168.10.1 255.255.255.0",

                # ruta hacia R3
                "ip route 192.168.30.0 255.255.255.0 200.1.13.2",

                # --- IPSEC ---
                "crypto isakmp policy 10",
                "encryption aes",
                "hash sha",
                "authentication pre-share",
                "group 2",

                "crypto isakmp key cisco123 address 200.1.13.2",

                "crypto ipsec transform-set TSET esp-aes esp-sha-hmac",
                "mode tunnel",

                "access-list 100 permit ip 192.168.10.0 0.0.0.255 192.168.30.0 0.0.0.255",

                "crypto map CMAP 10 ipsec-isakmp",
                "set peer 200.1.13.2",
                "set transform-set TSET",
                "match address 100",

                "interface g0/2",
                "crypto map CMAP"
            ]

            output = conn.send_config_set(config)
            print(output)

            conn.disconnect()

        except Exception as e:
            print(f"[ERROR R1] {e}")