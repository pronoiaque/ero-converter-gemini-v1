import csv
import os
import sys

# --- CONFIGURATION ---
if len(sys.argv) > 1:
    INPUT_FILE = sys.argv[1]
else:
    # Recherche automatique d'un fichier .dat récent si categori.dat n'existe pas
    INPUT_FILE = 'categori_hd.dat'

OUTPUT_FILE = 'categories_hd.csv'
BLOCK_SIZE = 31
START_OFFSET = 52     # Header (16) + Buffer (36)
ENCODING = 'latin-1'

def main():
    if not os.path.exists(INPUT_FILE):
        print(f"Erreur : {INPUT_FILE} introuvable.")
        return

    print(f"Lecture de {INPUT_FILE}...")
    
    with open(INPUT_FILE, 'rb') as f_in, open(OUTPUT_FILE, 'w', newline='', encoding=ENCODING) as f_out:
        writer = csv.writer(f_out, delimiter=';')
        
        # Sauter la zone technique (Header + Buffer)
        f_in.seek(START_OFFSET)

        count = 0
        while True:
            block = f_in.read(BLOCK_SIZE)
            if not block or len(block) < BLOCK_SIZE:
                break

            try:
                # Structure: [CODE 4] [ESPACE 1] [TEXTE...] [NULL] [PADDING]
                code_raw = block[0:4].decode(ENCODING, errors='ignore')
                
                raw_text = block[5:]
                null_index = raw_text.find(b'\x00')
                
                if null_index != -1:
                    clean_text = raw_text[:null_index]
                else:
                    clean_text = raw_text
                
                text_final = clean_text.decode(ENCODING).strip()
                
                if code_raw.strip():
                    writer.writerow([code_raw, text_final])
                    count += 1

            except Exception as e:
                print(f"Erreur bloc {count}: {e}")

    print(f"Succès : {count} enregistrements extraits vers {OUTPUT_FILE}.")

if __name__ == "__main__":
    main()
