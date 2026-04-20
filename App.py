import sys
from src.config import NODOS
from src.routers import RouterManager
from src.api_rest import R3Manager

def main():
    print("--- Iniciando Proceso de Automatización NetDevOps ---")
    
    # 1. Automatización Equipos Cisco (R1 y R2) vía SSH/Telnet
    # Según la pauta, R2 inyecta rutas y R1 configura IPsec [cite: 35, 36]
    try:
        print("\n[i] Configurando nodos Cisco (R1 y R2)...")
        cisco_manager = RouterManager(NODOS)
        
        # Configurar R2 (Tránsito)
        cisco_manager.configurar_r2()
        
        # Configurar R1 (Sede Central + IPsec)
        cisco_manager.configurar_r1()
        
    except Exception as e:
        print(f"[!] Error crítico en nodos Cisco: {e}")

    # 2. Automatización R3 (MikroTik) vía API REST
    # Se requiere inyectar el túnel IPsec hacia R1 usando JSON [cite: 39]
    try:
        print("\n[i] Configurando nodo R3 (MikroTik) vía API REST...")
        r3_manager = R3Manager(NODOS["R3"])
        
        # Ejecutar la inyección del Payload JSON
        resultado = r3_manager.configurar_ipsec_api()
        
        if resultado:
            print("[OK] Configuración en R3 aplicada con éxito.")
        else:
            print("[!] La API de R3 devolvió un error.")
            
    except Exception as e:
        print(f"[!] Error en la comunicación con la API de R3: {e}")

    print("\n--- Tareas finalizadas. Verifique conectividad con PING entre LANs ---")

if __name__ == "__main__":
    main()