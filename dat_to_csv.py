import csv
import os

# --- CONFIGURATION (FORMAT HD / 52 OCTETS OFFSET) ---
INPUT_FILE = 'categori_hd.dat'
OUTPUT_FILE = 'categories_hd.csv'
BLOCK_SIZE = 31       # Taille standard des enregistrements
START_OFFSET = 52     # Header (16) + Séquence d'initialisation (36) = 52
ENCODING = 'latin-1'

def main():
    if not os.path.exists(INPUT_FILE):
        print(f"Erreur : {INPUT_FILE} introuvable.")
        return

    print(f"Lecture de {INPUT_FILE}...")
    print(f"Offset de démarrage : {START_OFFSET} octets")
    print(f"Taille de bloc : {BLOCK_SIZE} octets")
    
    with open(INPUT_FILE, 'rb') as f_in, open(OUTPUT_FILE, 'w', newline='', encoding=ENCODING) as f_out:
        writer = csv.writer(f_out, delimiter=';')
        
        # 1. Sauter l'en-tête et le bloc technique
        # On se place directement au début des données utiles (octet 52)
        f_in.seek(START_OFFSET)

        count = 0
        while True:
            block = f_in.read(BLOCK_SIZE)
            
            # Fin de fichier
            if not block or len(block) < BLOCK_SIZE:
                break

            try:
                # Structure du bloc 31 octets :
                # [CODE 4o] [ESPACE 1o] [TEXTE... ] [NULL] [PADDING]
                
                # Extraction CODE
                code_raw = block[0:4].decode(ENCODING, errors='ignore')
                
                # Extraction TEXTE (du 6ème octet jusqu'au NULL)
                raw_text = block[5:]
                null_index = raw_text.find(b'\x00')
                
                if null_index != -1:
                    clean_text = raw_text[:null_index]
                else:
                    clean_text = raw_text
                
                text_final = clean_text.decode(ENCODING).strip()
                
                # Filtre : On ignore les lignes vides ou techniques si nécessaire
                if code_raw.strip(): 
                    writer.writerow([code_raw, text_final])
                    count += 1

            except Exception as e:
                print(f"Erreur bloc {count}: {e}")

    print(f"Succès : {count} enregistrements extraits vers {OUTPUT_FILE}.")

if __name__ == "__main__":
    main()
