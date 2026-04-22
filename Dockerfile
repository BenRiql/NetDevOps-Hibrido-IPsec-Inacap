# Imagen base de Python liviana
FROM python:3.11-slim

# Directorio de trabajo
WORKDIR /app

# Copiar archivos de dependencias e instalar
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código
COPY . .

# Comando para ejecutar la automatización al iniciar
CMD ["/bin/sh"]
