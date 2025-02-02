# Documentation des Scripts

---

## **1. Scripts et leurs objectifs principaux**

Les scripts sont conçus pour travailler ensemble dans un flux cohérent, avec des rôles clairement définis. La documentation incluse dans chaque script explique leur objectif et leur ordre d'exécution.

| **Script** | **Objectif** | **Fonctionnalités clés** |
| --- | --- | --- |
| **`auth.py`** | Authentifie les utilisateurs en interrogeant MongoDB. | Valide les identifiants utilisateur et retourne leur rôle via la fonction `authenticate_user`. |
| **`setup_users.py`** | Configure les utilisateurs MongoDB natifs avec des rôles spécifiques (`admin_user`, etc.). | Crée ou vérifie les utilisateurs dans MongoDB via la fonction `configure_users`. |
| **`initialize_users.py`** | Initialise la collection `users` pour gérer les identifiants et les rôles de manière centralisée. | Ajoute ou met à jour les utilisateurs dans `users` grâce à `initialize_user_collection`. |
| **`utils.py`** | Fournit des utilitaires pour MongoDB, comme la connexion, le hachage de mots de passe, etc. | Inclut des fonctions comme `connect_to_mongodb`, `hash_password` et `create_indexes`. |
| **`crud.py`** | Implémente les opérations CRUD et l’export des données MongoDB en CSV. | Gère les données via `insert_records`, `read_records`, `update_records`, `delete_records`, etc. |
| **`data_processing.py`** | Prépare les données brutes pour leur insertion dans MongoDB. | Nettoie, valide et sauvegarde les données via la fonction `data_processing`. |
| **`interactive_cli.py`** | Fournit une interface utilisateur CLI pour exécuter des opérations CRUD selon les rôles. | Offre un menu interactif basé sur `interactive_menu` pour manipuler les données MongoDB. |
| **`test.py`** | Automatise les tests unitaires pour valider les fonctionnalités CRUD et d’exportation. | Teste les fonctions CRUD et l'export via des tests comme `test_insert_records`, `test_export_to_csv`, etc. |
| **`main.py`** | Orchestration générale : authentification, insertion de données, gestion via CLI. | Coordonne les étapes comme l'authentification, le chargement des données, et l’accès au CLI. |

---

## **2. Interdépendances vérifiées**

| **Dépendance** | **Source** | **Cible** |
| --- | --- | --- |
| `hash_password` | `utils.py` | Utilisé dans `auth.py` et `initialize_users.py`. |
| `configure_users` | `setup_users.py` | Appelé dans `initialize_users.py`. |
| Connexion MongoDB (`connect_to_mongodb`) | `utils.py` | Utilisé dans presque tous les scripts. |
| CRUD operations (`insert_records`, etc.) | `crud.py` | Appelées dans `interactive_cli.py`, `test.py`, et `main.py`. |
| Chargement des données CSV | `utils.py` | Utilisé dans `main.py` pour insérer les données initiales. |
| `interactive_menu` | `interactive_cli.py` | Appelé dans `main.py` pour gérer les données après l'authentification. |

---

## **3. Ordre d'exécution suggéré**

### **Pourquoi cet ordre est recommandé ?**

L’ordre suivant garantit une exécution fluide en respectant les dépendances nécessaires entre les scripts :

1. **MongoDB en premier** : Tous les scripts nécessitent MongoDB pour fonctionner.
2. **Configuration des utilisateurs (`setup_users.py` et `initialize_users.py`)** : Les utilisateurs doivent être configurés avant que les opérations CRUD puissent être exécutées ou testées.
3. **Préparation des données (`data_processing.py`)** : Les données doivent être nettoyées et prêtes avant leur insertion.
4. **Insertion et interface utilisateur (`main.py`)** : Centralise toutes les étapes de gestion des données.
5. **Tests (`test.py`)** : Valide les fonctionnalités une fois que tout le système est opérationnel.

---

### **Ordre recommandé**

1. **Démarrage de MongoDB**
    
    ```bash
    docker-compose up -d mongodb_service
    ```
    
2. **Configuration des utilisateurs MongoDB (`setup_users.py`)**
    
    ```bash
    python setup_users.py
    ```
    
3. **Initialisation des utilisateurs (`initialize_users.py`)**
    
    ```bash
    python initialize_users.py
    ```
    
4. **Préparation des données (`data_processing.py`)**
    
    ```bash
    python data_processing.py
    ```
    
5. **Insertion et gestion des données (`main.py`)**
    
    ```bash
    python main.py data/processed/healthcare_dataset_cleaned.csv
    ```
    
6. **Exécution des tests (`test.py`)**
    
    ```bash
    pytest test.py
    ```
    

---

## **4. Problèmes potentiels et recommandations**

### **Sécurité**

- Remplacer les identifiants en dur par des variables d’environnement ou un fichier **`.env`**.

### **Tests**

- Étendre les tests à l’authentification et à la gestion des utilisateurs.

### **Validation des données**

- Ajouter des vérifications automatiques pour les fichiers CSV (structure, colonnes, types).

---

## **Conclusion**

L'architecture des scripts est bien pensée et les dépendances sont logiques. Avec des ajustements mineurs (comme la sécurisation des identifiants et des validations renforcées), le projet est robuste et prêt pour une utilisation en production.

# **Documentation du Script : `auth.py`**

---

## **Objectif principal**

Le script **`auth.py`** permet d'authentifier les utilisateurs en validant leurs identifiants (nom d'utilisateur et mot de passe). Il interroge MongoDB pour vérifier les informations fournies et renvoie les données utilisateur si elles sont correctes. Cette fonctionnalité est essentielle pour garantir que seuls les utilisateurs autorisés accèdent à l'application.

---

## **Fonctionnalités principales**

### **1. Importation des dépendances**

- **`hash_password`** : Importé depuis **`utils.py`**, il est utilisé pour transformer les mots de passe en une version sécurisée (hachée).
- **`logger`** : Fournit une gestion avancée des journaux pour enregistrer les étapes clés et les erreurs.

---

### **2. Fonction `authenticate_user`**

### **Arguments**

- **`username`** : Nom d'utilisateur saisi par l'utilisateur.
- **`password`** : Mot de passe saisi par l'utilisateur (en texte clair).
- **`db`** : Instance de la base MongoDB contenant la collection `users`.

### **Étapes principales**

1. **Hachage du mot de passe** :
    
    Le mot de passe saisi est transformé en une version sécurisée via la fonction **`hash_password`**.
    
2. **Recherche dans MongoDB** :
    
    La fonction interroge la collection `users` pour trouver un document correspondant au `username` et au mot de passe haché.
    
