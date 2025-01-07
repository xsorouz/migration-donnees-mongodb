from pymongo import MongoClient
from loguru import logger


def configure_users():
    try:
        # Connexion initiale sans authentification
        client = MongoClient("mongodb://localhost:27017/")
        admin_db = client.admin

        # Vérifier si admin_user existe déjà
        existing_admin = admin_db.command("usersInfo", "admin_user")
        if existing_admin.get("users"):
            logger.info("L'utilisateur administrateur 'admin_user' existe déjà.")
        else:
            logger.info("Création de l'utilisateur administrateur...")
            admin_db.command(
                "createUser", "admin_user", pwd="secure_password", roles=["root"]
            )

        # Connexion avec l'utilisateur administrateur
        client = MongoClient("mongodb://admin_user:secure_password@localhost:27017/")
        healthcare_db = client["healthcare_database"]

        # Vérifier si reader_user existe déjà
        existing_reader = healthcare_db.command("usersInfo", "reader_user")
        if existing_reader.get("users"):
            logger.info("L'utilisateur 'reader_user' existe déjà.")
        else:
            logger.info("Création de 'reader_user'...")
            healthcare_db.command(
                "createUser",
                "reader_user",
                pwd="reader_password",
                roles=[{"role": "read", "db": "healthcare_database"}],
            )

        # Vérifier si editor_user existe déjà
        existing_editor = healthcare_db.command("usersInfo", "editor_user")
        if existing_editor.get("users"):
            logger.info("L'utilisateur 'editor_user' existe déjà.")
        else:
            logger.info("Création de 'editor_user'...")
            healthcare_db.command(
                "createUser",
                "editor_user",
                pwd="editor_password",
                roles=[{"role": "readWrite", "db": "healthcare_database"}],
            )

        logger.success("Configuration des utilisateurs et des rôles terminée.")
    except Exception as e:
        logger.error(f"Erreur lors de la configuration des utilisateurs : {e}")


if __name__ == "__main__":
    configure_users()
