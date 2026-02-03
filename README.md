# Convertisseur Legacy DAT/CSV (Version 2.0 - Corrigée)

Ce projet contient les outils de conversion pour le format binaire spécifique `categori.dat` (Format 31 octets).

## Mises à jour techniques (v2)
Suite à l'analyse hexadécimale, le format a été corrigé :
- **Taille de bloc** : 31 octets (au lieu de 32).
- **En-tête** : Présence d'un header de 16 octets (`ERO...`) au début du fichier.
- **Padding** : Utilisation du caractère `0xCD` pour le remplissage (fidélité au fichier original).

## Structure du format binaire (.dat)

| Position | Taille | Contenu |
|----------|--------|---------|
| **En-tête** | 16 | Signature `ERO` + métadonnées fixes |
| **0-3** | 4      | CODE (Numérique 4 digits) |
| **4** | 1      | ESPACE (`0x20`) |
| **5-var**| Var    | TEXTE (Latin-1, max 25 chars) |
| **var** | 1      | NULL (`0x00`) Terminateur |
| **var-30**| Var   | PADDING (`0xCD`) |

**Total par enregistrement : 31 octets**

## Scripts

### 1. `dat_to_csv.py`
Lit le fichier binaire.
- Saute automatiquement l'en-tête de 16 octets.
- Lit par blocs de 31 octets.
- Extrait Code et Texte (arrête la lecture au NULL).

### 2. `csv_to_dat.py`
Reconstruit le fichier binaire.
- Écrit l'en-tête original (indispensable pour la compatibilité).
- Formate les données sur 31 octets.
- Remplit l'espace vide avec `0xCD`.

## Utilisation

```bash
# Convertir DAT -> CSV
python dat_to_csv.py

# Convertir CSV -> DAT
python csv_to_dat.py
```
