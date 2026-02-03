# Convertisseur Legacy DAT/CSV - Version 3 (Alignement HD Fix)

Ce pack contient les scripts corrigés pour l'alignement strict requis par le logiciel "ERO" (Format HD).

## Problème Résolu (V3)
Le logiciel final affichait un décalage car il attend les données à l'octet **52**, alors que la version précédente écrivait à l'octet 47 ou 16.
Ce correctif insère la séquence technique exacte (Header + Buffer) pour aligner parfaitement les données.

## Structure du fichier généré

1. **00 - 16** : En-tête ERO (16 octets)
2. **16 - 21** : Préfixe système (5 octets)
3. **21 - 52** : Bloc technique `<vide>` (31 octets)
   *(Total zone technique : 52 octets)*
4. **52 - Fin** : Enregistrements (Blocs de 31 octets)

## Scripts

### `csv_to_dat.py` (Prioritaire)
Utilisez ce script pour regénérer votre fichier `.dat`.
- Prend `categories_hd.csv` en entrée.
- Produit `categori_hd_regen.dat`.
- **Garantie** : Le code "0003" (ou le premier de votre liste) sera écrit exactement à l'octet 52.

### `dat_to_csv.py`
Pour extraire les données d'un fichier `.dat` existant.
- Configuré pour ignorer les 52 premiers octets techniques.

## Utilisation

```bash
python csv_to_dat.py
```
Ensuite, renommez `categori_hd_regen.dat` en `categori_hd.dat` pour le tester dans votre application.
