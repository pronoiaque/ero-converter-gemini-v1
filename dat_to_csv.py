import csv
import os

# --- CONFIGURATION ---
INPUT_FILE = 'categori_hd.dat'
OUTPUT_FILE = 'categories_hd.csv'
BLOCK_SIZE = 32
ENCODING = 'latin-1'
CSV_DELIMITER = ';'

def main():
    if not os.path.exists(INPUT_FILE):
        print(f"Erreur : Le fichier {INPUT_FILE} est introuvable.")
        return

    print(f"Lecture de {INPUT_FILE}...")
    
    with open(INPUT_FILE, 'rb') as f_in, open(OUTPUT_FILE, 'w', newline='', encoding=ENCODING) as f_out:
        writer = csv.writer(f_out, delimiter=CSV_DELIMITER)
        # writer.writerow(['CODE', 'LIBELLE']) # Décommenter pour ajouter un header
        
        count = 0
        while True:
            # Lecture du bloc fixe
            block = f_in.read(BLOCK_SIZE)
            if not block:
                break
            
            if len(block) < BLOCK_SIZE:
                print(f"Avertissement : Bloc final incomplet ignoré ({len(block)} octets)")
                break

            try:
                # 1. Extraction du CODE (4 premiers octets)
                code_raw = block[0:4].decode(ENCODING, errors='ignore')
                
                # 2. Vérification du séparateur (Octet 4)
                # On ne bloque pas si absent, mais on note que c'est la structure attendue
                # separator = block[4] 

                # 3. Extraction du TEXTE (Octet 5 jusqu'à la fin)
                # Logique stricte : Lire jusqu'au premier NULL (0x00)
                raw_text_data = block[5:]
                null_index = raw_text_data.find(b'\x00')
                
                if null_index != -1:
                    # On ne garde que ce qu'il y a avant le NULL (ignore le garbage)
                    clean_text_bytes = raw_text_data[:null_index]
                else:
                    # Si pas de NULL (bloc plein), on prend tout
                    clean_text_bytes = raw_text_data
                
                text_final = clean_text_bytes.decode(ENCODING).strip()
                
                writer.writerow([code_raw, text_final])
                count += 1

            except Exception as e:
                print(f"Erreur de parsing au bloc {count}: {e}")

    print(f"Terminé : {count} enregistrements exportés vers {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
