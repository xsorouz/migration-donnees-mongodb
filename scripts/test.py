from pymongo import MongoClient  # Permet d'interagir avec MongoDB
from crud import insert_records, read_records, update_records, delete_records, export_to_csv  # Fonctions CRUD
from loguru import logger  # Gestion avancée des logs
import os  # Module pour gérer les interactions avec le système de fichiers
import uuid  # Génération d'identifiants uniques

# === Configuration des logs ===
# Définition d'un fichier de log pour enregistrer les événements et erreurs
LOG_FILE = "logs/test.log"
logger.add(LOG_FILE, level="INFO", rotation="1 MB", compression="zip")

def get_mongodb_client():
    """
    Configure une base MongoDB temporaire pour les tests.
    Nettoie les données après utilisation.

    Returns:
        Tuple[Collection, Callable]: 
            - Une collection MongoDB vide prête pour les tests.
            - Une fonction de nettoyage à appeler après le test.
    """
    # Création d'un nom unique pour la base de données temporaire
    # Utilisation de `uuid.uuid4()` pour éviter les conflits entre les tests simultanés
    unique_db_name = f"test_healthcare_database_{uuid.uuid4()}"
    
    # Connexion au serveur MongoDB spécifié (dans ce cas, un conteneur Docker MongoDB)
    client = MongoClient("mongodb://mongodb_service_container:27017/")
    
    # Création de la base de données temporaire avec le nom unique
    db = client[unique_db_name]
    
    # Création d'une collection temporaire pour les tests
    collection = db["test_patients_data"]

    def cleanup():
        """
        Fonction interne pour effectuer un nettoyage une fois les tests terminés.
        Supprime la base de données temporaire et ferme la connexion au serveur MongoDB.
        """
        # Suppression de la base de données temporaire pour libérer de l'espace
        client.drop_database(unique_db_name)
        
        # Fermeture de la connexion pour éviter les fuites de ressources
        client.close()

    # Retourne la collection temporaire et la fonction de nettoyage
    return collection, cleanup


def test_insert_records(collection):
    """
    Teste l'insertion de documents dans MongoDB.
    Vérifie que tous les documents sont correctement insérés.
    """
    # Obtention de la collection MongoDB temporaire et de la fonction de nettoyage
    collection, cleanup = get_mongodb_client()
    
    try:
        # Nettoyage explicite de la collection avant le test
        collection.delete_many({"_id": {"$regex": "^test"}})
        assert collection.count_documents({}) == 0, "La collection n'est pas vide avant le test."

        # Données à insérer, avec des identifiants uniques pour éviter les conflits
        test_data = [
            {"_id": "test1_id_1", "name": "Alice In Wonderland", "age": 40, "gender": "Female"},
            {"_id": "test1_id_2", "name": "John Garry Smith", "age": 30, "gender": "Male"},
            {"_id": "test1_id_3", "name": "Partial User Test", "age": 25},
            {"_id": "test1_id_4", "name": "Complex Case", "age": 50, "gender": "Non-Binary"},
        ]

        # Appel de la fonction d'insertion
        inserted_count = insert_records(collection, test_data)

        # Vérification que tous les documents ont été insérés
        assert inserted_count == len(test_data), "Erreur : Les documents n'ont pas tous été insérés."

        # Log des données insérées
        logger.info(f"Documents insérés : {list(collection.find({}))}")
    
    finally:
        # Nettoyage explicite après le test
        cleanup()

def test_read_records(collection):
    """
    Teste la lecture de documents depuis MongoDB.
    Vérifie que les filtres simples et complexes fonctionnent correctement.
    """
    # Obtention de la collection MongoDB temporaire et de la fonction de nettoyage
    collection, cleanup = get_mongodb_client()
    
    try:
        # Nettoyage explicite de la collection avant le test
        collection.delete_many({"_id": {"$regex": "^test"}})
        assert collection.count_documents({}) == 0, "La collection n'est pas vide avant le test."

        logger.info("=== Test : Lecture de documents ===")
        # Données d'exemple pour la collection
        collection.insert_many([
            {"_id": "test2_id_1", "name": "Alice In Wonderland", "age": 40, "gender": "Female"},
            {"_id": "test2_id_2", "name": "John Garry Smith", "age": 30, "gender": "Male"},
        ])
        # Lecture d'un document spécifique
        results = read_records(collection, {"_id": "test2_id_1"})
        # Vérification qu'un seul document est retourné
        assert len(results) == 1, "Erreur : Lecture incorrecte pour un document spécifique."
    
    finally:
        # Nettoyage explicite après le test
        cleanup()


