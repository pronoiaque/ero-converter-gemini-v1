import csv
import os
import sys
from datetime import datetime

# --- CONFIGURATION ---
# 1. FICHIER D'ENTRÉE
# Par défaut 'categories_hd.csv', ou premier argument de la ligne de commande
if len(sys.argv) > 1:
    INPUT_FILE = sys.argv[1]
else:
    INPUT_FILE = 'categories_hd.csv'

# 2. FICHIER DE SORTIE
# Format : categori_YYYYMMDD_HHMMSS.dat
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
OUTPUT_FILE = f"categori_{timestamp}.dat"

# 3. PARAMÈTRES BINAIRES (V4 - CLONAGE PERFECT)
BLOCK_SIZE = 31
ENCODING = 'latin-1'

# HEADER EXACT (0-16) copié de Perso_OK
HEADER_BYTES = bytes.fromhex('45524F00FDFDFDFDDDDDDDDD41000000')

# BLOC TAMPON EXACT (16-52) copié de Perso_OK (36 octets)
BUFFER_BLOCK = bytes.fromhex(
    '4100000000'                      # Préfixe (5 octets)
    '3C766964653E20'                  # "<vide> " (7 octets)
    'CCCCCCCCCCCCCCCCCCCCCCCC'        # Padding CC (24 octets)
)

def main():
    if not os.path.exists(INPUT_FILE):
        print(f"Erreur : Le fichier d'entrée '{INPUT_FILE}' est introuvable.")
        print(f"Usage : python csv_to_dat.py [nom_du_fichier.csv]")
        return

    print(f"Source : {INPUT_FILE}")
    print(f"Cible  : {OUTPUT_FILE}")
    print("Génération en cours (Structure V4 - Clonage Perso_OK)...")
    
    with open(INPUT_FILE, 'r', newline='', encoding=ENCODING) as f_in, open(OUTPUT_FILE, 'wb') as f_out:
        # Écriture de la structure de démarrage (52 octets au total)
        f_out.write(HEADER_BYTES)
        f_out.write(BUFFER_BLOCK)
        
        reader = csv.reader(f_in, delimiter=';')
        count = 0
        
        for row in reader:
            if not row or len(row) < 2: continue
            
            code_str = row[0].strip()
            text_str = row[1].strip()
            
            # --- BLOC RECORD (31 OCTETS) ---
            
            # 1. CODE (4 chars)
            if code_str.isdigit():
                code_fmt = f"{int(code_str):04d}"
            else:
                code_fmt = code_str[:4].ljust(4)
            
            # 2. DATA
            max_text_len = BLOCK_SIZE - 4 - 1 - 1
            
            part_code = code_fmt.encode(ENCODING)
            part_sep = b'\x20'
            part_text = text_str.encode(ENCODING)[:max_text_len]
            part_null = b'\x00'
            
            payload = part_code + part_sep + part_text + part_null
            
            # 3. PADDING STANDARD (0xCD pour les records)
            padding_char = b'\xCD' 
            padding_len = BLOCK_SIZE - len(payload)
            if padding_len > 0:
                part_padding = padding_char * padding_len
            else:
                part_padding = b''
            
            final_block = payload + part_padding
            
            # Sécurité taille
            if len(final_block) != BLOCK_SIZE:
                final_block = final_block[:BLOCK_SIZE]

            f_out.write(final_block)
            count += 1

    print(f"Terminé : {count} enregistrements écrits dans {OUTPUT_FILE}.")

if __name__ == "__main__":
    main()
