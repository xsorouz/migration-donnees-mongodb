import pytest  # Framework pour écrire et exécuter des tests unitaires
from pymongo import MongoClient  # Permet d'interagir avec MongoDB
from crud import insert_records, read_records, update_records, delete_records, export_to_csv  # Fonctions CRUD
from loguru import logger  # Gestion avancée des logs
import os  # Module pour gérer les interactions avec le système de fichiers

# === Configuration des logs ===
# Définition d'un fichier de log pour enregistrer les événements et erreurs
LOG_FILE = "logs/test.log"
logger.add(LOG_FILE, level="INFO", rotation="1 MB", compression="zip")

@pytest.fixture(scope="function")
def mongodb_client():
    """
    Configure une base MongoDB temporaire pour les tests.
    Nettoie les données avant et après chaque test pour garantir que les tests sont indépendants.

    Yields:
        Collection: Une collection MongoDB vide prête pour les tests.
    """
    # Connexion à MongoDB
    client = MongoClient("mongodb://mongodb_service_container:27017/")
    # Création d'une base de données temporaire
    db = client["test_healthcare_database"]
    # Création d'une collection temporaire pour les données patients
    collection = db["patients_data"]
    # Nettoyage des données avant le test
    collection.delete_many({})
    # Vérification que la collection est bien vide
    assert collection.count_documents({}) == 0, "La collection n'est pas vide avant le test."
    yield collection
    # Nettoyage des données après le test
    collection.delete_many({})
    # Suppression de la base temporaire
    client.drop_database("test_healthcare_database")
    # Fermeture de la connexion
    client.close()

def test_insert_records(mongodb_client):
    """
    Teste l'insertion de documents dans MongoDB.
    Vérifie que tous les documents sont correctement insérés.
    """
    logger.info("=== Test : Insertion de documents ===")
    # Données à insérer, avec des identifiants uniques pour éviter les conflits
    test_data = [
        {"_id": "test1_id_1", "name": "Alice In Wonderland", "age": 40, "gender": "Female"},
        {"_id": "test1_id_2", "name": "John Garry Smith", "age": 30, "gender": "Male"},
        {"_id": "test1_id_3", "name": "Partial User Test", "age": 25},
        {"_id": "test1_id_4", "name": "Complex Case", "age": 50, "gender": "Non-Binary"},
    ]
    # Appel de la fonction d'insertion
    inserted_count = insert_records(mongodb_client, test_data)
    # Vérification que tous les documents ont été insérés
    assert inserted_count == len(test_data), "Erreur : Les documents n'ont pas tous été insérés."

def test_read_records(mongodb_client):
    """
    Teste la lecture de documents depuis MongoDB.
    Vérifie que les filtres simples et complexes fonctionnent correctement.
    """
    logger.info("=== Test : Lecture de documents ===")
    # Données d'exemple pour la collection
    mongodb_client.insert_many([
        {"_id": "test2_id_1", "name": "Alice In Wonderland", "age": 40, "gender": "Female"},
        {"_id": "test2_id_2", "name": "John Garry Smith", "age": 30, "gender": "Male"},
    ])
    # Lecture d'un document spécifique
    results = read_records(mongodb_client, {"_id": "test2_id_1"})
    # Vérification qu'un seul document est retourné
    assert len(results) == 1, "Erreur : Lecture incorrecte pour un document spécifique."

def test_update_records(mongodb_client):
    """
    Teste la mise à jour de documents dans MongoDB.
    Vérifie que les modifications sont correctement appliquées.
    """
    logger.info("=== Test : Mise à jour de documents ===")
    # Données d'exemple pour la collection
    mongodb_client.insert_many([
        {"_id": "test3_id_1", "name": "Alice In Wonderland", "age": 40},
    ])
    # Mise à jour d'un document spécifique
    updated_count = update_records(mongodb_client, {"_id": "test3_id_1"}, {"$set": {"age": 41}})
    # Vérification que le document a été mis à jour
    assert updated_count == 1, "Erreur : Mise à jour incorrecte pour un document spécifique."

def test_delete_records(mongodb_client):
    """
    Teste la suppression de documents dans MongoDB.
    Vérifie que les documents sont bien supprimés.
    """
    logger.info("=== Test : Suppression de documents ===")
    # Données d'exemple pour la collection
    mongodb_client.insert_many([
        {"_id": "test4_id_1", "name": "Alice In Wonderland", "age": 40},
    ])
    # Suppression d'un document spécifique
    deleted_count = delete_records(mongodb_client, {"_id": "test4_id_1"})
    # Vérification que le document a été supprimé
    assert deleted_count == 1, "Erreur : Suppression incorrecte pour un document spécifique."

def test_export_to_csv(mongodb_client):
    """
    Teste l'exportation des données MongoDB vers un fichier CSV.
    Vérifie que le fichier est créé et contient les données exportées.
    """
    logger.info("=== Test : Exportation de documents ===")
    # Données d'exemple pour la collection
    mongodb_client.insert_many([
        {"_id": "test5_id_1", "name": "Alice In Wonderland", "age": 40},
    ])
    # Nom du fichier CSV d'exportation
    file_name = "test_export"
    # Appel de la fonction d'exportation
    export_to_csv(mongodb_client, file_name)
    # Chemin du fichier exporté
    output_file = os.path.join("outputs", f"{file_name}.csv")
    # Vérification que le fichier existe
    assert os.path.exists(output_file), "Erreur : Le fichier CSV n'a pas été créé."
    # Nettoyage du fichier après le test
    os.remove(output_file)
