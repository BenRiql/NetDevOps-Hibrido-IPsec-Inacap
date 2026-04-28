import requests
from requests.auth import HTTPBasicAuth

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class R3Manager:
    def __init__(self, config):
        self.host = config["host"]
        self.auth = HTTPBasicAuth(config["username"], config["password"])
        self.base_url = f"http://{self.host}/rest"

    def _post(self, endpoint, payload):
        url = f"{self.base_url}{endpoint}"

        try:
            response = requests.post(
                url,
                json=payload,
                auth=self.auth,
                verify=False,
                timeout=10
            )

            print(f"[DEBUG] POST {endpoint}")
            print(response.text)

            return response

        except Exception as e:
            print(f"[ERROR CONEXIÓN] {e}")
            return None

    # -------------------------
    # LIMPIEZA (evita errores)
    # -------------------------
    def limpiar_ipsec(self):
        print("[R3] Limpiando configuración IPsec previa...")

        self._post("/ip/ipsec/policy/remove", {"numbers": "all"})
        self._post("/ip/ipsec/identity/remove", {"numbers": "all"})
        self._post("/ip/ipsec/peer/remove", {"numbers": "all"})

    # -------------------------
    # BASE: INTERFACES + IP
    # -------------------------
    def configurar_interfaces(self):
        print("[R3] Configurando direcciones IP...")

        self._post("/ip/address/add", {
            "address": "192.168.122.30/24",
            "interface": "ether1"
        })

        self._post("/ip/address/add", {
            "address": "200.1.13.2/30",
            "interface": "ether3"
        })

        self._post("/ip/address/add", {
            "address": "200.1.23.2/30",
            "interface": "ether2"
        })

    # -------------------------
    # LOOPBACK
    # -------------------------
    def configurar_loopback(self):
        print("[R3] Configurando loopback...")

        # crear interfaz (si ya existe, ignorar error)
        self._post("/interface/bridge/add", {
            "name": "loopback"
        })

        # asignar IP
        self._post("/ip/address/add", {
            "address": "192.168.30.1/24",
            "interface": "loopback"
        })

    # -------------------------
    # RUTAS
    # -------------------------
    def configurar_rutas(self):
        print("[R3] Configurando rutas...")

        self._post("/ip/route/add", {
            "dst-address": "192.168.10.0/24",
            "gateway": "200.1.13.1"
        })

    # -------------------------
    # IPsec
    # -------------------------
    def configurar_ipsec(self):
        print("[R3] Configurando IPsec...")

        # PEER
        peer_payload = {
            "name": "to-R1",
            "address": "200.1.13.1",
            "exchange-mode": "main"
        }

        r = self._post("/ip/ipsec/peer/add", peer_payload)
        if not r or r.status_code not in [200, 201]:
            print("[ERROR] Peer")
            return False

        # IDENTITY
        identity_payload = {
            "peer": "to-R1",
            "auth-method": "pre-shared-key",
            "secret": "cisco123"
        }

        r = self._post("/ip/ipsec/identity/add", identity_payload)
        if not r or r.status_code not in [200, 201]:
            print("[ERROR] Identity")
            return False

        # PROPOSAL (clave para compatibilidad)
        self._post("/ip/ipsec/proposal/add", {
            "name": "prop-cisco",
            "auth-algorithms": "sha1",
            "enc-algorithms": "aes-128-cbc",
            "pfs-group": "none"
        })

        # POLICY
        policy_payload = {
            "src-address": "192.168.30.0/24",
            "dst-address": "192.168.10.0/24",
            "sa-src-address": "200.1.13.2",
            "sa-dst-address": "200.1.13.1",
            "tunnel": "yes",
            "action": "encrypt",
            "proposal": "prop-cisco",
            "peer": "to-R1"
        }

        r = self._post("/ip/ipsec/policy/add", policy_payload)
        if not r or r.status_code not in [200, 201]:
            print("[ERROR] Policy")
            return False

        print("[OK] IPsec configurado")
        return True

    # -------------------------
    # MÉTODO FINAL
    # -------------------------
    def configurar_completo(self):
        print(">>> Configuración completa MikroTik (R3)")

        self.limpiar_ipsec()
        self.configurar_interfaces()
        self.configurar_loopback()
        self.configurar_rutas()

        ok = self.configurar_ipsec()

        if ok:
            print("[R3] TODO OK")
        else:
            print("[R3] ERROR EN CONFIG")