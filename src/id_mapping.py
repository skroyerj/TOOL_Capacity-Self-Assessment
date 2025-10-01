import pandas as pd
import hashlib
import os

# Fil til mapping
MAP_FILE = "IDs/id_map.csv"

def generate_id(email, existing_ids):
    """Lav et stabilt anonymt ID baseret på hash, men undgå kollisioner."""
    # Tag de første 8 tegn af hash
    base_id = hashlib.sha256(email.encode()).hexdigest()[:8].upper()
    # Hvis ID'et allerede findes, tilføj ekstra tegn
    new_id = base_id
    i = 1
    while new_id in existing_ids:
        new_id = f"{base_id}_{i}"
        i += 1
    return new_id

def update_mapping(new_data_file, output_file):
    # Indlæs nye data
    df = pd.read_excel(new_data_file)

    # Indlæs eller opret mapping
    if os.path.exists(MAP_FILE):
        mapping = pd.read_csv(MAP_FILE)
        print("jeg fandt en eksisterende mapping fil.")
    else:
        mapping = pd.DataFrame(columns=["email", "anon_id"])
        print("jeg oprettede en ny mapping fil.")

    # Lav et opslags-dict for hastighed
    email_to_id = dict(zip(mapping["email"], mapping["anon_id"]))
    existing_ids = set(mapping["anon_id"])

    # Find nye emails som ikke er i mapping
    new_emails = [e for e in df["Mail"] if e not in email_to_id]

    # Tilføj nye emails til mapping
    for email in new_emails:
        anon_id = generate_id(email, existing_ids)
        mapping = pd.concat([mapping, pd.DataFrame([[email, anon_id]], columns=["email","anon_id"])], ignore_index=True)
        email_to_id[email] = anon_id
        existing_ids.add(anon_id)

    # Tilføj anonym ID til datasættet
    df["anon_id"] = df["Mail"].map(email_to_id)

    # Gem opdateret mapping
    mapping.to_csv(MAP_FILE, index=False)

    # Gem anonymiseret datasæt
    df.drop(columns=["Mail"], inplace=True)  # fjern email, behold anon_id
    df.to_excel(output_file, index=False)

    print(f"✅ Færdig! Gemte anonymiseret data i {output_file} og opdaterede {MAP_FILE}")



update_mapping("IDs/xlsx_csv/rawdata/AGILE week 5 - Weekly check-in questions.xlsx", "IDs/xlsx_csv/anonymiseddata/AGILE_5_anon.xlsx")