def test_update_records(collection):
    """
    Teste la mise à jour de documents dans MongoDB.
    Vérifie que les modifications sont correctement appliquées.
    """
    # Obtention de la collection MongoDB temporaire et de la fonction de nettoyage
    collection, cleanup = get_mongodb_client()
    
    try:
        # Nettoyage explicite de la collection avant le test
        collection.delete_many({"_id": {"$regex": "^test"}})
        assert collection.count_documents({}) == 0, "La collection n'est pas vide avant le test."

        logger.info("=== Test : Mise à jour de documents ===")
        # Données d'exemple pour la collection
        collection.insert_many([
            {"_id": "test3_id_1", "name": "Alice In Wonderland", "age": 40},
        ])
        # Mise à jour d'un document spécifique
        updated_count = update_records(collection, {"_id": "test3_id_1"}, {"$set": {"age": 41}})
        # Vérification que le document a été mis à jour
        assert updated_count == 1, "Erreur : Mise à jour incorrecte pour un document spécifique."
    
    finally:
        # Nettoyage explicite après le test
        cleanup()


def test_delete_records(collection):
    """
    Teste la suppression de documents dans MongoDB.
    Vérifie que les documents sont bien supprimés.
    """
    # Obtention de la collection MongoDB temporaire et de la fonction de nettoyage
    collection, cleanup = get_mongodb_client()
    
    try:
        # Nettoyage explicite de la collection avant le test
        collection.delete_many({"_id": {"$regex": "^test"}})
        assert collection.count_documents({}) == 0, "La collection n'est pas vide avant le test."

        logger.info("=== Test : Suppression de documents ===")
        # Données d'exemple pour la collection
        collection.insert_many([
            {"_id": "test4_id_1", "name": "Alice In Wonderland", "age": 40},
        ])
        # Suppression d'un document spécifique
        deleted_count = delete_records(collection, {"_id": "test4_id_1"})
        # Vérification que le document a été supprimé
        assert deleted_count == 1, "Erreur : Suppression incorrecte pour un document spécifique."

        # Vérification supplémentaire que la collection est vide après la suppression
        remaining_count = collection.count_documents({})
        assert remaining_count == 0, f"Erreur : {remaining_count} documents restants après la suppression."

    finally:
        # Nettoyage explicite après le test
        cleanup()


def test_export_to_csv(collection):
    """
    Teste l'exportation des documents MongoDB vers un fichier CSV.
    Vérifie que le fichier est créé et contient les données exportées.
    """
    # Obtention de la collection MongoDB temporaire et de la fonction de nettoyage
    collection, cleanup = get_mongodb_client()

    try:
        # Nettoyage explicite de la collection avant le test
        collection.delete_many({"_id": {"$regex": "^test"}})
        assert collection.count_documents({}) == 0, "La collection n'est pas vide avant le test."

        logger.info(f"=== Début du test : {test_export_to_csv.__name__} ===")
        
        # Données d'exemple pour la collection
        collection.insert_many([
            {"_id": "test5_id_1", "name": "Alice In Wonderland", "age": 40},
        ])

        # Définir le nom du fichier sans chemin ni extension
        file_name = "test_export"

        try:
            # Appel de la fonction d'exportation, en respectant son contrat
            exported_count = export_to_csv(collection, file_name)

            # Vérification du nombre de documents exportés
            assert exported_count > 0, "Erreur : Aucun document exporté."

            # Construire le chemin complet pour vérifier le fichier
            output_file = os.path.join("outputs", f"{file_name}.csv")

            # Vérification que le fichier CSV a été créé
            assert os.path.exists(output_file), f"Erreur : Le fichier {output_file} n'a pas été créé."

            # Chargement et vérification du contenu du fichier CSV
            with open(output_file, "r", encoding="utf-8") as csv_file:
                content = csv_file.readlines()
                assert len(content) > 1, "Erreur : Le fichier CSV est vide ou mal généré."

                logger.info(f"Contenu du fichier CSV :\n{''.join(content[:5])}")  # Affichage des premières lignes

        except Exception as e:
            logger.error(f"Erreur lors de l'exportation des données : {e}")
            raise

    finally:
        # Nettoyage explicite après le test
        cleanup()

    logger.info(f"=== Fin du test : {test_export_to_csv.__name__} ===")


