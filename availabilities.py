#!/usr/bin/env python3
#VINHAS Jérémy
import json
import sys
if len(sys.argv)<3:
	print(f"""{sys.argv[0]} <fichier de disponibilité> <nombre de place minimum>
	Avec <fichier de dispobibilité> le chemin d'accès vers le fichier JSON de place libre
	<nombre de place minimum>, le nombre de place libre afin qu'on retourne l'identifiant d'un parking""", file=sys.stderr)
	exit(1)
try:
	nb_place= int(sys.argv[2])
except ValueError:
	print(f"L'argument {sys.argv[2]} doit être numérique !", file=sys.stderr)
	exit(2)
with open(sys.argv[1]) as dispo_json:
	dict_parking=json.load(dispo_json)
	parking_dispo=[]
	for i in dict_parking:
		if nb_place < i["fields"]["grp_disponible"]:
			parking_dispo.append(i["fields"]["idobj"])
if len(parking_dispo)==0:
	print("Pas de parking disponible avec ces conditions")
else:
	for i in parking_dispo:
		print(i)
exit(0)
