# =============================================================
# Dockerfile pour le projet MongoDB CRUD avec gestion des rôles
# =============================================================

# Étape 1 : Utiliser une image de base Python légère (version 3.12 slim)
FROM python:3.12-slim

# Étape 2 : Définir le répertoire de travail par défaut dans le conteneur
WORKDIR /app

# Étape 3 : Copier le fichier requirements.txt contenant les dépendances dans le conteneur
COPY requirements.txt .

# Étape 4 : Installer les dépendances Python spécifiées dans le fichier requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Étape 5 : Copier tous les modules nécessaires et les données dans le conteneur
COPY scripts/auth.py /app/auth.py
COPY scripts/crud.py /app/crud.py
COPY scripts/initialize_users.py /app/initialize_users.py
COPY scripts/setup_users.py /app/setup_users.py
COPY scripts/utils.py /app/utils.py
COPY scripts/main.py /app/main.py
COPY data /app/data

# Étape 6 : Créer le répertoire outputs pour l'exportation des fichiers CSV
RUN mkdir -p /app/outputs

# Étape 7 : Donner les permissions d'exécution aux scripts Python
RUN chmod +x /app/*.py

# Étape 8 : Spécifier la commande par défaut pour exécuter les scripts
# Le fichier CSV est passé comme argument pour le script principal
CMD ["bash", "-c", "python /app/setup_users.py && python /app/initialize_users.py && python /app/main.py /app/data/processed/healthcare_data_cleaned.csv"]
