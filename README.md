# P5_MongoDB_Docker

## Introduction

Ce projet illustre l’utilisation de **MongoDB** et de **Docker** pour la migration automatisée d’un dataset médical depuis un fichier CSV vers une base de données NoSQL.  
L’objectif est de proposer une solution **scalable, portable et reproductible**, adaptée à des contextes Big Data et potentiellement extensible vers des environnements cloud.

Ce dépôt contient l’ensemble des outils nécessaires pour :
- récupérer un dataset depuis Kaggle,
- importer ce dataset dans MongoDB,
- conteneuriser l’application avec Docker,
- documenter et versionner la solution.

---

## Contenu du dépôt
```
P5_MongoDB_Docker/
├── docker-compose.yaml # Définition des services Docker
├── dockerfile # Construction de l’image du migrateur Python
├── migrate.py # Script Python de migration des données
├── requirements.txt # Dépendances Python
├── README.md # Ce fichier de documentation
└── data/ # Dossier local pour stocker le CSV
└── healthcare-dataset.csv
```
## Description des composants

### 🐳 `docker-compose.yaml`

Fichier clé orchestrant les services Docker :

- `mongo` : conteneur exécutant MongoDB (base de données NoSQL).
- `migrator` : conteneur exécutant le script Python pour importer le CSV dans MongoDB.

Ce fichier configure également les volumes de stockage, les variables d’environnement et les dépendances inter-services (via `depends_on`).

---

### 📦 `dockerfile`

Dockerfile définissant l’image du migrateur Python :
1. Il installe Python et les dépendances (`pandas`, `pymongo`, etc.).
2. Il copie les scripts Python dans l’image.
3. Il définit le point d’entrée pour l’exécution automatique de la migration au démarrage du conteneur.

---

### 🐍 `migrate.py`

Script Python de migration :

- Charge le fichier CSV depuis le dossier `/app/data` (monté depuis le dossier `data/` de la racine).
- Se connecte à MongoDB via l’URI défini dans un environnement Docker.
- Transforme les lignes CSV en documents JSON compatibles MongoDB.
- Insère les documents dans la collection `patients`.
  
Ce script est conçu pour être réutilisable et paramétrable via des variables d’environnement.

---

### 📄 `requirements.txt`

Liste des bibliothèques Python requises par `migrate.py`.  
Les principales sont :
- `pandas` — pour la lecture et la manipulation du CSV.
- `pymongo` — pour l’interaction avec MongoDB.
- `kagglehub` - pour le téléchargement du CSV
---

### 📁 `data/`

Ce dossier doit contenir le dataset CSV que l’on souhaite importer (par exemple `healthcare_dataset.csv`).  
Il est utilisé comme **volume Docker** pour être accessible depuis le conteneur `migrator`.

---

## Comment exécuter le projet

### 1. Création des variables d'environnement

Dans le fichier .envsample, il faudra remplir les valeurs mise à '...' au valeur que vous désirez dans lesquelles :
  DB_USER=... (le nom utlisateur/utiliser comme admin)
  DB_PASSWORD=... (le mot de passe de connection à la base de données pour l'admin)
  DB_PORT=... (le port, attention doit être un nombre comme par exemple 27017)
  DB_NAME=... (le nom de la base de données)
  DB_READ_USER=... (le nom utilisateur pour le rôle lecteur)
  DB_READ_PASSWORD=... (le mot de passe pour le rôle lecteur)
  DB_READWRITE_USER=... (le nom utilisateur pour le rôle auteur)
  DB_READWRITE_PASSWORD=... (le mot de passe pour le rôle auteur)

### 2. Lancer les services avec Docker

Dans un terminal, à la racine du projet :
```bash
docker compose up --build
```
Cette commande va :

Télécharger le csv

Créer un dossier `data`

Déplacer le fichier csv dedans

Construire l’image du migrateur Python.

Démarrer MongoDB dans un conteneur.

Exécuter le script de migration dans le conteneur migrator.

Importer toutes les lignes du CSV dans la collection MongoDB.

3. Vérifier l’import

Vous pouvez vérifier que les données ont bien été importées dans un autre terminal :

```bash
docker exec -it mongodb mongosh -u admin -p password
```

Puis, dans le shell Mongo :

```js
use healthcare_db
db.patients.find().limit(5).pretty()
```
```mermaid
classDiagram
    class Patient {
        name : string
        age : number
        gender : string
        blood_type : string
    }

    class Medical {
        condition : string
        medication : string
        test_results : string
    }

    class Hospitalization {
        admission_date : date
        discharge_date : date
        admission_type : string
        room_number : number
        doctor : string
        hospital : string
    }

    class Billing {
        insurance_provider : string
        amount : number
    }
    Patient --> Medical
    Patient --> Hospitalization
    Patient --> Billing
```