3. **Validation des résultats** :
    - Si un document est trouvé :
        - Un message de succès est enregistré dans les journaux.
        - Les informations utilisateur (par exemple, rôle) sont retournées sous forme de dictionnaire.
    - Si aucun document ne correspond :
        - Un message d'échec est enregistré dans les journaux.
        - La fonction retourne `None`.

### **Retour**

- **Succès** : Renvoie un dictionnaire avec les informations utilisateur (par exemple : `{"username": "admin", "role": "admin_user"}`).
- **Échec** : Renvoie `None`.

---

## **Exemples de fonctionnement**

### **1. Cas de succès**

- L'utilisateur entre :
    - **Nom d'utilisateur** : `admin`
    - **Mot de passe** : `password123`
- Le mot de passe est haché (par exemple : `5e884898...`).
- MongoDB trouve un document avec `{"username": "admin", "password": "5e884898..."}`.
- La fonction retourne les informations utilisateur :
    
    ```python
    {"username": "admin", "role": "admin_user"}
    ```
    

### **2. Cas d'échec**

- Si aucun document ne correspond, la fonction retourne :
    
    ```python
    None
    ```
    
- Un message d'erreur est également enregistré dans les journaux :
    
    ```
    [ERROR] Authentification échouée pour l'utilisateur admin
    ```
    

---

## **Utilisation et dépendances**

### **1. Utilisation principale**

Le script est utilisé dans **`main.py`** pour valider les informations d'identification avant d'accorder l'accès à l'utilisateur.

### **2. Dépendances critiques**

- **`utils.py`** : Fournit la fonction **`hash_password`**, essentielle pour sécuriser les mots de passe.
- Une base de données MongoDB contenant une collection `users`, avec des noms d'utilisateur, mots de passe hachés et rôles associés.

---

## **Améliorations suggérées**

### **1. Sécurité renforcée**

- **Limite actuelle** : Utilisation de SHA-256 pour le hachage des mots de passe, sans ajout de **salt**.
- **Recommandations** :
    - Ajouter un **salt** unique pour chaque mot de passe.
    - Utiliser une bibliothèque plus robuste comme **bcrypt**, **argon2** ou **PBKDF2** pour le hachage.

### **2. Tests unitaires**

- Ajouter des tests unitaires pour valider les cas suivants :
    - Authentification réussie.
    - Nom d'utilisateur incorrect.
    - Mot de passe incorrect.
    - Utilisateur inexistant.
- Exemple de test avec `pytest` :
    
    ```python
    def test_authenticate_user_success(mongodb_mock):
        user_data = authenticate_user("admin", "password123", mongodb_mock)
        assert user_data == {"username": "admin", "role": "admin_user"}
    ```
    

### **3. Gestion des logs**

- Améliorer les messages pour inclure des détails comme l'heure de l'authentification et l'adresse IP de l'utilisateur (si applicable).

---

## **Conclusion**

Le script **`auth.py`** est essentiel pour sécuriser l'accès à l'application en validant les identifiants utilisateur. Bien qu'il soit fonctionnel, il pourrait être renforcé par des pratiques modernes de hachage et des tests unitaires pour garantir une robustesse maximale face aux divers scénarios.

---

### 

# **Documentation du Script : `setup_users.py`**

---

## **Objectif principal**

Le script **`setup_users.py`** configure les utilisateurs MongoDB avec des rôles spécifiques (`admin_user`, `reader_user`, `editor_user`). Il est indispensable pour structurer et sécuriser l'accès à MongoDB avant d'exécuter d'autres scripts.

---

## **Fonctionnalités principales**

### **1. Importation des dépendances**

- **`MongoClient`** : Fournit une interface pour interagir avec MongoDB.
- **`logger`** : Gère les journaux pour suivre les étapes et signaler les erreurs.

---

### **2. Fonction `configure_users`**

### **Arguments**

- Aucun (les connexions et configurations sont gérées en interne).

### **Étapes principales**

1. **Connexion initiale à MongoDB** :
    - Se connecte à l'instance MongoDB via `mongodb_service_container:27017`.
    - Accède à la base `admin` pour gérer les utilisateurs administratifs.
2. **Création de l'utilisateur `admin_user`** :
    - Vérifie si l'utilisateur existe déjà.
    - Si non, crée l'utilisateur avec un rôle `root` pour une gestion complète.
3. **Reconnexion avec `admin_user`** :
    - Se reconnecte à MongoDB avec les identifiants de `admin_user`.
    - Passe à la base `healthcare_database` pour configurer les utilisateurs spécifiques.
4. **Création des utilisateurs supplémentaires** :
    - **`reader_user`** : Crée un utilisateur avec un rôle `read`, limitant les permissions à la lecture.
    - **`editor_user`** : Crée un utilisateur avec un rôle `readWrite`, permettant la lecture et l’écriture.
5. **Validation post-création** :
    - Vérifie et journalise les utilisateurs et leurs rôles dans MongoDB :
        
        ```python
        created_users = admin_db.command("usersInfo")
        for user in created_users["users"]:
            logger.info(f"Utilisateur existant : {user['user']} avec rôle(s) : {user['roles']}")
        ```
        

### **Gestion des erreurs**

- Les erreurs critiques (ex. : échec de connexion ou création d’utilisateur) sont journalisées et une exception est levée.

---

## **Exemples de fonctionnement**

### **1. Connexion et création d'utilisateurs**

Lors de l'exécution du script, MongoDB est configuré avec :

- Un utilisateur `admin_user` avec accès complet (`root`).
- Deux utilisateurs spécifiques à `healthcare_database` :
    - **`reader_user`** (lecture seule).
    - **`editor_user`** (lecture et écriture).

### **2. Journalisation des résultats**

Un exemple de log attendu :

```
[INFO] Connexion initiale à MongoDB réussie.
[INFO] Utilisateur admin_user créé ou vérifié avec succès.
[INFO] Utilisateur reader_user créé ou vérifié avec succès.
[INFO] Utilisateur editor_user créé ou vérifié avec succès.
```

---

## **Utilisation et dépendances**

### **1. Utilisation principale**

- Ce script est une étape préalable pour configurer MongoDB avant d'exécuter les autres scripts (`initialize_users.py`, `main.py`).

### **2. Dépendances critiques**

- **MongoDB** : Nécessite une instance MongoDB accessible.
- **Loguru** : Gère les journaux pour tracer chaque étape.

---

## **Améliorations suggérées**

### **1. Gestion des mots de passe**

- **Limite actuelle** : Les mots de passe sont codés en dur dans le script.
- **Amélioration** : Utiliser un fichier **`.env`** pour stocker les mots de passe de manière sécurisée :
    
    ```python
    from decouple import config
    admin_password = config("ADMIN_PASSWORD")
    ```
    

### **2. Tests unitaires**

- Ajouter des tests pour vérifier :
    - Si chaque utilisateur a été correctement créé.
    - Si les rôles associés sont valides.

