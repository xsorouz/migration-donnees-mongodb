# Importation des bibliothèques et modules nécessaires
from utils import connect_to_mongodb, load_data  # Fonctions utilitaires pour MongoDB et chargement de données
from auth import authenticate_user  # Fonction pour authentifier un utilisateur
from crud import insert_records, read_records, update_records, delete_records, export_to_csv  # Opérations CRUD
from argparse import ArgumentParser  # Analyse des arguments en ligne de commande
from getpass import getpass  # Saisie sécurisée des mots de passe
from loguru import logger  # Gestion avancée des logs

# === Bloc principal ===
if __name__ == "__main__":
    try:
        # Étape 1 : Analyse des arguments en ligne de commande
        # Permet à l'utilisateur de spécifier un fichier CSV à charger lors de l'exécution du script.
        parser = ArgumentParser(description="Interface CLI CRUD pour MongoDB")
        parser.add_argument("file_path", help="Chemin complet du fichier CSV contenant les données à charger.")
        args = parser.parse_args()  # Analyse les arguments fournis en ligne de commande

        # Étape 2 : Connexion à MongoDB
        # Utilise la fonction connect_to_mongodb depuis le module utils.
        db = connect_to_mongodb("mongodb://mongodb_service_container:27017/")

        # Étape 3 : Authentification de l'utilisateur
        logger.info("=== Authentification requise ===")
        username = input("Entrez votre nom d'utilisateur : ").strip()  # Demande le nom d'utilisateur
        password = getpass("Entrez votre mot de passe : ").strip()  # Demande le mot de passe en mode sécurisé
        user = authenticate_user(username, password, db)  # Appelle la fonction d'authentification

        # Si l'authentification échoue, le script s'arrête.
        if not user:
            logger.error("Authentification échouée. Fin du script.")
            exit(1)

        # Étape 4 : Identification du rôle
        # Le rôle de l'utilisateur détermine les actions disponibles dans l'interface CLI.
        role = user["role"]
        logger.info(f"Authentification réussie. Rôle détecté : {role}")

        # Étape 5 : Chargement des données depuis le fichier CSV
        # Utilise la fonction load_data pour transformer le fichier CSV en une liste de dictionnaires.
        logger.info(f"Tentative de chargement des données depuis : {args.file_path}")
        records = load_data(args.file_path)

        # Étape 6 : Accès à la collection MongoDB
        # Permet d'insérer ou manipuler des données dans la collection principale.
        collection = db["patients_data"]

        # Aperçu initial de la base pour tous les utilisateurs
        logger.info("=== Aperçu initial de la base de données ===")
        initial_docs = read_records(collection, {}, limit=5)
        if initial_docs:
            logger.info("Documents initiaux dans la base :")
            for doc in initial_docs:
                print(doc)
        else:
            logger.warning("La base est vide avant insertion des données.")


        # Étape 7 : Insertion initiale des données
        # Insère les données chargées dans la collection MongoDB.
        inserted_count = insert_records(collection, records)
        logger.info(f"{inserted_count} documents insérés depuis le fichier {args.file_path}.")

        # Étape 8 : Interface utilisateur CLI
        # Propose un menu interactif pour effectuer des opérations CRUD.
        while True:
            print("\n=== Menu CRUD ===")
            print("1. Afficher des documents (READ)")
            if role in ["admin_user", "editor_user"]:  # Vérifie les permissions pour les opérations CREATE et UPDATE
                print("2. Insérer un document (CREATE)")
                print("3. Mettre à jour un document (UPDATE)")
            if role == "admin_user":  # Seul l'administrateur peut effectuer des suppressions
                print("4. Supprimer un document (DELETE)")
            print("5. Exporter les données dans un fichier CSV")
            print("6. Quitter")

            # Lecture du choix utilisateur
            choice = input("Votre choix : ").strip()

            # Option 1 : Lecture de documents (READ)
            if choice == "1":
                logger.info("=== READ : Lecture des documents ===")
                docs = read_records(collection, {}, limit=10)
                if docs:
                    logger.info("Documents lus avec succès :")
                    for doc in docs:
                        print(doc)
                else:
                    logger.warning("Aucun document trouvé.")

            # Option 2 : Insertion de documents (CREATE)
            elif choice == "2" and role in ["admin_user", "editor_user"]:
                logger.info("=== CREATE : Insertion de documents ===")
                try:
                    name = input("Entrez le nom : ").strip()
                    age = int(input("Entrez l'âge : ").strip())
                    insert_records(collection, [{"Name": name, "Age": age}])
                except ValueError:
                    logger.error("Erreur : L'âge doit être un nombre entier.")

            # Option 3 : Mise à jour de documents (UPDATE)
            elif choice == "3" and role in ["admin_user", "editor_user"]:
                logger.info("=== UPDATE : Mise à jour de documents ===")
                try:
                    name = input("Entrez le nom du document à mettre à jour : ").strip()
                    new_age = int(input("Entrez le nouvel âge : ").strip())
                    update_records(collection, {"Name": name}, {"$set": {"Age": new_age}})
                except ValueError:
                    logger.error("Erreur : L'âge doit être un nombre entier.")

            # Option 4 : Suppression de documents (DELETE)
            elif choice == "4" and role == "admin_user":
                logger.info("=== DELETE : Suppression de documents ===")
                name = input("Entrez le nom du document à supprimer : ").strip()
                delete_records(collection, {"Name": name})

            # Option 5 : Exportation des données dans un fichier CSV
            elif choice == "5":
                logger.info("=== EXPORT : Exporter les données ===")
                file_name = input("Entrez le nom du fichier CSV (sans extension) : ").strip()
                exported_count = export_to_csv(collection, file_name)
                if exported_count > 0:
                    logger.info(f"{exported_count} documents exportés avec succès dans 'outputs/{file_name}.csv'.")
                else:
                    logger.warning("Aucun document n'a été exporté.")

            # Option 6 : Quitter
            elif choice == "6":
                logger.info("Fermeture de l'interface MongoDB CRUD.")
                break

            # Option invalide
            else:
                logger.warning("Option invalide ou accès refusé pour votre rôle.")

    except Exception as e:
        logger.error(f"Erreur lors de l'exécution du script : {e}")
