import csv
import os
import sys

# --- CONFIGURATION (V7 - Nettoyage BOM & Flexibilité) ---
# Entrée : par défaut 'for_gemini.csv', sinon argument
if len(sys.argv) > 1:
    INPUT_FILE = sys.argv[1]
elif os.path.exists('for_gemini.csv'):
    INPUT_FILE = 'for_gemini.csv'
else:
    INPUT_FILE = 'categories_hd.csv'

OUTPUT_FILE = 'categori_corrected.dat'
BLOCK_SIZE = 31
# Important: On lira le CSV en 'utf-8-sig' pour éliminer automatiquement le BOM (ï»¿) s'il existe.
CSV_ENCODING = 'utf-8-sig' 
# Important: On écrira le DAT en 'latin-1' (format legacy).
DAT_ENCODING = 'latin-1'

# --- ZONE TECHNIQUE (VALIDÉE) ---
# Header (16) + Buffer (36) = 52 octets
HEADER_BYTES = bytes.fromhex('45524F00FDFDFDFDDDDDDDDD41000000')
BUFFER_BYTES = bytes.fromhex('41000000003C766964653E20CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC')

def main():
    if not os.path.exists(INPUT_FILE):
        print(f"ERREUR : Fichier source '{INPUT_FILE}' introuvable.")
        return

    print(f"--- GÉNÉRATION DE BINAIRE ERO (V7 - Anti-BOM) ---")
    print(f"Source : {INPUT_FILE}")
    print(f"Cible  : {OUTPUT_FILE}")
    
    # 1. Lecture CSV avec gestion automatique du BOM (utf-8-sig)
    # L'encodage 'utf-8-sig' est la clé : il consomme les 3 octets EF BB BF silencieusement.
    try:
        f_in = open(INPUT_FILE, 'r', newline='', encoding=CSV_ENCODING)
    except UnicodeDecodeError:
        # Fallback si le fichier est en ANSI/Latin-1 pur sans BOM
        print("Avertissement: Échec lecture UTF-8, tentative en Latin-1...")
        f_in = open(INPUT_FILE, 'r', newline='', encoding='latin-1')
        
    with f_in, open(OUTPUT_FILE, 'wb') as f_out:
        reader = csv.reader(f_in, delimiter=';')
        
        # 2. Injection Structure Technique (Offset 0-52)
        f_out.write(HEADER_BYTES)
        f_out.write(BUFFER_BYTES)
        
        count = 0
        for row in reader:
            if not row or len(row) < 2: continue
            
            # Nettoyage supplémentaire au cas où (espaces parasites)
            code_brut = row[0].strip()
            texte_brut = row[1].strip()
            
            # Concaténation Flexible
            full_string = f"{code_brut} {texte_brut}"
            
            # --- Contraintes Physiques ---
            # Max 30 chars (31 - 1 Null)
            max_content_len = BLOCK_SIZE - 1
            
            # Encodage vers le format cible (Latin-1)
            # errors='replace' permet d'éviter le crash si un charactère est impossible (ex: emoji)
            payload = full_string.encode(DAT_ENCODING, errors='replace')[:max_content_len]
            part_null = b'\x00'
            
            # Padding (0xCD)
            padding_len = BLOCK_SIZE - len(payload) - 1
            if padding_len > 0:
                part_padding = b'\xCD' * padding_len
            else:
                part_padding = b''
            
            final_block = payload + part_null + part_padding
            
            if len(final_block) != BLOCK_SIZE:
                 final_block = final_block[:BLOCK_SIZE]
            
            f_out.write(final_block)
            count += 1

    print(f"--- SUCCÈS ---")
    print(f"{count} enregistrements écrits sans BOM parasite.")

if __name__ == "__main__":
    main()
