import os
import pandas as pd
from pymongo import MongoClient
import time
import shutil
import kagglehub

# Télécharger le dataset
print("Téléchargement du dataset depuis Kaggle...")
path = kagglehub.dataset_download("prasad22/healthcare-dataset")
print("Dataset téléchargé dans :", path)

DEST_DIR = "./data"
os.makedirs(DEST_DIR, exist_ok=True)

file = 'healthcare_dataset.csv'
src = os.path.join(path, file)
print(src)
dst = os.path.join(DEST_DIR, file)
shutil.copy(src, dst)
print(f"CSV copié vers {dst}")


# Attendre un peu pour laisser Mongo démarrer
time.sleep(5)

# Connexion à MongoDB depuis localhost
client = MongoClient("mongodb://admin:password@localhost:27017/")


# Lire la variable d'environnement
mongo_uri = os.getenv("MONGO_URI", "mongodb://admin:password@mongo:27017/") 

client = MongoClient(mongo_uri)



db = client["healthcare_db"]
collection = db["patients"]
print("Connexion à MongoDB réussie")

if collection.count_documents({}) > 0:
    collection.delete_many({})
    print("Collection vidée")

# Charger le CSV si localhost
#df = pd.read_csv("./data/healthcare_dataset.csv")
#print(f"{len(df)} lignes chargées depuis le CSV.")

# Charger le CSV si docker
df = pd.read_csv("/app/data/healthcare_dataset.csv")
print(f"{len(df)} lignes chargées depuis le CSV.")

# Convertir en dictionnaires et insérer dans MongoDB
data = df.to_dict(orient="records")
collection.insert_many(data,)
print(f"{len(data)} documents insérés dans MongoDB")
