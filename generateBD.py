import pymysql
import pymysql.cursors
import names
import random
import datetime
from random import randint

conn= pymysql.connect(host='localhost',
                        user='root',
cur=conn.cursor()

"""Création de la base de données"""
cmd1 = "DROP DATABASE IF EXISTS basketballer;"
cur.execute(cmd1)
cmd2 = "create database basketballer;"
cur.execute(cmd2)
cmd3 = "use basketballer;"
cur.execute(cmd3)
cmd5 = "CREATE TABLE equipe (num_equipe int, nom_equipe char(20), ville char(20), pays char(20), "\
        "fondation date, PRIMARY KEY(num_equipe));"
cur.execute(cmd5)
cmd6 = "CREATE TABLE joueur (id_joueur int, prenom char(20), nom_famille char(20), naissance date, "\
        "taille_ft real, poids_lbs real, role char(20), est_droitier bool, dist_bras_ft real, PRIMARY KEY(id_joueur));"
cur.execute(cmd6)
cmd7 = "CREATE TABLE partie (annee int, num_partie int, ville char(20), date_partie date, PRIMARY KEY(annee, num_partie));"
cur.execute(cmd7)
cmd8 = "CREATE TABLE serie (annee int, num_serie int, PRIMARY KEY(annee, num_serie));"
cur.execute(cmd8)
cmd9 = "CREATE TABLE appartient(annee int, num_partie int NOT NULL, num_serie int NOT NULL, "\
        "num_sous_serie int NOT NULL, PRIMARY KEY(annee, num_serie, num_sous_serie), UNIQUE (annee, num_partie), "\
        "FOREIGN KEY(annee, num_partie) REFERENCES partie(annee, num_partie) ON DELETE CASCADE, FOREIGN KEY(annee, num_serie) "\
        "REFERENCES serie(annee, num_serie) ON DELETE CASCADE);"
cur.execute(cmd9)
cmd10 = '''
CREATE TRIGGER max7_parties_par_serie
BEFORE INSERT ON appartient
FOR EACH ROW
BEGIN
IF  (0 >= NEW.num_sous_serie) OR (NEW.num_sous_serie > 7)
OR
(	SELECT COUNT(*)
	FROM appartient
	WHERE annee=NEW.annee AND num_serie = NEW.num_serie
	) = 7
THEN SET NEW.annee = null;
END IF;
END; '''
cur.execute(cmd10)
cmd11 = "CREATE TRIGGER ordre_chronologique_serie"\
        " BEFORE INSERT ON appartient"\
        " FOR EACH ROW"\
        " BEGIN"\
        " IF (EXISTS (SELECT NULL"\
        "                        FROM appartient A, partie PN, partie P1"\
        "                        WHERE A.annee=NEW.annee AND A.num_serie=NEW.num_serie"\
        "                        AND A.num_sous_serie =(NEW.num_sous_serie-1)"\
        "                        AND PN.annee = A.annee and PN.num_partie = A.num_partie"\
        "                        AND P1.annee = A.annee AND P1.num_partie = A.num_partie"\
        "                        AND P1.date_partie > PN.date_partie))"\
        " OR"\
        " (EXISTS (SELECT NULL"\
        "                        FROM appartient A, partie PN, partie P2"\
        "                        WHERE A.annee=NEW.annee AND A.num_serie=NEW.num_serie"\
        "                        AND A.num_sous_serie =(NEW.num_sous_serie+1)"\
        "                        AND PN.annee = A.annee and PN.num_partie = A.num_partie"\
        "                        AND P2.annee = A.annee AND P2.num_partie = A.num_partie"\
        "                        AND P2.date_partie < PN.date_partie))"\
        " THEN SET NEW.annee = null;"\
        " END IF;"\
        " END;"
cur.execute(cmd11)
cmd12 = "CREATE TABLE concoure(annee int, num_partie int, num_equipe_loc int NOT NULL, num_equipe_vis int NOT NULL,"\
	" points_loc int, points_vis int, PRIMARY KEY(annee, num_partie),"\
	" FOREIGN KEY(annee, num_partie) REFERENCES partie(annee, num_partie) ON DELETE CASCADE,"\
	" FOREIGN KEY(num_equipe_loc) REFERENCES equipe(num_equipe) ON DELETE CASCADE,"\
	" FOREIGN KEY(num_equipe_vis) REFERENCES equipe(num_equipe) ON DELETE CASCADE);"
cur.execute(cmd12)
cmd13 = " CREATE TRIGGER points_null"\
        " BEFORE INSERT ON concoure"\
        " FOR EACH ROW"\
        " BEGIN"\
        "        IF (NEW.points_loc IS null)"\
        "        THEN SET NEW.points_loc = 0;"\
        "        END IF;"\
        "        IF (NEW.points_vis IS null)"\
        "        THEN SET NEW.points_vis = 0;"\
        "        END IF;"\
        " END;"
cur.execute(cmd13)
cmd14 = "CREATE TABLE contrat(num_equipe int NOT NULL, id_joueur int NOT NULL,"\
	" debut_incl date NOT NULL, fin_excl date, dossard int NOT NULL,"\
	" PRIMARY KEY(id_joueur, debut_incl),"\
	" UNIQUE (num_equipe, debut_incl, dossard),"\
	" FOREIGN KEY(id_joueur) REFERENCES joueur(id_joueur) ON DELETE CASCADE,"\
	" FOREIGN KEY(num_equipe) REFERENCES equipe(num_equipe) ON DELETE CASCADE);"
cur.execute(cmd14)
cmd15 = "CREATE TRIGGER fin_contrat_null"\
        " BEFORE INSERT ON contrat"\
        " FOR EACH ROW"\
        " BEGIN"\
        "        IF (NEW.fin_excl IS null)"\
        "        THEN SET NEW.fin_excl = '9999-12-31';"\
        "        END IF;"\
        " END;"
cur.execute(cmd15)
cmd16 = "CREATE TRIGGER date_coherentes"\
        " BEFORE INSERT ON contrat"\
        " FOR EACH ROW"\
        " BEGIN"\
        "  IF ( NEW.fin_excl <= NEW.debut_incl )"\
        "  THEN SET NEW.debut_incl = null;"\
        "  END IF;"\
        " END;"
cur.execute(cmd16)
cmd17 = "CREATE TRIGGER max_1_dossard"\
        " BEFORE INSERT ON contrat"\
        " FOR EACH ROW"\
        " BEGIN"\
        "  IF(SELECT COUNT(*)"\
        "    FROM contrat"\
        "    WHERE num_equipe = NEW.num_equipe"\
        "      AND debut_incl < NEW.fin_excl AND NEW.debut_incl < fin_excl"\
        "      AND dossard = NEW.dossard"\
        "    ) > 0"\
        "  THEN SET NEW.debut_incl = null;"\
        "  END IF;"\
        " END;"
cur.execute(cmd17)
cmd18 = "CREATE TRIGGER max_1_contrat"\
        " BEFORE INSERT ON contrat"\
        " FOR EACH ROW"\
        " BEGIN"\
        " IF ("\
        "  SELECT COUNT(*)"\
        "  FROM contrat"\
        "  WHERE id_joueur = NEW.id_joueur"\
        "    AND debut_incl < NEW.fin_excl AND NEW.debut_incl < fin_excl"\
        "  ) > 0"\
        " THEN SET NEW.debut_incl = null;"\
        " END IF;"\
        " END;"
cur.execute(cmd18)
cmd19 = "CREATE TABLE participe(id_joueur int, annee int, num_partie int NOT NULL, minutes int,"\
	"PRIMARY KEY(annee, num_partie, id_joueur),"\
	"FOREIGN KEY(annee, num_partie) REFERENCES partie(annee, num_partie) ON DELETE CASCADE,"\
	"FOREIGN KEY(id_joueur) REFERENCES joueur(id_joueur) ON DELETE CASCADE);"
cur.execute(cmd19)
cmd20 = "CREATE TRIGGER joueur_bonne_equipe"\
        " BEFORE INSERT ON participe"\
        " FOR EACH ROW"\
        " BEGIN"\
        " IF(SELECT COUNT(*)"\
        "     FROM partie P, concoure Cc, contrat Ct"\
        "     WHERE P.annee = NEW.annee AND P.num_partie = NEW.num_partie"\
        "      AND Cc.annee = NEW.annee AND Cc.num_partie = NEW.num_partie"\
        "      AND (Ct.num_equipe = Cc.num_equipe_loc OR Ct.num_equipe = Cc.num_equipe_vis) AND Ct.id_joueur = NEW.id_joueur"\
        "      AND Ct.debut_incl <= P.date_partie AND P.date_partie < Ct.fin_excl"\
        "    ) <> 1"\
        " THEN SET NEW.id_joueur = null;"\
        " END IF;"\
        " END;"
cur.execute(cmd20)
cmd21 = "CREATE TRIGGER 12_joueurs_par_equipe"\
        " BEFORE INSERT ON participe"\
        " FOR EACH ROW"\
        " BEGIN"\
        " IF	(SELECT COUNT(Ct2.id_joueur)"\
        "        FROM partie Pe, participe Pp, concoure Cc, contrat Ct1, contrat ct2"\
        "        WHERE Pe.annee = NEW.annee AND Pe.num_partie = NEW.num_partie"\
        "         AND Pp.annee = NEW.annee AND Pp.num_partie = NEW.num_partie"\
        "         AND Cc.annee = NEW.annee AND Cc.num_partie = NEW.num_partie"\
        "         AND Ct1.num_equipe = Cc.num_equipe_loc AND Ct1.id_joueur = NEW.id_joueur "\
        "         AND Ct1.debut_incl <= Pe.date_partie AND Pe.date_partie < Ct1.fin_excl"\
        "         AND Ct2.num_equipe = Ct1.num_equipe AND Ct2.id_joueur = Pp.id_joueur"\
        "         AND Ct2.debut_incl <= Pe.date_partie AND Pe.date_partie < Ct2.fin_excl"\
        "        ) = 12 "\
        " THEN SET NEW.id_joueur = null;"\
        " END IF;"\
        " END;"
cur.execute(cmd21)
cmd22 = "CREATE TABLE type_action(type char(20), PRIMARY KEY(type));"
cur.execute(cmd22)
cmd23 = "INSERT INTO type_action VALUES ('"'lancer'"'), ('"'revirement'"'), ('"'faute'"'), ('"'rebond'"');"
cur.execute(cmd23)
cmd24 = "CREATE TABLE action (annee int, num_partie int, instant time, type_action char(20),"\
	"id_joueur int NOT NULL,"\
	"PRIMARY KEY(annee, num_partie, instant),"\
	"FOREIGN KEY(annee, num_partie) REFERENCES partie(annee, num_partie) ON DELETE CASCADE,"\
	"FOREIGN KEY(type_action) REFERENCES type_action(type) ON DELETE CASCADE,"\
	"FOREIGN KEY(annee, num_partie,id_joueur) REFERENCES participe(annee, num_partie,id_joueur)"\
	"ON DELETE CASCADE);"
cur.execute(cmd24)
cmd24 = "CREATE TABLE type_lancer(type char(20), PRIMARY KEY(type));"
cur.execute(cmd24)
cmd25 = "INSERT INTO type_lancer VALUES ('"'1pt'"'), ('"'2pt'"'), ('"'3pt'"');"
cur.execute(cmd25)
cmd26 = "CREATE TABLE lancer (annee int, num_partie int, instant time, type_lancer char(20) NOT NULL, est_panier bool NOT NULL,"\
	"PRIMARY KEY(annee, num_partie, instant),"\
	"FOREIGN KEY(type_lancer) REFERENCES type_lancer(type),"\
	"FOREIGN KEY(annee, num_partie, instant) REFERENCES action(annee, num_partie, instant)"\
	"ON DELETE CASCADE);"
cur.execute(cmd26)
cmd27 = "CREATE TRIGGER type_action_lancer"\
        " BEFORE INSERT ON lancer"\
        " FOR EACH ROW"\
        " BEGIN"\
        "        IF (	SELECT type_action"\
        "                FROM action"\
        "                WHERE annee = NEW.annee AND num_partie = NEW.num_partie AND instant = NEW.instant)"\
        "         <> '"'lancer'"'"\
        "        THEN SET NEW.instant = null;"\
        "        END IF;"\
        " END;"
cur.execute(cmd27)
cmd28 = "CREATE TRIGGER update_points_au_panier"\
        " BEFORE INSERT ON lancer"\
        " FOR EACH ROW"\
        " BEGIN"\
        " IF (NEW.est_panier)"\
        " THEN"\
        "    SET @points = (SELECT( 1*COUNT(IF(NEW.type_lancer = '"'1pt'"',1,NULL)) +"\
        "                        2*COUNT(IF(NEW.type_lancer = '"'2pt'"',1,NULL)) +"\
        "                        3*COUNT(IF(NEW.type_lancer = '"'3pt'"',1,NULL))));"\
        "        SET @equipe_local ="\
        "        (SELECT COUNT(*)"\
        "        FROM partie P, concoure Cc, contrat Ct, action A"\
        "                 WHERE P.annee = NEW.annee AND P.num_partie = NEW.num_partie"\
        "                  AND Cc.annee = NEW.annee AND Cc.num_partie = NEW.num_partie"\
        "                  AND A.annee=NEW.annee AND A.num_partie=NEW.num_partie AND A.instant=NEW.instant"\
        "                  AND Ct.num_equipe = Cc.num_equipe_loc AND Ct.id_joueur = A.id_joueur"\
        "                  AND Ct.debut_incl <= P.date_partie AND P.date_partie < Ct.fin_excl );"\
        "        IF(@equipe_local > 0)"\
        "        THEN "\
        "                UPDATE concoure"\
        "                SET points_loc = points_loc + @points"\
        "                WHERE annee=NEW.annee AND num_partie=NEW.num_partie;"\
        "        ELSE"\
        "                UPDATE concoure"\
        "                SET points_vis = points_vis + @points"\
        "                WHERE annee=NEW.annee AND num_partie=NEW.num_partie;"\
        "        END IF;"\
        " END IF;"\
        " END;"
cur.execute(cmd28)
cmd29 = "CREATE TABLE assiste(id_joueur int NOT NULL, annee int, num_partie int, instant time,"\
	"PRIMARY KEY(annee, num_partie, instant),"\
	"FOREIGN KEY(annee, num_partie, instant) REFERENCES lancer(annee, num_partie, instant)"\
	"ON DELETE CASCADE,"\
	"FOREIGN KEY(annee, num_partie,id_joueur) REFERENCES participe(annee, num_partie,id_joueur)"\
	"ON DELETE CASCADE);"
cur.execute(cmd29)
cmd30 = "CREATE TRIGGER assiste_panier"\
        " BEFORE INSERT ON assiste"\
        " FOR EACH ROW"\
        " BEGIN"\
        "        IF (	SELECT est_panier"\
        "                FROM lancer"\
        "                WHERE annee = NEW.annee AND num_partie = NEW.num_partie AND instant = NEW.instant)"\
        "         = false"\
        "        THEN SET NEW.instant = null;"\
        "        END IF;"\
        " END;"
cur.execute(cmd30)
cmd31 = "CREATE TRIGGER assiste_mauvaise_equipe"\
        " BEFORE INSERT ON assiste"\
        " FOR EACH ROW"\
        " BEGIN"\
        " IF(SELECT COUNT(*)"\
        "     FROM action A, partie P, contrat Ct1, contrat Ct2"\
        "     WHERE  A.annee = NEW.annee AND A.num_partie = NEW.num_partie AND A.instant = NEW.instant"\
        "        AND P.annee = NEW.annee AND P.num_partie = NEW.num_partie"\
        "        AND Ct1.id_joueur = A.id_joueur"\
        "        AND Ct1.debut_incl <= P.date_partie AND P.date_partie < Ct1.fin_excl"\
        "        AND Ct2.num_equipe = Ct1.num_equipe AND Ct2.id_joueur = NEW.id_joueur"\
        "        AND Ct2.debut_incl <= P.date_partie AND P.date_partie < Ct2.fin_excl"\
        "    ) = 0"\
        " THEN SET NEW.instant = null;"\
        " END IF;"\
        " END;"
cur.execute(cmd31)
cmd32 = "CREATE TABLE type_faute(type char(20), PRIMARY KEY(type));"
cur.execute(cmd32)
cmd33 = "INSERT INTO type_faute VALUES ('"'offensif'"'), ('"'defensif'"');"
cur.execute(cmd33)
cmd34 = "CREATE TABLE revirement (annee int, num_partie int, instant time, type_revirement char(20) NOT NULL,"\
	"PRIMARY KEY(annee, num_partie, instant),"\
	"FOREIGN KEY(type_revirement) REFERENCES type_faute(type),"\
	"FOREIGN KEY(annee, num_partie, instant) REFERENCES action(annee, num_partie, instant)"\
	"ON DELETE CASCADE);"
cur.execute(cmd34)
cmd35 = "CREATE TRIGGER type_action_revirement"\
        " BEFORE INSERT ON revirement"\
        " FOR EACH ROW"\
        " BEGIN"\
        "        IF (	SELECT type_action"\
        "                FROM action"\
        "                WHERE annee = NEW.annee AND num_partie = NEW.num_partie AND instant = NEW.instant)"\
        "         <> '"'revirement'"'"\
        "        THEN SET NEW.instant = null;"\
        "        END IF;"\
        " END;"
cur.execute(cmd35)
cmd36 = "CREATE TABLE faute (annee int, num_partie int, instant time, type_faute char(20) NOT NULL,"\
	"PRIMARY KEY(annee, num_partie, instant),"\
	"FOREIGN KEY(type_faute) REFERENCES type_faute(type),"\
	"FOREIGN KEY(annee, num_partie, instant) REFERENCES action(annee, num_partie, instant)"\
	"ON DELETE CASCADE);"
cur.execute(cmd36)
cmd37 = "CREATE TRIGGER type_action_faute"\
        " BEFORE INSERT ON faute"\
        " FOR EACH ROW"\
        " BEGIN"\
        "        IF (	SELECT type_action"\
        "                FROM action"\
        "                WHERE annee = NEW.annee AND num_partie = NEW.num_partie AND instant = NEW.instant)"\
        "         <> '"'faute'"'"\
        "        THEN SET NEW.instant = null;"\
        "        END IF;"\
        " END;"
cur.execute(cmd37)
cmd38 = "CREATE TABLE rebond (annee int, num_partie int, instant time, type_rebond char(20) NOT NULL,"\
	"PRIMARY KEY(annee, num_partie, instant),"\
	"FOREIGN KEY(type_rebond) REFERENCES type_faute(type),"\
	"FOREIGN KEY(annee, num_partie, instant) REFERENCES action(annee, num_partie, instant) "\
	"ON DELETE CASCADE);"
cur.execute(cmd38)
cmd39 = "CREATE TRIGGER type_action_rebond"\
        " BEFORE INSERT ON rebond"\
        " FOR EACH ROW"\
        " BEGIN"\
        "        IF (	SELECT type_action"\
        "                FROM action"\
        "                WHERE annee = NEW.annee AND num_partie = NEW.num_partie AND instant = NEW.instant)"\
        "         <> '"'rebond'"'"\
        "        THEN SET NEW.instant = null;"\
        "        END IF;"\
        " END;"
cur.execute(cmd39)


"""Création de listes utiles"""
team = ["Hawks", "Celtics", "Nets", "Hornets", "Bulls", "Cavaliers", "Mavericks", "Nuggets", "Pistons", "Warriors", "Rockets", "Pacers", "Clippers", "Lakers", "Grizzlies", "Heat", "Bucks", "Timberwolves", "Pelicans", "Knicks", "Thunder", "Magic", "76ers", "Suns", "Trail Blazers", "Kings", "Spurs", "Raptors", "Jazz", "Wizards"]
town = ["Atlanta", "Bonston", "Brooklyn", "Charlotte", "Chicago", "Cleveland", "Dallas", "Denver", "Detroit", "Golden State", "Houston", "Indiana", "LA", "Los Angeles", "Memphis", "Miami", "Milwaukee", "Minnesota", "New Orleans", "New York", "Oklahoma City", "Orlando", "Philadelphia", "Phoenix", "Portland", "Sacramento", "San Antonio", "Toronto", "Utah", "Washington"]
country = ["Etats-Unis", "Canada"]
taille = [5.8, 5.9, 5.10, 5.11, 6, 6.1, 6.2, 6.3, 6.4, 6.5, 6.6, 6.7, 6.8, 6.9, 6.10, 6.11, 7, 7.1, 7.2, 7.3, 7.4, 7.5, 7.6, 7.7, 7.8, 7.9, 7.10]
role = ["Meneur", "Arrière", "Ailier", "Ailier fort", "Pivot"]

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

