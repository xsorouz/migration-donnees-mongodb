# Importation des bibliothèques nécessaires
from pymongo import MongoClient  # Pour interagir avec MongoDB
from loguru import logger  # Pour gérer les logs (informations, erreurs, etc.)
from setup_users import configure_users  # Importe la fonction de configuration des utilisateurs MongoDB
from hashlib import sha256  # Pour générer des mots de passe hachés

# Fonction pour hacher un mot de passe
def hash_password(password):
    """
    Génère un hash sécurisé pour un mot de passe donné.

    Args:
        password (str): Le mot de passe à hacher.

    Returns:
        str: Le mot de passe haché.
    """
    return sha256(password.encode()).hexdigest()

# Fonction pour initialiser la collection "users" dans MongoDB
def initialize_user_collection():
    """
    Initialise une collection MongoDB appelée "users" avec des utilisateurs et leurs rôles associés.
    Cette collection est utilisée pour authentifier les utilisateurs dans l'application.
    """
    try:
        # Connexion à MongoDB avec les identifiants de l'utilisateur administrateur
        client = MongoClient("mongodb://admin_user:secure_password@mongodb_service_container:27017/")
        db = client["healthcare_database"]  # Accès à la base de données "healthcare_database"
        user_collection = db["users"]  # Collection "users" pour stocker les informations utilisateur


        logger.info("Initialisation de la collection 'users'...")

        # Définir les utilisateurs à ajouter avec leurs rôles
        users = [
            {"username": "admin", "password": hash_password("admin_pass"), "role": "admin_user"},
            {"username": "reader", "password": hash_password("reader_pass"), "role": "reader_user"},
            {"username": "editor", "password": hash_password("editor_pass"), "role": "editor_user"},
        ]

        # Ajouter ou mettre à jour les utilisateurs dans la collection
        for user in users:
            user_collection.update_one(
                {"username": user["username"]},  # Filtre pour rechercher l'utilisateur
                {"$set": user},  # Met à jour ou insère les informations utilisateur
                upsert=True  # Insère un nouveau document si aucun utilisateur correspondant n'est trouvé
            )

        logger.success("Collection 'users' initialisée avec succès.")

    except Exception as e:
        logger.error(f"Erreur lors de l'initialisation des utilisateurs : {e}")
        raise

# Bloc principal pour exécuter le script
if __name__ == "__main__":
    logger.info("Démarrage de l'initialisation des utilisateurs...")
    try:
        # Étape 1 : Configurer les utilisateurs MongoDB via setup_users.py
        configure_users()  # Configure les utilisateurs MongoDB natifs avec leurs rôles

        # Étape 2 : Initialiser la collection "users" avec des informations utilisateur
        initialize_user_collection()

    except Exception as e:
        logger.error(f"Le script a échoué : {e}")
