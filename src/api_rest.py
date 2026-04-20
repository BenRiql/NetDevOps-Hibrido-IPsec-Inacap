import requests
import json
from requests.auth import HTTPBasicAuth

# Desactivar advertencias de SSL si usas HTTPS auto-firmado
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class R3Manager:
    def __init__(self, config_r3):
        self.host = config_r3['host']
        self.auth = HTTPBasicAuth(config_r3['auth'][0], config_r3['auth'][1])
        self.base_url = f"http://{self.host}/rest" # URL de la API de MikroTik

    def configurar_ipsec_api(self):
        """Inyecta el túnel IPsec en R3 usando Payload JSON"""
        print(f">>> Conectando a la API de MikroTik en {self.host}...")
        
        # Payload JSON para la Fase 1 (Peer) y Fase 2 (Policy)
        # Basado en la pauta: Conectar R3 (200.1.13.2) con R1 (200.1.13.1)
        endpoint = f"{self.base_url}/ip/ipsec/peer"
        
        payload = {
            "name": "to-R1",
            "address": "200.1.13.1",
            "exchange-mode": "main",
            "comment": "Tunel automatizado via API REST"
        }

        try:
            # Enviar configuración vía POST
            response = requests.put(endpoint, json=payload, auth=self.auth, verify=False)
            
            # PARSEO OBLIGATORIO: Usar json.loads para confirmar éxito [cite: 40]
            if response.status_code in [200, 201]:
                data = json.loads(response.text)
                print(f"[OK] Respuesta de la API parseada: {data}")
                return True
            else:
                print(f"[!] Error API: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            print(f"[!] Error de conexión API: {e}")
            return False