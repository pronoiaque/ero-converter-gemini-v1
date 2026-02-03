import csv
import os

# CONFIGURATION STRICTE
INPUT_FILE = 'categories_hd.csv'
OUTPUT_FILE = 'categori_regen.dat'
BLOCK_SIZE = 31
ENCODING = 'latin-1'

# Signature binaire exacte de l'en-tête (récupérée de votre fichier)
# ERO + padding spécifique
DEFAULT_HEADER = b'\x45\x52\x4F\x00\xFD\xFD\xFD\xFD\xDD\xDD\xDD\xDD\x41\x00\x00\x00'

def main():
    if not os.path.exists(INPUT_FILE):
        print(f"Erreur : Le fichier {INPUT_FILE} est introuvable.")
        return

    print(f"Génération de {OUTPUT_FILE} (Format 31 octets)...")
    
    with open(INPUT_FILE, 'r', newline='', encoding=ENCODING) as f_in, open(OUTPUT_FILE, 'wb') as f_out:
        # 1. Écriture de l'en-tête obligatoire
        f_out.write(DEFAULT_HEADER)
        
        reader = csv.reader(f_in, delimiter=';')
        count = 0
        
        for row in reader:
            if not row or len(row) < 2: continue
            
            code_str = row[0].strip()
            text_str = row[1].strip()
            
            # --- CONSTRUCTION DU BLOC (31 OCTETS) ---
            
            # 1. CODE (4 chars)
            if code_str.isdigit():
                code_fmt = f"{int(code_str):04d}"
            else:
                code_fmt = code_str[:4].ljust(4)
            
            # 2. DATA
            # Code (4) + Espace (1) + Texte (N) + Null (1) <= 31
            # Espace dispo pour le texte = 31 - 4 - 1 - 1 = 25 caractères max !
            max_text_len = BLOCK_SIZE - 4 - 1 - 1
            
            part_code = code_fmt.encode(ENCODING)      # 4 octets
            part_sep = b'\x20'                         # 1 octet
            part_text = text_str.encode(ENCODING)[:max_text_len]
            part_null = b'\x00'                        # 1 octet
            
            payload = part_code + part_sep + part_text + part_null
            
            # 3. PADDING (Remplissage propre avec 0xCD)
            # Standardisation à 0xCD (comme vu dans le dump) pour fidélité max
            padding_char = b'\xCD' 
            
            padding_len = BLOCK_SIZE - len(payload)
            if padding_len > 0:
                part_padding = padding_char * padding_len
            else:
                part_padding = b''
            
            final_block = payload + part_padding
            
            # Sécurité
            if len(final_block) != BLOCK_SIZE:
                final_block = final_block[:BLOCK_SIZE]

            f_out.write(final_block)
            count += 1

    print(f"Terminé : {count} blocs écrits (+ En-tête).")

if __name__ == "__main__":
    main()
