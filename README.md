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
    - **Opérations CRUD (Create, Read, Update, Delete) sur MongoDB.**
- **`notebooks/`** :
  - Contient les notebooks Jupyter pour :
    - Le nettoyage et la transformation des données.
    - Les analyses exploratoires et les visualisations des données.
- **`docker/`** :
  - Contient les fichiers liés à Docker, comme `Dockerfile` et `docker-compose.yml`.
- **`docs/`** :
  - Documentation du projet, incluant les recherches AWS et les guides techniques.
- **`logs/`** :
  - Fichiers de journalisation générés par le projet pour le suivi et le débogage.


---
 

## **Prérequis :**
- **Python** : Version 3.8 ou supérieure, pour exécuter les scripts Python et les notebooks.
- **Pip** : Gestionnaire de paquets Python, pour installer les dépendances requises.
- **MongoDB** : Installé localement ou via un conteneur Docker, pour gérer la base de données.
- **Docker et Docker Compose** : Pour la conteneurisation des services.
- **Jupyter Notebook ou VS Code** : Pour exécuter et analyser le notebook (nécessaire pour le nettoyage et la transformation des données).
- **MongoDB Compass** : Outil graphique pour visualiser les données stockées dans MongoDB de manière simplifiée.
 
---

# Détails des Opérations CRUD

## CREATE :
- Insertion de toutes les données du fichier CSV dans MongoDB.

## READ :
- Lecture d’un échantillon de documents pour validation.
- Lecture de documents filtrés selon des critères spécifiques (par exemple, patients de plus de 50 ans).

## UPDATE :
- Mise à jour conditionnelle de champs spécifiques (ajout d’un champ `Status` pour les patients seniors).

## DELETE :
- Suppression de documents en fonction d’un critère (par exemple, suppression des patients avec un statut `Senior`).

## Validation :
- Chaque étape est suivie d’une vérification des résultats via des requêtes MongoDB.

---

# Journalisation et Débogage

## **Logs :**
Tous les événements clés et les erreurs sont journalisés dans le répertoire `logs/`. Cela inclut :
- Les étapes de configuration.
- Les résultats des opérations CRUD.
- Les éventuelles erreurs rencontrées lors de l’exécution.

---

# Progression du projet

## **Étapes complétées :**
1. Préparation des données (Nettoyage, Transformation, Suppression des doublons).
2. Opérations CRUD complètes sur MongoDB avec validation des résultats.
3. Documentation des étapes CRUD.

 

---

# Instructions d'exécution

1. **Nettoyage et transformation :**
   - Exécutez le notebook pour :
     - Charger les données brutes depuis `data/raw/`.
     - Nettoyer et transformer les données.
     - Exporter les données nettoyées vers `data/processed/`.

2. **Insertion et tests CRUD :**
   - Exécutez le script des opérations CRUD :
     ```bash
     python scripts/mongodb_crud.py
     ```
   - Ce script insère les données nettoyées dans MongoDB et effectue des tests CRUD.

3. **Logs et suivi :**
   - Consultez les fichiers journaux dans `logs/migration.log`.


---
 
