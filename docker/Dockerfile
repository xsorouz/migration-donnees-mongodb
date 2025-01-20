# =============================================================
# Dockerfile pour le projet MongoDB CRUD avec gestion des rôles
# =============================================================

# === Étape 1 : Utiliser une image de base Python stable et légère ===
# Utilisation de Python 3.12-slim pour minimiser la taille de l'image
FROM python:3.12-slim

# === Étape 2 : Définir le répertoire de travail ===
# Tous les fichiers seront manipulés dans ce répertoire
WORKDIR /app

# === Étape 3 : Installer les dépendances système ===
# Installer des utilitaires nécessaires comme gcc pour certaines bibliothèques Python
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libssl-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# === Étape 4 : Installer les dépendances Python ===
# Copier le fichier requirements.txt dans le conteneur
COPY requirements.txt .

# Installer les dépendances listées dans requirements.txt
RUN pip install --no-cache-dir -r requirements.txt \
    && pip cache purge

# === Étape 5 : Copier les scripts Python du projet ===
# Importer les scripts Python nécessaires
COPY scripts /app/scripts

# Ajouter /app/scripts au PYTHONPATH pour permettre des imports corrects dans les tests et l'exécution
ENV PYTHONPATH=/app/scripts

# === Étape 6 : Copier les répertoires de données et de logs ===
# Importation des répertoires contenant les fichiers de données et les logs
COPY data /app/data
COPY logs /app/logs
COPY outputs /app/outputs
RUN chmod -R 755 /app/logs /app/outputs

# === Étape 7 : Créer les répertoires de sortie ===
# Création d'un répertoire pour stocker les fichiers générés pendant l'exécution
RUN mkdir -p /app/data/raw /app/data/processed 

# === Étape 8 : Appliquer les permissions d'exécution ===
# S'assurer que les scripts Python sont exécutables
RUN chmod +x /app/scripts/*.py

# === Étape 9 : Ajouter des fichiers de configuration ou d'attente (facultatif) ===
# Si nécessaire, inclure un script pour attendre que MongoDB soit prêt
# COPY docker/wait-for-mongo.sh /app/scripts/
# RUN chmod +x /app/scripts/wait-for-mongo.sh

# === Étape 10 : Définir des variables d'environnement ===
# Variables pour simplifier la gestion des chemins et des configurations
ENV RAW_DIR=/app/data/raw
ENV PROCESSED_DIR=/app/data/processed
ENV LOG_DIR=/app/logs
ENV OUTPUT_DIR=/app/outputs

# === Étape 11 : Spécifier la commande par défaut ===
# Définir les scripts à exécuter automatiquement au démarrage du conteneur
# L'ordre d'exécution est important : traitement des données -> création des utilisateurs -> lancement principal
CMD ["bash", "-c", "python /app/scripts/data_processing.py && \
                    python /app/scripts/setup_users.py && \
                    python /app/scripts/initialize_users.py && \
                    python /app/scripts/main.py /app/data/processed/healthcare_dataset_cleaned.csv"]
