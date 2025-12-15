# id_mapping.py
import pandas as pd
import hashlib
from pathlib import Path

# -----------------------------
# Brugervenlige variabler (kan ændres frit)
INPUT_FILES = [Path("data/input_data/AGILE_5.xlsx"),
          Path("data/input_data/AGILE_6.xlsx"),
          Path("data/input_data/AGILE_7.xlsx"),
          Path("data/input_data/AGILE_8.xlsx"),
          Path("data/input_data/AGILE_9.xlsx")]

    
OUTPUT_DIR = Path("data/output_data")  # hvor skal anonymiseret gemmes?
ID_MAP_FILE = Path("data/id_map.csv")  # hvor gemmes id_map?

EMAIL_COLUMN = "Mail"     # hvad hedder kolonnen med email?
NAME_COLUMN = "Navn"      # hvis du har navne i en kolonne
# -----------------------------

# læs eksisterende mapping hvis den findes

if ID_MAP_FILE.exists():
    id_map = pd.read_csv(ID_MAP_FILE, dtype=str).set_index(EMAIL_COLUMN)["Anon_ID"].to_dict()
else:
    id_map = {}

def get_or_create_id(email: str) -> str:
    if email not in id_map:
        anon_id = hashlib.sha256(email.encode("utf-8")).hexdigest()[:10]
        id_map[email] = anon_id
    return id_map[email]

print("input-filer: ",INPUT_FILES)

for infile in INPUT_FILES:
    if not infile.exists():
        print("file not found")
    else:
        df = pd.read_excel(infile)
        df["Anon_ID"] = df[EMAIL_COLUMN].astype(str).map(get_or_create_id)
        df = df.drop(columns=[NAME_COLUMN, EMAIL_COLUMN])  # fjern følsom kolonne
    
        outfile = OUTPUT_DIR / f"{infile.stem}_anon.xlsx"
        df.to_excel(outfile, index=False)
        print(f"Anonymised {infile} → {outfile}")

# gem opdateret mapping til sidst
pd.DataFrame(list(id_map.items()), columns=[EMAIL_COLUMN, "Anon_ID"]).to_csv(ID_MAP_FILE, index=False)
print(f"Mapping updated: {ID_MAP_FILE}")