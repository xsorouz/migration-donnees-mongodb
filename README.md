# Migration de Données Médicales vers MongoDB

Ce projet a pour objectif de migrer des données médicales d'un fichier CSV vers une base de données MongoDB, tout en utilisant Docker pour la conteneurisation et en explorant des solutions de déploiement cloud avec AWS.

---

## **Objectifs du projet :**
1. **Migration des données vers MongoDB** :
   - Charger les données depuis un fichier CSV.
   - Effectuer un nettoyage et une validation des données.
   - Insérer les données dans MongoDB.
2. **Conteneurisation avec Docker** :
   - Créer un environnement reproductible et portable pour MongoDB et les scripts Python.
   - Utiliser Docker Compose pour orchestrer les services.
3. **Documentation des recherches AWS** :
   - Étudier et documenter les options de déploiement de MongoDB dans le cloud.
   - Comparer les services AWS tels qu’Amazon RDS, ECS et DocumentDB.

---

## **Structure du projet :**
- **`data/`** :
  - **`raw/`** : Contient les données brutes non transformées.
  - **`processed/`** : Contient les données nettoyées prêtes à être insérées dans MongoDB.
- **`scripts/`** :
  - Contient les scripts Python pour effectuer les étapes suivantes :
    - Nettoyage et transformation des données.
    - Insertion des données dans MongoDB.
    - Tests CRUD (Create, Read, Update, Delete) sur MongoDB.
- **`notebooks/`** :
  - Contient les notebooks Jupyter pour les analyses exploratoires et les visualisations des données.
- **`docker/`** :
  - Contient les fichiers liés à Docker, comme `Dockerfile` et `docker-compose.yml`.
- **`docs/`** :
  - Documentation du projet, incluant les recherches AWS et les guides techniques.
- **`logs/`** :
  - Fichiers de journalisation générés par le projet pour le suivi et le débogage.

---

## **Prérequis :**
- **Python** : Version 3.8 ou supérieure.
- **MongoDB** : Installé localement ou via un conteneur Docker.
- **Docker et Docker Compose** : Pour la conteneurisation.
- **Pip** : Gestionnaire de paquets Python.

---
