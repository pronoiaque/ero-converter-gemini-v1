# Convertisseur Version 6 (Mode Flexible)

Cette version implémente l'hypothèse où le CODE et l'ESPACE font partie intégrante du TEXTE.

## Différence clé
- **Avant (V4/V5)** : Le programme forçait le Code à faire 4 caractères (ex: `202` -> `0202`).
- **Maintenant (V6)** : Le programme concatène simplement `Code + Espace + Libelle`.
  - Si votre CSV contient `202`, il écrira `202`.
  - Si votre CSV contient `0202`, il écrira `0202`.

## Utilisation

### CSV vers DAT
```bash
python csv_to_dat_flexible.py
```
*Prend par défaut `for_gemini.csv`.*

### DAT vers CSV
```bash
python dat_to_csv_flexible.py
```
