# ERO Legacy Converter (Version 7.0 - Anti-BOM)

![Version](https://img.shields.io/badge/version-7.0-blue)
![Fix](https://img.shields.io/badge/fix-UTF8_BOM_Removal-green)
![Status](https://img.shields.io/badge/status-Production_Critical-red)

## Problème Critique Résolu (V7)
Les versions précédentes (V4-V6) convertissaient littéralement le contenu du fichier CSV.
Or, de nombreux éditeurs (Excel, Notepad) ajoutent une signature invisible au début du fichier CSV : le **BOM (Byte Order Mark)** (`0xEF 0xBB 0xBF`).

**Symptôme :**
Ce BOM était écrit tel quel dans le fichier binaire `.dat`, créant un décalage de 3 octets.
Le premier enregistrement devenait `ï»¿0000` au lieu de `0000`, rendant le fichier illisible pour le logiciel ERO dès la première ligne.

**Solution V7 :**
Le script de génération détecte et élimine automatiquement cette signature invisible avant le traitement.

---

## Manuel Technique

### 1. Génération (`csv_to_dat_final_v7.py`)

Convertit un CSV en `.dat` en nettoyant les artefacts d'encodage.

* **Entrée :** Fichier CSV (UTF-8 avec ou sans BOM, ou Latin-1).
* **Sortie :** `categori_corrected.dat`.
* **Alignement :** Garantie absolue que le premier octet de donnée utile (le "0" de "0000") se trouve à l'offset **52** (0x34).

**Commande :**
```bash
python csv_to_dat_final_v7.py [votre_fichier.csv]
```

### 2. Audit (`dat_to_csv_audit_v7.py`)

Permet de vérifier qu'aucun artefact n'a survécu.

**Commande :**
```bash
python dat_to_csv_audit_v7.py categori_corrected.dat
```

---

## Structure Binaire Validée

Le fichier `.dat` généré respecte strictement cette cartographie mémoire :

| Zone | Offset Décimal | Contenu Attendu |
| :--- | :--- | :--- |
| **Header** | 0 - 16 | Signature ERO |
| **Buffer** | 16 - 52 | Séquence technique `<vide>` |
| **Record 1** | **52** | **"0"** (Premier caractère du code `0000`) |

*Si vous voyez des caractères étranges (`ï»¿`) entre l'offset 52 et 55 dans un éditeur hexadécimal, le fichier est corrompu. La V7 empêche cela.*

## Avertissement

Ne modifiez pas le fichier binaire généré avec un éditeur de texte classique. Utilisez uniquement ces scripts pour toute modification.
