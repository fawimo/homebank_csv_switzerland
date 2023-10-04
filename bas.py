# Clean and transform CSV statment from wise into Homebank readable CVS file

# Import libraries
from shared import *

## Detect file name
file_pattern = "*kto_ausz*"

# Get a list of file paths that match the pattern
file_paths = glob.glob(os.path.join(folder_path, file_pattern))

# Sort the file paths by their modification time in descending order
sorted_file_paths = sorted(file_paths, key=os.path.getmtime, reverse=True)

# Select the first file (the most recent one)
if sorted_file_paths:
    last_file_path = sorted_file_paths[0]    

# Import file
df_raw = pd.read_csv(last_file_path, encoding="iso-8859-1", header=None)
df_raw = df_raw[12:]

df_raw[["Date", "Libellé", "Montant", "Valeur"]] = df_raw[0].str.split(';', expand=True)
df_raw = df_raw.drop(columns=[0, "Valeur"])
df_raw = df_raw.reset_index(drop=True)


# Change date type
df_raw["Date"] = pd.to_datetime(df_raw["Date"], format="%d.%m.%y")
df_raw["Date"] = df_raw["Date"].dt.strftime("%m-%d-%y")

# Format the CSV to Homebank format
df_final = df_raw.rename(columns={"Libellé": "payee"})
df_final = df_final.rename(columns={"Montant": "amount"})

df_final.insert(1, "payment", 8)
df_final.insert(2 , "info", "")
df_final.insert(4 , "memo", "")
df_final.insert(6 , "category", "")
df_final.insert(7 , "tags", "")

# Export file to 
# Get the current date and time
current_date = datetime.datetime.now().strftime("%Y-%m-%d")

# Create the file name with the current date
file_name = f"/home/fabien/Statements/bas_{current_date}.csv"

# Export the DataFrame to CSV with the updated file name
df_final.to_csv(file_name, index=False)
