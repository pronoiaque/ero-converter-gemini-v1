import csv
import os
import struct

# CONFIGURATION STRICTE
INPUT_FILE = 'categori.dat' # Ou categori_hd.dat
OUTPUT_FILE = 'categories_hd.csv'
BLOCK_SIZE = 31      # Analyse hexadécimale confirme 31 octets exacts
HEADER_SIZE = 16     # Signature "ERO..." au début
ENCODING = 'latin-1'

def main():
    if not os.path.exists(INPUT_FILE):
        print(f"Erreur : {INPUT_FILE} introuvable.")
        return

    print(f"Lecture de {INPUT_FILE} (Blocs: {BLOCK_SIZE}o, Header: {HEADER_SIZE}o)...")
    
    with open(INPUT_FILE, 'rb') as f_in, open(OUTPUT_FILE, 'w', newline='', encoding=ENCODING) as f_out:
        writer = csv.writer(f_out, delimiter=';')
        
        # 1. Gestion de l'En-tête
        # On lit les 16 premiers octets pour vérifier/sauter
        header = f_in.read(HEADER_SIZE)
        if len(header) < HEADER_SIZE:
            print("Fichier trop court (pas d'en-tête valide).")
            return
            
        print(f"En-tête détecté (Signature: {header[:3]}). Début des données à l'octet {HEADER_SIZE}.")

        count = 0
        while True:
            block = f_in.read(BLOCK_SIZE)
            if not block:
                break
                
            # Gestion des blocs incomplets (fin de fichier)
            if len(block) < BLOCK_SIZE:
                continue 

            try:
                # Structure : [CODE 4o] [ESPACE 1o] [TEXTE... ] [NULL] [PADDING]
                
                # Extraction CODE
                code_raw = block[0:4].decode(ENCODING, errors='ignore')
                
                # Extraction TEXTE (du 6ème octet jusqu'au NULL)
                # Note: block[4] est l'espace (0x20)
                raw_text = block[5:]
                null_index = raw_text.find(b'\x00')
                
                if null_index != -1:
                    clean_text = raw_text[:null_index]
                else:
                    clean_text = raw_text # Cas rare sans NULL
                
                text_final = clean_text.decode(ENCODING).strip()
                
                writer.writerow([code_raw, text_final])
                count += 1

            except Exception as e:
                print(f"Erreur bloc {count}: {e}")

    print(f"Succès : {count} enregistrements extraits.")

if __name__ == "__main__":
    main()
