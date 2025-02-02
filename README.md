# Readme.md

# **Migration de Données Médicales vers MongoDB**

Ce projet propose une solution complète pour migrer un fichier de données médicales (au format CSV) vers une base de données NoSQL MongoDB. Il comprend des étapes détaillées pour la préparation, le nettoyage des données, leur insertion dans MongoDB, et la réalisation d'opérations CRUD. Le projet inclut également une conteneurisation avec Docker et des recherches approfondies sur les options de déploiement dans le cloud AWS.

---

## **Objectifs du Projet**

1. **Préparation et nettoyage des données :**
    - Charger les données à partir d’un fichier CSV brut.
    - Vérifier et valider les données (types, doublons, valeurs manquantes).
    - Appliquer un nettoyage approfondi et exporter un fichier prêt pour MongoDB.
2. **Migration des données vers MongoDB :**
    - Insérer les données nettoyées dans une base MongoDB structurée.
    - Configurer des utilisateurs avec des rôles spécifiques (lecture, écriture, administration).
3. **Opérations CRUD :**
    - Fournir des scripts Python pour illustrer les opérations CRUD (Create, Read, Update, Delete) sur MongoDB.
4. **Conteneurisation avec Docker :**
    - Déployer MongoDB et les scripts Python dans un environnement conteneurisé.
    - Utiliser Docker Compose pour gérer les services de manière orchestrée.
5. **Recherches sur le déploiement dans AWS :**
    - Étudier et documenter les options de déploiement de MongoDB sur AWS.
    - Comparer les services tels qu'Amazon RDS, ECS et DocumentDB.

---

## **Structure du Projet**

