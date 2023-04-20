#!/usr/bin/env python3
#VINHAS Jérémy
import json
import sys
if len(sys.argv) !=3:
	print(f"""Recherche de coordonnées associés à une adresse.
	Usage : <fichier de coordonnées> <adresse>""", file=sys.stderr)
	exit(1)
adresse = (sys.argv[2]).encode('latin-1').lower() #Lower permet de tout mettre en  minuscule, afin que même si l'on ne met pas les majuscule, l'adresse sera trouvé.
with open(sys.argv[1]) as fichier_json:
	adresse_postale=json.load(fichier_json)
	for rec in adresse_postale:
		if rec["fields"]["adresse"].encode('latin-1').lower() == adresse: # encode permet de prendre en compte les caractères spéciaux
			coordonne=rec["fields"]["geo_shape"]["coordinates"]
			print(f"{coordonne}")
			exit(0)
print(f"Impossible de trouver l'adresse dans la base de données", file=sys.stderr)
exit(3)
