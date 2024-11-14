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
chemin_fichier_csv = "C:\\Users\\Boriska Mbilongo\\Desktop\\EneoX3\\Data-Eneo\\recon_orange_dec2023.csv\\recon_orange_dec2023.csv"

# Charger le fichier CSV avec pandas en utilisant '#' comme séparateur
donnees_csv = pd.read_csv(chemin_fichier_csv, delimiter='#').dropna()

print(donnees_csv.isnull().sum())

# Parcourir les lignes du DataFrame
for index, ligne in donnees_csv.iterrows():
    # Remplacez les noms de colonnes par ceux de votre fichier CSV
    POS = ligne["POS"]
    TOKEN = ligne["TOKEN"]
    PAID = ligne["PAID"]
    PURCHASING_RESOURCE = ligne["PURCHASING_RESOURCE"]
    VENING_TIME= ligne["VENING_TIME"]
    ORDERS_ID= ligne["ORDERS_ID"]
    METER_NO= ligne["METER_NO"]
    MSGID = ligne["MSGID"]

    
    # ...

    # Exemple d'insertion dans la base de données
    requete_insertion = "INSERT INTO ENEO (POS , TOKEN,PAID,PURCHASING_RESOURCE,VENING_TIME,ORDERS_ID,METER_NO,MSGID) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"
    valeurs = ( POS , TOKEN,PAID,PURCHASING_RESOURCE,VENING_TIME,ORDERS_ID,METER_NO,MSGID)
    curseur.execute(requete_insertion, valeurs)
# Valider les changements dans la base de données
connexion.commit()

# Fermer le curseur et la connexion
curseur.close()
connexion.close()
