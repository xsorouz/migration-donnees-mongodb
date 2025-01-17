import pandas as pd  # Pour afficher les résultats sous forme de tableau
from crud import insert_records, read_records, update_records, delete_records, export_to_csv  # Fonctions CRUD
from loguru import logger  # Gestion des logs

def display_menu(role):
    """
    Affiche le menu en fonction du rôle de l'utilisateur.

    Args:
        role (str): Rôle de l'utilisateur ('admin_user', 'editor_user', etc.).
    """
    print("\n=== Menu CRUD ===")
    print("1. Afficher des documents (READ)")
    if role in ["admin_user", "editor_user"]:
        print("2. Insérer un document (CREATE)")
        print("3. Mettre à jour un document (UPDATE)")
    if role == "admin_user":
        print("4. Supprimer un document (DELETE)")
    print("5. Exporter les données dans un fichier CSV")
    print("6. Quitter")


def handle_read(collection):
    """
    Gestion de l'opération READ (lecture de documents).
    """
    try:
        print("\n=== READ : Lecture des documents ===")
        # Option de filtrage personnalisé
        filter_query = input("Entrez un filtre JSON (laisser vide pour aucun filtre) : ").strip()
        filter_query = eval(filter_query) if filter_query else {}
        limit = int(input("Entrez une limite de documents (par défaut : 10) : ") or 10)

        # Lecture des documents
        docs = read_records(collection, filter_query, limit)
        if docs:
            df = pd.DataFrame(docs)
            print(df)  # Affichage tabulaire
        else:
            print("Aucun document trouvé.")
    except Exception as e:
        logger.error(f"Erreur lors de la lecture des documents : {e}")


def handle_create(collection):
    """
    Gestion de l'opération CREATE (insertion de documents).
    """
    try:
        print("\n=== CREATE : Insertion de documents ===")
        # Saisie des données
        name = input("Entrez le nom : ").strip()
        age = int(input("Entrez l'âge : ").strip())
        gender = input("Entrez le genre (Male/Female) : ").strip()
        blood_type = input("Entrez le groupe sanguin : ").strip()

        # Insertion du document
        record = {
            "name": name,
            "age": age,
            "gender": gender,
            "blood_type": blood_type,
        }
        inserted_count = insert_records(collection, [record])
        print(f"{inserted_count} document(s) inséré(s) avec succès.")
    except Exception as e:
        logger.error(f"Erreur lors de l'insertion : {e}")


def handle_update(collection):
    """
    Gestion de l'opération UPDATE (mise à jour de documents).
    """
    try:
        print("\n=== UPDATE : Mise à jour de documents ===")
        # Filtre et mise à jour
        filter_query = eval(input("Entrez le filtre pour les documents à mettre à jour (ex: {\"name\": \"John\"}) : "))
        update_query = eval(input("Entrez la mise à jour à appliquer (ex: {\"$set\": {\"age\": 40}}) : "))

        # Mise à jour
        updated_count = update_records(collection, filter_query, update_query)
        print(f"{updated_count} document(s) mis à jour.")
    except Exception as e:
        logger.error(f"Erreur lors de la mise à jour : {e}")


def handle_delete(collection):
    """
    Gestion de l'opération DELETE (suppression de documents).
    """
    try:
        print("\n=== DELETE : Suppression de documents ===")
        # Filtre pour la suppression
        filter_query = eval(input("Entrez le filtre pour les documents à supprimer (ex: {\"name\": \"John\"}) : "))

        # Suppression
        deleted_count = delete_records(collection, filter_query)
        print(f"{deleted_count} document(s) supprimé(s).")
    except Exception as e:
        logger.error(f"Erreur lors de la suppression : {e}")


def handle_export(collection):
    """
    Gestion de l'opération EXPORT (exportation vers CSV).
    """
    try:
        print("\n=== EXPORT : Exportation des documents ===")
        file_name = input("Entrez le nom du fichier CSV (sans extension) : ").strip()
        exported_count = export_to_csv(collection, file_name)
        if exported_count > 0:
            print(f"{exported_count} document(s) exporté(s) dans 'outputs/{file_name}.csv'.")
        else:
            print("Aucun document n'a été exporté.")
    except Exception as e:
        logger.error(f"Erreur lors de l'exportation : {e}")


def interactive_menu(role, collection):
    """
    Lance le menu interactif en fonction du rôle et de la collection MongoDB.

    Args:
        role (str): Rôle de l'utilisateur.
        collection (Collection): Collection MongoDB cible.
    """
    while True:
        display_menu(role)
        choice = input("Votre choix : ").strip()
        if choice == "1":
            handle_read(collection)
        elif choice == "2" and role in ["admin_user", "editor_user"]:
            handle_create(collection)
        elif choice == "3" and role in ["admin_user", "editor_user"]:
            handle_update(collection)
        elif choice == "4" and role == "admin_user":
            handle_delete(collection)
        elif choice == "5":
            handle_export(collection)
        elif choice == "6":
            print("Fermeture de l'interface interactive.")
            break
        else:
            print("Option invalide ou accès refusé.")
