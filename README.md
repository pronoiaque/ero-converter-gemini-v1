# Convertisseur Legacy DAT/CSV

Ce projet contient des outils de conversion bidirectionnelle entre un format binaire propriétaire (`.dat`) et un format lisible (`.csv`). 

L'objectif est d'assurer une **réversibilité parfaite** tout en nettoyant les artefacts mémoire (padding sale) présents dans les fichiers originaux.

## Structure du format binaire (.dat)

Le fichier est composé d'enregistrements de taille fixe (**32 octets**).

| Position | Taille | Contenu | Règles |
|----------|--------|---------|--------|
| 0-3      | 4      | CODE    | Numérique, cadré à gauche ou avec zéros (ex: "0202") |
| 4        | 1      | ESPACE  | Séparateur obligatoire (`0x20`) |
| 5-30     | 26     | TEXTE   | Libellé (encodage Latin-1) |
| Var.     | 1      | NULL    | Terminateur de chaîne (`0x00`) obligatoire |
| Var.     | Var.   | PADDING | Remplissage jusqu'à 32 octets (nettoyé avec `0x00`) |

## Scripts

### 1. `dat_to_csv.py`
Lit le fichier binaire.
- **Nettoyage :** Lit jusqu'au caractère `NULL` et ignore les "données fantômes" (résidus de mémoire) qui suivent.
- **Sortie :** CSV standard (séparateur `;`).

### 2. `csv_to_dat.py`
Reconstruit le fichier binaire.
- **Contraintes :**
    - Force le Code sur 4 caractères.
    - Insère l'espace séparateur.
    - Tronque le texte si nécessaire pour garantir la présence du NULL final.
    - Comble le reste du bloc avec des zéros (`0x00`) pour un fichier propre (sans garbage).

## Utilisation

```bash
# Vers CSV
python dat_to_csv.py

# Vers DAT (Régénération)
python csv_to_dat.py
```
