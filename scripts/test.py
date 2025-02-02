from pymongo import MongoClient  # Permet d'interagir avec MongoDB
from crud import insert_records, read_records, update_records, delete_records, export_to_csv  # Fonctions CRUD pour MongoDB
from loguru import logger  # Bibliothèque pour gérer et enregistrer les logs
import os  # Module pour gérer les interactions avec le système de fichiers

# === Configuration des logs ===
# Définition du fichier où les logs seront enregistrés
LOG_FILE = "logs/test.log"
# Configuration des logs avec rotation : limite à 1 Mo par fichier et compression automatique
logger.add(LOG_FILE, level="INFO", rotation="1 MB", compression="zip")

# === Paramètres globaux ===
# URI pour se connecter au service MongoDB (via un conteneur Docker)
MONGO_URI = "mongodb://mongodb_service_container:27017/"
# Nom de la base de données MongoDB
DATABASE_NAME = "healthcare_database"
# Nom de la collection MongoDB contenant les données des patients
DEFAULT_COLLECTION_NAME = "patients_data"# Nom par défaut de la collection principale
 
def connect_to_collection(collection_name=DEFAULT_COLLECTION_NAME):
    """
    Établit une connexion à une collection MongoDB spécifique.

    Cette fonction connecte l'application au serveur MongoDB, accède à la base de données définie 
    dans les paramètres globaux, puis se connecte à une collection spécifique. En cas d'erreur, 
    elle enregistre les détails dans les logs et lève une exception.

    Args:
        collection_name (str): Nom de la collection MongoDB cible. 
                               Par défaut, utilise la valeur définie dans DEFAULT_COLLECTION_NAME.

    Returns:
        pymongo.collection.Collection: Objet représentant la collection MongoDB cible. 
                                       Cet objet peut être utilisé pour effectuer des opérations sur les documents.

    Raises:
        Exception: Si une erreur survient lors de la connexion au serveur MongoDB ou à la collection.
    """
    try:
        # Étape 1 : Création d'un client MongoDB pour interagir avec le serveur
        # `MONGO_URI` est défini globalement pour contenir l'adresse du serveur MongoDB.
        client = MongoClient(MONGO_URI)
        logger.info("Connexion au serveur MongoDB réussie.")

        # Étape 2 : Accès à la base de données définie par `DATABASE_NAME`
        # Cette base de données contient toutes les collections nécessaires à l'application.
        db = client[DATABASE_NAME]
        logger.info(f"Connexion établie avec la base de données : {DATABASE_NAME}")

        # Étape 3 : Accès à la collection cible
        # Le nom de la collection est passé en paramètre. Si non fourni, une valeur par défaut est utilisée.
        collection = db[collection_name]
        logger.info(f"Connexion établie avec la collection : {collection_name}")

        # Étape 4 : Retourner l'objet collection pour permettre des opérations (CRUD)
        return collection

    except Exception as e:
        # Gestion des erreurs : loguer et remonter l'exception en cas de problème
        # Cela inclut des erreurs de connexion réseau, base de données introuvable, etc.
        logger.error(f"Erreur lors de la connexion à MongoDB : {e}")
        raise



def create_test_collection(db, source_collection_name, test_collection_name):
    """
    Crée une collection de test en copiant les documents de la collection principale.

    Cette fonction crée une nouvelle collection MongoDB pour les tests en copiant les données 
    existantes d'une collection principale (source). Si la collection source est vide, 
    elle génère un avertissement dans les logs.

    Args:
        db (pymongo.database.Database): Instance de la base de données MongoDB connectée.
        source_collection_name (str): Nom de la collection MongoDB source (principale).
        test_collection_name (str): Nom de la collection MongoDB temporaire pour les tests.

    Returns:
        pymongo.collection.Collection: Objet représentant la collection MongoDB de test.

    Raises:
        Exception: Si une erreur survient lors de l'accès ou de la copie des collections.
    """
    try:
        # Étape 1 : Accéder aux collections source et cible
        # La collection source contient les données initiales que nous voulons copier.
        source_collection = db[source_collection_name]

        # La collection de test sera créée (ou réinitialisée) à chaque exécution.
        test_collection = db[test_collection_name]

        # Étape 2 : Nettoyer la collection de test
        # Supprime tous les documents existants dans la collection de test pour garantir un état initial propre.
        logger.info(f"Nettoyage de la collection de test : {test_collection_name}")
        test_collection.delete_many({})
        logger.info(f"Collection {test_collection_name} vidée avec succès.")

        # Étape 3 : Copier les documents de la collection source vers la collection de test
        # Récupérer tous les documents de la collection source
        documents = list(source_collection.find())
        if not documents:
            # Si la collection source est vide, loguer un avertissement
            logger.warning(f"La collection source {source_collection_name} est vide. Aucun document copié.")
        else:
            # Insérer les documents dans la collection de test
            test_collection.insert_many(documents)
            logger.info(f"{len(documents)} document(s) copié(s) de {source_collection_name} vers {test_collection_name}.")

        # Étape 4 : Retourner la collection de test pour permettre des opérations ultérieures
        return test_collection

    except Exception as e:
        # Gestion des erreurs : loguer et remonter l'exception pour un traitement ultérieur
        logger.error(f"Erreur lors de la création de la collection de test : {e}")
        raise


