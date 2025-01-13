# Importation des bibliothèques nécessaires
import os  # Gestion des variables d'environnement
from pymongo import MongoClient  # Interagir avec MongoDB
from loguru import logger  # Gestion des logs
import pandas as pd  # Manipulation des données tabulaires
import argparse  # Analyse des arguments en ligne de commande
from time import sleep  # Délais d'attente

# Fonction pour attendre que MongoDB soit prêt
def wait_for_mongodb(uri, timeout=30):
    """
    Attend que MongoDB soit prêt.

    Args:
        uri (str): URI pour se connecter à MongoDB.
        timeout (int): Temps maximum pour attendre (en secondes).

    Returns:
        MongoClient: Instance connectée à MongoDB.

    Raises:
        TimeoutError: Si MongoDB n'est pas prêt dans le temps imparti.
    """
    logger.info(f"Tentative de connexion à MongoDB ({uri}).")
    for attempt in range(timeout):
        try:
            client = MongoClient(uri, serverSelectionTimeoutMS=1000)
            client.server_info()  # Vérifie si MongoDB répond
            logger.success("Connexion à MongoDB réussie.")
            return client
        except Exception as e:
            logger.warning(f"Tentative {attempt + 1}/{timeout} : MongoDB non prêt. Erreur : {e}")
            sleep(1)
    raise TimeoutError("MongoDB n'a pas répondu à temps.")

# Fonction pour établir une connexion à MongoDB
def connect_to_mongodb(uri, database_name="healthcare_database"):
    """
    Établit une connexion à MongoDB.

    Args:
        uri (str): URI pour se connecter à MongoDB.
        database_name (str): Nom de la base MongoDB.

    Returns:
        Database: Instance de la base MongoDB.

    Raises:
        Exception: En cas de problème de connexion.
    """
    try:
        client = wait_for_mongodb(uri)
        db = client[database_name]
        logger.info(f"Connexion réussie à la base de données '{database_name}'.")
        return db
    except Exception as e:
        logger.error(f"Impossible de se connecter à MongoDB : {e}")
        raise

# Fonction pour charger les données depuis un fichier CSV
def load_data(file_path):
    """
    Charge un fichier CSV et retourne les données sous forme de liste de dictionnaires.

    Args:
        file_path (str): Chemin du fichier CSV.

    Returns:
        list: Données formatées pour MongoDB.
    """
    try:
        df = pd.read_csv(file_path)
        logger.info(f"Données chargées : {len(df)} lignes, {len(df.columns)} colonnes.")
        return df.to_dict(orient="records")
    except Exception as e:
        logger.error(f"Erreur lors du chargement des données : {e}")
        raise

# Fonctions CRUD pour MongoDB
def insert_records(collection, records):
    """Insère des documents dans une collection MongoDB."""
    if not records:
        logger.warning("Aucune donnée à insérer.")
        return 0
    try:
        result = collection.insert_many(records)
        logger.info(f"{len(result.inserted_ids)} documents insérés.")
        return len(result.inserted_ids)
    except Exception as e:
        logger.error(f"Erreur lors de l'insertion : {e}")
        raise

def read_records(collection, query={}, limit=5):
    """Lit des documents depuis MongoDB."""
    try:
        records = collection.find(query).limit(limit)
        logger.info(f"{limit} documents lus.")
        return list(records)
    except Exception as e:
        logger.error(f"Erreur lors de la lecture : {e}")
        raise

def update_records(collection, filter_query, update_query):
    """Met à jour des documents dans MongoDB."""
    try:
        result = collection.update_many(filter_query, update_query)
        logger.info(f"{result.modified_count} documents mis à jour.")
        return result.modified_count
    except Exception as e:
        logger.error(f"Erreur lors de la mise à jour : {e}")
        raise

def delete_records(collection, filter_query):
    """Supprime des documents dans MongoDB."""
    try:
        result = collection.delete_many(filter_query)
        logger.info(f"{result.deleted_count} documents supprimés.")
        return result.deleted_count
    except Exception as e:
        logger.error(f"Erreur lors de la suppression : {e}")
        raise

# Bloc principal
if __name__ == "__main__":
    try:
        # Arguments en ligne de commande
        parser = argparse.ArgumentParser(description="Migration des données vers MongoDB")
        parser.add_argument("file_path", type=str, help="Chemin du fichier CSV.")
        args = parser.parse_args()

        logger.info("Démarrage du script...")

        # Connexion à MongoDB
        uri = "mongodb://mongodb_service_container:27017/"  # Utilise le nom du conteneur
        db = connect_to_mongodb(uri)
        collection = db["patients_data"]


        # Opérations CRUD
        logger.info("=== CREATE : Insertion des données ===")
        records = load_data(args.file_path)
        insert_count = insert_records(collection, records)

        logger.info("=== READ : Lecture des données ===")
        all_data = read_records(collection, {}, limit=10)
        logger.info("Données lues :")
        for doc in all_data:
            logger.info(doc)

        logger.info("=== UPDATE : Mise à jour ===")
        update_query = {"$set": {"ValidationStatus": "Validated"}}
        update_count = update_records(collection, {"Age": {"$gte": 50}}, update_query)
        logger.info(f"Documents mis à jour avec ValidationStatus='Validated' : {update_count}")

        logger.info("=== DELETE : Suppression ===")
        delete_count = delete_records(collection, {"Age": {"$lt": 30}})
        logger.info(f"Documents supprimés où Age < 30 : {delete_count}")

        logger.info("=== TESTS SUPPLÉMENTAIRES ===")
        # Insérer un seul document
        single_doc = {"Name": "Test User", "Age": 45, "ValidationStatus": "Pending"}
        insert_records(collection, [single_doc])

        # Lire avec un filtre
        filtered_data = read_records(collection, {"Name": "Test User"}, limit=1)
        logger.info(f"Document filtré : {filtered_data}")

        # Mettre à jour un document précis
        update_records(collection, {"Name": "Test User"}, {"$set": {"ValidationStatus": "Completed"}})

        # Vérifier après mise à jour
        updated_data = read_records(collection, {"Name": "Test User"}, limit=1)
        logger.info(f"Document mis à jour : {updated_data}")

        # Supprimer le document de test
        delete_records(collection, {"Name": "Test User"})

        # Insertion de documents avec des champs facultatifs
        optional_field_docs = [
            {"Name": "User A", "Age": 40},
            {"Name": "User B", "ValidationStatus": "Pending"},
        ]
        insert_records(collection, optional_field_docs)

        # Lire avec tri et limite
        sorted_data = collection.find().sort("Age", -1).limit(5)
        logger.info("Documents triés par Age descendant :")
        for doc in sorted_data:
            logger.info(doc)

        # Mise à jour avec ajout de champs
        update_records(collection, {"Name": "User A"}, {"$set": {"ValidationStatus": "Completed"}})

        # Lecture avec projection de champs
        projected_data = collection.find({}, {"_id": 0, "Name": 1, "ValidationStatus": 1}).limit(5)
        logger.info("Projection des champs (Name, ValidationStatus) :")
        for doc in projected_data:
            logger.info(doc)

        # Suppression conditionnelle par ValidationStatus
        delete_records(collection, {"ValidationStatus": "Pending"})
 

        logger.success("Toutes les opérations et tests supplémentaires sont terminés avec succès.")
    except Exception as e:
        logger.error(f"Erreur dans le script : {e}")
