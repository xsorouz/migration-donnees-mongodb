from loguru import logger  # Gestion avancée des logs
import pandas as pd  # Manipulation de données tabulaires
import os

# === Fonction d'insertion de documents dans MongoDB ===
def insert_records(collection, records):
    """
    Insère une liste de documents dans une collection MongoDB.

    Args:
        collection (Collection): Collection cible dans MongoDB.
        records (list): Liste de dictionnaires représentant les documents à insérer.

    Returns:
        int: Nombre de documents insérés.

    Raises:
        Exception: En cas d'erreur lors de l'insertion.
    """
    if not records:  # Si la liste est vide, prévenir l'utilisateur
        logger.warning("Aucune donnée à insérer.")
        return 0
    try:
        result = collection.insert_many(records) # Insère plusieurs documents
        logger.info(f"{len(result.inserted_ids)} documents insérés.")
        # Afficher les documents insérés
        for record in records:
            print(record)
        return len(result.inserted_ids)
    except Exception as e:
        logger.error(f"Erreur lors de l'insertion : {e}")
        raise
# === Fonction de lecture de documents dans MongoDB ===
def read_records(collection, query={}, limit=5):
    """
    Lit des documents depuis une collection MongoDB avec des filtres et une limite.

    Args:
        collection (Collection): Collection cible dans MongoDB.
        query (dict): Filtre pour la lecture des documents (par défaut : {}).
        limit (int): Nombre maximum de documents à lire.

    Returns:
        list: Liste des documents lus.

    Raises:
        Exception: En cas d'erreur lors de la lecture.
    """
    try:
        records = collection.find(query).limit(limit)  # Applique le filtre et limite les résultats
        logger.info(f"{limit} documents lus.")
        return list(records)
    except Exception as e:
        logger.error(f"Erreur lors de la lecture : {e}")
        raise

# === Fonction de mise à jour de documents dans MongoDB ===
def update_records(collection, filter_query, update_query):
    """
    Met à jour les documents correspondant à un filtre dans MongoDB.

    Args:
        collection (Collection): Collection cible dans MongoDB.
        filter_query (dict): Filtre pour sélectionner les documents à mettre à jour.
        update_query (dict): Mise à jour à appliquer.

    Returns:
        int: Nombre de documents modifiés.

    Raises:
        Exception: En cas d'erreur lors de la mise à jour.
    """
    try:
        result = collection.update_many(filter_query, update_query) # Met à jour plusieurs documents
        logger.info(f"{result.modified_count} documents mis à jour.")
        # Afficher les documents après mise à jour
        updated_docs = collection.find(filter_query)
        for doc in updated_docs:
            print(doc)
        return result.modified_count
    except Exception as e:
        logger.error(f"Erreur lors de la mise à jour : {e}")
        raise

# === Fonction de suppression de documents dans MongoDB ===
def delete_records(collection, filter_query):
    """
    Supprime les documents correspondant à un filtre dans MongoDB.

    Args:
        collection (Collection): Collection cible dans MongoDB.
        filter_query (dict): Filtre pour sélectionner les documents à supprimer.

    Returns:
        int: Nombre de documents supprimés.

    Raises:
        Exception: En cas d'erreur lors de la suppression.
    """
    try:
        result = collection.delete_many(filter_query)  # Supprime plusieurs documents
        logger.info(f"{result.deleted_count} documents supprimés.")
        return result.deleted_count
    except Exception as e:
        logger.error(f"Erreur lors de la suppression : {e}")
        raise

# === Fonction d'exportation de documents vers un fichier CSV ===
def export_to_csv(collection, file_name):
    """
    Exporte les documents d'une collection MongoDB vers un fichier CSV.

    Args:
        collection (Collection): Collection cible.
        file_name (str): Nom du fichier CSV (sans chemin ni extension).

    Returns:
        int: Nombre de documents exportés.
    """
    try:
        # Définir le répertoire d'exportation
        output_dir = "outputs"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)  # Créer le répertoire si inexistant
            logger.info(f"Répertoire créé : {output_dir}")
        
        # Ajouter l'extension .csv au nom du fichier
        output_file = os.path.join(output_dir, f"{file_name}.csv")
        
        # Récupérer les documents de MongoDB
        records = list(collection.find())
        if not records:
            logger.warning("Aucun document à exporter.")
            return 0
        
        # Convertir en DataFrame et supprimer la colonne "_id"
        df = pd.DataFrame(records)
        if "_id" in df.columns:
            df.drop(columns=["_id"], inplace=True)
        
        # Exporter en CSV
        df.to_csv(output_file, index=False)
        logger.info(f"Données exportées dans le fichier : {output_file}")
        return len(df)
    except Exception as e:
        logger.error(f"Erreur lors de l'exportation : {e}")
        raise
