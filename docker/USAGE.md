# Guide d'utilisation de Docker pour le projet

Ce document explique comment utiliser Docker pour gérer MongoDB et l'application Python de ce projet. Vous trouverez des explications détaillées sur les fichiers Docker ainsi que les étapes pour les utiliser efficacement.

---

## 📋 **Fichier Dockerfile**

### Détails des sections
#### `FROM`
```Dockerfile
FROM python:3.12-slim
```
- **`FROM`** : Définit l'image de base pour construire le conteneur.
- **`python:3.12-slim`** : Utilise une version légère de Python 3.12, ce qui réduit la taille de l'image.

#### `WORKDIR`
```Dockerfile
WORKDIR /app
```
- **`WORKDIR`** : Définit le répertoire de travail dans le conteneur. Toutes les commandes suivantes s'exécutent depuis `/app`.

#### `COPY requirements.txt .`
```Dockerfile
COPY requirements.txt .
```
- **`COPY`** : Copie le fichier `requirements.txt` de votre machine locale dans le répertoire `/app` du conteneur.

#### `RUN`
```Dockerfile
RUN pip install --no-cache-dir -r requirements.txt
```
- **`RUN`** : Exécute des commandes pendant la construction de l'image.
- Installe les dépendances Python listées dans `requirements.txt`.
- **`--no-cache-dir`** : Empêche `pip` de stocker les fichiers temporaires, réduisant ainsi la taille finale de l'image.

#### `COPY . .`
```Dockerfile
COPY . .
```
- Copie tous les fichiers du projet dans le répertoire `/app` du conteneur.

#### `CMD`
```Dockerfile
CMD ["python", "scripts/mongodb_crud.py"]
```
- **`CMD`** : Définit la commande à exécuter lorsque le conteneur démarre.
- Ici, cela lance le script principal `mongodb_crud.py`.

---

## 📚 **Comment fonctionne ce Dockerfile ?**
1. **Image de base** : L'image légère `python:3.12-slim` garantit un environnement minimal.
2. **Installation des dépendances** : Les bibliothèques nécessaires (comme `pymongo`) sont installées avec `pip`.
3. **Ajout des fichiers** : Tout le projet est copié dans le conteneur, rendant l'application autonome.
4. **Exécution** : Lorsque le conteneur démarre, il exécute le script Python principal.

---

## 📋 **Fichier docker-compose.yml**

### Détails des sections
#### `version`
```yaml
version: '3.9'
```
- Spécifie la version de syntaxe Docker Compose. La version `3.9` est compatible avec les dernières fonctionnalités de Docker.

#### `services`
```yaml
services:
```
- Définit les services gérés par Docker Compose. Ici, nous avons deux services :
  - **`mongodb`** pour la base de données.
  - **`app`** pour l'application Python.

#### `mongodb`
```yaml
  mongodb:
    image: mongo:5.0
    container_name: mongodb_container
    ports:
      - "27017:27017"
    volumes:
      - mongodb_data:/data/db
```
- **`image`** : Utilise l'image officielle MongoDB, version 5.0.
- **`container_name`** : Définit un nom pour ce conteneur MongoDB.
- **`ports`** : Expose le port MongoDB sur la machine hôte (`localhost:27017`).
- **`volumes`** : Monte un volume pour persister les données MongoDB.

#### `app`
```yaml
  app:
    build:
      context: .
    container_name: python_app
    depends_on:
      - mongodb
    volumes:
      - .:/app
    ports:
      - "5000:5000"
    environment:
      - MONGO_URI=mongodb://mongodb:27017
```
- **`build`** : Construit l'image Docker en utilisant le fichier `Dockerfile`.
- **`depends_on`** : Assure que MongoDB démarre avant ce service.
- **`volumes`** : Monte le répertoire local dans le conteneur pour synchroniser les fichiers.
- **`environment`** : Définit l'URI pour connecter l'application à MongoDB.

#### `volumes`
```yaml
volumes:
  mongodb_data:
```
- Définit un volume nommé `mongodb_data` pour persister les données de la base de données.

---

## 🔍 **Pourquoi ces options ?**
- **`ports`** : Vous permet d'accéder aux services depuis votre machine hôte.
- **`volumes`** : Garantit que les données MongoDB ne sont pas perdues entre les cycles de conteneurs.
- **`depends_on`** : Assure que MongoDB est prêt avant le démarrage de l'application Python.
- **`environment`** : Simplifie la configuration en passant des variables d'environnement.

---

## 💠 **Tester les conteneurs**

### Construire et exécuter :
1. Construire l'image :
   ```bash
   docker build -t python-mongodb-app .
   ```
2. Lancer MongoDB et l'application ensemble :
   ```bash
   docker-compose -f docker/docker-compose.yml up --build
   ```

### Arrêter les conteneurs :
```bash
docker-compose down
```

---

## 🗂 **Structure du projet avec Docker**
```plaintext
project/
├── docker/
│   ├── Dockerfile           # Définit l'image Docker
│   ├── docker-compose.yml   # Orchestration entre MongoDB et l'application
│   ├── USAGE.md             # Ce guide d'utilisation
│   ├── .dockerignore        # Exclut certains fichiers inutiles
├── scripts/
│   ├── mongodb_crud.py      # Script principal
├── requirements.txt         # Dépendances Python
└── data/                    # Données pour le projet
```

---

Avec ce guide, vous pouvez gérer Docker et Docker Compose efficacement pour ce projet. Si vous avez des questions, n'hésitez pas à demander !

