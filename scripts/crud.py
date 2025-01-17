from loguru import logger  # Gestion avancée des logs
import pandas as pd  # Manipulation de données tabulaires
import os  # Gestion des interactions avec le système de fichiers

# === Fonction d'insertion de documents dans MongoDB ===
def insert_records(collection, records):
    """
    Insère une liste de documents dans une collection MongoDB.

    Cette fonction permet d'ajouter plusieurs documents (sous forme de dictionnaires Python)
    dans une collection MongoDB. Elle gère également les erreurs potentielles pendant
    l'opération d'insertion.

    Args:
        collection (Collection): Collection cible dans MongoDB.
        records (list): Liste de dictionnaires représentant les documents à insérer.

    Returns:
        int: Nombre de documents insérés.

    Raises:
        Exception: En cas d'erreur lors de l'insertion.
    """
    if not records:  # Si la liste de documents à insérer est vide
        logger.warning("Aucune donnée à insérer.")
        return 0
    try:
        # Insérer les documents dans la collection MongoDB
        result = collection.insert_many(records)
        logger.info(f"{len(result.inserted_ids)} documents insérés avec succès.")

        # Exemple : Afficher uniquement un échantillon de 5 documents
        logger.info("Exemple de documents insérés :")
        for record in records[:5]:  # Limité à 5 documents
            logger.info(record)

        return len(result.inserted_ids)
    except Exception as e:
        # Gérer et enregistrer les erreurs
        logger.error(f"Erreur lors de l'insertion : {e}")
        raise

# === Fonction de lecture de documents dans MongoDB ===
def read_records(collection, query={}, limit=5):
    """
    Lit des documents depuis une collection MongoDB avec des filtres et une limite.

    Cette fonction permet de lire un nombre limité de documents depuis une collection,
    en appliquant un filtre optionnel pour restreindre les résultats.

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
        # Lire les documents depuis MongoDB avec un filtre et une limite
        records = collection.find(query).limit(limit)
        logger.info(f"{len(list(records))} documents récupérés (après application de la limite).")
        records.rewind()  # Remet l'état du curseur pour pouvoir réutiliser `records`
         # Retourner les documents sous forme de liste
        return list(records)
    except Exception as e:
        # Gérer les erreurs potentielles
        logger.error(f"Erreur lors de la lecture : {e}")
        raise

# === Fonction de mise à jour de documents dans MongoDB ===
def update_records(collection, filter_query, update_query):
    """
    Met à jour les documents correspondant à un filtre dans MongoDB.

    Cette fonction applique une mise à jour aux documents qui correspondent à un filtre
    spécifique. Elle retourne le nombre de documents modifiés.

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
        # Appliquer la mise à jour aux documents correspondants
        result = collection.update_many(filter_query, update_query)
        logger.info(f"{result.modified_count} documents mis à jour avec succès.")

        # Afficher les documents mis à jour pour confirmation
        updated_docs = collection.find(filter_query)
        for doc in updated_docs:
            print(doc)

        return result.modified_count
    except Exception as e:
        # Gérer les erreurs potentielles
        logger.error(f"Erreur lors de la mise à jour : {e}")
        raise

# === Fonction de suppression de documents dans MongoDB ===
def delete_records(collection, filter_query):
    """
    Supprime les documents correspondant à un filtre dans MongoDB.

    Cette fonction supprime tous les documents qui correspondent au filtre fourni et
    retourne le nombre de documents supprimés.

    Args:
        collection (Collection): Collection cible dans MongoDB.
        filter_query (dict): Filtre pour sélectionner les documents à supprimer.

    Returns:
        int: Nombre de documents supprimés.

    Raises:
        Exception: En cas d'erreur lors de la suppression.
    """
    try:
        # Supprimer les documents qui correspondent au filtre
        result = collection.delete_many(filter_query)
        logger.info(f"{result.deleted_count} documents supprimés de la collection MongoDB.")

        return result.deleted_count
    except Exception as e:
        # Gérer les erreurs potentielles
        logger.error(f"Erreur lors de la suppression : {e}")
        raise

# === Fonction d'exportation de documents vers un fichier CSV ===
def export_to_csv(collection, file_name):
    """
    Exporte les documents d'une collection MongoDB vers un fichier CSV.

    Cette fonction lit tous les documents d'une collection MongoDB, les transforme
    en un DataFrame Pandas, puis les exporte dans un fichier CSV.

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
            # Créer le répertoire si inexistant
            os.makedirs(output_dir)
            logger.info(f"Répertoire créé : {output_dir}")

        # Construire le chemin complet du fichier CSV
        output_file = os.path.join(output_dir, f"{file_name}.csv")

        # Récupérer tous les documents de la collection MongoDB
        records = list(collection.find())
        if not records:
            # Avertir si la collection est vide
            logger.warning("Aucun document à exporter. La collection est vide.")
            return 0

        # Convertir les documents en DataFrame Pandas
        df = pd.DataFrame(records)
        if "_id" in df.columns:
            # Supprimer la colonne MongoDB _id pour l'exportation
            df.drop(columns=["_id"], inplace=True)

        # Exporter les données en fichier CSV
        df.to_csv(output_file, index=False)
        logger.info(f"Données exportées avec succès dans le fichier : {output_file}")

        return len(df)
    except Exception as e:
        # Gérer les erreurs potentielles
        logger.error(f"Erreur lors de l'exportation : {e}")
        raise