### **3. Feedback utilisateur**

- Ajouter des messages plus détaillés dans les logs pour améliorer la traçabilité.

---

## **Conclusion**

Le script **`setup_users.py`** joue un rôle central dans la configuration initiale de MongoDB. Il établit des utilisateurs et des rôles nécessaires pour garantir une gestio sécurisée des accès. Les améliorations proposées renforceraient sa robustesse et sa sécurité

# **Documentation du Script : `initialize_users.py`**

---

## **Objectif principal**

Le script **`initialize_users.py`** prépare MongoDB en deux étapes essentielles :

1. Configurer les utilisateurs MongoDB natifs avec des rôles spécifiques via le script **`setup_users.py`**.
2. Initialiser une collection **`users`** pour centraliser la gestion des utilisateurs et leurs rôles avec des mots de passe hachés.

Ce script ajoute une couche supplémentaire d'authentification applicative, renforçant la sécurité globale de l'application.

---

## **Fonctionnalités principales**

### **1. Importation des bibliothèques**

- **`MongoClient`** : Fournit une interface pour interagir avec MongoDB.
- **`logger`** : Gère les journaux pour capturer les étapes et erreurs importantes.
- **`configure_users`** : Importé de **`setup_users.py`**, il configure les utilisateurs MongoDB natifs.
- **`sha256`** : Permet de générer des hachages sécurisés pour les mots de passe.

---

### **2. Fonction `hash_password(password)`**

### **Rôle**

- Génère un hachage sécurisé SHA-256 pour un mot de passe donné.

### **Pourquoi**

- Les mots de passe ne sont jamais stockés en clair dans la base de données pour garantir la sécurité.

### **Retour**

- Le mot de passe haché sous forme de chaîne hexadécimale.

---

### **3. Fonction `initialize_user_collection()`**

### **Rôle**

- Initialise une collection MongoDB appelée **`users`** pour centraliser les informations d'authentification utilisateur.

### **Étapes principales**

1. **Connexion à MongoDB** :
    - Se connecte avec les identifiants de l'utilisateur `admin_user` créé via **`setup_users.py`**.
    - Accède à la base de données `healthcare_database`.
2. **Définition des utilisateurs** :
    - Crée une liste d'utilisateurs (`admin_user`, `reader_user`, `editor_user`) avec des mots de passe hachés et leurs rôles associés.
3. **Ajout ou mise à jour des utilisateurs** :
    - Utilise `update_one()` avec `upsert=True` pour insérer les nouveaux utilisateurs ou mettre à jour les utilisateurs existants.
4. **Validation des opérations** :
    - Enregistre un message de succès dans les journaux pour chaque utilisateur ajouté ou mis à jour.

---

## **Enchaînement logique**

1. **Configuration des utilisateurs natifs MongoDB** :
    - Appelle la fonction **`configure_users()`** pour garantir que `admin_user`, `reader_user`, et `editor_user` sont bien créés avec leurs rôles.
2. **Initialisation de la collection `users`** :
    - Ajoute ou met à jour les documents utilisateur dans la collection, incluant leurs rôles et mots de passe hachés.

---

## **Exemples de fonctionnement**

### **1. Configuration initiale des utilisateurs**

Lors de l'exécution, le script :

- Vérifie que MongoDB contient les utilisateurs natifs avec les rôles configurés.
- Initialise ou met à jour la collection **`users`** avec les données suivantes :
    
    ```json
    {
      "username": "admin_user",
      "password": "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd92c...",
      "role": "admin_user"
    }
    ```
    

### **2. Journalisation des résultats**

Exemple de journal attendu :

```
[INFO] Connexion à MongoDB réussie.
[INFO] Utilisateur admin_user ajouté ou mis à jour dans la collection users.
[INFO] Utilisateur reader_user ajouté ou mis à jour dans la collection users.
[INFO] Utilisateur editor_user ajouté ou mis à jour dans la collection users.
```

---

## **Utilisation et dépendances**

### **1. Utilisation principale**

- Ce script est exécuté après **`setup_users.py`** pour préparer la collection `users`.
- La collection est utilisée par **`auth.py`** pour valider les identifiants et les rôles des utilisateurs.

### **2. Dépendances critiques**

- **Connexion MongoDB** : MongoDB doit être accessible et configuré.
- **Script `setup_users.py`** : Assure que les utilisateurs natifs sont correctement créés avant d'initialiser la collection `users`.

---

## **Améliorations suggérées**

### **1. Gestion sécurisée des mots de passe**

- **Limite actuelle** : Les mots de passe hachés utilisent SHA-256, qui est vulnérable aux attaques par force brute.
- **Amélioration** : Utiliser une méthode plus robuste comme **bcrypt** ou **argon2**, avec un **salt** unique pour chaque utilisateur.

### **2. Tests unitaires**

- Ajouter des tests pour valider que :
    - La collection `users` est bien initialisée.
    - Les rôles et hachages sont correctement enregistrés.
    - Les utilisateurs existants sont correctement mis à jour.

### **3. Validation des utilisateurs**

- Ajouter une étape pour vérifier les rôles associés à chaque utilisateur dans la collection `users` après l'initialisation.

---

## **Conclusion**

Le script **`initialize_users.py`** joue un rôle clé en ajoutant une couche d'authentification applicative via la collection `users`. Il garantit une gestion sécurisée et centralisée des utilisateurs. Cependant, des améliorations comme l'utilisation de hachages plus robustes et des tests unitaires renforceraient davantage sa fiabilité et sa sécurité.

# **Documentation du Script : `data_processing.py`**

---

## **Objectif principal**

Le script **`data_processing.py`** gère le téléchargement, le nettoyage, la validation, et la sauvegarde des données médicales à partir d'un dataset Kaggle. Son objectif est de préparer les données pour une insertion dans MongoDB ou une analyse ultérieure, tout en garantissant leur qualité et leur cohérence.

---

## **Fonctionnalités principales**

### **1. Importation des bibliothèques**

- **`os` et `Path`** : Gèrent les interactions avec le système de fichiers et les chemins.
- **`pandas`** : Permet de manipuler les données sous forme de DataFrames.
- **`loguru`** : Enregistre chaque étape et capture les erreurs dans des fichiers de logs.
- **`kagglehub`** : Télécharge les datasets directement depuis Kaggle.

---

### **2. Configuration des logs**

- **Chemin des logs** : Les événements et erreurs sont enregistrés dans `logs/data_preparation.log`.
- **Rotation des logs** : Les fichiers de logs sont compressés une fois qu’ils atteignent 1 Mo, assurant une gestion efficace des fichiers.

---

### **3. Fonction principale : `data_processing(output_path)`**

### **Rôle**

