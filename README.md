# Descripteur-Flou
Projet modélisation M2 VMI - Descripteur de position relative basé sur les sous-ensembles flous

Pour exécuter le programme, il est nécessaire de passer dans un environnement virtuel.

Sur Linux dans le dossier source:

	pip3 install virtualenv
	python -m venv env
	source ./env/bin/activate
	pip install -r requirements.txt

Sur Windows dans le dossier source :

	pip install virtualenv
	python -m venv env
	./env/Scripts/activate
	pip install -r requirements.txt

(Si une erreur de segmentation se présente changer la version de numpy à 1.18.5 dans requirements.txt et exécutez pip install -r requirements.txt)
