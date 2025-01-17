# Importation des bibliothèques nécessaires
from pymongo import MongoClient  # Pour interagir avec MongoDB
from loguru import logger  # Pour la gestion des logs

def configure_users():
    """
    Configure les utilisateurs MongoDB et leurs rôles.

    Cette fonction effectue les étapes suivantes :
    - Connexion initiale à MongoDB en mode administrateur (sans authentification).
    - Création de l'utilisateur administrateur (admin_user) avec les permissions "root".
    - Création des utilisateurs "reader_user" et "editor_user" avec des rôles spécifiques :
        - reader_user : Permissions de lecture uniquement sur une base spécifique.
        - editor_user : Permissions de lecture et écriture sur une base spécifique.
    - Si les utilisateurs existent déjà, un log d'information est enregistré.

    Raises:
        Exception: En cas d'échec de connexion ou de création d'utilisateur.
    """
    try:
        logger.info("Début de la configuration des utilisateurs MongoDB...")

        # Connexion initiale à MongoDB sans authentification
        client = MongoClient("mongodb://mongodb_service_container:27017/")  # Connexion à MongoDB via le service Docker
        admin_db = client.admin  # Accès à la base de données "admin"

        # Étape 1 : Création de l'utilisateur administrateur
        logger.info("Vérification de l'existence de l'utilisateur 'admin_user'...")
        try:
            existing_admin = admin_db.command("usersInfo", "admin_user")
            if not existing_admin.get("users"):
                admin_db.command(
                    "createUser", "admin_user", pwd="secure_password", roles=["root"]
                )
        except Exception as e:
            logger.error(f"Erreur lors de la création de l'utilisateur admin : {e}")
            raise
        # Étape 2 : Connexion avec les permissions de l'utilisateur administrateur
        logger.info("Connexion avec l'utilisateur 'admin_user' pour configurer les autres utilisateurs...")
        client = MongoClient("mongodb://admin_user:secure_password@mongodb_service_container:27017/")
        healthcare_db = client["healthcare_database"]  # Accès à la base de données cible

        # Étape 3 : Création de l'utilisateur reader_user
        logger.info("Vérification de l'existence de l'utilisateur 'reader_user'...")
        existing_reader = healthcare_db.command("usersInfo", "reader_user")
        if existing_reader.get("users"):
            logger.info("L'utilisateur 'reader_user' existe déjà.")
        else:
            logger.info("Création de l'utilisateur 'reader_user' avec des permissions de lecture...")
            healthcare_db.command(
                "createUser",
                "reader_user",
                pwd="reader_password",
                roles=[{"role": "read", "db": "healthcare_database"}],
            )
            logger.success("Utilisateur 'reader_user' créé avec succès.")

        # Étape 4 : Création de l'utilisateur editor_user
        logger.info("Vérification de l'existence de l'utilisateur 'editor_user'...")
        existing_editor = healthcare_db.command("usersInfo", "editor_user")
        if existing_editor.get("users"):
            logger.info("L'utilisateur 'editor_user' existe déjà.")
        else:
            logger.info("Création de l'utilisateur 'editor_user' avec des permissions de lecture et écriture...")
            healthcare_db.command(
                "createUser",
                "editor_user",
                pwd="editor_password",
                roles=[{"role": "readWrite", "db": "healthcare_database"}],
            )
            logger.success("Utilisateur 'editor_user' créé avec succès.")

        logger.success("Configuration des utilisateurs et des rôles terminée avec succès.")

    except Exception as e:
        logger.error(f"Erreur lors de la configuration des utilisateurs MongoDB : {e}")
        raise


# Bloc principal exécuté lorsque le script est lancé
if __name__ == "__main__":
    logger.info("Démarrage du script de configuration des utilisateurs MongoDB...")
    try:
        configure_users()  # Appel de la fonction principale pour configurer les utilisateurs
    except Exception as e:
        logger.error(f"Le script a échoué : {e}")
