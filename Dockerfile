FROM python:3.11-slim

# Instalar FFmpeg y dependencias del sistema
RUN apt-get update && \
    apt-get install -y ffmpeg && \
    rm -rf /var/lib/apt/lists/*

# Copiar requirements e instalar dependencias
COPY requirements.txt .
# FORZAMOS la actualización de yt-dlp a la última versión durante la construcción
RUN pip install --no-cache-dir --upgrade yt-dlp && \
    pip install --no-cache-dir -r requirements.txt

# Copiar la aplicación
COPY app.py .

# Puerto de Streamlit
EXPOSE 8501

# Comando de inicio
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