def clean_collection(test_collection):
    """
    Supprime tous les documents de la collection MongoDB pour garantir un état propre.

    Étapes principales :
    1. Supprime tous les documents présents dans la collection.
    2. Compte le nombre de documents supprimés et enregistre cette information dans les logs.
    3. Garantit que la collection est vidée avant toute autre opération.

    Args:
        test_collection : Collection MongoDB cible.
    
    Returns:
        None
    """
    # Log indiquant le début de la phase de nettoyage de la collection
    logger.info("=== Nettoyage de la collection MongoDB ===")

    # Supprimer tous les documents dans la collection
    deleted_count = test_collection.delete_many({}).deleted_count  # Renvoie le nombre de documents supprimés

    # Enregistrer dans les logs le nombre de documents effectivement supprimés
    logger.info(f"{deleted_count} document(s) supprimé(s) de la collection.")


def remove_export_file(file_name="test_export"):
    """
    Supprime le fichier exporté précédent s'il existe.

    Cette fonction vérifie si un fichier exporté (CSV) existe dans un répertoire spécifique,
    le supprime s'il est présent, ou logue qu'il n'y a rien à supprimer. Si le répertoire
    n'existe pas, il est créé pour garantir que les futures exportations ne rencontrent pas
    de problème.

    Args:
        file_name (str): Nom du fichier CSV (sans extension). Par défaut, "test_export".

    Returns:
        None
    """
    # Étape 1 : Définir le répertoire de sortie pour les fichiers exportés
    output_dir = "outputs"  # Répertoire où les fichiers exportés seront stockés

    # Étape 2 : Vérifier si le répertoire de sortie existe, sinon le créer
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)  # Crée le répertoire manquant
        logger.info(f"Répertoire créé : {output_dir}")  # Logue la création du répertoire

    # Étape 3 : Construire le chemin complet du fichier exporté
    output_file = os.path.join(output_dir, f"{file_name}.csv")

    # Étape 4 : Vérifier si le fichier exporté existe
    logger.info("=== Vérification du fichier exporté existant ===")
    if os.path.exists(output_file):
        # Si le fichier existe, le supprimer
        os.remove(output_file)
        logger.info(f"Fichier exporté supprimé : {output_file}")
    else:
        # Sinon, loguer qu'aucun fichier n'a été trouvé
        logger.info("Aucun fichier exporté existant à supprimer.")


def extract_initial_data(test_collection):
    """
    Extrait et affiche les 10 premières lignes de la collection MongoDB.

    Cette fonction effectue une requête pour récupérer les 10 premiers documents d'une collection MongoDB,
    les affiche dans les logs et compte le nombre de documents extraits. En cas d'erreur, elle logue
    les détails de l'exception.

    Args:
        test_collection: Collection MongoDB cible.

    Returns:
        None
    """
    # Étape 1 : Loguer le début de l'opération
    logger.info("=== Début de l'extraction des 10 premières lignes de la collection ===")
    
    try:
        # Étape 2 : Lire les 10 premiers documents de la collection
        # Utilise une requête vide `{}` pour sélectionner tous les documents et limite les résultats à 10
        results = read_records(test_collection, query={}, limit=10)

        # Étape 3 : Loguer le nombre de documents extraits
        logger.info(f"Nombre de documents extraits : {len(results)}")

        # Étape 4 : Parcourir et afficher chaque document extrait
        for i, doc in enumerate(results, start=1):
            logger.info(f"Document {i} : {doc}")  # Loguer chaque document pour une meilleure traçabilité

    except Exception as e:
        # Étape 5 : Gestion des erreurs
        # Si une exception survient, loguer l'erreur avec les détails
        logger.error(f"Erreur lors de l'extraction initiale des données : {e}")


