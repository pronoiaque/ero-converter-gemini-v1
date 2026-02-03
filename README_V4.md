# Convertisseur Legacy DAT/CSV - Version 4 (Clonage & Timestamp)

Cette version inclut la correction stricte de la structure binaire (copiée du fichier de référence `categori_Perso_OK.dat`) et la gestion dynamique des fichiers.

## Fonctionnalités V4
1. **Clonage Binaire Parfait** : Reproduction exacte de l'en-tête et du buffer `<vide>` pour une compatibilité 100% avec le logiciel ERO.
2. **Noms de fichiers dynamiques** :
   - Entrée : Par défaut `categories_hd.csv` ou via argument ligne de commande.
   - Sortie : Format `categori_YYYYMMDD_HHMMSS.dat` (Timestamp).

## Utilisation

### 1. Générer le fichier .dat (CSV vers DAT)
Le script générera un fichier daté (ex: `categori_20231025_143000.dat`).

**Mode standard (utilise `categories_hd.csv`) :**
```bash
python csv_to_dat.py
```

**Mode fichier spécifique :**
```bash
python csv_to_dat.py mon_fichier_perso.csv
```

### 2. Extraire en CSV (DAT vers CSV)
```bash
python dat_to_csv.py [fichier.dat]
```

## Structure Technique (Rappel)
- **00-16** : Header (Signature ERO)
- **16-52** : Buffer Système (`<vide>`)
- **52-Fin** : Données (Blocs de 31 octets, Padding `Í` / `0xCD`)
