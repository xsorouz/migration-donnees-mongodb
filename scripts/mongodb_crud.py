from pymongo import MongoClient
from loguru import logger
import pandas as pd

# Connexion à MongoDB
def connect_to_mongodb(uri="mongodb://localhost:27017/", database_name="healthcare_database"):
    """
    Établit une connexion à MongoDB et retourne la base de données spécifiée.

    Args:
        uri (str): URI de connexion à MongoDB.
        database_name (str): Nom de la base de données.

    Returns:
        Database: Objet base de données MongoDB.
    """
    client = MongoClient(uri)
    db = client[database_name]
    logger.info(f"Connecté à MongoDB, base de données : {database_name}")
    return db

# CREATE : Insérer des documents
def insert_records(collection, records):
    """
    Insère une liste de documents dans une collection MongoDB.

    Args:
        collection (Collection): Collection MongoDB.
        records (list): Liste de documents à insérer.

    Returns:
        int: Nombre de documents insérés.
    """
    result = collection.insert_many(records)
    logger.info(f"{len(result.inserted_ids)} documents insérés avec succès.")
    return len(result.inserted_ids)

# READ : Lire des documents
def read_records(collection, query={}, limit=5):
    """
    Lit des documents d'une collection MongoDB.

    Args:
        collection (Collection): Collection MongoDB.
        query (dict): Filtre pour la lecture.
        limit (int): Nombre maximum de documents à lire.

    Returns:
        list: Liste de documents.
    """
    records = collection.find(query).limit(limit)
    logger.info(f"{limit} documents récupérés avec la requête : {query}")
    return list(records)

# UPDATE : Mettre à jour des documents
def update_records(collection, filter_query, update_query):
    """
    Met à jour les documents dans une collection MongoDB.

    Args:
        collection (Collection): Collection MongoDB.
        filter_query (dict): Filtre pour sélectionner les documents à mettre à jour.
        update_query (dict): Changements à appliquer.

    Returns:
        int: Nombre de documents modifiés.
    """
    result = collection.update_many(filter_query, update_query)
    logger.info(f"{result.modified_count} documents mis à jour avec succès.")
    return result.modified_count

# DELETE : Supprimer des documents
def delete_records(collection, filter_query):
    """
    Supprime des documents d'une collection MongoDB.

    Args:
        collection (Collection): Collection MongoDB.
        filter_query (dict): Filtre pour sélectionner les documents à supprimer.

    Returns:
        int: Nombre de documents supprimés.
    """
    result = collection.delete_many(filter_query)
    logger.info(f"{result.deleted_count} documents supprimés avec succès.")
    return result.deleted_count

if __name__ == "__main__":
    # Exemple d'utilisation
    db = connect_to_mongodb()
    collection = db["patients_data"]

    # CREATE : Insérer des données
    sample_data = [{"Name": "John Doe", "Age": 30, "Gender": "Male"}, {"Name": "Jane Doe", "Age": 28, "Gender": "Female"}]
    insert_records(collection, sample_data)

    # READ : Lire des données
    records = read_records(collection, {}, limit=2)
    logger.info(f"Exemple de documents : {records}")

    # UPDATE : Mettre à jour des données
    update_records(collection, {"Name": "John Doe"}, {"$set": {"Age": 31}})

    # DELETE : Supprimer des données
    delete_records(collection, {"Name": "John Doe"})
