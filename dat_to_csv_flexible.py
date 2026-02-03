import csv
import os
import sys

# --- CONFIGURATION FLEXIBLE ---
if len(sys.argv) > 1:
    INPUT_FILE = sys.argv[1]
else:
    INPUT_FILE = 'categori_flexible.dat'

OUTPUT_FILE = 'export_flexible.csv'
BLOCK_SIZE = 31
START_OFFSET = 52
ENCODING = 'latin-1'

def main():
    if not os.path.exists(INPUT_FILE):
        print(f"Erreur : {INPUT_FILE} introuvable.")
        return

    print(f"Lecture flexible de {INPUT_FILE}...")
    
    with open(INPUT_FILE, 'rb') as f_in, open(OUTPUT_FILE, 'w', newline='', encoding=ENCODING) as f_out:
        writer = csv.writer(f_out, delimiter=';')
        
        f_in.seek(START_OFFSET)

        while True:
            block = f_in.read(BLOCK_SIZE)
            if not block or len(block) < BLOCK_SIZE: break

            null_idx = block.find(b'\x00')
            if null_idx != -1:
                content_bytes = block[:null_idx]
            else:
                content_bytes = block
            
            full_text = content_bytes.decode(ENCODING).strip()
            
            if not full_text: continue

            # Séparation sur le premier espace
            parts = full_text.split(' ', 1)
            
            if len(parts) == 2:
                code = parts[0]
                libelle = parts[1]
            else:
                code = parts[0]
                libelle = ""
            
            writer.writerow([code, libelle])

    print(f"Extraction terminée vers {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