- Orchestrer toutes les étapes nécessaires pour préparer les données, du téléchargement à leur sauvegarde finale.

### **Étapes principales**

1. **Téléchargement des données** :
    - Télécharge le dataset **`prasad22/healthcare-dataset`** depuis Kaggle.
    - Vérifie l’existence du fichier `healthcare_dataset.csv`.
    - Loggue une erreur si le téléchargement échoue.
2. **Chargement des données** :
    - Charge les données avec **`pandas.read_csv`**.
    - Enregistre des informations sur la structure initiale des données :
        - Noms, types des colonnes, aperçu des premières lignes.
    - Loggue une erreur en cas de problème.
3. **Nettoyage et validation des données** :
    - Supprime les doublons et les valeurs hors limites.
    - Convertit les colonnes de date (`Date of Admission`, `Discharge Date`) en format **`datetime`**.
    - Valide les types et les valeurs pour certaines colonnes (`gender`, `blood_type`).
    - Standardise les noms de colonnes (ex. : remplace les espaces par des underscores).
    - Nettoie les colonnes textuelles (`doctor`, `hospital`) pour uniformiser les données.
4. **Sauvegarde des données nettoyées** :
    - Sauvegarde les données nettoyées dans un fichier CSV spécifié par **`output_path`**.
    - Loggue une erreur si la sauvegarde échoue.

---

## **Enchaînement logique**

1. Téléchargement des données depuis Kaggle.
2. Chargement du fichier CSV et validation initiale.
3. Nettoyage et transformation des colonnes :
    - Suppression des doublons.
    - Standardisation des formats.
    - Validation des types et des valeurs.
4. Sauvegarde des données prêtes dans un fichier CSV nettoyé.

---

## **Exemples de fonctionnement**

### **1. Téléchargement et chargement des données**

- Télécharge automatiquement le dataset Kaggle.
- Charge le fichier `healthcare_dataset.csv` en DataFrame.
- Enregistre dans les logs :
    
    ```
    [INFO] Chargement des données réussi : 1000 lignes, 15 colonnes.
    ```
    

### **2. Nettoyage des colonnes**

- Suppression des doublons, logue le nombre de lignes supprimées :
    
    ```
    [INFO] 10 doublons supprimés.
    ```
    

### **3. Validation des données**

- Convertit les types et signale les anomalies :
    
    ```
    [WARNING] Valeurs inattendues détectées dans la colonne 'gender'.
    ```
    

### **4. Sauvegarde des données**

- Sauvegarde les données nettoyées :
    
    ```
    [INFO] Données nettoyées sauvegardées dans data/processed/healthcare_dataset_cleaned.csv.
    ```
    

---

## **Utilisation et dépendances**

### **1. Utilisation principale**

- Prépare les données brutes pour les étapes suivantes :
    - Insertion dans MongoDB.
    - Analyse exploratoire ou modélisation.

### **2. Dépendances critiques**

- **`kagglehub`** : Nécessaire pour télécharger les données depuis Kaggle.
- **`pandas`** : Manipule les données pour les transformer et les valider.
- **`loguru`** : Fournit des journaux détaillés pour suivre le processus.

---

## **Améliorations suggérées**

### **1. Gestion des erreurs plus détaillée**

- Actuellement, les erreurs sont enregistrées dans les logs mais peu explicites. Une amélioration consisterait à inclure des messages plus descriptifs :
    
    ```
    [ERROR] Le fichier healthcare_dataset.csv est introuvable après téléchargement.
    ```
    

### **2. Tests unitaires**

- Ajouter des tests pour valider :
    - Que les données sont correctement nettoyées.
    - Que les colonnes ont les bons types et valeurs après traitement.
    - Que le fichier de sortie contient le bon nombre de lignes.

### **3. Configuration dynamique**

- Permettre de passer dynamiquement le chemin ou le nom du fichier Kaggle à télécharger en paramètre.

---

## **Conclusion**

Le script **`data_processing.py`** est indispensable pour garantir que les données brutes sont prêtes à être utilisées dans MongoDB ou pour une analyse approfondie. Avec des validations robustes et une gestion efficace des erreurs, il constitue une base solide pour le pipeline de traitement des données. Des améliorations comme l’ajout de tests et une configuration dynamique renforceraient encore sa fiabilité.

# **Documentation du Script : `utils.py`**

---

## **Objectif principal**

Le script **`utils.py`** regroupe des fonctions utilitaires partagées pour gérer des tâches communes dans le projet, notamment :

- Hachage sécurisé des mots de passe.
- Gestion des connexions à MongoDB.
- Chargement et transformation des données à partir de fichiers CSV.
- Création d'index dans les collections MongoDB pour optimiser les performances des requêtes.

---

## **Fonctionnalités principales**

### **1. Fonction `hash_password(password)`**

### **Rôle**

- Génère un hachage sécurisé **SHA-256** pour un mot de passe.

### **Pourquoi**

- Garantit que les mots de passe ne sont jamais stockés en clair, renforçant ainsi la sécurité de l'application.

### **Entrée**

- **`password`** : Mot de passe brut (texte clair).

### **Retour**

- Mot de passe haché sous forme de chaîne hexadécimale.

---

### **2. Fonction `wait_for_mongodb(uri, timeout=30)`**

### **Rôle**

- Attend que le service MongoDB soit opérationnel avant d'établir une connexion.

### **Pourquoi**

- Utile dans des environnements où MongoDB peut prendre du temps à démarrer, comme dans des conteneurs Docker.

### **Étapes principales**

1. Tente de se connecter à MongoDB via l’URI spécifié.
2. Réessaie toutes les secondes jusqu'à ce que MongoDB réponde ou que le délai maximal soit atteint.

### **Entrées**

- **`uri`** : URI de connexion à MongoDB.
- **`timeout`** : Durée maximale (en secondes) pour attendre MongoDB.

### **Retour**

- Objet **`MongoClient`** connecté si MongoDB répond.

### **Exceptions levées**

- **`TimeoutError`** si MongoDB n’est pas accessible dans le délai imparti.

---

### **3. Fonction `connect_to_mongodb(uri, database_name="healthcare_database")`**

### **Rôle**

- Établit une connexion avec une base MongoDB spécifique après avoir attendu que le service soit prêt.

### **Pourquoi**

- Simplifie et centralise les connexions à MongoDB pour les autres scripts.

### **Étapes principales**

1. Appelle **`wait_for_mongodb`** pour vérifier que MongoDB est disponible.
2. Accède à la base spécifiée (par défaut : `healthcare_database`).

### **Entrées**

- **`uri`** : URI de connexion à MongoDB.
- **`database_name`** : Nom de la base de données cible.

### **Retour**

- Objet **`Database`** pour interagir avec la base.

### **Exceptions levées**

- Toute erreur liée à la connexion.

---

