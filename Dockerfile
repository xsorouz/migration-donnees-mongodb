# Utilise une image de base Python
FROM python:3.12-slim

# Définit le répertoire de travail dans le conteneur
WORKDIR /app

# Copie le fichier requirements.txt dans le conteneur
COPY requirements.txt .

# Installe les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copie le contenu de votre projet dans le conteneur
COPY . .

# Définit le script principal à exécuter
CMD ["python", "scripts/mongodb_crud.py"]
