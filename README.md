# Détecteur de Registre Linguistique
Ce projet a été développé dans le cadre du cours Fouille des données.
Il permet de prédire le prix d'une voiture à partir de caractéristiques telles que la marque, le modèle, le carburant, etc.
##  Fonctionnalités


-   **SCrapper un site d'annonces** : permets de récolter des annonces de voitures
-   **Nettoyage des fichiers et création des JSON** :  permet de nettoyer les pages html et créer des fichiers json avec des données prête à utilisation 
-   **Insertion en base** : pemret d'insérer les données de voitures en bases de donées postgresSQL
-   **FASTAPI** : permet de séparer back end et front end 
-   **Interface Web** : Formulaire avec les carractéristiques d'une voiture
-   **Prédiction** : Analyse et prédire prix d'une voiture


##  Démarrage rapide

Suivez ces étapes pour exécuter l'application sur votre machine locale.

### Prérequis

Assurez-vous d'avoir Python 3.9+ et PostgreSQL installé sur votre système.
Dans un terminal exécutez ces commandes : 

### 1. Cloner le dépôt (ou télécharger les fichiers)
Importer le projet : 

```bash 
git clone https://github.com/formationQA/PredictionVoiture.git
cd /PredictionVoiture/src
python3 -m venv .venv
source .venv/bin/activate
Vérifier la base de données et importer les tables :
sudo service postgresql start
CREATE DATABASE postgres;
\q`
`psql -U postgres -d dataproject -f ../SQl/Alter_schema_projet.sql


Lancer back end API :

uvicorn mainApi:app --reload --host 0.0.0.0 --port 8002

Lancer le front end :

python3 -m http.server 8080

Simuler des appels API :

http://localhost:8080/doc

Interface WEB :

http://localhost:8080/ihm