### **4. Fonction `load_data(file_path)`**

### **Rôle**

- Charge un fichier CSV et le transforme en une liste de dictionnaires utilisables par MongoDB.

### **Pourquoi**

- Simplifie l’importation de données tabulaires dans MongoDB.

### **Étapes principales**

1. Lit le fichier CSV avec **Pandas**.
2. Convertit les données en format JSON-like (liste de dictionnaires).

### **Entrées**

- **`file_path`** : Chemin vers le fichier CSV.

### **Retour**

- Liste de dictionnaires représentant les données.

### **Exceptions levées**

- **`FileNotFoundError`** si le fichier n’existe pas.
- Autres erreurs liées à la lecture des données.

---

### **5. Fonction `create_indexes(collection)`**

### **Rôle**

- Crée des index pour optimiser les performances des requêtes sur une collection MongoDB.

### **Pourquoi**

- Accélère les recherches et tris sur des champs fréquemment utilisés.

### **Étapes principales**

1. Définit une liste de champs à indexer.
2. Ajoute chaque index à la collection MongoDB.
3. Enregistre les index créés dans les logs.

### **Entrées**

- **`collection`** : Collection MongoDB cible.

### **Retour**

- Aucun (les index sont créés directement dans MongoDB).

### **Exceptions levées**

- Erreurs lors de la création d’un index.

---

## **Enchaînement logique**

1. **Hachage des mots de passe** : Utilisé pour sécuriser les données utilisateur.
2. **Connexion MongoDB** : Gère la disponibilité de MongoDB avant toute opération.
3. **Chargement des données CSV** : Transforme les fichiers en un format compatible MongoDB.
4. **Création des index** : Optimise les performances des requêtes sur les collections.

---

## **Exemples de fonctionnement**

### **1. Connexion à MongoDB**

```python
db = connect_to_mongodb("mongodb://mongodb_service_container:27017/")
```

### **2. Chargement des données**

```python
data = load_data("data/processed/healthcare_dataset_cleaned.csv")
**3. Création des index**
```

```python
create_indexes(collection)
```

---

## **Utilisation et dépendances**

### **1. Utilisation principale**

- **`hash_password`** : Utilisé par **`initialize_users.py`** et **`auth.py`** pour sécuriser les mots de passe.
- **`connect_to_mongodb`** : Appelé par plusieurs scripts (`setup_users.py`, `main.py`) pour établir une connexion.
- **`load_data`** : Utilisé dans **`main.py`** pour préparer les données pour MongoDB.
- **`create_indexes`** : Appelé par **`main.py`** pour optimiser les requêtes MongoDB.

### **2. Dépendances critiques**

- **MongoDB** : Nécessaire pour tester les connexions.
- **Pandas** : Manipule les données dans le format requis.
- **Loguru** : Gère les logs pour chaque étape.

---

## **Améliorations suggérées**

### **1. Gestion des exceptions**

- Ajouter des messages d’erreur plus explicites pour faciliter le débogage, par exemple :
    
    ```
    [ERROR] Impossible de lire le fichier CSV : data/raw/missing_file.csv.
    ```
    

### **2. Tests unitaires**

- Vérifier le bon fonctionnement des fonctions :
    - Hachage des mots de passe avec des entrées valides et invalides.
    - Connexion à MongoDB avec un URI incorrect.
    - Chargement d’un fichier CSV manquant ou mal formaté.

### **3. Dynamisme**

- Permettre de définir dynamiquement les champs à indexer via un paramètre.

---

## **Conclusion**

Le script **`utils.py`** est une boîte à outils essentielle pour centraliser des tâches récurrentes dans le projet. Sa modularité réduit la duplication de code et garantit une meilleure maintenabilité. Des améliorations comme des tests unitaires ou une gestion des exceptions plus détaillée renforceraient encore sa fiabilité.

# **Documentation du Script : `crud.py`**

---

## **Objectif principal**

Le script **`crud.py`** regroupe les opérations CRUD (Create, Read, Update, Delete) pour gérer les données dans une collection MongoDB. Il inclut également une fonctionnalité d’exportation des données vers un fichier CSV, permettant une analyse ou un partage simplifié.

---

## **Fonctionnalités principales**

### **1. Fonction `insert_records(collection, records)`**

### **Rôle**

- Insère plusieurs documents (sous forme de liste de dictionnaires) dans une collection MongoDB.

### **Pourquoi**

- Permet d'ajouter de nouvelles données dans la base de manière structurée.

### **Entrées**

- **`collection`** : Collection MongoDB cible.
- **`records`** : Liste de dictionnaires à insérer.

### **Retour**

- Nombre de documents insérés.

### **Étapes principales**

1. Vérifie que la liste `records` n’est pas vide.
2. Utilise la méthode **`insert_many`** pour insérer les documents.
3. Loggue les documents insérés et affiche un échantillon de 5 documents.

### **Gestion des erreurs**

- Loggue une erreur descriptive et lève une exception si l’insertion échoue.

---

### **2. Fonction `read_records(collection, query={}, limit=5)`**

### **Rôle**

- Récupère des documents dans une collection MongoDB en appliquant un filtre et une limite.

### **Pourquoi**

- Utile pour obtenir un aperçu des données ou pour récupérer des données spécifiques.

### **Entrées**

- **`collection`** : Collection MongoDB cible.
- **`query`** : Filtre pour les documents (par défaut : aucun filtre).
- **`limit`** : Nombre maximum de documents à récupérer.

### **Retour**

- Liste des documents correspondant au filtre.

### **Étapes principales**

1. Applique le filtre et la limite avec une requête MongoDB.
2. Utilise **`records.rewind()`** pour réinitialiser le curseur MongoDB, permettant de relire les documents si nécessaire.
3. Retourne les résultats sous forme de liste.

### **Gestion des erreurs**

- Loggue une erreur descriptive et lève une exception si la lecture échoue.

---

### **3. Fonction `update_records(collection, filter_query, update_query)`**

### **Rôle**

- Met à jour plusieurs documents correspondant à un filtre donné.

### **Pourquoi**

- Permet de modifier ou d’enrichir les données existantes.

### **Entrées**

- **`collection`** : Collection MongoDB cible.
- **`filter_query`** : Critères pour sélectionner les documents à mettre à jour.
- **`update_query`** : Modifications à appliquer (ex. : `{"$set": {"field": "value"}}`).

### **Retour**

- Nombre de documents modifiés.

### **Étapes principales**

1. Applique les modifications avec la méthode **`update_many`**.
2. Loggue les détails des documents mis à jour.
3. Affiche les documents mis à jour pour confirmation.

### **Gestion des erreurs**

- Loggue une erreur descriptive et lève une exception si la mise à jour échoue.

---

### **4. Fonction `delete_records(collection, filter_query)`**

