import kagglehub
import os
import pandas as pd

# Télécharger le dataset
print("Téléchargement du dataset depuis Kaggle...")
path = kagglehub.dataset_download("prasad22/healthcare-dataset")
print("Dataset téléchargé dans :", path)

# Vérifie les fichiers présents
print("\nFichiers disponibles :")
for f in os.listdir(path):
    print("-", f)

# Si tu veux charger un CSV spécifique
csv_path = os.path.join(path, "healthcare_dataset.csv")  # adapte le nom si différent
if os.path.exists(csv_path):
    df = pd.read_csv(csv_path)
    print("\nAperçu des données :")
    print(df.head())
else:
    print("\n⚠️ Aucun fichier CSV trouvé. Vérifie le nom exact dans le dossier téléchargé.")