def insert_new_data(test_collection):
    """
    Insère 10 nouvelles lignes dans la collection MongoDB.

    Étapes principales :
    1. Définit un ensemble de 10 documents à insérer, respectant la structure de la collection.
    2. Insère les documents dans la collection.
    3. Logue le nombre de documents insérés avec succès.

    Args:
        test_collection : Collection MongoDB cible.
    """
    # Enregistrer dans les logs que l'insertion commence
    logger.info("=== Insertion de 10 nouvelles lignes dans la collection ===")

    # Liste des nouveaux documents à insérer
    new_records = [
        {
            "_id": "test1_id_1", "name": "Alice Johnson", "age": 34, "gender": "Female",
            "blood_type": "A+", "medical_condition": "Diabetes", "date_of_admission": "2023-06-15",
            "doctor": "Dr. Harris", "hospital": "Central Hospital", "insurance_provider": "Aetna",
            "billing_amount": 5000.50, "room_number": 101, "admission_type": "Routine",
            "discharge_date": "2023-06-20", "medication": "Metformin", "test_results": "Stable"
        },
        {
            "_id": "test1_id_2", "name": "Michael Brown", "age": 45, "gender": "Male",
            "blood_type": "O-", "medical_condition": "Hypertension", "date_of_admission": "2024-03-11",
            "doctor": "Dr. Lee", "hospital": "East Side Clinic", "insurance_provider": "Blue Cross",
            "billing_amount": 3000.00, "room_number": 202, "admission_type": "Emergency",
            "discharge_date": "2024-03-13", "medication": "Lisinopril", "test_results": "Improving"
        },
        {
            "_id": "test1_id_3", "name": "Clara Martinez", "age": 29, "gender": "Female",
            "blood_type": "B+", "medical_condition": "Asthma", "date_of_admission": "2023-12-01",
            "doctor": "Dr. Gomez", "hospital": "Westside Medical", "insurance_provider": "United Health",
            "billing_amount": 2000.00, "room_number": 303, "admission_type": "Routine",
            "discharge_date": "2023-12-05", "medication": "Inhaler", "test_results": "Stable"
        },
        {
            "_id": "test1_id_4", "name": "Ethan Clark", "age": 52, "gender": "Male",
            "blood_type": "AB-", "medical_condition": "Heart Disease", "date_of_admission": "2024-02-17",
            "doctor": "Dr. Adams", "hospital": "Downtown Clinic", "insurance_provider": "Cigna",
            "billing_amount": 7000.00, "room_number": 404, "admission_type": "Emergency",
            "discharge_date": "2024-02-22", "medication": "Aspirin", "test_results": "Improving"
        },
        {
            "_id": "test1_id_5", "name": "Sophia White", "age": 38, "gender": "Female",
            "blood_type": "O+", "medical_condition": "Arthritis", "date_of_admission": "2023-09-10",
            "doctor": "Dr. Ford", "hospital": "Green Valley Hospital", "insurance_provider": "Aetna",
            "billing_amount": 2500.00, "room_number": 505, "admission_type": "Routine",
            "discharge_date": "2023-09-15", "medication": "Ibuprofen", "test_results": "Stable"
        },
        {
            "_id": "test1_id_6", "name": "Oliver Black", "age": 60, "gender": "Male",
            "blood_type": "A-", "medical_condition": "Diabetes", "date_of_admission": "2023-11-12",
            "doctor": "Dr. Roberts", "hospital": "Mountain View Clinic", "insurance_provider": "Blue Cross",
            "billing_amount": 4500.00, "room_number": 606, "admission_type": "Routine",
            "discharge_date": "2023-11-18", "medication": "Insulin", "test_results": "Stable"
        },
        {
            "_id": "test1_id_7", "name": "Liam Green", "age": 48, "gender": "Male",
            "blood_type": "B-", "medical_condition": "High Cholesterol", "date_of_admission": "2023-07-22",
            "doctor": "Dr. Watson", "hospital": "Sunnyvale Medical", "insurance_provider": "United Health",
            "billing_amount": 3200.00, "room_number": 707, "admission_type": "Routine",
            "discharge_date": "2023-07-27", "medication": "Statins", "test_results": "Improving"
        },
        {
            "_id": "test1_id_8", "name": "Emma Wilson", "age": 41, "gender": "Female",
            "blood_type": "AB+", "medical_condition": "Migraine", "date_of_admission": "2023-10-08",
            "doctor": "Dr. Bell", "hospital": "Hilltop Hospital", "insurance_provider": "Cigna",
            "billing_amount": 2800.00, "room_number": 808, "admission_type": "Emergency",
            "discharge_date": "2023-10-11", "medication": "Sumatriptan", "test_results": "Stable"
        },
        {
            "_id": "test1_id_9", "name": "William Scott", "age": 50, "gender": "Male",
            "blood_type": "O-", "medical_condition": "Kidney Stones", "date_of_admission": "2024-01-15",
            "doctor": "Dr. Collins", "hospital": "Lakeside Hospital", "insurance_provider": "Aetna",
            "billing_amount": 6200.00, "room_number": 909, "admission_type": "Emergency",
            "discharge_date": "2024-01-20", "medication": "Painkillers", "test_results": "Improving"
        },
        {
            "_id": "test1_id_10", "name": "Isabella Moore", "age": 37, "gender": "Female",
            "blood_type": "A+", "medical_condition": "Anemia", "date_of_admission": "2023-05-10",
            "doctor": "Dr. Wright", "hospital": "Riverside Clinic", "insurance_provider": "Blue Cross",
            "billing_amount": 3100.00, "room_number": 1010, "admission_type": "Routine",
            "discharge_date": "2023-05-15", "medication": "Iron Supplements", "test_results": "Stable"
        }
    ]
    try:
        # Appeler la fonction d'insertion pour insérer les nouveaux documents
        inserted_count = insert_records(test_collection, new_records)
        
        # Enregistrer dans les logs le succès de l'opération
        logger.info(f"{inserted_count} nouveaux documents insérés avec succès.")
    except Exception as e:
        # En cas d'erreur, loguer le problème avec le message détaillé
        logger.error(f"Erreur lors de l'insertion des nouvelles données : {e}")


