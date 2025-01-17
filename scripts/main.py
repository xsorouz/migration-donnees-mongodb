# Importation des bibliothèques et modules nécessaires
from utils import connect_to_mongodb, load_data, create_indexes  # Fonctions utilitaires pour MongoDB et chargement de données
from auth import authenticate_user  # Fonction pour authentifier un utilisateur
from crud import insert_records, read_records, update_records, delete_records, export_to_csv  # Opérations CRUD
from interactive_cli import interactive_menu  # Importation du menu interactif
from test import (
    test_insert_records,
    test_read_records,
    test_update_records,
    test_delete_records,
    test_export_to_csv,
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

        # === Étape 7 : Vérification et insertion des données ===
        if not collection.count_documents({}):  # Si la collection est vide
            logger.info("La collection est vide. Insertion des données...")
            inserted_count = insert_records(collection, records)
            logger.info(f"{inserted_count} documents insérés depuis le fichier {args.file_path}.")
        else:
            logger.info("La collection contient déjà des données. Aucune insertion nécessaire.")

        # === Étape 8 : Création des index dans MongoDB ===
        logger.info("Création des index pour optimiser les requêtes.")
        create_indexes(collection)

# === Étape 9 : Exécution des tests unitaires ===
        logger.info("=== Début des tests CRUD ===")
        test_results = {"success": 0, "failure": 0}  # Initialisation des compteurs de tests
        test_functions = [
            ("Insertion de documents", test_insert_records),
            ("Lecture de documents", test_read_records),
            ("Mise à jour de documents", test_update_records),
            ("Suppression de documents", test_delete_records),
            ("Exportation de documents", test_export_to_csv),
        ]

        for test_name, test_function in test_functions:
            try:
                logger.info(f"Exécution du test : {test_name}")
                test_function(collection)
                logger.success(f"Test réussi : {test_name}")
                test_results["success"] += 1
            except AssertionError as e:
                logger.error(f"Échec du test : {test_name}. Détails : {e}")
                test_results["failure"] += 1

        logger.info("=== Résumé des tests CRUD ===")
        logger.info(f"Tests réussis : {test_results['success']}")
        logger.info(f"Tests échoués : {test_results['failure']}")

        # === Étape 10 : Lancer l'interface utilisateur CLI ===
        if test_results["failure"] == 0:
            logger.info("Tous les tests ont été validés. Lancement de l'interface CLI.")
            interactive_menu(role, collection)
        else:
            logger.warning("Certains tests ont échoué. Vérifiez les logs avant de continuer.")

    except Exception as e:
        logger.error(f"Erreur lors de l'exécution du script : {e}")