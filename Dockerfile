FROM python:3.12-slim

# Définir le répertoire de travail
WORKDIR /app

# Installer dépendances système (incluant curl pour healthcheck)
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copier uniquement requirements.txt d'abord (cache Docker)
COPY requirements.txt .

# Installer dépendances Python
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && pip install "pydantic[email]"

# Copier tout le code de l'application
COPY . .

# Ajouter le répertoire /app au PYTHONPATH
ENV PYTHONPATH="/app"

# Créer le dossier logs avec permissions
RUN mkdir -p /app/logs && chmod -R 777 /app/logs

# Créer un utilisateur non-root
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# Exposer le port
EXPOSE 8000

# Healthcheck interne (test de l'API)
HEALTHCHECK --interval=30s --timeout=30s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8000/api/health || exit 1

# Lancer l’application avec uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
