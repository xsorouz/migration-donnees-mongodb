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
   ```Dockerfile
   FROM python:3.12-slim
   ```
   - Utilise une image légère de Python 3.12.

2. **Installation des dépendances :**
   ```Dockerfile
   RUN pip install --no-cache-dir -r requirements.txt
   ```
   - Installe les bibliothèques nécessaires depuis `requirements.txt`.

3. **Copie des fichiers dans le conteneur :**
   ```Dockerfile
   COPY scripts /app/scripts
   COPY data /app/data
   COPY outputs /app/outputs
   ```
   - Copie les scripts, les données et le répertoire de sortie.

4. **Commandes exécutées par défaut :**
   ```Dockerfile
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

### **Exemples de commandes CLI**

1. **Afficher des documents (READ)**
   - Choix : `1`
   - Affiche un aperçu des documents présents dans MongoDB.

2. **Insérer un document (CREATE)**
   - Choix : `2`
   - Exemple d'entrée :
     ```
     Entrez le nom : John Doe
     Entrez l'âge : 45
     ```

3. **Mettre à jour un document (UPDATE)**
   - Choix : `3`
   - Exemple d'entrée :
     ```
     Entrez le nom du document à mettre à jour : John Doe
     Entrez le nouvel âge : 50
     ```

4. **Exporter des données dans un fichier CSV (EXPORT)**
   - Choix : `5`
   - Exemple d'entrée :
     ```
     Entrez le nom du fichier CSV : export_test
     ```
   - Le fichier sera enregistré dans le répertoire `outputs/` avec l'extension `.csv`.

5. **Quitter**
   - Choix : `6`

---

## **Vérification de MongoDB**

### **Accéder au shell MongoDB**
Pour interagir avec MongoDB directement :
```bash
docker exec -it mongodb_service_container mongosh
```

### **Vérifier les collections**
1. Passer à la base de données :
   ```javascript
   use healthcare_database
   ```

2. Lister les collections :
   ```javascript
   show collections
   ```

3. Afficher les documents :
   ```javascript
   db.patients_data.find().pretty()
   ```

---

## **Tests d'usage pour les rôles MongoDB**

### **Tests avec l'utilisateur `admin_user`**

- Connexion :
  ```bash
  mongosh --username admin_user --password admin_password --authenticationDatabase admin
  ```
- Droits :
  - Lecture, écriture et administration complète.

### **Tests avec l'utilisateur `editor_user`**

- Connexion :
  ```bash
  mongosh --username editor_user --password editor_password --authenticationDatabase healthcare_database
  ```
- Droits :
  - Lecture et écriture uniquement sur `healthcare_database`.

### **Tests avec l'utilisateur `reader_user`**

- Connexion :
  ```bash
  mongosh --username reader_user --password reader_password --authenticationDatabase healthcare_database
  ```
- Droits :
  - Lecture seule sur `healthcare_database`.
  - Toute tentative d'écriture ou de suppression sera refusée.

---

## **Gestion des erreurs et logs**

- Les journaux des erreurs et des opérations sont enregistrés dans le conteneur dans le répertoire `/app/logs`.
- Pour consulter les logs :
  ```bash
  docker logs python_application_container
  ```

---

## **Nettoyage final**

Pour libérer de l'espace disque :

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