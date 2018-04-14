import pymysql
import pymysql.cursors
import names
import random
import datetime
from random import randint

conn= pymysql.connect(host='localhost',
                        user='root',
                        password='12345',
                        db='basketballer' )
cur=conn.cursor()

"""Création de listes utiles"""
team = ["Hawks", "Celtics", "Nets", "Hornets", "Bulls", "Cavaliers", "Mavericks", "Nuggets", "Pistons", "Warriors", "Rockets", "Pacers", "Clippers", "Lakers", "Grizzlies", "Heat", "Bucks", "Timberwolves", "Pelicans", "Knicks", "Thunder", "Magic", "76ers", "Suns", "Trail Blazers", "Kings", "Spurs", "Raptors", "Jazz", "Wizards"]
town = ["Atlanta", "Bonston", "Brooklyn", "Charlotte", "Chicago", "Cleveland", "Dallas", "Denver", "Detroit", "Golden State", "Houston", "Indiana", "LA", "Los Angeles", "Memphis", "Miami", "Milwaukee", "Minnesota", "New Orleans", "New York", "Oklahoma City", "Orlando", "Philadelphia", "Phoenix", "Portland", "Sacramento", "San Antonio", "Toronto", "Utah", "Washington"]
country = ["Etats-Unis", "Canada"]
taille = [5.8, 5.9, 5.10, 5.11, 6, 6.1, 6.2, 6.3, 6.4, 6.5, 6.6, 6.7, 6.8, 6.9, 6.10, 6.11, 7, 7.1, 7.2, 7.3, 7.4, 7.5, 7.6, 7.7, 7.8, 7.9, 7.10]
role = ["Meneur", "Arrière", "Ailier", "Ailler fort", "Pivot"]

"""Création d'équipe"""
i=0
while (i < 30):
    
    if town[i] == "Toronto":
        pays = country[1]
    else:
        pays = country[0]
        
    year = random.randint(1946, 1995)
    month = random.randint(1,12)
    day = random.randint(1,28)
    fondation = datetime.date(year, month, day)
    
    equipe = "INSERT INTO equipe(num_equipe, nom_equipe, ville, pays, fondation) VALUES ("'"{0}"'", "'"{1}"'", "'"{2}"'", "'"{3}"'", "'"{4}"'");".format(i, team[i], town[i], pays, fondation)
    cur.execute(equipe)
    i = i+1

"""Création de joueurs"""
j=0
while (j<500):
    
    year = random.randint(1975, 2001)
    month = random.randint(1,12)
    day = random.randint(1,28)
    naissance = datetime.date(year, month, day)

    if random.randint(0,100)>25:
        main = 'true'
    else:
        main = 'false'
    
    joueur = "INSERT INTO joueur(id_joueur, prenom, nom_famille, naissance, taille_ft, poids_lbs, role, est_droitier, dist_bras_ft) VALUES ("'"{0}"'", "'"{1}"'", "'"{2}"'","'"{6}"'","'"{3}"'","'"{4}"'","'"{5}"'","'{7}'","'"{3}"'");".format(j, names.get_first_name(gender='male'), names.get_last_name(), taille[randint(0,25)], randint(160,260), role[randint(0,4)], naissance, main)
    cur.execute(joueur)
    j = j+1

"""Création de contrats"""
equipe = 0
joueur = 0
while equipe<30:
    joueurMax = 0
    while joueurMax<15:
        dateDebut = datetime.date(randint(2010,2013), randint(1,12), randint(1,28))
        dateFin = datetime.date(randint(2019,2025), randint(1,12), randint(1,28))
        contrat = "INSERT INTO contrat(num_equipe, id_joueur, debut_incl, fin_excl, dossard) VALUES ("'"{0}"'", "'"{1}"'", "'"{2}"'", "'"{3}"'", "'"{4}"'");".format(equipe, joueur, dateDebut, dateFin, joueurMax)
        cur.execute(contrat)
        joueur = joueur+1
        joueurMax = joueurMax+1
    equipe = equipe+1

