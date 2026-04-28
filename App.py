import time
from src.config import NODOS
from src.routers import RouterManager
from src.api_rest import R3Manager

def main():
    print("=== INICIO AUTOMATIZACIÓN ===")

    print("Esperando que los routers levanten...")
    time.sleep(60)

    router_mgr = RouterManager(NODOS)

    router_mgr.configurar_r2()
    router_mgr.configurar_r1()

    print(">>> Configurando MikroTik (R3)...")
    r3 = R3Manager(NODOS["R3"])
    r3.configurar_completo()

    print("=== FIN ===")

if __name__ == "__main__":
    main()