# === Importation des bibliothèques nécessaires ===
import os  # Interaction avec le système de fichiers
import pandas as pd  # Manipulation et analyse des données (DataFrames)
from loguru import logger  # Gestion avancée des logs
import kagglehub  # Téléchargement de datasets depuis Kaggle
from pathlib import Path  # Manipulation intuitive des chemins de fichiers

# === Configuration des logs ===
LOG_FILE = "logs/data_preparation.log"  # Chemin du fichier de log
logger.add(LOG_FILE, level="INFO", rotation="1 MB", compression="zip")

# === Fonction principale : Traitement des données ===
def data_processing(output_path):
    """
    Télécharge, valide, nettoie et sauvegarde des données médicales.

    Args:
        output_path (str): Chemin pour sauvegarder le fichier nettoyé.
    """
    try:
        # === Étape 1 : Téléchargement et localisation des données ===
        kaggle_dataset = "prasad22/healthcare-dataset"  # Nom du dataset Kaggle
        expected_file = "healthcare_dataset.csv"  # Fichier attendu dans le dataset

        logger.info(f"Téléchargement des données depuis Kaggle : {kaggle_dataset}...")
        try:
            # Télécharge le dataset depuis Kaggle
            dataset_path = kagglehub.dataset_download(kaggle_dataset)
            logger.success(f"Dataset téléchargé avec succès dans : {dataset_path}")

            # Localisation du fichier attendu
            file_path = Path(dataset_path) / expected_file
            if not file_path.exists():
                raise FileNotFoundError(f"Fichier attendu non trouvé : {file_path}")

            logger.info(f"Fichier localisé pour traitement : {file_path}")
        except Exception as e:
            logger.error(f"Erreur lors du téléchargement ou de la localisation du fichier : {e}")
            raise

        # === Étape 2 : Chargement des données ===
        logger.info(f"Chargement des données depuis : {file_path}")
        try:
            df = pd.read_csv(file_path)
            logger.info(f"Données chargées : {len(df)} lignes, {len(df.columns)} colonnes.")
            logger.info(f"Colonnes disponibles : {df.columns.tolist()}")
            logger.info("Types des colonnes avant nettoyage :\n" + str(df.dtypes))

            # Aperçu des premières lignes des données brutes
            logger.info("Aperçu des premières lignes des données brutes :\n" + str(df.head()))
        except Exception as e:
            logger.error(f"Erreur lors du chargement des données : {e}")
            raise

        # === Étape 3 : Nettoyage des données ===
        logger.info("Début du nettoyage des données...")

        # Suppression des doublons
        initial_rows = len(df)
        df.drop_duplicates(inplace=True)
        logger.info(f"Doublons supprimés : {initial_rows - len(df)} lignes.")

        # Validation des types de colonnes et gestion des valeurs aberrantes
        type_checks = {
            "Age": (int, (0, 120)),  # La colonne 'Age' doit être un entier entre 0 et 120 ans.
            "Billing Amount": (float, (0, None)),  # 'Billing Amount' doit être un float strictement positif.
        }
        for col, (expected_type, valid_range) in type_checks.items():
            if col in df.columns:
                # Étape 1 : Conversion des colonnes au type attendu
                try:
                    df[col] = df[col].astype(expected_type)
                    logger.info(f"Colonne '{col}' convertie avec succès en {expected_type}.")
                except Exception as e:
                    logger.warning(f"Erreur lors de la conversion de la colonne '{col}' : {e}")

                # Étape 2 : Suppression des valeurs hors limites si une plage est définie
                if valid_range:
                    min_val, max_val = valid_range
                    before_filter = len(df)  # Nombre de lignes avant filtrage
                    # Filtrage des données en respectant la plage définie
                    df = df[(df[col] >= min_val) & (df[col] <= max_val if max_val else True)]
                    logger.info(f"Valeurs aberrantes supprimées pour '{col}' : {before_filter - len(df)} lignes supprimées.")

        # Conversion des colonnes contenant des dates
        date_cols = ["Date of Admission", "Discharge Date"]
        for col in date_cols:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors="coerce")
                invalid_dates = df[col].isna().sum()
                logger.info(f"Colonne '{col}' : {invalid_dates} valeurs invalides après conversion.")

        # Renommage des colonnes
        df.rename(columns={c: c.lower().replace(" ", "_") for c in df.columns}, inplace=True)
        logger.info("Colonnes renommées pour standardisation.")

        # Validation des valeurs dans certaines colonnes
        if "gender" in df.columns:
            valid_genders = {"Male", "Female"}
            invalid_genders = set(df["gender"].unique()) - valid_genders
            if invalid_genders:
                logger.warning(f"Valeurs inattendues dans 'gender' : {invalid_genders}")

        if "blood_type" in df.columns:
            valid_blood_types = {"A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"}
            invalid_blood_types = set(df["blood_type"].unique()) - valid_blood_types
            if invalid_blood_types:
                logger.warning(f"Valeurs inattendues dans 'blood_type' : {invalid_blood_types}")

        # Nettoyage des colonnes textuelles
        text_cols = ["doctor", "hospital", "medical_condition", "insurance_provider", "medication", "test_results"]
        for col in text_cols:
            if col in df.columns:
                df[col] = df[col].str.strip().str.title()
                logger.info(f"Colonne '{col}' nettoyée : suppression des espaces et mise en forme standardisée.")

        # Formatage de la colonne 'name' pour une cohérence
        if "name" in df.columns:
            df["name"] = df["name"].str.strip().str.title()
            logger.info("Colonne 'name' formatée avec une majuscule pour chaque mot.")

        # Aperçu des données nettoyées
        logger.info("Aperçu des premières lignes des données nettoyées :\n" + str(df.head()))
        logger.info("Types des colonnes après nettoyage :\n" + str(df.dtypes))

        logger.success("Nettoyage des données terminé.")

        # === Étape 4 : Sauvegarde des données nettoyées ===
        logger.info(f"Sauvegarde des données nettoyées dans : {output_path}")
        try:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            df.to_csv(output_path, index=False)
            logger.success(f"Fichier nettoyé sauvegardé avec succès dans : {output_path}")
        except Exception as e:
            logger.error(f"Erreur lors de la sauvegarde des données : {e}")
            raise

    except Exception as e:
        logger.critical(f"Erreur critique : {e}")
        raise

# === Programme principal ===
if __name__ == "__main__":
    # Définition des chemins par défaut
    output_file = "data/processed/healthcare_dataset_cleaned.csv"

    # Exécution de la fonction principale
    data_processing(output_path=output_file)
