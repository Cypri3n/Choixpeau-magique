'''
LE CHOIXPEAU MAGIQUE
Ce programme prédit la maison d'un profil selon ses caractéristiques à partir d'un algorithme de k plus proches voisins,
Et peut être executé avec des profils préexistants. 
Il possède également un proccessus de validaion croisée visant à garantir son efficacité.

AUTEURS:
Cyprien Venard
Ewen Le Grand
Martin Ray


LICENCE:
CC-BY-NC-SA


VERSION:
1.8.1


DATE DE DERNIERE REVISION:
01/02/2024


ADRESSE GITHUB: 
https://github.com/Cypri3n/Choixpeau-magique/tree/main

'''

# coding: utf-8

# Import des modules
import csv
import time
from math import sqrt
from random import randint

# VARIABLES
# Table des personnages et leurs caractéristiques
house_tab = []

# Profil par défaut
new_students = [{'Courage': 9, 'Ambition': 2, 'Intelligence': 8, 'Good': 9},
           {'Courage': 6, 'Ambition': 7, 'Intelligence': 8, 'Good': 7},
           {'Courage': 3, 'Ambition': 8, 'Intelligence': 6, 'Good': 3},
           {'Courage': 2, 'Ambition': 3, 'Intelligence': 7, 'Good': 8},
           {'Courage': 3, 'Ambition': 4, 'Intelligence': 8, 'Good': 8}]

# Mise en page
yellow = "\033[93m"  # YELLOW
green = "\033[92m"  # GREEN
red = "\033[91m"  # RED
blue = "\033[0;34m" # BLUE
purple = "\033[0;35m" # PURPLE
bold = "\033[1m" # BOLD
italic = "\033[3m" # ITALIC
underline = "\033[4m"# UNDERLINE
reset = "\033[0m"  # RESET

# FONCTIONS ET PROCEDURES
# Distance 
def distance(perso_cible, voisin):
    return sqrt( (int(voisin['Courage']) - int(perso_cible['Courage']))**2 + 
    (int(voisin['Ambition']) - int(perso_cible['Ambition']))**2 + 
    (int(voisin['Intelligence']) - int(perso_cible['Intelligence']))**2 + 
    (int(voisin['Good']) - int(perso_cible['Good']))**2)

def ajout_distances(students_tab, unknow_student):
    for student in students_tab:
        student['Distance'] = distance(unknow_student, student)
    return students_tab

# Algorithme des kppv
def best_house(tab):
    houses = {}
    for voisin in tab:
        if voisin['House'] in houses:
            houses[voisin['House']] += 1
        else:
            houses[voisin['House']] = 1
    maximum = 0
    for house, nb in houses.items():
        if nb > maximum:
            maximum = nb
            top_house = house
    return top_house

