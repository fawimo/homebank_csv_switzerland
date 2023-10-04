# Clean and transform CSV statment from wise into Homebank readable CVS file

# Import libraries
from shared import *

# Library option
pd.set_option('display.max_columns', None)

## Detect file name
file_pattern = "*Transaction*"

# Get a list of file paths that match the pattern
file_paths = glob.glob(os.path.join(folder_path, file_pattern))

# Sort the file paths by their modification time in descending order
sorted_file_paths = sorted(file_paths, key=os.path.getmtime, reverse=True)

# Select the first file (the most recent one)
if sorted_file_paths:
    last_file_path = sorted_file_paths[0]   


## Import file
df_raw = tabula.read_pdf(last_file_path, pages='all')[0]

## Set first row as colum labels
df_raw.columns = df_raw.iloc[0]
df_raw = df_raw[1:]

## Remove unwanted columns
df_raw = df_raw.dropna(axis=1, how='all')
df_raw = df_raw.drop(columns=['Solde'], errors='ignore')

## Remove unwante NaN line
df_raw = df_raw.dropna(subset=['Date'])

# change date formate
df_raw['Date'] = pd.to_datetime(df_raw['Date'], format="%d.%m.%Y").dt.strftime("%m-%d-%Y")

## Clean Débit and Crédit column
# Change column types to float
df_raw['Débits'] = df_raw['Débits'].replace('’', '', regex=True).astype(float)
df_raw['Crédits'] = df_raw['Crédits'].replace('’', '', regex=True).astype(float)

df_raw['Débits'] = df_raw['Débits'] * -1

# Replace NaN values with 0 in 'Débits' and 'Crédits' columns
df_raw['Débits'].fillna(0, inplace=True)
df_raw['Crédits'].fillna(0, inplace=True)

# Merge 'Débits' and 'Crédits' columns
df_raw['amount'] = df_raw['Débits'] + df_raw['Crédits']

# Remove Débits and Crédits columns
columns_to_drop_1 = ["Débits", "Crédits"]
df_raw = df_raw.drop(columns_to_drop_1, axis=1)


## Format the CSV to Homebank format
df_final = df_raw.rename(columns={"Date": "date"})
df_final.insert(1, "payment", 4)
df_final.insert(2 , "info", "")
df_final = df_final.rename(columns={"Désignation": "payee"})
df_final.insert(4 , "memo", "")
df_final.insert(6 , "category", "")
df_final.insert(7 , "tags", "")

# Export file to 
# Get the current date and time
current_date = datetime.datetime.now().strftime("%Y-%m-%d")

# Create the file name with the current date
file_name = f"/home/fabien/Statements/reka_{current_date}.csv"

# Export the DataFrame to CSV with the updated file name
df_final.to_csv(file_name, index=False)


