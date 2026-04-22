from src.config import NODOS
from src.routers import RouterManager
from src.api_rest import R3Manager

def main():
    print("=== INICIO AUTOMATIZACIÓN ===")

    router_mgr = RouterManager(NODOS)

    # 1. R2 primero (ISP)
    router_mgr.configurar_r2()

    # 2. R1 (VPN + rutas)
    router_mgr.configurar_r1()

    # 3. MikroTik API
    r3 = R3Manager(NODOS["R3"])
    r3.configurar_ipsec_api()

    print("=== FIN ===")

if __name__ == "__main__":
    main()