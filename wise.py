# Clean and transform CSV statment from wise into Homebank readable CVS file

# Import libraries
from shared import *

## Detect file name
file_pattern = "*statement_1815638*"

# Get a list of file paths that match the pattern
file_paths = glob.glob(os.path.join(folder_path, file_pattern))

# Sort the file paths by their modification time in descending order
sorted_file_paths = sorted(file_paths, key=os.path.getmtime, reverse=True)

# Select the first file (the most recent one)
if sorted_file_paths:
    last_file_path = sorted_file_paths[0] 


## Import file
df_raw = pd.read_csv(last_file_path,
                     usecols = ["Date", "Amount", "Merchant"],
                     dtype = {"Date": str, "Amount": str})

## Select the rows and change date type
df_raw["Date"] = pd.to_datetime(df_raw["Date"], format='%d-%m-%Y')
df_raw["Date"] = df_raw["Date"].dt.strftime('%m-%d-%Y')

#change to final table
df_final = df_raw

# Format the CSV to Homebank format
df_final.rename(columns={"Date": "date"})
df_final.insert(1, "payment", 1)
df_final.insert(2 , "info", "")

df_final = df_final.rename(columns={"Merchant": "payee"})
column_to_move = df_final.pop("payee")
df_final.insert(3, "payee", column_to_move)

df_final.insert(4 , "memo", "")
df_final = df_final.rename(columns={"Amount": "amount"})
df_final.insert(6 , "category", "")
df_final.insert(7 , "tags", "")

# Export file to 
# Get the current date and time
current_date = datetime.datetime.now().strftime("%Y-%m-%d")

# Create the file name with the current date
file_name = f"/home/fabien/Statements/wise_{current_date}.csv"

# Export the DataFrame to CSV with the updated file name
df_final.to_csv(file_name, index=False)
