import fitz  # PyMuPDF
import re
import csv
import pandas as pd
from datetime import datetime
import os

# Demander à l'utilisateur le nom du fichier PDF
pdf_name = input("Entrez le nom du fichier PDF (ex: Bill - February.pdf) : ")

# Construire le chemin du fichier
pdf_path = os.path.join("/home/fabien/Inbox", pdf_name)

# Vérifier si le fichier existe
if not os.path.exists(pdf_path):
    print(f"Erreur : Le fichier '{pdf_name}' n'existe pas dans /home/fabien/Inbox.")
    exit()

# Ouvrir le document PDF
doc = fitz.open(pdf_path)

# Extraire toutes les lignes du PDF
lines = []
for page in doc:
    text = page.get_text("text")
    lines.extend(text.split("\n"))

# Filtrer les lignes qui commencent par deux dates (format XX.XX.XX XX.XX.XX)
pattern = re.compile(r'^\d{2}\.\d{2}\.\d{2} \d{2}\.\d{2}\.\d{2}')

filtered_data = []
i = 0
while i < len(lines) - 1:
    if pattern.match(lines[i]):
        filtered_data.append([lines[i], lines[i + 1]])  # Ajouter la ligne suivante
    i += 1

# Nettoyer les données : supprimer la deuxième date
cleaned_data = []
for transaction, montant in filtered_data:
    cleaned_transaction = re.sub(r'^(\d{2}\.\d{2}\.\d{2}) \d{2}\.\d{2}\.\d{2}', r'\1', transaction)
    cleaned_data.append([cleaned_transaction, montant])

# Reformater les dates en %m-%d-%y
formatted_data = []
for transaction, montant in cleaned_data:
    date_part, description = transaction.split(" ", 1)  # Séparer la date du reste
    formatted_date = datetime.strptime(date_part, "%d.%m.%y").strftime("%m-%d-%y")  # Convertir la date
    formatted_data.append([formatted_date, description, montant])

# Charger les données formatées dans un DataFrame Pandas
df_final = pd.DataFrame(formatted_data, columns=["Date", "Description", "Montant"])

# Renommer les colonnes pour HomeBank
df_final = df_final.rename(columns={"Date": "date", "Description": "payee", "Montant": "amount"})

# Insérer les colonnes nécessaires pour HomeBank
df_final.insert(1, "payment", 8)
df_final.insert(2, "info", "")
df_final.insert(4, "memo", "")
df_final.insert(6, "category", "")
df_final.insert(7, "tags", "")

# Sauvegarder le fichier CSV compatible avec HomeBank
output_csv = os.path.join("/home/fabien/Inbox", "homebank_transactions_viseca.csv")
df_final.to_csv(output_csv, index=False, encoding="utf-8")

print(f"✅ Le fichier CSV pour HomeBank a été généré : {output_csv}")
