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

    def configurar_ipsec_api(self):
        print(">>> Configurando MikroTik (R3)...")

        # -------------------------
        # 1. PEER
        # -------------------------
        peer_payload = {
            "name": "to-R1",
            "address": "200.1.13.1",
            "exchange-mode": "main"
        }

        r = self._post("/ip/ipsec/peer/add", peer_payload)

        if not r or r.status_code not in [200, 201]:
            print("[ERROR] No se pudo crear peer")
            return False

        print("[OK] Peer creado")

        # -------------------------
        # 2. IDENTITY (PSK)
        # -------------------------
        identity_payload = {
            "peer": "to-R1",
            "auth-method": "pre-shared-key",
            "secret": "cisco123"
        }

        r = self._post("/ip/ipsec/identity/add", identity_payload)

        if not r or r.status_code not in [200, 201]:
            print("[ERROR] No se pudo crear identity")
            return False

        print("[OK] Identity creada")

        # -------------------------
        # 3. POLICY
        # -------------------------
        policy_payload = {
            "src-address": "192.168.30.0/24",
            "dst-address": "192.168.10.0/24",
            "sa-src-address": "200.1.13.2",
            "sa-dst-address": "200.1.13.1",
            "tunnel": "yes",
            "action": "encrypt",
            "proposal": "default",
            "peer": "to-R1"
        }

        r = self._post("/ip/ipsec/policy/add", policy_payload)

        if not r or r.status_code not in [200, 201]:
            print("[ERROR] No se pudo crear policy")
            return False

        print("[OK] Policy creada")

        print("[OK] IPsec configurado completamente en MikroTik")
        return True