def read_all_data(test_collection):
    """
    Lit toutes les données présentes dans la collection après insertion.

    Étapes principales :
    1. Exécute une requête sans filtre pour récupérer tous les documents présents.
    2. Compte et logue le nombre total de documents récupérés.
    3. Gère les exceptions pour détecter et loguer les erreurs éventuelles.

    Args:
        test_collection : Collection MongoDB cible.
    """
    # Log indiquant le début de la lecture des données
    logger.info("=== Lecture de toutes les données présentes dans la collection ===")
    try:
        # Lire tous les documents de la collection (pas de filtre)
        results = read_records(test_collection, query={})
        
        # Loguer le nombre total de documents récupérés
        logger.info(f"Nombre total de documents dans la collection : {len(results)}")
    except Exception as e:
        # Loguer les erreurs si une exception survient
        logger.error(f"Erreur lors de la lecture des données : {e}")


def update_data(test_collection):
    """
    Applique 10 mises à jour différentes dans la collection MongoDB, dont 2 sur le même identifiant (_id).

    Étapes principales :
    1. Définit une liste de mises à jour, comprenant les filtres et les modifications à appliquer.
    2. Parcourt la liste et applique chaque mise à jour à la collection.
    3. Vérifie que chaque mise à jour a bien été appliquée avec une assertion.
    4. Logue le succès ou l'échec de chaque mise à jour.

    Args:
        test_collection : Collection MongoDB cible.
    """
    # Log indiquant le début de la phase de mise à jour
    logger.info("=== Mise à jour des données ===")
    
    # Liste des mises à jour à appliquer
    updates = [
        {"filter": {"_id": "test1_id_1"}, "update": {"$set": {"billing_amount": 6000.00}}},  # Modifier le montant facturé
        {"filter": {"_id": "test1_id_1"}, "update": {"$set": {"room_number": 102}}},  # Changer le numéro de chambre
        {"filter": {"_id": "test1_id_2"}, "update": {"$set": {"test_results": "Critical"}}},  # Résultat critique
        {"filter": {"_id": "test1_id_3"}, "update": {"$set": {"hospital": "Northwest Medical"}}},  # Changer l'hôpital
        {"filter": {"_id": "test1_id_4"}, "update": {"$set": {"medication": "Beta Blockers"}}},  # Médicament prescrit
        {"filter": {"_id": "test1_id_5"}, "update": {"$set": {"gender": "Non-Binary"}}},  # Modifier le genre
        {"filter": {"_id": "test1_id_6"}, "update": {"$set": {"date_of_admission": "2024-01-01"}}},  # Nouvelle date d'admission
        {"filter": {"_id": "test1_id_7"}, "update": {"$set": {"blood_type": "AB+"}}},  # Modifier le groupe sanguin
        {"filter": {"_id": "test1_id_8"}, "update": {"$set": {"medical_condition": "Severe Migraine"}}},  # Nouvelle condition médicale
        {"filter": {"_id": "test1_id_9"}, "update": {"$set": {"insurance_provider": "Medicare"}}}  # Modifier le fournisseur d'assurance
    ]

    try:
        # Parcourir chaque mise à jour dans la liste
        for i, update in enumerate(updates, start=1):
            # Appliquer la mise à jour à la collection
            update_count = update_records(test_collection, update["filter"], update["update"])
            
            # Vérifier qu'au moins un document a été modifié
            assert update_count > 0, f"Erreur : Aucune mise à jour appliquée pour l'update {i}."
            
            # Loguer le succès de la mise à jour
            logger.info(f"Mise à jour {i} appliquée avec succès.")
    except Exception as e:
        # Loguer les erreurs si une exception survient
        logger.error(f"Erreur lors des mises à jour des données : {e}")

