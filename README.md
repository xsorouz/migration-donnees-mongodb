# Migration de Données Médicales vers MongoDB

Ce projet démontre les étapes de migration d'un fichier de données médicales au format CSV vers une base de données MongoDB. Il comprend des notebooks pour préparer et nettoyer les données, ainsi que des scripts Python pour configurer les utilisateurs MongoDB, migrer les données et exécuter des opérations CRUD.

---

## **Objectifs du projet :**
1. **Préparation et nettoyage des données** :
   - Charger et valider les données à partir d'un fichier CSV.
   - Effectuer un nettoyage approfondi (suppression des doublons, transformation des colonnes).
   - Exporter les données nettoyées prêtes à être insérées dans MongoDB.
2. **Migration des données vers MongoDB** :
   - Insérer les données nettoyées dans une base MongoDB.
   - Configurer des utilisateurs avec différents rôles (lecture, écriture, administration).
3. **Opérations CRUD** :
   - Fournir des exemples d'insertion, lecture, mise à jour et suppression des données dans MongoDB.
4. **Conteneurisation avec Docker** :
   - Créer un environnement reproductible et portable pour MongoDB et les scripts Python.
   - Utiliser Docker Compose pour orchestrer les services.
5. **Documentation des recherches AWS** :
   - Étudier et documenter les options de déploiement de MongoDB dans le cloud.
   - Comparer les services AWS tels qu’Amazon RDS, ECS et DocumentDB.

---

## **Structure du projet :**

- **`data/`** :
  - **`raw/`** : Contient les données brutes non transformées.
  - **`processed/`** : Contient les données nettoyées prêtes à être insérées dans MongoDB.
- **`scripts/`** :
  - Contient les scripts Python pour effectuer les étapes suivantes :
    - **Configuration des utilisateurs MongoDB**.
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

## **Détails du Notebook de Préparation des Données**

Le notebook effectue les étapes suivantes :

### Chargement et Validation des Données :
- Chargement des données brutes depuis `data/raw/`.
- Validation des types de colonnes et détection des valeurs inattendues.

### Nettoyage et Transformation :
- Suppression des doublons et des valeurs manquantes.
- Normalisation des colonnes de texte (suppression des espaces, uniformisation des majuscules/minuscules).
- Conversion des colonnes de dates en format datetime.
- Ajout ou modification de colonnes spécifiques pour enrichir les données.

### Exportation :
- Les données nettoyées sont sauvegardées dans `data/processed/healthcare_data_cleaned.csv`.
- Les journaux des opérations sont enregistrés dans `logs/migration.log`.

---

## **Configuration des utilisateurs MongoDB**

Le script `setup_users.py` configure les utilisateurs suivants :

- **`admin_user`** :
  - **Rôle** : `root`
  - **Base** : `admin`
  - Utilisé pour administrer MongoDB.

- **`editor_user`** :
  - **Rôle** : `readWrite`
  - **Base** : `healthcare_database`
  - Utilisé pour insérer, lire, mettre à jour et supprimer des données.

- **`reader_user`** :
  - **Rôle** : `read`
  - **Base** : `healthcare_database`
  - Utilisé pour lire des données uniquement.

### Créer les utilisateurs

Exécutez le script pour créer les utilisateurs :
```bash
python scripts/setup_users.py
```

### Vérifier les utilisateurs

- Lister les utilisateurs dans la base `admin` :
  ```javascript
  use admin
  db.getUsers()
  ```

- Lister les utilisateurs dans la base `healthcare_database` :
  ```javascript
  use healthcare_database
  db.getUsers()
  ```

---

## **Migration des données**

Le script `mongodb_crud.py` migre les données d'un fichier CSV vers MongoDB. Assurez-vous que le fichier à migrer est dans le répertoire `data/processed`.

### Exécuter la migration

Utilisez la commande suivante pour migrer les données :
```bash
python scripts/mongodb_crud.py data/processed/healthcare_data_cleaned.csv
```
Les journaux des opérations sont enregistrés dans `logs/migration.log`.

---

## Exemples d'opérations CRUD