"""Création de parties"""
annee = 2014
while annee<2019:
    k=0
    """Création de séries éliminatoires"""
    a=0
    while a<3:
        serie = "INSERT INTO serie (annee, num_serie) VALUES ("'"{0}"'", "'"{1}"'")".format(annee, a)
        cur.execute(serie)
        a = a+1
    while k<160:
        if k<20:
            mois = 10
            jour = k+1
        elif 20<=k<40:
            mois = 11
            jour = (k-20)+1
        elif 40<=k<60:
            mois = 12
            jour = (k-40)+1
        elif 60<=k<80:
            mois = 1
            jour = (k-60)+1
        elif 80<=k<100:
            mois = 2
            jour = (k-80)+1
        elif 100<=k<120:
            mois = 3
            jour = (k-100)+1
        elif 120<=k<140:
            mois = 4
            jour = (k-120)+1
        else:
            mois = 5
            jour = (k-140)+1

        if k<148:
            loc = randint(0,29)
            inv = randint(0,29)
            while loc == inv:
                inv = randint(0,29)
            partie = "INSERT INTO partie (annee, num_partie, ville, date_partie) VALUES ("'"{0}"'", "'"{1}"'", "'"{2}"'","'"{3}"'");".format(annee, k, town[loc], datetime.date(annee, mois, jour))
            cur.execute(partie)
        elif 148<=k<152:
            """Création d'une sous-série (appartient)"""
            loc = 5
            inv = 1
            partie = "INSERT INTO partie (annee, num_partie, ville, date_partie) VALUES ("'"{0}"'", "'"{1}"'", "'"{2}"'","'"{3}"'");".format(annee, k, town[loc], datetime.date(annee, mois, jour))
            cur.execute(partie)
            sousSerie = "INSERT INTO appartient(annee, num_partie, num_serie, num_sous_serie) VALUES ("'"{0}"'", "'"{1}"'", "'"{2}"'", "'"{3}"'");".format(annee, k, 0, k-147)
            cur.execute(sousSerie)
        elif 152<=k<156:
            loc = 9
            inv = 26
            partie = "INSERT INTO partie (annee, num_partie, ville, date_partie) VALUES ("'"{0}"'", "'"{1}"'", "'"{2}"'","'"{3}"'");".format(annee, k, town[loc], datetime.date(annee, mois, jour))
            cur.execute(partie)
            sousSerie = "INSERT INTO appartient(annee, num_partie, num_serie, num_sous_serie) VALUES ("'"{0}"'", "'"{1}"'", "'"{2}"'", "'"{3}"'");".format(annee, k, 1, k-151)
            cur.execute(sousSerie)
        else:
            loc = 26
            inv = 5
            partie = "INSERT INTO partie (annee, num_partie, ville, date_partie) VALUES ("'"{0}"'", "'"{1}"'", "'"{2}"'","'"{3}"'");".format(annee, k, town[loc], datetime.date(annee, mois, jour))
            cur.execute(partie)
            sousSerie = "INSERT INTO appartient(annee, num_partie, num_serie, num_sous_serie) VALUES ("'"{0}"'", "'"{1}"'", "'"{2}"'", "'"{3}"'");".format(annee, k, 2, k-155)
            cur.execute(sousSerie)
        
        
        """Relation d'une partie entre deux équipes (concoure)"""
        concoure = "INSERT INTO concoure(annee, num_partie, num_equipe_loc, num_equipe_vis) VALUES ("'"{0}"'", "'"{1}"'", "'"{2}"'", "'"{3}"'");".format(annee, k, loc, inv)
        cur.execute(concoure)

        """Participer à une partie (participe)"""
        joueurLoc = 0 + (15*loc)
        joueurMaxLoc = 0
        minutes = 0
        secondes = 20
        while joueurMaxLoc<12:
            participeLoc = "INSERT INTO participe(id_joueur, annee, num_partie , minutes) VALUES ("'"{0}"'", "'"{1}"'", "'"{2}"'", "'"{3}"'");".format(joueurLoc, annee, k, randint(0,30))
            cur.execute(participeLoc)
            
            """Création d'actions dans une partie"""
            moment = datetime.time(0,minutes,secondes)
            
            action1 = "INSERT INTO action (annee, num_partie, instant, type_action, id_joueur) VALUES ("'"{0}"'", "'"{1}"'", "'"{2}"'", "'"lancer"'", "'"{3}"'");".format(annee, k, moment, joueurLoc)
            cur.execute(action1)
            
            if random.randint(0,100)>35:
                panier = 1
            else:
                panier = 0
                
            lancer1 = "INSERT INTO lancer (annee, num_partie, instant, type_lancer, est_panier) VALUES ("'"{0}"'", "'"{1}"'", "'"{2}"'", "'"1pt"'", "'"{3}"'");".format(annee, k, moment, panier)
            cur.execute(lancer1)
            secondes = secondes+20
            moment = datetime.time(0,minutes,secondes)

            action2 = "INSERT INTO action (annee, num_partie, instant, type_action, id_joueur) VALUES ("'"{0}"'", "'"{1}"'", "'"{2}"'", "'"lancer"'", "'"{3}"'");".format(annee, k, moment, joueurLoc)
            cur.execute(action2)
            
            if random.randint(0,100)>35:
                panier = 1
            else:
                panier = 0
                
            lancer2 = "INSERT INTO lancer (annee, num_partie, instant, type_lancer, est_panier) VALUES ("'"{0}"'", "'"{1}"'", "'"{2}"'", "'"2pt"'", "'"{3}"'");".format(annee, k, moment, panier)
            cur.execute(lancer2)
            minutes = minutes+1
            secondes = 0
            moment = datetime.time(0,minutes,secondes)

            action3 = "INSERT INTO action (annee, num_partie, instant, type_action, id_joueur) VALUES ("'"{0}"'", "'"{1}"'", "'"{2}"'", "'"lancer"'", "'"{3}"'");".format(annee, k, moment, joueurLoc)
            cur.execute(action3)
            
            if random.randint(0,100)>35:
                panier = 1
            else:
                panier = 0
                
            lancer3 = "INSERT INTO lancer (annee, num_partie, instant, type_lancer, est_panier) VALUES ("'"{0}"'", "'"{1}"'", "'"{2}"'", "'"3pt"'", "'"{3}"'");".format(annee, k, moment, panier)
            cur.execute(lancer3)
            secondes = secondes+20
            moment = datetime.time(0,minutes,secondes)
            
            action4 = "INSERT INTO action (annee, num_partie, instant, type_action, id_joueur) VALUES ("'"{0}"'", "'"{1}"'", "'"{2}"'", "'"revirement"'", "'"{3}"'");".format(annee, k, moment, joueurLoc)
            cur.execute(action4)

            revirement = "INSERT INTO revirement (annee, num_partie, instant, type_revirement) VALUES ("'"{0}"'", "'"{1}"'", "'"{2}"'","'"offensif"'");".format(annee, k, moment)
            cur.execute(revirement)
            secondes = secondes+20
            moment = datetime.time(0,minutes,secondes)

            action5 = "INSERT INTO action (annee, num_partie, instant, type_action, id_joueur) VALUES ("'"{0}"'", "'"{1}"'", "'"{2}"'", "'"faute"'", "'"{3}"'");".format(annee, k, moment, joueurLoc)
            cur.execute(action5)

            faute = "INSERT INTO faute (annee, num_partie, instant, type_faute) VALUES ("'"{0}"'", "'"{1}"'", "'"{2}"'","'"defensif"'");".format(annee, k, moment)
            cur.execute(faute)
            minutes = minutes+1
            secondes = 0        
        
            
            joueurLoc = joueurLoc+1
            joueurMaxLoc = joueurMaxLoc+1
            
        joueurInv = 0+(15*inv)
        joueurMaxInv = 0
        minutes = 0
        secondes = 10
        while joueurMaxInv<12:
            participeInv = "INSERT INTO participe(id_joueur, annee, num_partie , minutes) VALUES ("'"{0}"'", "'"{1}"'", "'"{2}"'", "'"{3}"'");".format(joueurInv, annee, k, randint(0,30))
            cur.execute(participeInv)

            """Création d'actions dans une partie"""
            moment = datetime.time(0,minutes,secondes)
            action1 = "INSERT INTO action (annee, num_partie, instant, type_action, id_joueur) VALUES ("'"{0}"'", "'"{1}"'", "'"{2}"'", "'"lancer"'", "'"{3}"'");".format(annee, k, moment, joueurInv)
            cur.execute(action1)
            
            if random.randint(0,100)>50:
                panier = 1
            else:
                panier = 0
                
            lancer1 = "INSERT INTO lancer (annee, num_partie, instant, type_lancer, est_panier) VALUES ("'"{0}"'", "'"{1}"'", "'"{2}"'", "'"1pt"'", "'"{3}"'");".format(annee, k, moment, panier)
            cur.execute(lancer1)
            secondes = secondes+20
            moment = datetime.time(0,minutes,secondes)

            action2 = "INSERT INTO action (annee, num_partie, instant, type_action, id_joueur) VALUES ("'"{0}"'", "'"{1}"'", "'"{2}"'", "'"lancer"'", "'"{3}"'");".format(annee, k, moment, joueurInv)
            cur.execute(action2)
            
            if random.randint(0,100)>50:
                panier = 1
            else:
                panier = 0
                
            lancer2 = "INSERT INTO lancer (annee, num_partie, instant, type_lancer, est_panier) VALUES ("'"{0}"'", "'"{1}"'", "'"{2}"'", "'"2pt"'", "'"{3}"'");".format(annee, k, moment, panier)
            cur.execute(lancer2)

            if 3<joueurMaxInv<8 and panier == 1:
                assist = "INSERT INTO assiste(id_joueur,annee,num_partie,instant) VALUES ("'"{0}"'", "'"{1}"'", "'"{2}"'", "'"{3}"'");".format(joueurInv-1, annee, k, moment)
                cur.execute(assist)
                
            secondes = secondes+20
            moment = datetime.time(0,minutes,secondes)            

            action3 = "INSERT INTO action (annee, num_partie, instant, type_action, id_joueur) VALUES ("'"{0}"'", "'"{1}"'", "'"{2}"'", "'"lancer"'", "'"{3}"'");".format(annee, k, moment, joueurInv)
            cur.execute(action3)
            
            if random.randint(0,100)>50:
                panier = 1
            else:
                panier = 0
                
            lancer3 = "INSERT INTO lancer (annee, num_partie, instant, type_lancer, est_panier) VALUES ("'"{0}"'", "'"{1}"'", "'"{2}"'", "'"3pt"'", "'"{3}"'");".format(annee, k, moment, panier)
            cur.execute(lancer3)
            minutes = minutes+1
            secondes = 10
            moment = datetime.time(0,minutes,secondes)

            action4 = "INSERT INTO action (annee, num_partie, instant, type_action, id_joueur) VALUES ("'"{0}"'", "'"{1}"'", "'"{2}"'", "'"rebond"'", "'"{3}"'");".format(annee, k, moment, joueurInv)
            cur.execute(action4)

            rebond = "INSERT INTO rebond (annee, num_partie, instant, type_rebond) VALUES ("'"{0}"'", "'"{1}"'", "'"{2}"'","'"defensif"'");".format(annee, k, moment)
            cur.execute(rebond)
            secondes = secondes+20
            moment = datetime.time(0, minutes, secondes)

            action5 = "INSERT INTO action (annee, num_partie, instant, type_action, id_joueur) VALUES ("'"{0}"'", "'"{1}"'", "'"{2}"'", "'"faute"'", "'"{3}"'");".format(annee, k, moment, joueurInv)
            cur.execute(action5)

            faute = "INSERT INTO faute (annee, num_partie, instant, type_faute) VALUES ("'"{0}"'", "'"{1}"'", "'"{2}"'","'"offensif"'");".format(annee, k, moment)
            cur.execute(faute)
            secondes = secondes+20
            moment = datetime.time(0, minutes, secondes)

            action6 = "INSERT INTO action (annee, num_partie, instant, type_action, id_joueur) VALUES ("'"{0}"'", "'"{1}"'", "'"{2}"'", "'"revirement"'", "'"{3}"'");".format(annee, k, moment, joueurInv)
            cur.execute(action6)

            revirement = "INSERT INTO revirement (annee, num_partie, instant, type_revirement) VALUES ("'"{0}"'", "'"{1}"'", "'"{2}"'","'"defensif"'");".format(annee, k, moment)
            cur.execute(revirement)
            minutes = minutes+1
            secondes = 10
            
            joueurInv = joueurInv+1
            joueurMaxInv = joueurMaxInv+1
            
        k = k+1
    annee = annee+1

cur.close()
conn.commit()
conn.close()

