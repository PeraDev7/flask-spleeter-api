# Usa Python 3.8 per compatibilità con Spleeter
FROM python:3.8

# Imposta la working directory
WORKDIR /app

# Copia tutti i file nel container
COPY . /app

# Installa i pacchetti di sistema richiesti
RUN apt-get update && apt-get install -y ffmpeg

# Installa le dipendenze
RUN pip install --no-cache-dir -r requirements.txt

# Esporta la porta usata da Flask
EXPOSE 10000

# Comando per avviare l'app
CMD ["flask", "run", "--host=0.0.0.0", "--port=10000"]
