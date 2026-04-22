import requests
import json
from requests.auth import HTTPBasicAuth
import urllib3

urllib3.disable_warnings()

class R3Manager:
    def __init__(self, config):
        self.host = config["host"]
        self.auth = HTTPBasicAuth(config["username"], config["password"])
        self.base_url = f"http://{self.host}/rest"

    def configurar_ipsec_api(self):
        print(">>> Configurando MikroTik (R3)...")

        endpoint = f"{self.base_url}/ip/ipsec/peer"

        payload = {
            "name": "to-R1",
            "address": "200.1.13.1",
            "exchange-mode": "main",
            "secret": "cisco123"
        }

        try:
            response = requests.post(
                endpoint,
                json=payload,
                auth=self.auth,
                verify=False,
                timeout=5
            )

            if response.status_code in [200, 201]:
                data = json.loads(response.text)
                print("[OK] MikroTik responde:")
                print(data)
                return True
            else:
                print(f"[ERROR API] {response.status_code}")
                print(response.text)
                return False

        except Exception as e:
            print(f"[ERROR R3] {e}")
            return False