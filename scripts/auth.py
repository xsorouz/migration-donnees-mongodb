from utils import hash_password  # Importer la fonction pour hacher un mot de passe
from loguru import logger  # Bibliothèque pour enregistrer des messages dans les logs

def authenticate_user(username, password, db):
    """
    Authentifie un utilisateur en fonction de son nom d'utilisateur et de son mot de passe.

    Étapes principales :
    1. Hachage du mot de passe entré par l'utilisateur.
    2. Recherche d'un utilisateur correspondant dans la collection 'users' de la base de données MongoDB.
    3. Retourne les informations de l'utilisateur si elles sont valides, sinon enregistre une erreur et retourne None.

    Args:
        username (str): Nom d'utilisateur fourni.
        password (str): Mot de passe fourni (non haché).
        db (Database): Instance de la base de données MongoDB où se trouve la collection 'users'.

    Returns:
        dict: Informations sur l'utilisateur si l'authentification réussit, sinon None.
    """

    # Étape 1 : Hacher le mot de passe pour le comparer à celui stocké dans la base de données
    hashed_password = hash_password(password)

    # Étape 2 : Rechercher dans la base de données un utilisateur correspondant au nom d'utilisateur et au mot de passe haché
    user = db["users"].find_one({"username": username, "password": hashed_password})

    if user:  # Si un utilisateur correspondant est trouvé
        logger.success(f"Authentification réussie pour l'utilisateur '{username}'.")
        return user  # Retourne les informations de l'utilisateur
    else:  # Si aucun utilisateur ne correspond
        logger.error("Échec de l'authentification. Identifiant ou mot de passe incorrect.")
        return None  # Retourne None pour indiquer que l'authentification a échoué
