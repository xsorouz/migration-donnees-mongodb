import os  # Pour gérer les variables d'environnement
from pymongo import MongoClient  # Pour interagir avec MongoDB
from hashlib import sha256  # Pour hacher les mots de passe
from loguru import logger  # Pour gérer les logs
from time import sleep  # Pour insérer des délais
import pandas as pd  # Pour manipuler les données tabulaires
from pymongo import ASCENDING, DESCENDING  # Import des constantes pour les index

# === Fonction de hachage ===

def hash_password(password):
    """
    Hache un mot de passe en utilisant SHA-256.

    Args:
        password (str): Mot de passe en clair.

    Returns:
        str: Mot de passe haché sous forme de chaîne hexadécimale.
    """
    return sha256(password.encode()).hexdigest()

# === Fonction pour attendre MongoDB ===

def wait_for_mongodb(uri, timeout=30):
    """
    Attend que MongoDB soit disponible avant de continuer.

    Args:
        uri (str): URI de connexion à MongoDB.
        timeout (int): Durée maximale pour attendre (en secondes).

    Returns:
        MongoClient: Client MongoDB connecté.

    Raises:
        TimeoutError: Si MongoDB n'est pas disponible dans le temps imparti.
    """
    logger.info(f"Tentative de connexion à MongoDB ({uri}).")
    for attempt in range(timeout):  # Répéter jusqu'à `timeout` tentatives
        try:
            # Crée un client MongoDB avec un délai de connexion court
            client = MongoClient(uri, serverSelectionTimeoutMS=1000)
            client.server_info()  # Vérifie que MongoDB répond
            logger.success("Connexion à MongoDB réussie.")
            return client
        except Exception as e:
            # Enregistre un avertissement et attend avant de réessayer
            logger.warning(f"Tentative {attempt + 1}/{timeout} : MongoDB non prêt. Erreur : {e}")
            sleep(1)
    raise TimeoutError("MongoDB n'a pas répondu à temps.")

# === Fonction pour établir une connexion à MongoDB ===

def connect_to_mongodb(uri, database_name="healthcare_database"):
    """
    Établit une connexion à une base de données MongoDB.

    Args:
        uri (str): URI de connexion à MongoDB.
        database_name (str): Nom de la base de données cible.

    Returns:
        Database: Instance de la base de données MongoDB.

    Raises:
        Exception: En cas de problème de connexion.
    """
    try:
        # Appelle la fonction pour attendre MongoDB
        client = wait_for_mongodb(uri)
        # Accède à la base de données spécifiée
        db = client[database_name]
        logger.info(f"Connexion réussie à la base '{database_name}'.")
        return db
    except Exception as e:
        logger.error(f"Impossible de se connecter à MongoDB : {e}")
        raise

# === Fonction pour charger des données depuis un fichier CSV ===

def load_data(file_path):
    """
    Charge un fichier CSV et retourne les données sous forme de liste de dictionnaires.

    Args:
        file_path (str): Chemin du fichier CSV.

    Returns:
        list: Données formatées pour MongoDB (liste de dictionnaires).

    Raises:
        FileNotFoundError: Si le fichier CSV n'est pas trouvé.
        Exception: Pour toute autre erreur lors du chargement.
    """
    try:
        logger.info(f"Tentative de chargement du fichier CSV : {file_path}")
        # Lit le fichier CSV avec Pandas
        df = pd.read_csv(file_path)
        logger.info(f"Données chargées : {len(df)} lignes, {len(df.columns)} colonnes.")
        # Convertit les données en une liste de dictionnaires pour MongoDB
        return df.to_dict(orient="records")
    except FileNotFoundError:
        logger.error(f"Fichier non trouvé : {file_path}")
        raise
    except Exception as e:
        logger.error(f"Erreur lors du chargement : {e}")
        raise

# === Fonction pour créer les index ===

def create_indexes(collection):
    """
    Ajoute des index à une collection MongoDB pour optimiser les requêtes.

    Args:
        collection (pymongo.collection.Collection): Collection MongoDB.
    """
    try:
        logger.info("Ajout des index dans la collection MongoDB...")
        index_fields = [
            ("age", ASCENDING),  # Index sur 'age' pour les recherches par âge
            ("name", ASCENDING),  # Index sur 'name' pour les recherches par nom
            ("gender", ASCENDING),  # Index sur 'gender' pour filtrer les genres
            ("date_of_admission", DESCENDING),  # Index sur 'date_of_admission' pour les tris décroissants
        ]
        for field, direction in index_fields:
            index_name = collection.create_index([(field, direction)])
            logger.info(f"Index créé : {field} ({direction}). Nom de l'index : {index_name}")

        logger.success("Tous les index ont été créés avec succès.")
    except Exception as e:
        logger.error(f"Erreur lors de la création des index : {e}")
        raise
