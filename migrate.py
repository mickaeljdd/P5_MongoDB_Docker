import os
from dotenv import load_dotenv
import pandas as pd
from pymongo import MongoClient, errors
import time
import shutil
import kagglehub
from datetime import datetime
from pymongo.errors import BulkWriteError

DATA_DIR = "./data"
CSV_FILE = "healthcare_dataset.csv"
CSV_PATH = os.path.join(DATA_DIR, CSV_FILE)

load_dotenv()

def chunked(iterable, size):
    for i in range(0, len(iterable), size):
        yield iterable[i:i + size]

def recup_fichier():
    os.makedirs(DATA_DIR, exist_ok=True)

    if os.path.exists(CSV_PATH):
        print("Le fichier CSV existe déjà, téléchargement ignoré.")
        return

    print("Téléchargement du dataset depuis Kaggle...")
    path = kagglehub.dataset_download("prasad22/healthcare-dataset")

    src = os.path.join(path, CSV_FILE)
    if not os.path.exists(src):
        raise FileNotFoundError(f"Fichier introuvable : {src}")

    shutil.copy(src, CSV_PATH)
    print(f"CSV copié vers {CSV_PATH}")


def connectandmigrate():
    time.sleep(5000)

    mongo_uri = os.getenv(
        "MONGO_URI",
        f"mongodb://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@localhost:{os.getenv('DB_PORT')}/"
    )
    print(mongo_uri)
    client = MongoClient(mongo_uri)
    db = client["healthcare_db"]
    collection = db["hospitalisations"]

    print("Connexion à MongoDB réussie")

    # Index unique (idempotent)
    collection.create_index(
        [
            ("patient.name", 1),
            ("hospitalization.admission_date", 1)
        ],
        unique=True
    )

    if not os.path.exists(CSV_PATH):
        raise FileNotFoundError("Le fichier CSV est introuvable.")

    df = pd.read_csv(CSV_PATH)
    print(f"{len(df)} lignes chargées depuis le CSV.")

    documents = []

    for _, row in df.iterrows():
        doc = {
            "patient": {
                "name": row["Name"],
                "age": int(row["Age"]),
                "gender": row["Gender"],
                "blood_type": row["Blood Type"]
            },
            "medical": {
                "condition": row["Medical Condition"],
                "medication": row["Medication"],
                "test_results": row["Test Results"]
            },
            "hospitalization": {
                "admission_date": row["Date of Admission"],
                "discharge_date": row["Discharge Date"],
                "admission_type": row["Admission Type"],
                "doctor": row["Doctor"],
                "hospital": row["Hospital"],
                "room_number": row["Room Number"]
            },
            "billing": {
                "insurance_provider": row["Insurance Provider"],
                "amount": float(row["Billing Amount"])
            },
        }
        documents.append(doc)

    BATCH_SIZE = 1000

    for batch in chunked(documents, BATCH_SIZE):
        try:
            collection.insert_many(batch, ordered=False)
        except BulkWriteError:
            pass  # doublons ignorés



if __name__ == "__main__":
    recup_fichier()
    connectandmigrate()
