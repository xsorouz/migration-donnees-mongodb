# Guide d'utilisation de Docker pour le projet

Ce document explique comment utiliser Docker pour gérer MongoDB et l'application Python associée à ce projet. Il contient des détails sur la configuration, les commandes utiles et les tests d'usage avec Docker.

---

## **Introduction**

Docker est utilisé dans ce projet pour :

- Garantir la portabilité et la reproductibilité de l'environnement.
- Simplifier la configuration des services MongoDB et Python.
- Fournir un environnement isolé pour l'exécution des scripts et des opérations CRUD.

---

## **Structure des fichiers Docker**

### **Dockerfile**

Le fichier `Dockerfile` définit l'image pour l'application Python. Voici un résumé de ses étapes principales :

1. **Image de base :**
    
    ```
    FROM python:3.12-slim
    
    ```
    
    - Utilise une image légère de Python 3.12.
2. **Installation des dépendances :**
    
    ```
    RUN pip install --no-cache-dir -r requirements.txt
    
    ```
    
    - Installe les bibliothèques nécessaires depuis `requirements.txt`.
3. **Copie des fichiers dans le conteneur :**
    
    ```
    COPY scripts /app/scripts
    COPY data /app/data
    COPY outputs /app/outputs
    
    ```
    
    - Copie les scripts, les données et le répertoire de sortie.
4. **Commandes exécutées par défaut :**
    
    ```
    CMD ["bash", "-c", "python /app/setup_users.py && python /app/initialize_users.py && python /app/main.py /app/data/processed/healthcare_data_cleaned.csv"]
    
    ```
    
    - Configure les utilisateurs MongoDB, initialise les données et lance l'interface CLI.

---

### **docker-compose.yml**

Le fichier `docker-compose.yml` orchestre les services nécessaires :

1. **Service MongoDB :**
    
    ```yaml
    mongodb_service:
      image: mongo:5.0
      container_name: mongodb_service_container
      ports:
        - "27017:27017"
      volumes:
        - mongodb_data:/data/db
    
    ```
    
    - Utilise MongoDB version 5.0.
    - Monte un volume pour persister les données.
2. **Service Application Python :**
    
    ```yaml
    python_application:
      build:
        context: ../
        dockerfile: docker/Dockerfile
      container_name: python_application_container
      depends_on:
        - mongodb_service
      volumes:
        - ../:/app
      stdin_open: true
      tty: true
    
    ```
    
    - Dépend du service MongoDB.
    - Monte le répertoire de travail local dans le conteneur.
3. **Volumes partagés :**
    
    ```yaml
    volumes:
      mongodb_data:
        driver: local
    
    ```
    
    - Assure la persistance des données MongoDB.

---

## **Commandes Docker**

### **Construire et exécuter les conteneurs**

1. Construire et démarrer les services définis dans `docker-compose.yml` :
    
    ```bash
    docker-compose up --build -d
    
    ```
    
2. Arrêter et supprimer les conteneurs :
    
    ```bash
    docker-compose down
    
    ```
    
3. Nettoyer les volumes inutilisés :
    
    ```bash
    docker volume prune -f
    
    ```
    

---

## **Accès à l'interface CLI**

### **Accéder au conteneur Python**

Pour accéder à l'interface CLI via le conteneur Python :

1. Ouvrir un terminal interactif dans le conteneur :
    
    ```bash
    docker exec -it python_application_container bash
    
    ```
    
2. Lancer l'interface CLI :
    
    ```bash
    python /app/main.py /app/data/processed/healthcare_data_cleaned.csv
    
    ```
    

---

## **Exemples de commandes CLI**

### **Commandes disponibles selon le rôle utilisateur**

### **a. Rôle `admin_user`**

