import csv
import os
import sys

# --- CONFIGURATION FLEXIBLE (V6) ---
if len(sys.argv) > 1:
    INPUT_FILE = sys.argv[1]
elif os.path.exists('for_gemini.csv'):
    INPUT_FILE = 'for_gemini.csv'
else:
    INPUT_FILE = 'categories_hd.csv'

OUTPUT_FILE = 'categori_flexible.dat'
BLOCK_SIZE = 31
ENCODING = 'latin-1'

# --- ZONE TECHNIQUE ---
HEADER_BYTES = bytes.fromhex('45524F00FDFDFDFDDDDDDDDD41000000')
BUFFER_BYTES = bytes.fromhex('41000000003C766964653E20CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC')

def main():
    if not os.path.exists(INPUT_FILE):
        print(f"ERREUR : Fichier {INPUT_FILE} absent.")
        return

    print(f"--- MODE FLEXIBLE (CODE INCLUS DANS TEXTE) ---")
    print(f"Entrée : {INPUT_FILE}")
    print(f"Sortie : {OUTPUT_FILE}")
    
    with open(INPUT_FILE, 'r', newline='', encoding=ENCODING) as f_in, open(OUTPUT_FILE, 'wb') as f_out:
        reader = csv.reader(f_in, delimiter=';')
        
        # 1. Écriture Header + Buffer
        f_out.write(HEADER_BYTES)
        f_out.write(BUFFER_BYTES)
        
        count = 0
        for row in reader:
            if not row or len(row) < 2: continue
            
            code_brut = row[0].strip().replace('\ufeff', '')
            texte_brut = row[1].strip()
            
            # Construction flexible : concaténation simple
            full_string = f"{code_brut} {texte_brut}"
            
            # Max 30 chars (31 - 1 Null)
            max_content_len = BLOCK_SIZE - 1
            
            payload = full_string.encode(ENCODING)[:max_content_len]
            part_null = b'\x00'
            
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

    print(f"Terminé : {count} enregistrements générés.")

if __name__ == "__main__":
    main()
