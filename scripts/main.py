# Importation des bibliothèques et modules nécessaires
from utils import connect_to_mongodb, load_data, create_indexes  # Fonctions utilitaires pour MongoDB et chargement de données
from auth import authenticate_user  # Fonction pour authentifier un utilisateur
from crud import insert_records, read_records, update_records, delete_records, export_to_csv  # Opérations CRUD
from interactive_cli import interactive_menu  # Importation du menu interactif
from test import ( 
    DEFAULT_COLLECTION_NAME,
    connect_to_collection,
    create_test_collection,
    clean_collection,
    remove_export_file,
    extract_initial_data,
    insert_new_data,
    read_all_data,
    update_data,
    delete_specific_data,
    export_final_data,
)  # Importation des tests CRUD
from argparse import ArgumentParser  # Analyse des arguments en ligne de commande
from getpass import getpass  # Saisie sécurisée des mots de passe
from loguru import logger  # Gestion avancée des logs
import os  # Manipulation des chemins et variables d'environnement
import sys  # Interactions système

# Configuration de Loguru pour éviter les doublons
if not logger._core.handlers:
    logger.add(sys.stdout, level="INFO")

# === Configuration des logs ===
LOG_FILE = "logs/main.log"  # Chemin du fichier de log
logger.add(LOG_FILE, level="INFO", rotation="1 MB", compression="zip")

# === Bloc principal ===
if __name__ == "__main__":
    try:
        # === Étape 1 : Analyse des arguments en ligne de commande ===
        parser = ArgumentParser(description="Interface CLI CRUD pour MongoDB")
        parser.add_argument("file_path", help="Chemin complet du fichier CSV contenant les données à charger.")
        args = parser.parse_args()  # Analyse les arguments fournis en ligne de commande

        if not os.path.exists(args.file_path):
            logger.error(f"Fichier introuvable : {args.file_path}")
            exit(1)
        
        # === Étape 2 : Connexion à MongoDB ===
        logger.info("Connexion à MongoDB en cours...")
        db = connect_to_mongodb("mongodb://mongodb_service_container:27017/")

        # === Étape 3 : Authentification de l'utilisateur ===
        logger.info("=== Authentification requise ===")
        username = input("Entrez votre nom d'utilisateur : ").strip()  # Demande le nom d'utilisateur
        password = getpass("Entrez votre mot de passe : ").strip()  # Demande le mot de passe en mode sécurisé
        user = authenticate_user(username, password, db)

        if not user:
            logger.error("Authentification échouée. Fin du script.")
            exit(1)

        # === Étape 4 : Identification du rôle de l'utilisateur ===
        role = user["role"]
        logger.info(f"Authentification réussie. Rôle détecté : {role}")

        # === Étape 5 : Chargement des données depuis le fichier CSV ===
        logger.info(f"Tentative de chargement des données depuis : {args.file_path}")
        records = load_data(args.file_path)

        # === Étape 6 : Accès à la collection MongoDB ===
        collection = db["patients_data"]

        # Nettoyage explicite de la collection principale
        logger.info("Nettoyage de la collection principale avant les tests...")
        collection.delete_many({})
        assert collection.count_documents({}) == 0, "La collection principale n'est pas vide après le nettoyage."

        # === Étape 7 : Vérification et insertion des données ===
        if collection.count_documents({}) > 0:  # Si la collection contient déjà des données
            logger.info("Collection déjà remplie. Aucune nouvelle insertion.")
        else:
            logger.info("La collection est vide. Insertion des données...")
            inserted_count = insert_records(collection, records)
            logger.info(f"{inserted_count} documents insérés depuis le fichier {args.file_path}.")

        # === Étape 8 : Création des index dans MongoDB ===
        logger.info("Création des index pour optimiser les requêtes.")
        create_indexes(collection)

        # === Étape 9 : Préparation de l'environnement pour les tests ===
        logger.info("=== Préparation de l'environnement pour les tests ===")
 
        # Utiliser `connect_to_collection` pour obtenir la collection principale
        collection = connect_to_collection(DEFAULT_COLLECTION_NAME)

        # Nom de la collection temporaire pour les tests
        test_collection_name = f"{DEFAULT_COLLECTION_NAME}_test"

        # Copier les données de la collection principale vers la collection de test
        logger.info(f"Création d'une collection temporaire pour les tests : {test_collection_name}")

        # Créer une collection de test à partir de la collection principale
        test_collection = create_test_collection(db, DEFAULT_COLLECTION_NAME, test_collection_name)


        # Nettoyer la collection de test pour garantir un état initial propre
        logger.info("Nettoyage de la collection de test MongoDB...")
        clean_collection(test_collection)  # Supprime tous les documents de la collection de test

        # Supprimer le fichier exporté existant s'il y en a un
        logger.info("Suppression du fichier exporté existant...")
        remove_export_file("test_export")  # Supprime le fichier CSV précédent pour éviter les conflits

        # === Étape 10 : Exécution des tests unitaires ===
        logger.info("=== Début des tests ===")

        # Initialisation des compteurs pour suivre les résultats des tests
        test_results = {"success": 0, "failure": 0}  # Dictionnaire pour stocker le nombre de tests réussis et échoués

        # Liste des fonctions de test avec leurs descriptions
        test_functions = [
            ("Extraction initiale des données", extract_initial_data),  # Test pour extraire les premières données
            ("Insertion de documents", insert_new_data),                # Test pour insérer 10 documents
            ("Lecture de toutes les données", read_all_data),           # Test pour lire toutes les données
            ("Mise à jour de documents", update_data),                  # Test pour appliquer des mises à jour
            ("Suppression de documents spécifiques", delete_specific_data),  # Test pour supprimer des documents
            ("Exportation des données", export_final_data),             # Test pour exporter les données vers un CSV
        ]

        # Parcourir et exécuter chaque test défini
        for test_name, test_function in test_functions:
            try:
                # Log indiquant le début de l'exécution du test
                logger.info(f"Exécution du test : {test_name}")
                
                # Appeler la fonction de test en passant la collection de test MongoDB
                test_function(test_collection)
                
                # Loguer le succès du test et incrémenter le compteur correspondant
                logger.success(f"Test réussi : {test_name}")
                test_results["success"] += 1
            except AssertionError as e:
                # Loguer les échecs dus à une assertion avec des détails précis
                logger.error(f"Échec du test : {test_name}. Détails : {e}")
                test_results["failure"] += 1
            except Exception as e:
                # Loguer toute autre exception inattendue
                logger.error(f"Erreur inattendue lors du test : {test_name}. Détails : {e}")
                test_results["failure"] += 1

        # Résumé final des résultats des tests
        logger.info("=== Résumé des tests ===")
        logger.info(f"Tests réussis : {test_results['success']}")  # Nombre total de tests réussis
        logger.info(f"Tests échoués : {test_results['failure']}")  # Nombre total de tests échoués

        # === Étape 11 : Lancer l'interface utilisateur CLI ===
        if test_results["failure"] == 0:
            logger.info("Tous les tests ont été validés. Lancement de l'interface CLI.")
            interactive_menu(role, collection)
        else:
            logger.warning("Certains tests ont échoué. Vérifiez les logs avant de continuer.")

    except Exception as e:
        logger.error(f"Erreur lors de l'exécution du script : {e}")