### **Rôle**

- Supprime tous les documents correspondant à un filtre donné.

### **Pourquoi**

- Permet de nettoyer ou supprimer des données obsolètes ou incorrectes.

### **Entrées**

- **`collection`** : Collection MongoDB cible.
- **`filter_query`** : Filtre pour sélectionner les documents à supprimer.

### **Retour**

- Nombre de documents supprimés.

### **Étapes principales**

1. Utilise la méthode **`delete_many`** pour supprimer les documents.
2. Loggue le nombre de documents supprimés.

### **Gestion des erreurs**

- Loggue une erreur descriptive et lève une exception si la suppression échoue.

---

### **5. Fonction `export_to_csv(collection, file_name)`**

### **Rôle**

- Exporte tous les documents d’une collection MongoDB vers un fichier CSV.

### **Pourquoi**

- Simplifie le partage ou l’analyse des données dans un format tabulaire.

### **Entrées**

- **`collection`** : Collection MongoDB cible.
- **`file_name`** : Nom du fichier CSV (sans extension).

### **Retour**

- Nombre de documents exportés.

### **Étapes principales**

1. Vérifie si le répertoire `outputs` existe ; sinon, le crée.
2. Récupère les documents depuis la collection.
3. Loggue un avertissement si la collection est vide et retourne `0`.
4. Convertit les documents en un DataFrame Pandas et supprime la colonne `_id`.
5. Sauvegarde les données dans un fichier CSV.

### **Gestion des erreurs**

- Loggue une erreur descriptive et lève une exception si l’export échoue.

---

## **Enchaînement logique**

1. **Insertion** : Ajout de nouveaux documents dans MongoDB.
2. **Lecture** : Consultation des documents avec des filtres et des limites.
3. **Mise à jour** : Modification des données existantes selon des critères spécifiques.
4. **Suppression** : Nettoyage de documents obsolètes ou incorrects.
5. **Exportation** : Sauvegarde des données dans un fichier CSV pour une analyse externe.

---

## **Exemples de fonctionnement**

### **1. Insertion de documents**

```python
records = [{"name": "John Doe", "age": 30}, {"name": "Jane Doe", "age": 28}]
inserted_count = insert_records(collection, records)
print(f"{inserted_count} documents insérés.")
```

### **2. Lecture de documents**

```python
documents = read_records(collection, query={"age": {"$gte": 25}}, limit=3)
print(documents)
```

### **3. Exportation des données**

```python
export_to_csv(collection, "exported_data")
```

---

## **Utilisation et dépendances**

### **1. Utilisation principale**

- **Insertion des données** : Utilisé dans **`main.py`** pour importer des données en MongoDB.
- **Lecture des données** : Permet aux utilisateurs de visualiser les documents via une interface CLI.
- **Mise à jour et suppression** : Gère la modification et le nettoyage des données.
- **Exportation** : Génère des rapports CSV pour l’analyse.

### **2. Dépendances critiques**

- **`pandas`** : Convertit les données MongoDB en DataFrame pour l’exportation.
- **MongoDB** : Requis pour toutes les opérations CRUD.
- **`loguru`** : Gère la journalisation des événements (succès, erreurs).

---

## **Améliorations suggérées**

### **1. Validation des entrées**

- Vérifier la structure et la validité des documents avant de les insérer ou mettre à jour.
- Ajouter des messages d’erreur détaillés pour des cas comme :
    
    ```
    [ERROR] Le filtre pour la suppression est vide. Action annulée.
    ```
    

### **2. Tests unitaires**

- Tester chaque opération CRUD avec des scénarios variés :
    - Insertion avec des documents invalides.
    - Lecture avec un filtre inexistant.
    - Mise à jour sur une collection vide.
    - Exportation avec une collection vide.

### **3. Flexibilité pour l’export**

- Permettre de spécifier dynamiquement les colonnes à exclure ou inclure lors de l’export.

---

## **Conclusion**

Le script **`crud.py`** est un module central pour la gestion des données dans MongoDB. Il encapsule les opérations CRUD de manière robuste, tout en offrant une fonctionnalité d’export pratique. Des validations renforcées et des tests unitaires augmenteraient encore sa fiabilité.

# **Documentation du Script :`interactive_cli.py`**

---

## **Objectif principal**

Le script **`interactive_cli.py`** fournit une interface utilisateur en ligne de commande (CLI) pour manipuler une collection MongoDB. Les utilisateurs peuvent effectuer des opérations CRUD (Create, Read, Update, Delete) et exporter les données en CSV, selon leur rôle.

---

## **Fonctionnalités principales**

### **1. Importation des bibliothèques**

- **`pandas`** : Affiche les résultats sous forme de tableau.
- **`crud`** : Fournit les fonctions CRUD pour MongoDB (insertion, lecture, mise à jour, suppression, exportation).
- **`loguru`** : Enregistre les journaux pour suivre les événements et erreurs.

---

### **2. Fonction `display_menu(role)`**

### **Rôle**

- Affiche un menu interactif basé sur le rôle utilisateur.

### **Pourquoi**

- Restreint ou autorise les actions disponibles selon le rôle.

### **Étapes principales**

1. Affiche des options CRUD et d’exportation pour les rôles suivants :
    - **`admin_user`** : Accès complet (CRUD + exportation).
    - **`editor_user`** : Accès à CREATE, READ, UPDATE, et exportation.
    - **`reader_user`** : Accès limité à READ et exportation.

---

### **3. Fonction `handle_read(collection)`**

### **Rôle**

- Récupère et affiche des documents MongoDB selon un filtre et une limite.

### **Pourquoi**

- Permet à l’utilisateur de lire des données spécifiques.

### **Étapes principales**

1. Demande un filtre JSON (optionnel) et une limite.
2. Utilise `read_records` pour récupérer les documents.
3. Affiche les documents sous forme de tableau avec Pandas.
4. Affiche "Aucun document trouvé" si aucun résultat.

### **Gestion des erreurs**

- Loggue une erreur descriptive en cas de problème.

---

### **4. Fonction `handle_create(collection)`**

### **Rôle**

- Insère un document dans MongoDB en collectant les champs via le CLI.

### **Pourquoi**

- Permet d’ajouter des données dynamiquement.

### **Étapes principales**

1. Demande les champs requis (ex. : `name`, `age`, `gender`).
2. Formate les données en dictionnaire et utilise `insert_records` pour les insérer.
3. Affiche le nombre de documents insérés.

### **Gestion des erreurs**

- Loggue une erreur descriptive en cas de problème.

---

### **5. Fonction `handle_update(collection)`**

### **Rôle**

- Met à jour les documents MongoDB correspondant à un filtre.

### **Pourquoi**

- Permet de modifier ou enrichir les données existantes.

### **Étapes principales**