- **📁 data/**
    - **raw/** : Contient les données brutes non transformées.
    - **processed/** : Contient les données nettoyées prêtes à être insérées dans MongoDB.
- **📁 scripts/**
    
    Contient les scripts Python pour les étapes suivantes :
    
    - Migration des données.
    - Configuration des utilisateurs MongoDB avec rôles.
    - Exemples d’opérations CRUD.
- **📁 notebooks/**
    
    Contient les notebooks Jupyter pour :
    
    - Analyse exploratoire et visualisation des données.
    - Nettoyage et transformation des données.
- **📁 docker/**
    
    Contient les fichiers nécessaires à la conteneurisation, tels que `Dockerfile` et `docker-compose.yml`.
    
- **📁 docs/**
    
    Documentation complète du projet, incluant les recherches AWS et les schémas de la base de données.
    
- **📁 logs/**
    
    Fichiers de logs générés pour le suivi des étapes et le débogage.
    

---

## **Prérequis**

Avant d'exécuter le projet, assurez-vous d’avoir installé les outils suivants :

- **Python** : Version 3.8 ou supérieure (pour exécuter les scripts et notebooks).
- **Pip** : Gestionnaire de paquets Python (pour installer les dépendances).
- **MongoDB** : Installé localement ou via un conteneur Docker.
- **Docker et Docker Compose** : Pour conteneuriser MongoDB et les scripts Python.
- **Jupyter Notebook ou VS Code** : Pour exécuter les notebooks Jupyter.
- **MongoDB Compass** : Pour visualiser et manipuler les données dans MongoDB via une interface graphique.

---

## **Présentation des Données**

### **Utilité du Notebook**

Le notebook de préparation des données est une étape cruciale pour garantir la qualité et la cohérence des informations avant leur migration dans MongoDB. Il est conçu pour :

- Charger et valider les données brutes fournies sous forme de fichier CSV.
- Identifier et corriger les incohérences présentes dans les données.
- Appliquer des transformations pour standardiser les formats et enrichir les informations.
- Générer un fichier nettoyé, prêt à être inséré dans une base de données MongoDB.

En résumé, ce notebook constitue la base du pipeline de traitement des données pour ce projet.

### **Source des Données**

Le fichier d'entrée, nommé `healthcare_data.csv`, se trouve dans le répertoire `data/raw/`. Il contient des informations sur les patients, comme leurs âges, conditions médicales, traitements et informations administratives.

### **Résumé des Colonnes**

Voici une description des principales colonnes du fichier CSV :

- **Name** : Nom complet du patient.
- **Age** : Âge du patient (entier).
- **Gender** : Genre du patient (Male ou Female).
- **Blood Type** : Groupe sanguin (ex. : A+, O-).
- **Medical Condition** : Condition médicale principale (ex. : Diabetes, Cancer).
- **Date of Admission** : Date d’admission à l’hôpital.
- **Doctor** : Nom du médecin traitant.
- **Hospital** : Nom de l’hôpital.
- **Insurance Provider** : Fournisseur d’assurance.
- **Billing Amount** : Montant facturé (float, en USD).
- **Room Number** : Numéro de chambre d’hôpital.
- **Admission Type** : Type d’admission (Urgent, Elective).
- **Discharge Date** : Date de sortie (si applicable).
- **Medication** : Médicaments prescrits.
- **Test Results** : Résultats des tests médicaux (Normal, Abnormal).
- **Status** *(optionnel)* : Champ calculé dans le notebook (ex. : Senior pour les patients > 50 ans).

### **Étapes Réalisées dans le Notebook**

1. **Chargement et Validation des Données :**
    - Les données sont chargées depuis `data/raw/`.
    - Les types des colonnes sont vérifiés pour détecter d’éventuelles incohérences.
    - Les valeurs inattendues ou aberrantes sont signalées.
2. **Nettoyage et Transformation :**
    - Suppression des doublons et des valeurs manquantes significatives.
    - Standardisation des chaînes de texte (uniformisation majuscules/minuscules, suppression des espaces inutiles).
    - Conversion des colonnes de date au format `datetime`.
    - Ajout d’un champ `Status` pour enrichir les données (indique si un patient a plus de 50 ans).
3. **Exportation des Données :**
    - Les données nettoyées sont enregistrées dans `data/processed/healthcare_data_cleaned.csv` pour leur migration dans MongoDB.
    - Les logs des opérations sont sauvegardés dans `logs/migration.log` pour le suivi.

### **Objectifs du Notebook**

- Faciliter la migration des données vers MongoDB en fournissant des données propres et cohérentes.
- Optimiser les performances de la base de données en préparant les champs avec un typage approprié (entiers, chaînes, dates, etc.).
- Permettre une analyse exploratoire et une visualisation des tendances grâce à des données standardisées.

## **Les Scripts**

Les scripts Python jouent un rôle central dans ce projet. Voici leur description et leur rôle dans le processus

| **Script** | **Rôle** |
| --- | --- |
| **`setup_users.py`** | Configure les utilisateurs MongoDB avec des rôles spécifiques (lecture, écriture, administration). |
| **`data_processing.py`** | Nettoie et transforme les données brutes en un fichier exploitable pour MongoDB. |
| **`initialize_users.py`** | Initialise la collection `users` dans MongoDB avec des informations d'authentification. |
| **`main.py`** | Orchestration principale : insère les données nettoyées dans MongoDB, configure les index, et prépare la base pour les opérations CRUD. |
| **`crud.py`** | Implémente les fonctionnalités CRUD pour MongoDB (ajout, lecture, mise à jour, suppression). |
| **`interactive_cli.py`** | Fournit une interface utilisateur interactive pour exécuter les opérations CRUD. |
| **`test.py`** | Teste les fonctionnalités CRUD avec des scénarios unitaires pour garantir leur bon fonctionnement. |
| **`utils.py`** | Fournit des fonctions utilitaires partagées par les autres scripts (connexion MongoDB, création d’index). |
| **`auth.py`** | Gère l'authentification des utilisateurs MongoDB.

 |

Pour des explications détaillées sur les scripts, consultez le fichier **`scripts/scripts.md`**.

---

### **Résumé du Flux**

| **Étape** | **Description** |
| --- | --- |
| **Étapes initiales** | Configurez les utilisateurs et préparez les données (`setup_users.py`, `data_processing.py`, `initialize_users.py`). |
| **Migration et configuration** | Insérez les données nettoyées et configurez MongoDB (`main.py`). |
| **Manipulation des données** | Utilisez les fonctionnalités CRUD via les scripts ou l’interface interactive (`crud.py`, `interactive_cli.py`). |
| **Validation** | Exécutez les tests unitaires pour garantir que tout fonctionne (`test.py`). |

### **Migration des Données vers MongoDB**

### **Processus Général de Migration**

La migration des données consiste à transformer le fichier CSV nettoyé en documents JSON insérés dans une base MongoDB. Voici les étapes principales :

1. **Préparation des données** :
    - Utilisation du script `data_processing.py` pour nettoyer et transformer les données brutes.
    - Les données nettoyées sont exportées dans le fichier `data/processed/healthcare_data_cleaned.csv`.
2. **Configuration de MongoDB** :
    - Création des utilisateurs avec des rôles spécifiques à l'aide des scripts `setup_users.py` et `initialize_users.py`.
    - Initialisation des index pour optimiser les requêtes.
3. **Migration des données** :
    - Utilisation de `main.py` pour insérer les données nettoyées dans la collection `patients_data`.
    - Les journaux des opérations sont enregistrés dans `logs/migration.log`.

---

### **Authentification des Utilisateurs**

Pour sécuriser l’accès à MongoDB, une collection `users` a été configurée, contenant les informations des utilisateurs avec des mots de passe hachés et des rôles spécifiques. Voici les principaux rôles créés :

| **Utilisateur** | **Mot de Passe** | **Rôle** | **Base de Données** | **Description** |
| --- | --- | --- | --- | --- |
| `admin_user` | `admin_password` | `root` | `admin` | Administrateur complet avec accès à toutes les bases. |
| `editor_user` | `editor_password` | `readWrite` | `healthcare_database` | Lecture et écriture dans la base `healthcare_database`. |
| `reader_user` | `reader_password` | `read` | `healthcare_database` | Lecture seule dans la base `healthcare_database`. |

**Gestion des Utilisateurs :**

- Les utilisateurs et leurs rôles sont créés automatiquement via le script `setup_users.py`.
- Une fois les utilisateurs configurés, leurs informations sont insérées dans la collection `users` grâce au script `initialize_users.py`.

**Authentification avec les Scripts Python :**

- Le script `auth.py` vérifie les identifiants fournis par l’utilisateur et renvoie son rôle s’il est valide.
- Exemple : Lorsqu’un utilisateur se connecte via `main.py`, son rôle (`admin_user`, `editor_user`, ou `reader_user`) détermine les actions qu’il peut effectuer.

**Vérification des Utilisateurs dans MongoDB :**
Dans le shell MongoDB, vous pouvez vérifier les utilisateurs avec les commandes suivantes :

```bash
use admin
db.getUsers()
```

Pour la base de données `healthcare_database` :

```bash
use healthcare_database
db.getUsers()
```

---

### **Validation des Données Migrées**

Pour garantir la qualité des données après migration, les vérifications suivantes ont été effectuées :

1. **Validation des types de champs** :
    - Vérification que les champs numériques, chaînes de caractères et dates respectent leur typage prévu.
2. **Comptage des documents** :
    - Le nombre de documents insérés dans la collection `patients_data` correspond au nombre de lignes du fichier nettoyé.
3. **Tests CRUD** :
    - Des tests unitaires réalisés dans `test.py` garantissent que les opérations suivantes fonctionnent correctement :
        - **Insertion** : Ajout de nouveaux documents.
        - **Lecture** : Récupération de documents avec des filtres.
        - **Mise à jour** : Modification des données existantes.
        - **Suppression** : Suppression des documents spécifiques.

---

### **Schéma de la Base de Données**

La collection principale `patients_data` suit ce schéma :

| Champ | Type | Description |
| --- | --- | --- |
| `_id` | ObjectId | Identifiant unique généré automatiquement par MongoDB. |
| `name` | String | Nom complet du patient. |
| `age` | Integer | Âge du patient. |
| `gender` | String | Genre du patient (Male ou Female). |
| `blood_type` | String | Groupe sanguin (ex. : A+, O-). |
| `medical_condition` | String | Condition médicale principale (ex. : Diabetes, Cancer). |
| `date_of_admission` | Date | Date d’admission à l’hôpital. |
| `doctor` | String | Nom du médecin traitant. |
| `hospital` | String | Nom de l’hôpital. |
| `insurance_provider` | String | Fournisseur d’assurance. |
| `billing_amount` | Float | Montant facturé (en USD). |
| `room_number` | Integer | Numéro de chambre d’hôpital. |
| `admission_type` | String | Type d’admission (Urgent, Elective). |
| `discharge_date` | Date | Date de sortie (le cas échéant). |
| `medication` | String | Médicaments prescrits. |
| `test_results` | String | Résultats des tests médicaux (Normal, Abnormal). |
| `status` | String | Champ calculé indiquant si le patient est senior (> 50 ans). |

---

### **Index Configurés**

Pour optimiser les performances des requêtes, les index suivants ont été configurés :

- **`age`** : Index croissant pour rechercher ou trier par âge.
- **`name`** : Index croissant pour les recherches basées sur le nom.
- **`date_of_admission`** : Index décroissant pour les requêtes par date d’admission.
- **`gender`** : Index croissant pour filtrer les genres.

---

### **Instructions Générales**

Pour effectuer la migration des données vers MongoDB, suivez ces étapes :

1. Assurez-vous que MongoDB est en cours d’exécution (localement ou via Docker).
2. Exécutez les scripts dans l’ordre suivant :
    - `setup_users.py` : Configure les utilisateurs et leurs rôles.
    - `data_processing.py` : Nettoie et transforme les données.
    - `initialize_users.py` : Initialise la collection `users`.
    - `main.py` : Insère les données nettoyées et configure les index.
3. Vérifiez les données insérées :
    - Utilisez MongoDB Compass pour explorer la base de données.
    - Utilisez des requêtes Python pour effectuer des tests.

---

### **Conteneurisation avec Docker**

### **Objectif**

Le projet est conçu pour être exécuté dans des conteneurs Docker, garantissant un environnement portable et reproductible. MongoDB et les scripts Python interagissent via un réseau Docker.

---

### **Architecture des Services**

1. **MongoDB** :
    - Utilise l'image officielle MongoDB.
    - Héberge la base de données `healthcare_database` avec les utilisateurs et les rôles configurés.
    - Accessible depuis les autres conteneurs via l’URI `mongodb_service_container`.
2. **Application Python** :
    - Exécute les scripts Python pour la migration, la gestion des données, et les opérations CRUD.
    - Contient toutes les dépendances Python nécessaires (via `requirements.txt`).

---

### **Structure des Fichiers Docker**

1. **`docker/Dockerfile` (Application Python)** :
    
    Configure une image Docker pour l’application Python :
    
    - Installe les dépendances.
    - Définit le point d’entrée pour exécuter les scripts.
2. **`docker/docker-compose.yml`** :
    
    Orchestration des services Docker. Configure MongoDB, l’application Python, les volumes, et les réseaux.
    
3. **`docker/.dockerignore`** :
    
    Exclut les fichiers inutiles de la construction des images Docker.
    

---

### **Commandes Docker**

1. **Construire les Conteneurs**
    
    Construisez les images Docker :
    
    ```bash
    docker-compose build
    ```
    
2. **Démarrer les Services**
    
    Lancez MongoDB et l’application Python :
    
    ```bash
    docker-compose up -d
    ```
    
3. **Vérifier l’état des Conteneurs**
    
    Vérifiez si les conteneurs fonctionnent correctement :
    
    ```bash
    docker ps
    
    ```
    
4. **Arrêter les Services**
    
    Stoppez et nettoyez tous les conteneurs en cours d’exécution :
    
    ```bash
    docker-compose down
    
    ```
    

Pour des explications détaillées sur la configuration Docker, consultez le fichier **`docker/USAGE.md`**.

---

### **Interaction avec MongoDB**

Dans les scripts Python, la connexion à MongoDB est établie avec l’URI Docker suivant :

```python
db = connect_to_mongodb("mongodb://mongodb_service_container:27017/")
```

- MongoDB est accessible via le nom de service Docker (`mongodb_service_container`).
- Cette configuration garantit que les conteneurs communiquent correctement sur le réseau Docker.

---

### **Volumes et Réseaux**

- **Volumes** :
    - MongoDB stocke ses données dans un volume persistant nommé `mongodb_data`.
    - Les fichiers de données sont partagés entre l’hôte et le conteneur Python via un montage de volume (`data/`).
- **Réseaux** :
    - Les services Python et MongoDB communiquent via un réseau Docker personnalisé défini dans `docker-compose.yml`.

---

### **Instructions d’Utilisation**

1. Placez les fichiers nécessaires dans les répertoires (`data/`, `scripts/`, etc.).
2. Exécutez la commande suivante pour lancer MongoDB et l’application Python :
    
    ```bash
    docker-compose up -d
    
    ```
    
3. Utilisez MongoDB Compass pour explorer la base de données :
    - URI : `mongodb://mongodb_service_container:27017/`
4. Exploitez les scripts Python pour manipuler les données dans MongoDB.

### **Déploiement sur AWS**

### **Objectif**

Explorer les solutions pour héberger MongoDB sur AWS, comparer leurs avantages et limitations, et proposer une stratégie de sauvegarde et de surveillance des données.

### **Options Principales**

1. **Amazon DocumentDB** :
    - Base de données gérée compatible MongoDB.
    - Idéal pour les besoins de haute disponibilité et de gestion simplifiée.
    - Limitation : compatibilité partielle avec MongoDB.
2. **Amazon ECS** :
    - Hébergement conteneurisé pour MongoDB avec Docker.
    - Offre une grande flexibilité pour les configurations spécifiques.
    - Nécessite une gestion manuelle des sauvegardes et de la réplication.
3. **Amazon EC2** :
    - Instances virtuelles pour une installation manuelle de MongoDB.
    - Contrôle total sur la configuration.
    - Demande une gestion avancée des sauvegardes et de la maintenance.
4. **Amazon S3** :
    - Stockage fiable pour les sauvegardes des bases MongoDB et des fichiers sources.
    - Intégration facile avec d'autres services AWS comme CloudWatch ou Lambda.

### **Sauvegardes et Surveillance**

- **Sauvegardes** :
    - Utilisation de `mongodump` pour exporter les données et les sauvegarder dans un bucket S3.
    - Automatisation des sauvegardes avec des scripts ou des tâches AWS.
- **Surveillance** :
    - Surveillance des performances via Amazon CloudWatch.
    - Configuration d’alarmes pour détecter les anomalies ou les pannes.

### **Recommandation**

Pour un déploiement simple avec une gestion automatisée, **Amazon DocumentDB** est recommandé. Si le projet nécessite une flexibilité ou un contrôle accru, **Amazon ECS** ou **EC2** peuvent être envisagés.

### **Détails Supplémentaires**

Pour une documentation complète sur le déploiement de MongoDB sur AWS, consultez le fichier **`Documentation_MongoDB_AWS.md`** dans le répertoire principal.