1. **Afficher des documents (READ)**
    - Option : `1`
    - Entrées utilisateur :
        
        ```
        Entrez un filtre JSON (laisser vide pour aucun filtre) : {"gender": "Male"}
        Entrez une limite de documents (par défaut : 10) : 5
        
        ```
        
    - Résultat attendu : 5 documents où `gender` est "Male".
2. **Insérer un document (CREATE)**
    - Option : `2`
    - Entrées utilisateur :
        
        ```
        Entrez le nom : John Doe
        Entrez l'âge : 45
        
        ```
        
    - Résultat attendu : Le document est inséré dans la collection.
3. **Exporter les données (EXPORT)**
    - Option : `5`
    - Entrées utilisateur :
        
        ```
        Entrez le nom du fichier CSV : admin_export
        
        ```
        
    - Résultat attendu : Un fichier `admin_export.csv` est créé dans le répertoire `outputs/`.

### **b. Rôle `editor_user`**

1. **Afficher des documents (READ)**
    - Option : `1`
    - Entrées utilisateur :
        
        ```
        Entrez un filtre JSON (laisser vide pour aucun filtre) : {"medical_condition": "Hypertension"}
        Entrez une limite de documents (par défaut : 10) : 3
        
        ```
        
    - Résultat attendu : 3 documents où `medical_condition` est "Hypertension".
2. **Insérer un document (CREATE)**
    - Option : `2`
    - Entrées utilisateur :
        
        ```
        Entrez le nom : Jane Doe
        Entrez l'âge : 40
        Entrez le genre (Male/Female) : Female
        
        ```
        
    - Résultat attendu : Le document est ajouté dans la collection.

### **c. Rôle `reader_user`**

1. **Afficher des documents (READ)**
    - Option : `1`
    - Entrées utilisateur :
        
        ```
        Entrez un filtre JSON (laisser vide pour aucun filtre) : {}
        Entrez une limite de documents (par défaut : 10) : 5
        
        ```
        
    - Résultat attendu : Affiche 5 documents.
2. **Exporter les données (EXPORT)**
    - Option : `5`
    - Entrées utilisateur :
        
        ```
        Entrez le nom du fichier CSV : readonly_export
        
        ```
        
    - Résultat attendu : Un fichier `readonly_export.csv` est créé dans le répertoire `outputs/`.

---

## **Tests d'utilisation pour MongoDB**

### **Vérification directe via MongoDB Shell**

### **a. Connexion avec `admin_user`**

```bash
docker exec -it mongodb_service_container mongosh --username admin_user --password admin_password --authenticationDatabase admin

```

- **Exemple de commande :** Lister toutes les bases de données :
    
    ```jsx
    show dbs;
    
    ```
    

### **b. Connexion avec `editor_user`**

```bash
docker exec -it mongodb_service_container mongosh --username editor_user --password editor_password --authenticationDatabase healthcare_database

```

- **Exemple de commande :** Insérer un document :
    
    ```jsx
    db.patients_data.insertOne({ name: "Jane Doe", age: 45 });
    
    ```
    

### **c. Connexion avec `reader_user`**

```bash
docker exec -it mongodb_service_container mongosh --username reader_user --password reader_password --authenticationDatabase healthcare_database

```

- **Exemple de commande :** Lire les documents :
    
    ```jsx
    db.patients_data.find().pretty();
    
    ```
    

---

## **Gestion des erreurs et logs**

1. Les journaux des erreurs et des opérations sont enregistrés dans le conteneur sous `/app/logs`.
2. Pour consulter les logs :
    
    ```bash
    docker logs python_application_container
    
    ```
    

---

## **Nettoyage final**

1. Supprimer les volumes inutilisés :
    
    ```bash
    docker volume prune -f
    
    ```
    
2. Supprimer les images inutilisées :
    
    ```bash
    docker system prune -f
    
    ```
    

---

**Ce guide est conçu pour assurer une utilisation fluide et sans erreur de Docker pour ce projet. Si vous rencontrez des problèmes, vérifiez les logs ou contactez un administrateur.**