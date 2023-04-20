#!/usr/bin/env bash
#VINHAS Jérémy
if [ $# -ne 4 ]; then
	echo "./jemegare.sh <adresse> <durée> <bmin> <nombre>
	Usage : <adresse> l'adresse a renseigné
		<durée> la durée de stationnement
		<bmin> le nombre minimum de places libres
		<nombre> le nombre de parking que vous souhaitez afficher" 1>&2 2>/dev/null
	exit 1
fi

repertoire=~/jemegare

if [ ! -d $repertoire ]; then
	mkdir ~/jemegare | cd $repertoire
fi
adresse=~/jemegare/adresse_nantes.json
tarif=~/jemegare/tarif_parking.json
dispo=~/jemegare/dispo_parking.json

if [ ! -f $adresse ]; then
	wget -O $adresse https://data.nantesmetropole.fr/explore/dataset/244400404_adresses-postales-nantes-metropole/download/?format=json&timezone=Europe/Berlin&lang=fr 
fi

if [ ! -f $tarif ] || [ $(find $tarif -mtime +30) ]; then
	echo -e "Téléchargement du fichier des tarifs des parkings sur Nantes"
	wget -O $tarif https://data.nantesmetropole.fr/explore/dataset/244400404_parkings-publics-nantes-tarification-horaire/download/?format=json&timezone=Europe/Berlin&lang=fr
fi

if [ ! -f $dispo ] || [ $(find $dispo -mmin +60) ]; then
	echo -e "Téléchargement du fichier des disponibilités des parkings sur Nantes"
	wget -O $dispo https://data.nantesmetropole.fr/explore/dataset/244400404_parkings-publics-nantes-disponibilites/download/?format=json&timezone=Europe/Berlin&lang=fr
fi


if [ $? -eq 3 ]; then
	echo "L'adresse $1 n'a pas été trouvé" 1>&2
	exit 6 
else
	lattitude=$(./adress2coords.py "adresse_nantes.json" "$1" | sed 's/^.//;s/.$//;s/,//' | cut -d " " -f 1) #sed permet d'enlever les caractères indésirables de la sortie adress2coords
	longitude=$(./adress2coords.py "adresse_nantes.json" "$1" | sed 's/^.//;s/.$//;s/,//' | cut -d " " -f 2)
	parking=$(./availabilities.py "dispo_parking.json" "$3" | ./jemegare.py "tarif_parking.json" "$lattitude" "$longitude" "$2" | head -n $4) 
	#head permet de sélectionner le nb de parking à afficher
	echo "$parking "" " #permet d'afficher les parkings lignes par lignes
	exit 0 
fi




