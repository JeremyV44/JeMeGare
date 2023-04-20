#!/usr/bin/env python3
#VINHAS Jérémy
import sys
import json
import prog_distance #j'ai renommé le prgramme pour que ce soit plus lisible car distance.distance porte à confusion
import time
	
if len(sys.argv) !=5:
	print(f"""{sys.argv[0]} <fichier de tarification parking> <latitude> <longitude> <durée de stationnement prévu> 
	Permet de retourner les parkings les plus proche ainsi que la tarifcation de chacun.""")
try:
	latitude1=float(sys.argv[2])
	longitude1=float(sys.argv[3])
except ValueError :
	print(f"Les arguments {sys.argv[2]} et {sys.argv[3]} doivent être numériques !", file=sys.stderr)
	exit(1)
	
minutes=int(sys.argv[4])
tri={}	

for i in sys.stdin:
	parking_dispo=int(i) # Récupération des id de parking du programme availabilities.py	
	with open(sys.argv[1]) as tarif_json:
		dict_json=json.load(tarif_json)
		for j in dict_json:
		
			fields=j["fields"]
			idobj=int(j["fields"]["idobj"])
			nom_parking=fields["nom_du_parking"]
			latitude2=fields["location"][1]
			longitude2=fields["location"][0]
			parking = prog_distance.distance(latitude1,longitude1,latitude2,longitude2)
			
			if parking_dispo == idobj:
				t= int(time.strftime('%H', time.localtime()))
				try:
					if t>9 and t <18:
						if minutes < 10:
							tarif = fields["10min"]
						elif minutes < 20:
							tarif= fields["20min"]
						elif minutes < 30:
							tarif= fields["30min"]
						elif minutes < 40:
							tarif= fields["40min"]
						elif minutes < 50:
							tarif = fields["50min"]
						elif minutes < 60:
							tarif = fields["1h"]
						elif minutes < 90:
							tarif = fields["1h30"]
						elif minutes < 120:
							tarif= fields["2h"]
						elif minutes < 150:
							tarif= fields['2h30']
						elif minutes < 180:
							tarif = fields["3h"]
						else:
							tarif = fields["11h"]
					else:
						if minutes < 10:
							tarif = fields["nuit_10min"]
						elif minutes < 20:
							tarif= fields["nuit_20min"]
						elif minutes < 30:
							tarif= fields["nuit_30min"]
						elif minutes < 40:
							tarif= fields["nuit_40min"]
						elif minutes < 50:
							tarif = fields["nuit_50min"]
						elif minutes < 60:
							tarif = fields["nuit_1h"]
						elif minutes < 90:
							tarif = fields["nuit_1h30"]
						elif minutes < 120:
							tarif= fields["nuit_2h"]
						elif minutes < 150:
							tarif= fields["nuit_2h30"]
						else: 
							tarif = fields["nuit_3h_et"]
				except KeyError:
					tarif= "Pas de tarif pour cette durée"
						
				tri[parking] = (nom_parking,tarif)
				
liste_parking= sorted(tri.items(), key=lambda item:item[0])
for i in range(len(liste_parking)):
	print(liste_parking[i][1][0],':',liste_parking[i][1][1], '€')
	
	
	
	
	
	
