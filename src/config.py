# Direccionamiento OOB (Out-of-Band) según la pauta
NODOS = {
    "R1": {
        "device_type": "cisco_ios",
        "host": "192.168.122.10",
        "auth": {"username": "admin", "password": "cisco123"} # Ajusta según tu GNS3
    },
    "R2": {
        "device_type": "cisco_ios",
        "host": "192.168.122.20",
        "auth": {"username": "admin", "password": "cisco123"}
    },
    "R3": {
        "host": "192.168.122.30",
        "api_port": 80,
        "auth": ("admin", "admin123")
    }
}