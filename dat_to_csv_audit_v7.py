import csv
import os
import sys

# --- CONFIGURATION ---
if len(sys.argv) > 1:
    INPUT_FILE = sys.argv[1]
else:
    INPUT_FILE = 'categori_corrected.dat'

OUTPUT_FILE = 'export_audit_v7.csv'
BLOCK_SIZE = 31
START_OFFSET = 52 
ENCODING = 'latin-1'

def main():
    if not os.path.exists(INPUT_FILE):
        print(f"Erreur : Fichier '{INPUT_FILE}' introuvable.")
        return

    print(f"--- AUDIT BINAIRE ERO ---")
    print(f"Lecture de : {INPUT_FILE}")
    
    with open(INPUT_FILE, 'rb') as f_in, open(OUTPUT_FILE, 'w', newline='', encoding=ENCODING) as f_out:
        writer = csv.writer(f_out, delimiter=';')
        
        # Vérification Header (optionnelle mais recommandée)
        header = f_in.read(START_OFFSET)
        if len(header) < START_OFFSET:
            print("Erreur: Fichier trop court ou sans en-tête valide.")
            return

        # Vérification qu'il n'y a pas de BOM UTF-8 résiduel dans le buffer (Signature EF BB BF)
        if b'\xef\xbb\xbf' in header:
             print("ALERTE CRITIQUE : Des octets BOM (EF BB BF) ont été détectés dans l'en-tête !")
        
        count = 0
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

            parts = full_text.split(' ', 1)
            if len(parts) == 2:
                writer.writerow([parts[0], parts[1]])
            else:
                writer.writerow([parts[0], ""])
            count += 1

    print(f"--- TERMINÉ ---")
    print(f"{count} lignes extraites.")

if __name__ == "__main__":
    main()