def delete_specific_data(test_collection):
    """
    Supprime des documents spécifiques de la collection en fonction de 5 critères différents.

    Étapes principales :
    1. Définit une liste de suppressions, comprenant les filtres et une description pour chaque suppression.
    2. Parcourt la liste et applique chaque suppression à la collection.
    3. Vérifie que chaque suppression a bien été effectuée avec une assertion.
    4. Logue le succès ou l'échec de chaque suppression.

    Args:
        test_collection : Collection MongoDB cible.
    """
    # Log indiquant le début de la phase de suppression
    logger.info("=== Suppression de données spécifiques ===")
    
    # Liste des conditions de suppression
    deletions = [
        {"filter": {"_id": "test1_id_2"}, "description": "Suppression par _id (test1_id_2)"},
        {"filter": {"age": {"$gt": 50}}, "description": "Suppression des documents où l'âge est > 50"},
        {"filter": {"hospital": "Central Hospital"}, "description": "Suppression des documents pour l'hôpital 'Central Hospital'"},
        {"filter": {"test_results": "Critical"}, "description": "Suppression des documents avec des résultats critiques"},
        {"filter": {"medical_condition": "Diabetes"}, "description": "Suppression des documents avec la condition médicale 'Diabetes'"}
    ]
    
    try:
        # Parcourir chaque condition de suppression dans la liste
        for i, deletion in enumerate(deletions, start=1):
            # Appliquer la suppression à la collection
            delete_count = delete_records(test_collection, deletion["filter"])
            
            # Vérifier qu'au moins un document a été supprimé
            assert delete_count > 0, f"Erreur : Aucun document supprimé pour la condition {i} ({deletion['description']})."
            
            # Loguer le succès de la suppression
            logger.info(f"Suppression {i} réussie : {delete_count} document(s) supprimé(s) ({deletion['description']}).")
    except Exception as e:
        # Loguer les erreurs si une exception survient
        logger.error(f"Erreur lors de la suppression des données : {e}")

 

def export_final_data(test_collection):
    """
    Exporte les données restantes de la collection MongoDB dans un fichier CSV.

    Étapes principales :
    1. Appelle la fonction `export_to_csv` pour exporter les documents MongoDB.
    2. Vérifie que des documents ont été exportés avec succès.
    3. Logue les succès ou erreurs rencontrés lors de l'exportation.

    Args:
        test_collection : Collection MongoDB cible.
    """
    logger.info("=== Début de l'exportation finale des données ===")
    try:
        # Appeler la fonction `export_to_csv` pour effectuer l'exportation
        logger.info("Tentative d'exportation des données...")
        export_count = export_to_csv(test_collection, "test_export")  # Nom sans extension

        # Vérifier que des documents ont bien été exportés
        if export_count > 0:
            logger.info(f"Données exportées avec succès : {export_count} document(s).")
        else:
            logger.warning("Aucun document exporté. La collection est peut-être vide.")
    except Exception as e:
        # Loguer toute erreur rencontrée pendant l'exportation
        logger.error(f"Erreur lors de l'exportation des données : {e}")
