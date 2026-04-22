from netmiko import ConnectHandler

class RouterManager:
    def __init__(self, config):
        self.config = config

    def _connect(self, name):
        return ConnectHandler(**self.config[name])

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

                # Rutas correctas
                "ip route 200.1.13.0 255.255.255.252 200.1.23.2",
                "ip route 200.1.12.0 255.255.255.252 200.1.12.1"
            ]

            print(conn.send_config_set(comandos))
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

                # Ruta hacia R3
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

            print(conn.send_config_set(config))
            conn.disconnect()

        except Exception as e:
            print(f"[ERROR R1] {e}")