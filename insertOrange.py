import pandas as pd
import mysql.connector

# Remplacez ces informations par celles de votre base de données
host = 'localhost'
user = 'root'
password = ''
database = 'eneopay'

# Établir la connexion
connexion = mysql.connector.connect(
    host=host,
    user=user,
    password=password,
    database=database
)

# Créer un curseur pour exécuter des requêtes SQL
curseur = connexion.cursor()

# Remplacez le chemin du fichier CSV par le vôtre
chemin_fichier_csv = "c:\\Users\\Boriska Mbilongo\\Desktop\\EneoX3\\Data-Eneo\\Dec\\Txns_EneoPrePaid_20231231.csv"

# Charger le fichier CSV avec pandas en utilisant '#' comme séparateur
donnees_csv = pd.read_csv(chemin_fichier_csv, delimiter=';').dropna()

print(donnees_csv.isnull().sum())

# Parcourir les lignes du DataFrame
for index, ligne in donnees_csv.iterrows():
    # Remplacez les noms de colonnes par ceux de votre fichier CSV
    METER_NO= ligne["Numéro de compteur"]
    Nom_Client = ligne["Nom du client"]
    Num_Client = ligne["Numéro de téléphone du client"]
    Montant = ligne["Montant de la transaction"]
    TOKEN = ligne["Token"]
    Date = ligne["Date de la transaction"]
    Num_Ref =ligne["Numéro de référence"]
    KWH = ligne["KWH"]
    Status = ligne["Paid Status"]


    
    # ...

    # Exemple d'insertion dans la base de données
    requete_insertion = "INSERT INTO ORANGE(METER_NO , Nom_Client,Num_Client,Montant,TOKEN,Date,Num_Ref,KWH,Status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s,%s);"
    valeurs = ( METER_NO , Nom_Client,Num_Client,Montant,TOKEN,Date,Num_Ref,KWH,Status)
    curseur.execute(requete_insertion, valeurs)
# Valider les changements dans la base de données
connexion.commit()

# Fermer le curseur et la connexion
curseur.close()
connexion.close()