### Avec `editor_user`
#### Connexion
```bash
mongosh --username editor_user --password editor_password --authenticationDatabase healthcare_database
```

#### Insertion (CREATE)
```python
# Insérer un document
record = {"Name": "John Doe", "Age": 50, "Gender": "Male"}
insert_records(collection, [record])
```
Exemple de sortie dans les logs :
```
2025-01-02 15:25:33.940 | INFO | mongodb_crud:insert_records:35 - 1 document inséré avec succès.
```

#### Lecture (READ)
```python
# Lire les documents insérés
query = {"Age": {"$gt": 40}}
sample_records = read_records(collection, query, limit=5)
print(sample_records)
```
Exemple de sortie dans les logs :
```
2025-01-02 15:25:33.952 | INFO | mongodb_crud:read_records:52 - 5 documents récupérés avec la requête : {"Age": {"$gt": 40}}
```

#### Mise à jour (UPDATE)
```python
# Mettre à jour un document
filter_query = {"Name": "John Doe"}
update_query = {"$set": {"Age": 51}}
update_count = update_records(collection, filter_query, update_query)
```
Exemple de sortie dans les logs :
```
2025-01-02 15:25:36.012 | INFO | mongodb_crud:update_records:69 - 1 document mis à jour avec succès.
```

#### Suppression (DELETE)
```python
# Supprimer un document
filter_query = {"Name": "John Doe"}
delete_count = delete_records(collection, filter_query)
```
Exemple de sortie dans les logs :
```
2025-01-02 15:25:37.273 | INFO | mongodb_crud:delete_records:85 - 1 document supprimé avec succès.
```

### Avec `reader_user`
#### Connexion
```bash
mongosh --username reader_user --password reader_password --authenticationDatabase healthcare_database
```

#### Lecture (READ)
Les utilisateurs avec le rôle `read` peuvent uniquement lire les données :
```javascript
db.patients_data.find()
```

#### Test d'écriture (doit échouer)
```javascript
db.patients_data.insertOne({ Name: "Unauthorized User" })
```
Résultat attendu : Erreur d'autorisation.

---

## Commandes utiles

### Lancer MongoDB
```bash
net start MongoDB
```

### Arrêter MongoDB
```bash
net stop MongoDB
```

### Accéder à MongoDB Shell
```bash
mongosh
```

---

## Conteneurisation avec Docker

Le projet est conçu pour être exécuté dans des conteneurs Docker. Deux services sont configurés :
1. **MongoDB** : Utilise l'image officielle MongoDB.
2. **Application Python** : Gère la migration et les opérations CRUD.

### **Fichiers Docker**

- **`docker/Dockerfile`** : Définit l'image pour l'application Python.
- **`docker/docker-compose.yml`** : Orchestration entre MongoDB et l'application Python.
- **`docker/.dockerignore`** : Définit les fichiers à exclure lors de la création de l'image Docker.
- **`docker/USAGE.md`** : Guide détaillé pour comprendre et utiliser Docker avec ce projet.

Pour des explications détaillées sur la configuration Docker, consultez le fichier **`docker/USAGE.md`**.

---

### **Commandes Docker**

#### 1. **Construire l'image Docker**
Pour construire l'image Docker pour l'application Python :
```bash
docker build -t python-mongodb-app -f docker/Dockerfile .
```

#### 2. **Lancer Docker Compose**
Pour démarrer MongoDB et l'application Python ensemble :
```bash
docker-compose -f docker/docker-compose.yml up --build
```

#### 3. **Arrêter les conteneurs**
Pour arrêter tous les conteneurs en cours d'exécution :
```bash
docker-compose -f docker/docker-compose.yml down
```

---

## Progression du projet

### **Étapes complétées :**
1. Préparation des données (Nettoyage, Transformation, Suppression des doublons).
2. Opérations CRUD complètes sur MongoDB avec validation des résultats.
3. Documentation des étapes CRUD.

---

## Instructions d'exécution

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

## Prochaines étapes

- Explorer les options de déploiement sur AWS (Amazon DocumentDB, ECS, etc.).
- Optimiser les scripts pour des bases de données plus volumineuses.
- Étendre les tests à des scénarios plus complexes.

 