1. Demande un filtre JSON pour sélectionner les documents.
2. Demande une mise à jour en format JSON.
3. Utilise `update_records` pour appliquer les changements.
4. Affiche le nombre de documents mis à jour.

### **Gestion des erreurs**

- Loggue une erreur descriptive en cas de problème.

---

### **6. Fonction `handle_delete(collection)`**

### **Rôle**

- Supprime les documents MongoDB correspondant à un filtre.

### **Pourquoi**

- Nettoie ou retire des données obsolètes.

### **Étapes principales**

1. Demande un filtre JSON pour supprimer les documents.
2. Utilise `delete_records` pour exécuter la suppression.
3. Affiche le nombre de documents supprimés.

### **Gestion des erreurs**

- Loggue une erreur descriptive en cas de problème.

---

### **7. Fonction `handle_export(collection)`**

### **Rôle**

- Exporte tous les documents MongoDB vers un fichier CSV.

### **Pourquoi**

- Permet de partager ou d’analyser les données en dehors de MongoDB.

### **Étapes principales**

1. Demande un nom de fichier CSV.
2. Utilise `export_to_csv` pour effectuer l’opération.
3. Affiche le nombre de documents exportés.

### **Gestion des erreurs**

- Loggue une erreur descriptive si l’export échoue.

---

### **8. Fonction `interactive_menu(role, collection)`**

### **Rôle**

- Implémente un menu interactif pour les actions CRUD et l’exportation.

### **Pourquoi**

- Permet une gestion simplifiée des données via une interface intuitive.

### **Étapes principales**

1. Affiche un menu basé sur le rôle utilisateur (via `display_menu`).
2. Déclenche les fonctions appropriées (`handle_read`, `handle_create`, etc.) selon le choix.
3. Loggue un message pour les choix invalides.
4. Permet de quitter avec l’option 6.

---

## **Utilisation dans le projet**

### **1. Interface utilisateur interactive**

- Permet aux utilisateurs d’interagir avec les données MongoDB directement depuis le terminal.

### **2. Gestion basée sur les rôles**

- Autorise ou restreint les actions en fonction des permissions attribuées (via `setup_users.py`).

### **3. Opérations flexibles**

- Prend en charge les filtres dynamiques et les mises à jour personnalisées via des entrées utilisateur.

---

## **Dépendances critiques**

1. **`crud`** : Implémente les fonctions d’interaction avec MongoDB.
2. **`pandas`** : Utilisé pour afficher les données sous forme tabulaire.
3. **`loguru`** : Gère les journaux d’événements et d’erreurs.

---

## **Améliorations suggérées**

### **1. Validation des entrées**

- Ajouter une validation pour les filtres et mises à jour JSON afin d’éviter les erreurs dues à des formats incorrects.

### **2. Messages d’erreur détaillés**

- Inclure des messages plus descriptifs pour les choix invalides dans le menu.

### **3. Tests unitaires**

- Tester les cas suivants :
    - Lecture avec un filtre inexistant.
    - Mise à jour ou suppression avec des filtres invalides.
    - Exportation avec une collection vide.

---

## **Conclusion**

Le script **`interactive_cli.py`** est un outil puissant et flexible pour interagir avec MongoDB via le terminal. Sa gestion basée sur les rôles garantit un contrôle sécurisé des actions disponibles. Des validations renforcées et des tests unitaires augmenteraient encore sa fiabilité.

# **Documentation du Script : `test.py`**

---

## **Objectif principal**

Le script **`test.py`** est conçu pour valider les fonctionnalités principales du module **`crud.py`**, notamment les opérations CRUD (Create, Read, Update, Delete) et l'exportation de données depuis MongoDB vers un fichier CSV. Chaque test est isolé grâce à l'utilisation de bases de données temporaires et garantit que les fonctions fonctionnent comme prévu.

---

## **Structure et Configuration**

### **1. Configuration des logs**

- **Fichier de log** : `logs/test.log`.
- **Niveau de log** : INFO.
- **Rotation** : Les fichiers de log sont compressés automatiquement lorsqu'ils atteignent 1 Mo.

---

### **2. Fonction utilitaire : `get_mongodb_client()`**

### **Rôle**

- Configure une base de données MongoDB temporaire pour chaque test.
- Retourne une collection MongoDB prête à l'emploi et une fonction de nettoyage associée.

### **Étapes principales**

1. Crée une base de données temporaire avec un nom unique pour éviter les conflits.
2. Connecte à MongoDB via **`MongoClient`**.
3. Crée une collection temporaire : `test_patients_data`.
4. Définit une fonction interne **`cleanup()`** pour supprimer la base de données temporaire et fermer la connexion après chaque test.

### **Retour**

- Une collection MongoDB et une fonction de nettoyage à appeler après chaque test.

---

## **Détails des tests**

### **1. Test : `test_insert_records()`**

### **Rôle**

- Vérifie que les documents sont correctement insérés dans MongoDB.

### **Étapes principales**

1. Prépare une liste de documents avec des identifiants uniques.
2. Insère les documents via **`insert_records()`**.
3. Vérifie que le nombre de documents insérés correspond au nombre attendu.

### **Assertions**

- Le nombre de documents insérés doit être exact.
- Les documents insérés doivent correspondre aux données initiales.

---

### **2. Test : `test_read_records()`**

### **Rôle**

- Vérifie que les documents peuvent être lus correctement, avec ou sans filtres.

### **Étapes principales**

1. Insère des documents dans la collection temporaire.
2. Utilise **`read_records()`** pour lire les documents avec un filtre spécifique.
3. Vérifie que les résultats correspondent au filtre appliqué.

### **Assertions**

- Le filtre doit retourner exactement les résultats attendus.

---

### **3. Test : `test_update_records()`**

### **Rôle**

- Vérifie que les documents MongoDB peuvent être mis à jour correctement.

### **Étapes principales**

1. Insère un document initial avec des valeurs définies.
2. Met à jour un champ du document via **`update_records()`**.
3. Vérifie que la mise à jour est appliquée correctement.

### **Assertions**

- Le nombre de documents mis à jour doit être exact.
- La valeur mise à jour doit correspondre à la nouvelle valeur.

---

### **4. Test : `test_delete_records()`**

### **Rôle**

- Vérifie que les documents peuvent être supprimés correctement.

### **Étapes principales**

1. Insère un ou plusieurs documents dans la collection.
2. Supprime un document spécifique via **`delete_records()`**.
3. Vérifie que le document supprimé n'existe plus.

### **Assertions**

- Le nombre de documents supprimés doit être exact.
- La collection doit être vide après la suppression si tous les documents ont été supprimés.

---

### **5. Test : `test_export_to_csv()`**

### **Rôle**

- Vérifie que les documents MongoDB peuvent être exportés correctement dans un fichier CSV.

