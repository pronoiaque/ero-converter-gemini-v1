import csv
import os

# --- CONFIGURATION (FORMAT HD - ALIGNEMENT STRICT) ---
INPUT_FILE = 'categories_hd.csv'
OUTPUT_FILE = 'categori_hd_regen.dat'
BLOCK_SIZE = 31
ENCODING = 'latin-1'

# 1. EN-TÊTE (0-16) : Signature ERO + Métadonnées
HEADER_BYTES = b'\x45\x52\x4F\x00\xFD\xFD\xFD\xFD\xDD\xDD\xDD\xDD\x41\x00\x00\x00'

# 2. BLOC TAMPON (16-52) : 36 octets
# Contient un préfixe technique (5 octets) + un enregistrement "<vide>" (31 octets)
# Indispensable pour que le premier vrai code (ex: 0003) démarre à l'octet 52.
BUFFER_BLOCK = (
    b'\xC0\x05\x00\x00\x5C'       # Préfixe système (5 octets)
    b'<vide>\x00'                 # Contenu technique
    b'\xCC' * 24                  # Padding spécifique (0xCC = Ì)
)
# Note : 5 + 7 + 24 = 36 octets.
# 16 (Header) + 36 (Buffer) = 52. Le compte est bon.

def main():
    if not os.path.exists(INPUT_FILE):
        print(f"Erreur : {INPUT_FILE} introuvable.")
        return

    print(f"Génération de {OUTPUT_FILE}...")
    print("Application du correctif d'alignement (Offset 52)...")
    
    with open(INPUT_FILE, 'r', newline='', encoding=ENCODING) as f_in, open(OUTPUT_FILE, 'wb') as f_out:
        # Écriture de la structure technique fixe
        f_out.write(HEADER_BYTES)
        f_out.write(BUFFER_BLOCK)
        
        reader = csv.reader(f_in, delimiter=';')
        count = 0
        
        for row in reader:
            if not row or len(row) < 2: continue
            
            code_str = row[0].strip()
            text_str = row[1].strip()
            
            # --- BLOC STANDARD (31 OCTETS) ---
            
            # 1. CODE (4 chars)
            if code_str.isdigit():
                code_fmt = f"{int(code_str):04d}"
            else:
                code_fmt = code_str[:4].ljust(4)
            
            # 2. DATA
            # 31 (Total) - 4 (Code) - 1 (Espace) - 1 (Null) = 25 dispo
            max_text_len = BLOCK_SIZE - 4 - 1 - 1
            
            part_code = code_fmt.encode(ENCODING)
            part_sep = b'\x20'
            part_text = text_str.encode(ENCODING)[:max_text_len]
            part_null = b'\x00'
            
            payload = part_code + part_sep + part_text + part_null
            
            # 3. PADDING
            # Utilisation de 0xCD (Í) pour fidélité aux blocs de données
            padding_char = b'\xCD' 
            
            padding_len = BLOCK_SIZE - len(payload)
            if padding_len > 0:
                part_padding = padding_char * padding_len
            else:
                part_padding = b''
            
            final_block = payload + part_padding
            
            # Sécurité taille
            if len(final_block) != BLOCK_SIZE:
                 final_block = final_block[:BLOCK_SIZE].ljust(BLOCK_SIZE, padding_char)

            f_out.write(final_block)
            count += 1

    print(f"Terminé : {count} enregistrements écrits.")
    print(f"Taille finale attendue : 52 + ({count} * 31) octets.")

if __name__ == "__main__":
    main()
