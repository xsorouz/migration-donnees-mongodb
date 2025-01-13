# Utiliser Python 3.12 slim comme image de base
FROM python:3.12-slim

# Définir le répertoire de travail par défaut dans le conteneur
WORKDIR /app

# Copier le fichier requirements.txt et installer les dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier le script et les données nécessaires dans le conteneur
COPY scripts /app/scripts
COPY data /app/data

# Donner les permissions d'exécution aux scripts Python
RUN chmod +x /app/scripts/mongodb_crud.py

# Commande par défaut pour exécuter le script
CMD ["python", "/app/scripts/mongodb_crud.py", "/app/data/processed/healthcare_data_cleaned.csv"]