### **Étapes principales**

1. Insère des documents dans la collection temporaire.
2. Utilise **`export_to_csv()`** pour générer un fichier CSV.
3. Vérifie que :
    - Le fichier CSV est créé.
    - Le contenu du fichier correspond aux données insérées.
4. Supprime le fichier CSV après le test.

### **Améliorations par rapport à la version précédente**

- Ajout d'une étape explicite pour créer le répertoire cible avant l'exportation.
- Utilisation de `os.makedirs()` pour s'assurer que le chemin cible existe.
- Log détaillé des premières lignes du fichier CSV exporté pour validation.

### **Assertions**

- Le fichier CSV doit exister après l'exportation.
- Le contenu du fichier doit correspondre aux documents insérés.

---

## **Utilisation dans le projet**

### **1. Validation fonctionnelle**

- Garantit que toutes les opérations CRUD et d'exportation fonctionnent comme prévu.

### **2. Détection des erreurs**

- Identifie rapidement les anomalies ou régressions dans les fonctions CRUD.

### **3. Automatisation**

- Peut être intégré dans une pipeline CI/CD pour des tests automatisés.

---

## **Dépendances**

1. **`pymongo`** : Interagit avec MongoDB.
2. **`crud.py`** : Fournit les fonctions CRUD testées.
3. **`loguru`** : Gère les logs d'événements et d'erreurs.
4. **`os`** : Gère les fichiers exportés (CSV).
5. **`uuid`** : Génère des identifiants uniques pour les bases de données temporaires.

---

## **Améliorations suggérées**

### **1. Couverture des cas limites**

- Tester l'insertion de documents invalides.
- Exportation avec une collection vide.

### **2. Paramètres dynamiques**

- Tester différentes bases ou collections via des paramètres.

### **3. Documentation**

- Inclure des exemples d'utilisation pour chaque test.

---

## **Résumé**

Le script **`test.py`** est un outil clé pour valider la robustesse des opérations CRUD et d’exportation dans MongoDB. Il garantit que les modules fonctionnent comme prévu et identifie rapidement les anomalies.

# **Documentation du Script :  `main.py`**

---

## **Objectif principal**

Le script **`main.py`** constitue le point d'entrée principal de l'application. Il orchestre les étapes nécessaires pour :

1. Authentifier l'utilisateur.
2. Charger les données depuis un fichier CSV dans MongoDB.
3. Fournir une interface CLI pour exécuter des opérations CRUD sur MongoDB.

---

## **Détails des fonctionnalités**

### **1. Importations**

- **`utils`** :
    - `connect_to_mongodb` : Établit une connexion sécurisée à MongoDB.
    - `load_data` : Charge un fichier CSV et le transforme en liste de dictionnaires.
    - `create_indexes` : Crée des index pour optimiser les requêtes MongoDB.
- **`auth`** :
    - `authenticate_user` : Valide les identifiants utilisateur.
- **`crud`** :
    - Implémente les opérations CRUD : insertion, lecture, mise à jour, suppression, et export en CSV.
- **`interactive_cli`** :
    - `interactive_menu` : Interface CLI pour exécuter les opérations CRUD.
- **Autres bibliothèques** :
    - `argparse` : Analyse des arguments en ligne de commande.
    - `getpass` : Permet une saisie sécurisée des mots de passe.
    - `loguru` : Gestion avancée des journaux.

---

### **2. Étapes principales**

### **Étape 1 : Analyse des arguments**

- Utilise `ArgumentParser` pour extraire :
    - Le chemin du fichier CSV contenant les données à insérer dans MongoDB.

### **Étape 2 : Connexion à MongoDB**

- Appelle `connect_to_mongodb` pour se connecter à MongoDB via l’URI par défaut `mongodb_service_container:27017`.

### **Étape 3 : Authentification**

- Demande un **nom d'utilisateur** et un **mot de passe**.
- Appelle `authenticate_user` pour valider les identifiants :
    - Si la validation échoue, loggue un message d'erreur et quitte le programme.

### **Étape 4 : Identification du rôle utilisateur**

- Récupère le rôle utilisateur (`admin_user`, `editor_user`, ou `reader_user`) pour définir les permissions disponibles.

### **Étape 5 : Chargement des données**

- Utilise `load_data` pour charger et transformer le fichier CSV en une liste de dictionnaires.
- Vérifie la validité des données.

### **Étape 6 : Initialisation de la collection MongoDB**

- Accède ou crée une collection MongoDB nommée **`patients_data`**.

### **Étape 7 : Insertion des données**

- Insère les données nettoyées dans MongoDB via `insert_records`.
- Affiche les 5 premiers documents pour validation.

### **Étape 8 : Création des index**

- Optimise les performances des requêtes avec `create_indexes`.

### **Étape 9 : Interface utilisateur CLI**

- Lance le **menu interactif** via `interactive_menu` :
    - Propose les opérations CRUD et exportation.
    - Respecte les permissions définies par le rôle utilisateur.

---

### **3. Gestion des erreurs**

- Si une erreur survient à n'importe quelle étape :
    - Elle est enregistrée dans un fichier de journalisation (`logs/main.log`).
    - Le programme s'arrête proprement.

---

## **Utilisation typique**

1. Lancer le script depuis un terminal avec :
    
    ```bash
    bash
    CopierModifier
    python main.py /chemin/vers/healthcare_dataset_cleaned.csv
    
    ```
    
2. Saisir les identifiants de l'utilisateur pour s'authentifier.
3. Accéder à l'interface CLI pour gérer les données MongoDB.

---

## **Dépendances critiques**

1. **`utils.py`** : Fournit des fonctions pour la connexion à MongoDB, le chargement des données, et la création des index.
2. **`auth.py`** : Valide les identifiants utilisateur.
3. **`crud.py`** : Implémente les opérations CRUD et l’exportation.
4. **`interactive_cli.py`** : Fournit une interface utilisateur.
5. **MongoDB** : Base de données pour stocker et manipuler les données.

---

## **Améliorations suggérées**

### **1. Gestion avancée des arguments**

- Ajouter une validation pour vérifier si le fichier CSV existe avant de lancer le script.

### **2. Tests unitaires**

- Tester chaque étape de manière isolée :
    - Connexion MongoDB.
    - Authentification.
    - Chargement et insertion des données.
    - Interactions CLI.

### **3. Sécurisation**

- Remplacer les identifiants en dur par des variables d’environnement ou un fichier `.env`.

---

## **Résumé**

Le script **`main.py`** est la pierre angulaire du projet, coordonnant toutes les étapes nécessaires pour charger, authentifier, et manipuler les données via MongoDB. Des améliorations mineures comme la validation des arguments et l’intégration de tests unitaires renforceraient encore sa robustesse.