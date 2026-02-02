import csv
import os

# --- CONFIGURATION ---
INPUT_FILE = 'categories_hd.csv'
OUTPUT_FILE = 'categori_hd_regen.dat'
BLOCK_SIZE = 32
ENCODING = 'latin-1'
CSV_DELIMITER = ';'

def main():
    if not os.path.exists(INPUT_FILE):
        print(f"Erreur : Le fichier {INPUT_FILE} est introuvable.")
        return

    print(f"Génération de {OUTPUT_FILE} depuis {INPUT_FILE}...")
    
    with open(INPUT_FILE, 'r', newline='', encoding=ENCODING) as f_in, open(OUTPUT_FILE, 'wb') as f_out:
        reader = csv.reader(f_in, delimiter=CSV_DELIMITER)
        
        count = 0
        for row in reader:
            if not row or len(row) < 2:
                continue
                
            code_input = row[0].strip()
            text_input = row[1].strip()
            
            # --- CONSTRUCTION DU BLOC (32 OCTETS) ---
            
            # 1. CODE (4 octets)
            # Formatage : Si numérique, on padde avec des 0 (202 -> 0202)
            # Sinon on aligne à gauche avec des espaces
            if code_input.isdigit():
                code_formatted = f"{int(code_input):04d}"
            else:
                code_formatted = code_input[:4].ljust(4)
            
            part_code = code_formatted.encode(ENCODING)

            # 2. SEPARATEUR (1 octet)
            part_sep = b'\x20' # Espace

            # 3. TEXTE (Variable, suivi d'un NULL)
            # Calcul de l'espace disponible pour le texte :
            # 32 (Total) - 4 (Code) - 1 (Sep) - 1 (Null obligatoire) = 26 octets max
            max_text_len = BLOCK_SIZE - len(part_code) - len(part_sep) - 1
            
            part_text = text_input.encode(ENCODING)[:max_text_len]
            part_null = b'\x00'
            
            # 4. PADDING (Remplissage)
            # On calcule ce qu'il reste à combler pour atteindre 32 octets
            current_len = len(part_code) + len(part_sep) + len(part_text) + len(part_null)
            padding_len = BLOCK_SIZE - current_len
            part_padding = b'\x00' * padding_len
            
            # Assemblage
            final_block = part_code + part_sep + part_text + part_null + part_padding
            
            # Sécurité finale avant écriture
            if len(final_block) != BLOCK_SIZE:
                # Ne devrait théoriquement pas arriver avec le calcul ci-dessus
                print(f"Erreur dimensionnelle ligne {count}")
                final_block = final_block[:BLOCK_SIZE].ljust(BLOCK_SIZE, b'\x00')

            f_out.write(final_block)
            count += 1

    print(f"Succès : {count} blocs écrits (Format strict 32o).")

if __name__ == "__main__":
    main()