# Vérification croisée
def validation_croisée():
    nb_tests = 100
    best_perf = 0
    best_k = 0

    # Extraction d'un tiers des données pour test de validation  
    def creation_donnees_test(tab):
        joueurs_test = []
        copie_joueurs = house_tab[:]
        for _ in range(len(copie_joueurs) // 4):
            joueurs_test.append(copie_joueurs.pop(randint(0, len(copie_joueurs) - 1)))
        return joueurs_test, copie_joueurs

    for k in range(1, 31):
        bingo = 0
        for test in range(nb_tests):
            joueurs_test, joueurs_reference = creation_donnees_test(house_tab)
            for joueur_cible in joueurs_test:
                joueurs_reference = ajout_distances(joueurs_reference, joueur_cible)
                other_voisins = sorted(joueurs_reference, key=lambda x: x['Distance'])
                if best_house(other_voisins[:k]) == joueur_cible['House']:
                    bingo += 1
        perf = round(bingo / len(joueurs_test))
        if perf > best_perf:
            best_perf = perf
            best_k = k
        print(f"Pourcentage de réussite avec k = {k} : {purple}{perf} %{reset}.")

    print(f"Meilleur k : {green}{best_k}{reset}, avec {purple}{best_perf} %{reset} de réussite.\n")
    time.sleep(1)
    print(f"{italic}Nous utiliserons donc k = {best_k}.{reset}\n")
    time.sleep(2)
    return best_k

# Profil de l'utilisateur
def user_characteristics():
        student_courage = input("Quelle est votre courage ?")
        student_ambition = input("Quelle est votre ambition ?")
        student_intelligence = input("Quelle est votre intelligence ?")
        student_good = input("Quelle est votre bontée ?")
        return {'Courage': student_courage, 'Ambition': student_ambition, 'Intelligence': student_intelligence, 'Good': student_good}

# Affichage
def validation_wanted_or_not():
    answer_validation = input(f"\nVoulez-vous faire une validation croisée ou définir k à 5 ?\nFaire une validation croisée => {bold}entrez 1{reset}\nDéfinir k à 5 => {bold}entrez 2{reset}\n => ")
    if answer_validation == '1':
        return validation_croisée()
    else:
        print(f"\n{italic}Nous utiliserons donc k = 5.{reset}\n")
        return 5

def printing(neighbor):
    if neighbor['House'] == 'Gryffindor':
        print(f"{italic}{neighbor['Name']}{reset}, de {red}{neighbor['House']}{reset}, à {purple}{neighbor['Distance']}{reset} de distance,")
    elif neighbor['House'] == 'Ravenclaw':
        print(f"{italic}{neighbor['Name']}{reset}, de {blue}{neighbor['House']}{reset}, à {purple}{neighbor['Distance']}{reset} de distance,")
    elif neighbor['House'] == 'Hufflepuff':
        print(f"{italic}{neighbor['Name']}{reset}, de {yellow}{neighbor['House']}{reset}, à {purple}{neighbor['Distance']}{reset} de distance,")
    elif neighbor['House'] == 'Slytherin':
        print(f"{italic}{neighbor['Name']}{reset}, de {green}{neighbor['House']}{reset}, à {purple}{neighbor['Distance']}{reset} de distance,")
    time.sleep(0.5)

def printing_house(tab, k):
    if best_house(tab[:k]) == 'Gryffindor':
        print(f" => La maison est donc : {red}{bold}{underline}{best_house(tab[:k])}{reset} !\n")
        #print(house_tab[['Minerva McGonagall']])
    elif best_house(tab[:k]) == 'Ravenclaw':
        print(f"=> La maison est donc : {blue}{bold}{underline}{best_house(tab[:k])}{reset} !\n")
    elif best_house(tab[:k]) == 'Hufflepuff':
        print(f"=> La maison est donc : {yellow}{bold}{underline}{best_house(tab[:k])}{reset} !\n")
    elif best_house(tab[:k]) == 'Slytherin':
        print(f"=> La maison est donc : {green}{bold}{underline}{best_house(tab[:k])}{reset} !\n")

def continue_or_stop():
    return input(f"Souhaitez-vous continuez ?\nVoir les maisons des nouveaux élèves => {bold}entrez 1{reset}\nDéterminer quelle maison me correspond le mieux => {bold}entrez 2{reset}\n{italic}attention : tout autre choix vous ramènera chez les moldus.{reset}\n => ")

def leaving():
    print(f"{italic}Vous avez décidé de nous quitter.{reset}")
    time.sleep(1.5)
    print("\nLe poudlard express vous attend pour rentrer.")
    time.sleep(1.5)
    print("\nAu revoir !\n")
    time.sleep(1)  

# DATA
# Extraction des données
with open("Caracteristiques_des_persos.csv", mode='r', encoding='utf-8') as f:
  reader = csv.DictReader(f,delimiter=';')
  caracteristiques_tab = [{key : value for key, value in element.items()} for element in reader]
with open("Characters.csv", mode='r', encoding='utf-8') as f:
    reader = csv.DictReader(f, delimiter=';')
    characters_tab = [{key : value.replace('\xa0', ' ') for key, value in element.items()} for element in reader]    

# Fusion des tables
for kaggle_character in characters_tab:
    for poudlard_character in caracteristiques_tab:
        if kaggle_character['Name'] == poudlard_character['Name']:
            kaggle_character.update(poudlard_character)
            house_tab.append(kaggle_character)  


# IHM
answer = input(f"\nBienvenue à Poudlard, que souhaitez-vous faire ?\n\nVoir les maisons des nouveaux élèves => {bold}entrez 1{reset}\nDéterminer quelle\
maison me correspond le mieux => {bold}entrez 2{reset}\n{italic}attention : tout autre choix vous ramènera chez les moldus.{reset}\n => ")

while answer in ('1', '2'):
    if answer == '1':
        # Profil par défauts
        k = validation_wanted_or_not()
        for student in new_students:
            house_tab = ajout_distances(house_tab, student)
            neighbors = sorted(house_tab, key=lambda x: x['Distance'])
            print(f"Pour un profil de {student}, on a :")
            for neighbor in neighbors[:k]:
                printing(neighbor)
            printing_house(neighbors, k)
            time.sleep(2)
        answer = continue_or_stop()
    else:
        # Profil utilisateur 
        k = validation_wanted_or_not()
        print("Veuillez vous noter sur chacune de ces caractéristiques avec un chiffre entre 0 et 9...")
        time.sleep(1.5)
        student_user = user_characteristics()
        house_tab = ajout_distances(house_tab, student_user)
        neighbors = sorted(house_tab, key=lambda x: x['Distance'])
        print("\nPour votre profil, on a :")
        for neighbor in neighbors[:k]:
            printing(neighbor)
        time.sleep(1)
        printing_house(neighbors, k)
        time.sleep(2)
        answer = continue_or_stop()

leaving()
