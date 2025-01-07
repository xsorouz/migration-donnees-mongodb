# Importation des bibliothèques nécessaires
import os  # Pour lire les variables d'environnement (comme MONGO_URI)
from pymongo import MongoClient  # Pour interagir avec MongoDB
from loguru import logger  # Pour la gestion des logs (messages d'information et d'erreur)
import pandas as pd  # Pour lire et manipuler les données sous forme de DataFrame
import argparse  # Pour permettre l'utilisation d'arguments en ligne de commande

# Fonction pour établir une connexion à MongoDB
def connect_to_mongodb():
    """
    Établit une connexion à MongoDB en lisant la variable d'environnement MONGO_URI.
    Si la variable n'est pas définie, utilise une URI par défaut.
    Retourne l'objet représentant la base de données spécifiée ('healthcare_database').
    """
    try:
        # Lire l'URI MongoDB depuis les variables d'environnement (ou utiliser une valeur par défaut)
        uri = os.environ.get("MONGO_URI", "mongodb://reader_user:reader_password@localhost:27017/")
        database_name = "healthcare_database"

        # Connexion au serveur MongoDB
        client = MongoClient(uri)
        db = client[database_name]  # Sélection de la base de données
        logger.info(f"Connecté à MongoDB avec la base : {database_name}")
        return db
    except Exception as e:
        # Loguer et relancer l'erreur en cas de problème de connexion
        logger.error(f"Erreur lors de la connexion à MongoDB : {e}")
        raise

# Fonction pour charger les données depuis un fichier CSV
def load_data(file_path):
    """
    Charge les données depuis un fichier CSV et les transforme en une liste de dictionnaires.
    
    Args:
        file_path (str): Chemin du fichier CSV à charger.
    
    Returns:
        list: Liste de documents sous forme de dictionnaires.
    """
    try:
        # Lire le fichier CSV en tant que DataFrame
        df = pd.read_csv(file_path)
        logger.info(f"Données chargées depuis {file_path} : {len(df)} lignes, {len(df.columns)} colonnes.")
        # Convertir le DataFrame en une liste de dictionnaires pour MongoDB
        return df.to_dict(orient="records")
    except Exception as e:
        # Loguer et relancer l'erreur si le fichier ne peut pas être chargé
        logger.error(f"Erreur lors du chargement des données : {e}")
        raise

# Fonction pour insérer des documents dans MongoDB
def insert_records(collection, records):
    """
    Insère une liste de documents dans une collection MongoDB.
    
    Args:
        collection (Collection): Collection MongoDB où insérer les documents.
        records (list): Liste de documents à insérer.
    
    Returns:
        int: Nombre de documents insérés avec succès.
    """
    if not records:
        logger.warning("Aucune donnée à insérer. La liste des documents est vide.")
        return 0
    try:
        result = collection.insert_many(records)
        logger.info(f"{len(result.inserted_ids)} documents insérés avec succès.")
        return len(result.inserted_ids)
    except Exception as e:
        logger.error(f"Erreur lors de l'insertion des documents : {e}")
        raise

# Fonction pour lire des documents depuis MongoDB
def read_records(collection, query={}, limit=5):
    """
    Lit un nombre limité de documents depuis une collection MongoDB.
    
    Args:
        collection (Collection): Collection MongoDB où effectuer la lecture.
        query (dict): Filtre pour la requête (par défaut, aucun filtre).
        limit (int): Nombre maximum de documents à lire.
    
    Returns:
        list: Liste de documents récupérés.
    """
    try:
        records = collection.find(query).limit(limit)
        logger.info(f"{limit} documents récupérés avec la requête : {query}")
        return list(records)
    except Exception as e:
        logger.error(f"Erreur lors de la lecture des documents : {e}")
        raise

# Fonction pour mettre à jour des documents dans MongoDB
def update_records(collection, filter_query, update_query):
    """
    Met à jour des documents dans une collection MongoDB selon un filtre.
    
    Args:
        collection (Collection): Collection MongoDB où effectuer la mise à jour.
        filter_query (dict): Critères pour sélectionner les documents à mettre à jour.
        update_query (dict): Modifications à appliquer aux documents sélectionnés.
    
    Returns:
        int: Nombre de documents modifiés.
    """
    try:
        result = collection.update_many(filter_query, update_query)
        logger.info(f"{result.modified_count} documents mis à jour.")
        return result.modified_count
    except Exception as e:
        logger.error(f"Erreur lors de la mise à jour des documents : {e}")
        raise


# Fonction pour supprimer des documents depuis MongoDB
def delete_records(collection, filter_query):
    """
    Supprime des documents d'une collection MongoDB selon un filtre.
    
    Args:
        collection (Collection): Collection MongoDB où effectuer la suppression.
        filter_query (dict): Critères pour sélectionner les documents à supprimer.
    
    Returns:
        int: Nombre de documents supprimés.
    """
    try:
        result = collection.delete_many(filter_query)
        logger.info(f"{result.deleted_count} documents supprimés.")
        return result.deleted_count
    except Exception as e:
        logger.error(f"Erreur lors de la suppression des documents : {e}")
        raise


# Bloc principal exécuté lorsque le script est lancé
if __name__ == "__main__":
    try:
        # Configurer les arguments en ligne de commande
        parser = argparse.ArgumentParser(description="Migration des données vers MongoDB")
        parser.add_argument("file_path", type=str, help="Chemin du fichier CSV à charger")
        args = parser.parse_args()

        # Étape 1 : Connexion à MongoDB
        db = connect_to_mongodb()
        collection = db["patients_data"]  # Nom de la collection MongoDB

        # Étape 2 : Charger les données depuis le fichier CSV
        records = load_data(args.file_path)

        # Étape 3 : Insérer les données dans MongoDB
        insert_count = insert_records(collection, records)
        logger.info(f"{insert_count} documents insérés dans la collection.")

        # Étape 4 : Lire quelques documents pour validation
        read_data = read_records(collection, {}, limit=5)
        logger.info(f"Exemple de documents : {read_data}")
    except Exception as e:
        # Gestion globale des erreurs pour éviter l'arrêt brutal du script
        logger.error(f"Erreur lors de l'exécution du script : {e}")
