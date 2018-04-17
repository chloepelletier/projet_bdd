from flask import Flask, render_template, request
from datetime import date

import pymysql 
import pymysql.cursors 

app = Flask(__name__) 

#=======IDENTIFIANT DE CONNEXION A LA BASE DE DONNEES ============
userid = 'root'
userpassword = '1994'
#==============================


@app.route("/") 
def accueil(id=None): 
    conn= pymysql.connect( 
        host='localhost', 
        user=userid, 
        password=userpassword,
        db='basketballer' )
    #TODO
    cmd='SELECT num_equipe, nom_equipe, ville FROM equipe GROUP BY nom_equipe;'
    cur=conn.cursor()
    cur.execute(cmd)
    equipes = cur.fetchall()
    return render_template('accueil.html', equipes=equipes) 

#================================

@app.route("/resultsearchjoueur", methods=['POST'])
def resultsearchjoueur():
   nom = request.form.get('nom')
   prenom = request.form.get('prenom')
   return getResult(nom,prenom)


@app.route("/resultsearchjoueur")
def getResult(nom,prenom):
    today = date.today()
    ajd = ""+str(today.year)+"-"+str(today.month)+"-"+str(today.day)+""
    conn= pymysql.connect( 
        host='localhost', 
        user=userid, 
        password=userpassword,
        db='basketballer' )
    if(nom and prenom): 
        cmd="SELECT joueur.id_joueur, joueur.nom_famille, joueur.prenom, equipe.nom_equipe FROM joueur, equipe, contrat WHERE equipe.num_equipe = contrat.num_equipe AND contrat.id_joueur=joueur.id_joueur AND contrat.fin_excl >= %s AND joueur.nom_famille=%s AND joueur.prenom= %s GROUP BY joueur.prenom;"
        cur=conn.cursor()
        cur.execute(cmd,(ajd,nom,prenom))
        info = cur.fetchall()
    elif(nom):
        cmd="SELECT joueur.id_joueur, joueur.nom_famille, joueur.prenom, equipe.nom_equipe FROM joueur, equipe, contrat WHERE equipe.num_equipe = contrat.num_equipe AND contrat.id_joueur=joueur.id_joueur AND contrat.fin_excl >= %s AND joueur.nom_famille=%s GROUP BY joueur.prenom;"
        cur=conn.cursor()
        cur.execute(cmd,(ajd,nom))
        info = cur.fetchall()
    elif(prenom):
        cmd="SELECT joueur.id_joueur, joueur.nom_famille, joueur.prenom, equipe.nom_equipe FROM joueur, equipe, contrat WHERE equipe.num_equipe = contrat.num_equipe AND contrat.id_joueur=joueur.id_joueur AND contrat.fin_excl >= %s AND joueur.prenom=%s GROUP BY joueur.nom_famille;"
        cur=conn.cursor()
        cur.execute(cmd, (ajd,prenom))
        info = cur.fetchall()
    else : 
        cmd="SELECT joueur.id_joueur, joueur.nom_famille, joueur.prenom, equipe.nom_equipe FROM joueur, equipe, contrat WHERE equipe.num_equipe = contrat.num_equipe AND contrat.id_joueur=joueur.id_joueur AND contrat.fin_excl >= %s GROUP BY joueur.nom_famille, joueur.prenom;"
        cur=conn.cursor()
        cur.execute(cmd,ajd)
        info = cur.fetchall()
    return render_template('resultsearchjoueur.html',info=info)
        

#================================

@app.route("/resultsearchpartie", methods=['POST'])
def resultsearchpartie():
   equipelocal = request.form.get('equipelocal')
   equipevisiteur = request.form.get('equipevisiteur')
   dateDebut = request.form.get('dateDebut')
   dateFin = request.form.get('dateFin')
   return getResultPartie(equipelocal,equipevisiteur,dateDebut,dateFin)


@app.route("/resultsearchpartie")
def getResultPartie(equipelocal,equipevisiteur,dateDebut, dateFin):
    conn= pymysql.connect( 
        host='localhost', 
        user=userid, 
        password=userpassword,
        db='basketballer' )
    if (dateDebut or dateFin):
        if not(dateDebut): 
            dateDebut='0000-00-00'
        if not(dateFin): 
            dateFin='9999-12-31'
        cmd="SELECT partie.annee, partie.num_partie, partie.date_partie, E1.nom_equipe, E2.nom_equipe, concoure.points_loc, concoure.points_vis from partie,equipe E1, equipe E2, concoure WHERE E1.num_equipe= concoure.num_equipe_loc AND E2.num_equipe= concoure.num_equipe_vis AND concoure.annee = partie.annee AND concoure.num_partie = partie.num_partie AND (E1.num_equipe= %s OR E2.num_equipe= %s) AND (E2.num_equipe =%s OR E1.num_equipe = %s) AND partie.date_partie >= %s  AND partie.date_partie <=  %s ;"
        cur=conn.cursor()
        cur.execute(cmd, (equipelocal,equipelocal,equipevisiteur,equipevisiteur,dateDebut,dateFin))
        info = cur.fetchall()
    else : 
        cmd2="SELECT partie.annee, partie.num_partie, partie.date_partie, E1.nom_equipe, E2.nom_equipe, concoure.points_loc, concoure.points_vis from partie,equipe E1, equipe E2, concoure WHERE E1.num_equipe= concoure.num_equipe_loc AND E2.num_equipe= concoure.num_equipe_vis AND concoure.annee = partie.annee AND concoure.num_partie = partie.num_partie AND (E1.num_equipe= %s OR E2.num_equipe=%s) AND (E2.num_equipe =%s OR E1.num_equipe = %s);"
        cur=conn.cursor()
        cur.execute(cmd2, (equipelocal,equipelocal,equipevisiteur,equipevisiteur))
        info = cur.fetchall()
    return render_template('resultsearchpartie.html',info=info)
        
#====================
@app.route("/joueur/<id>/saison", methods=['POST'])
def saisonJoueur(id=None,saison=None):
     saison = str(request.form.get('saisonJoueur'))
     return getJoueur(id = id, saison = saison)

@app.route("/joueur/<id>")
def getJoueur(id=None, saison = None):
    conn= pymysql.connect(
        host='localhost', 
        user=userid, 
        password=userpassword,
        db='basketballer' )

    # Tout init à 0
    nb_partie = nb_revirement_p = nb_revirement_n = nb_lancer_1pt = nb_lancer_2pt = nb_lancer_3pt = nb_panier_1pt = nb_panier_2pt = nb_panier_3pt = 0
    moy_assiste = moy_assiste = moy_rebond = moy_faute = moy_vol_balle = moy_revirement =  moy_point = pourcentage_lancer_franc = pourcentage_2pt = pourcentage_3pt = moy_min =0
    cur=conn.cursor()

    # Pour notre menu déroulant:
    cmd02 = 'SELECT DISTINCT annee FROM participe WHERE id_joueur=%s ORDER BY annee DESC;'
    cur.execute(cmd02, (id,))
    saisons = cur.fetchall()

    cmd = 'SELECT * FROM joueur WHERE id_joueur=%s;'
    cur.execute(cmd,(id,))
    info = cur.fetchone()

    if(not saison):
    #Prendre la saison courante pour identifier notre équipe:
        cmd0 = 'SELECT MAX(annee) FROM partie;' #mettre seulement les années où il a joué? Si jamais joué, compliqué
        #cmd0 = 'SELECT MAX(annee) FROM participe WHERE id_joueur='+id+';'
        cur.execute(cmd0)
        saison = str(cur.fetchone()[0])
    if(saison == "Carriere") :
    #Prendre aussi la saison courante pour identifier notre équipe
        cmd01 = 'SELECT MAX(date_partie) FROM partie, (SELECT MAX(annee) as annee_max FROM partie) as P WHERE annee = P.annee_max;'
        cur.execute(cmd01)
        date = str(cur.fetchone()[0])
    else :
        #On considère l'équipe du joueur comme étant celle avec laquelle il a fini la saison, si elle est finie:
        cmd01 = 'SELECT MAX(date_partie) FROM partie WHERE annee = %s;'
        cur.execute(cmd01, (saison,))
        date = str(cur.fetchone()[0])

    cmd2 = "SELECT * FROM contrat WHERE id_joueur=%s AND debut_incl <= %s AND %s < fin_excl;"
    cur.execute(cmd2,(id,date,date))
    info2 = cur.fetchone()
    if (info2) :
        cmd3="SELECT * FROM equipe WHERE num_equipe=%s;"
        cur.execute(cmd3,(str(info2[0]),))
        info3 = cur.fetchone()
    else :
        info3=("inconnu","inconnu","inconnu","inconnu")
        info2=("inconnu","inconnu","inconnu","inconnu","inconnu")

    #Requêtes différentes si une seule saison (égalité) ou plusieurs (gamme):
    if (saison != "Carriere"):
        #nombre de match joués dans la saison. Enregistré dans variable nb_partie */
        cmd4="SELECT COUNT(*), SUM(P.minutes) FROM participe P WHERE P.id_joueur = %s AND P.annee=%s;"
        cur.execute(cmd4,(id,saison))
        infoParticipe = cur.fetchone()
        nb_partie = infoParticipe[0]
        nb_minute = infoParticipe[1]
        if(nb_partie) : #pour éviter les divisions par 0
            moy_min = round(nb_minute / nb_partie,2)
            #Moyenne des assists  par partie
            cmd5='SELECT COUNT(*) FROM  assiste A WHERE A.annee=%s AND A.id_joueur=%s;'
            cur.execute(cmd5,(saison,id))
            nb_assiste = round(cur.fetchone()[0],2)
            #action
            cmd6 = 'SELECT * FROM  action A WHERE A.annee=%s AND A.id_joueur=%s;'
            cur.execute(cmd6,(saison,id))
            action = cur.fetchall()
            #Moyenne des rebonds et fautes par partie
            nb_rebond = nb_faute = 0
            for Tuple in action:
                if Tuple[3] == "rebond":
                    nb_rebond +=1
                if Tuple[3] == "faute" :
                    nb_faute +=1
            moy_rebond = round(nb_rebond / nb_partie,2)
            moy_faute = round(nb_faute / nb_partie,2)
            #lancers e trevirements:
            for Tuple in action :
                if Tuple[3] == "lancer" :
                    cmd7 = 'SELECT L.type_lancer, L.est_panier FROM lancer L WHERE L.annee=%s AND L.num_partie=%s AND L.instant=%s;'
                    cur.execute(cmd7,(str(Tuple[0]),str(Tuple[1]),str(Tuple[2])))
                    lancer = cur.fetchone()
                    if lancer[0] == "1pt":
                        nb_lancer_1pt +=1
                        if (lancer[1]):
                            nb_panier_1pt +=1
                    elif lancer[0] == "2pt" :
                        nb_lancer_2pt +=1
                        if (lancer[1]) :
                            nb_panier_2pt +=1
                    elif lancer[0] == "3pt" :
                        nb_lancer_3pt +=1
                        if (lancer[1]):
                            nb_panier_3pt +=1

                if Tuple[3] == "revirement":
                    cmd8 = 'SELECT R.type_revirement FROM revirement R WHERE R.annee=%s AND R.num_partie=%s AND R.instant=%s;'
                    cur.execute(cmd8,(str(Tuple[0]),str(Tuple[1]),str(Tuple[2])))
                    revirement = cur.fetchone()
                    if revirement[0] == "offensif":
                        nb_revirement_n +=1
                    elif revirement[0] == "defensif":
                        nb_revirement_p +=1

            moy_assiste = round(nb_assiste / nb_partie,2)
            moy_vol_balle = round(nb_revirement_p / nb_partie,2)
            moy_revirement = round(nb_revirement_n / nb_partie,2)
            nb_point =  1*nb_panier_1pt + 2*nb_panier_2pt +3*nb_panier_3pt
            moy_point = round(nb_point / nb_partie,2)
            if(nb_lancer_1pt) :
                pourcentage_lancer_franc = round((nb_panier_1pt / nb_lancer_1pt) * 100,2) #prob de division par zéro hahaha
            if(nb_lancer_2pt) :
                pourcentage_2pt = round((nb_panier_2pt / nb_lancer_2pt) * 100,2)
            if (nb_lancer_3pt):
                pourcentage_3pt = round((nb_panier_3pt / nb_lancer_3pt) * 100,2)
    else : #saison = "Carriere"
        cmd_carr = '''SELECT P.id_joueur, P2.nb_partie, SUM(P.minutes),
        COUNT(IF(A.type_action='faute' ,1,NULL)) AS nb_faute,
        COUNT(IF(A.type_action='rebond',1,NULL)) AS nb_rebond,
        COUNT(IF(A.type_action='revirement' AND
            (SELECT type_revirement FROM revirement WHERE annee=A.annee AND num_partie = A.num_partie AND instant = A.instant)='defensif'
            ,1,NULL)) AS nb_revirement_p,
        COUNT(IF(A.type_action='revirement' AND
            (SELECT type_revirement FROM revirement WHERE annee=A.annee AND num_partie = A.num_partie AND instant = A.instant)='offensif'
            ,1,NULL)) AS nb_revirement_n,
        COUNT(IF(A.type_action='lancer' AND
            (SELECT type_lancer FROM lancer WHERE annee=A.annee AND num_partie = A.num_partie AND instant = A.instant) = '1pt'
            ,1,NULL)) AS lancerfranc,
        COUNT(IF(A.type_action='lancer' AND
            (SELECT type_lancer FROM lancer WHERE annee=A.annee AND num_partie = A.num_partie AND instant = A.instant AND est_panier=1) = '1pt'
            ,1,NULL)) AS panierfranc,
        COUNT(IF(A.type_action='lancer' AND
            (SELECT type_lancer FROM lancer WHERE annee=A.annee AND num_partie = A.num_partie AND instant = A.instant) = '2pt'
            ,1,NULL)) AS lancer2pt,
        COUNT(IF(A.type_action='lancer' AND
            (SELECT type_lancer FROM lancer WHERE annee=A.annee AND num_partie = A.num_partie AND instant = A.instant AND est_panier=1) = '2pt'
            ,1,NULL)) AS panier2pt,
        COUNT(IF(A.type_action='lancer' AND
            (SELECT type_lancer FROM lancer WHERE annee=A.annee AND num_partie = A.num_partie AND instant = A.instant) = '3pt'
            ,1,NULL)) AS lancer3pt,
        COUNT(IF(A.type_action='lancer' AND
            (SELECT type_lancer FROM lancer WHERE annee=A.annee AND num_partie = A.num_partie AND instant = A.instant AND est_panier=1) = '3pt'
            ,1,NULL)) AS panier3pt
        FROM action A, joueur J, participe P, (SELECT COUNT(*) as nb_partie FROM participe WHERE id_joueur = %s) as P2
        WHERE A.annee=P.annee AND A.num_partie=P.num_partie AND A.id_joueur = P.id_joueur AND J.id_joueur=P.id_joueur AND P.id_joueur = %s
        GROUP BY J.id_joueur;'''
        cur.execute(cmd_carr,(id,id))
        stats = cur.fetchone()
        if(stats): #pour éviter les divisions par 0
            nb_partie = stats[1]
            nb_lancer_1pt = stats[7]
            nb_panier_1pt = stats[8]
            nb_lancer_2pt = stats[9]
            nb_panier_2pt = stats[10]
            nb_lancer_3pt = stats[11]
            nb_panier_3pt = stats[12]
            moy_vol_balle = round((stats[6] / nb_partie) , 2)
            moy_revirement = round((stats[5] / nb_partie) , 2)
            nb_point = nb_panier_1pt + 2*nb_panier_2pt + 3*nb_panier_3pt
            moy_point = round(nb_point /nb_partie, 2)
            if (nb_lancer_1pt):
                pourcentage_lancer_franc = round((nb_panier_1pt / nb_lancer_1pt) * 100, 2)
            if (nb_lancer_2pt):
                pourcentage_2pt = round((nb_panier_2pt / nb_lancer_2pt) * 100, 2)
            if (nb_lancer_3pt):
                pourcentage_3pt = round((nb_panier_3pt / nb_lancer_3pt) * 100, 2)
            moy_min = round(stats[2] / nb_partie , 2)
            moy_rebond = round(stats[4] / nb_partie , 2)
            moy_faute = round( stats[3] / nb_partie , 2)

            cmd_carr2 = "SELECT COUNT(*) FROM assiste A, joueur J, participe P \
                        WHERE A.annee=P.annee AND A.num_partie=P.num_partie AND A.id_joueur = P.id_joueur AND J.id_joueur=P.id_joueur AND P.id_joueur = %s;"
            cur.execute(cmd_carr2,(id,))
            moy_assiste = round (cur.fetchone()[0] / nb_partie * 100, 2)

    #S'exécute dans  tous les cas, car les variables containers ont les mêmes noms.
    return render_template('joueur.html', prenom=info[1], nom=info[2],
                           naissance=info[3], taille=info[4], poids=info[5],
                           position=info[6], bras=info[8], numero=info2[4], equipe=info3[1],
                           pays=info3[3], nb_partie=nb_partie, moy_assiste=moy_assiste,
                           moy_rebond=moy_rebond, moy_faute=moy_faute, moy_vol_balle=moy_vol_balle,
                           moy_revirement=moy_revirement, moy_point=moy_point,
                           pourcentage_lancer_franc=pourcentage_lancer_franc,
                           pourcentage_2pt=pourcentage_2pt, pourcentage_3pt=pourcentage_3pt,
                           moy_min=moy_min, saisons=saisons, id=id, saison=saison)


#=========================
@app.route("/equipe", methods=['POST'])
def equipe():
     equipe = request.form.get('equipeSearch')
     return getEquipe(equipe)


@app.route("/equipe")
def getEquipe(id):
    today = date.today()
    ajd = ""+str(today.year)+"-"+str(today.month)+"-"+str(today.day)+""
    conn= pymysql.connect( 
        host='localhost', 
        user=userid, 
        password=userpassword,
        db='basketballer' )

    cmd='SELECT * FROM equipe WHERE num_equipe=%s;'
    cur=conn.cursor()
    cur.execute(cmd,(str(id),))
    info = cur.fetchone()
    cmd4="SELECT num_partie, annee FROM concoure WHERE num_equipe_loc=%s OR num_equipe_vis=%s;"
    cur.execute(cmd4,(str(id),str(id)))
    info4 = cur.fetchall()
    id_partie=()
    for i in range (0,len(info4)): 
        id_partie = id_partie + ((info4[i][0],info4[i][1], ),)
    if(len(id_partie)==1) : 
        id_partie="("+ str(id_partie[0])+")"
    if (id_partie) :
        cmd5="SELECT partie.date_partie, E1.nom_equipe, E2.nom_equipe, partie.annee,partie.num_partie, concoure.points_loc, concoure.points_vis \
                FROM partie,concoure, equipe E1, equipe E2 WHERE partie.num_partie=concoure.num_partie AND partie.annee=concoure.annee  \
                AND E1.num_equipe = concoure.num_equipe_loc AND E2.num_equipe = concoure.num_equipe_vis AND (partie.num_partie,partie.annee) IN %s\
                 GROUP BY annee DESC,num_partie DESC;"
        cur.execute(cmd5,(id_partie,))
        infoPartie = cur.fetchall()
    else : 
        infoPartie = ("inconnu","inconnu","inconnu","inconnu","inconnu")
    cmd2="SELECT id_joueur FROM contrat WHERE fin_excl>=%s AND num_equipe= %s;"
    cur.execute(cmd2,(ajd,str(id)))
    info2 = cur.fetchall()
    id_joueur=()
    for i in range (0,len(info2)): 
        id_joueur = id_joueur + (info2[i][0], )
    if(len(id_joueur)==1) : 
        id_joueur="("+ str(id_joueur[0])+")"

    if (id_joueur) :
        cmd3="SELECT joueur.id_joueur, joueur.nom_famille, joueur.prenom,joueur.role, contrat.dossard FROM joueur," \
             "contrat WHERE joueur.id_joueur = contrat.id_joueur AND joueur.id_joueur IN %s;"
        cur.execute(cmd3,(id_joueur,))
        infoJoueur = cur.fetchall()
    else : 
        infoJoueur = ("inconnu","inconnu","inconnu","inconnu","inconnu")

    #trouver les saisons remportées par l'équipe en vérifiant si elle a gagné la dernière partie de la dernière série de chaque saison:
    cmd4= '''SELECT A.annee, A.annee FROM appartient A, concoure C WHERE A.annee= C.annee AND A.num_serie = 2 AND A.num_partie=C.num_partie
            AND ((C.num_equipe_loc = %s AND C.points_loc > C.points_vis) OR (C.num_equipe_vis = %s AND C.points_vis > C.points_loc))
            AND A.num_sous_serie =
            (SELECT MAX(A2.num_sous_serie) FROM appartient A2 WHERE A2.annee=A.annee); '''
    cur.execute(cmd4, (str(id),str(id)))
    saisons_gagnees = cur.fetchall()

    return render_template('equipe.html', nom=info[1], ville=info[2],pays=info[3],fondation=info[4],
                           infoPartie=infoPartie, infoJoueur=infoJoueur, saisons_gagnees = saisons_gagnees)


@app.route("/partie/<annee>/<num>")
def getPartie(annee=None,num=None):
    conn= pymysql.connect( 
        host='localhost', 
        user=userid, 
        password=userpassword,
        db='basketballer' )
    #recuperation des infos generales
    cmd='SELECT * FROM partie WHERE num_partie =%s AND annee=%s;'
    cur=conn.cursor()
    cur.execute(cmd,(num,annee))
    info = cur.fetchone()
    # récupartion d'info sur le type de partie
    cmd1 = 'SELECT num_serie, num_sous_serie FROM appartient WHERE num_partie = %s AND annee= %s;'
    cur.execute(cmd1,(num,annee))
    info_serie = cur.fetchone()
    if (info_serie):
        if info_serie[0] == 2:
            ronde = "Finales"
        else:
            ronde = "Ronde 1"
        type_partie = "Séries - " + ronde + " - Partie " + str(info_serie[1])
    else:
        type_partie = "Saison régulière"
    #recuperation des noms d'equipe
    cmd2='SELECT E1.nom_equipe, E2.nom_equipe FROM concoure,equipe E1, equipe E2 WHERE E1.num_equipe = concoure.num_equipe_loc AND E2.num_equipe = concoure.num_equipe_vis AND num_partie =%s AND annee=%s;'
    cur.execute(cmd2,(num,annee))
    equipes = cur.fetchone()
    # recuperation des points 
    cmd6='SELECT C.points_loc, C.points_vis FROM concoure C WHERE num_partie =%s AND annee=%s;'
    cur.execute(cmd6,(num,annee))
    scores = cur.fetchone()
    #liste joueur equipe 1 
    cmd3="""SELECT J.id_joueur, Ct.dossard,J.nom_famille, J.prenom, J.role, PA.minutes,
        COUNT(IF(A.type_action='faute'  AND A.id_joueur=J.id_joueur,1,NULL)) AS nb_faute,
        COUNT(IF(A.type_action='rebond' AND A.id_joueur=J.id_joueur,1,NULL)) AS nb_rebond,
        COUNT(IF(A.type_action='revirement'  AND A.id_joueur=J.id_joueur AND
            (SELECT type_revirement FROM revirement WHERE annee=A.annee AND num_partie = A.num_partie AND instant = A.instant)='offensif'
            ,1,NULL)) AS nb_revirement ,
        COUNT(IF(A.type_action='lancer'  AND
            (SELECT id_joueur FROM assiste WHERE annee=A.annee AND num_partie = A.num_partie AND instant = A.instant) = J.id_joueur
            ,1,NULL)) AS asisstance ,
        COUNT(IF(A.type_action='lancer' AND  A.id_joueur=J.id_joueur AND
            (SELECT type_lancer FROM lancer WHERE annee=A.annee AND num_partie = A.num_partie AND instant = A.instant AND est_panier=1) = '1pt'
            ,1,NULL)) AS lancerfranc,
        COUNT(IF(A.type_action='lancer'  AND A.id_joueur=J.id_joueur AND
            (SELECT type_lancer FROM lancer WHERE annee=A.annee AND num_partie = A.num_partie AND instant = A.instant AND est_panier=1) = '2pt'
            ,1,NULL)) AS panier2pt,
        COUNT(IF(A.type_action='lancer'  AND A.id_joueur=J.id_joueur AND
            (SELECT type_lancer FROM lancer WHERE annee=A.annee AND num_partie = A.num_partie AND instant = A.instant AND est_panier=1) = '3pt'
            ,1,NULL)) AS panier3ptc,
        COUNT(IF(A.type_action='revirement' AND A.id_joueur=J.id_joueur AND
            (SELECT type_revirement FROM revirement WHERE annee=A.annee AND num_partie = A.num_partie AND instant = A.instant)='defensif'
            ,1,NULL)) AS nb_volballe
        FROM  concoure Cc, contrat Ct, participe PA, joueur J ,partie P LEFT JOIN  action A ON (P.annee, P.num_partie) = (A.annee, A.num_partie)
        WHERE P.annee = %s AND P.num_partie =%s AND
                Cc.annee= P.annee AND Cc.num_partie = P.num_partie
                AND PA.annee = P.annee AND PA.num_partie = P.num_partie
                AND J.id_joueur = PA.id_joueur
                AND Ct.id_joueur = J.id_joueur AND Ct.num_equipe = Cc.num_equipe_loc
                AND Ct.debut_incl <= P.date_partie AND P.date_partie < Ct.fin_excl
        GROUP BY J.id_joueur;"""
    cur.execute(cmd3,(annee,num))
    joueurs1 = cur.fetchall()
    #liste joueur equipe 2 
    cmd4="""SELECT J.id_joueur, Ct.dossard,J.nom_famille, J.prenom, J.role, PA.minutes,
        COUNT(IF(A.type_action='faute'  AND A.id_joueur=J.id_joueur,1,NULL)) AS nb_faute,
        COUNT(IF(A.type_action='rebond' AND A.id_joueur=J.id_joueur,1,NULL)) AS nb_rebond,
        COUNT(IF(A.type_action='revirement'  AND A.id_joueur=J.id_joueur AND
            (SELECT type_revirement FROM revirement WHERE annee=A.annee AND num_partie = A.num_partie AND instant = A.instant)='offensif'
            ,1,NULL)) AS nb_revirement ,
        COUNT(IF(A.type_action='lancer'  AND
            (SELECT id_joueur FROM assiste WHERE annee=A.annee AND num_partie = A.num_partie AND instant = A.instant) = J.id_joueur
            ,1,NULL)) AS asisstance ,
        COUNT(IF(A.type_action='lancer' AND  A.id_joueur=J.id_joueur AND
            (SELECT type_lancer FROM lancer WHERE annee=A.annee AND num_partie = A.num_partie AND instant = A.instant AND est_panier=1) = '1pt'
            ,1,NULL)) AS lancerfranc,
        COUNT(IF(A.type_action='lancer'  AND A.id_joueur=J.id_joueur AND
            (SELECT type_lancer FROM lancer WHERE annee=A.annee AND num_partie = A.num_partie AND instant = A.instant AND est_panier=1) = '2pt'
            ,1,NULL)) AS panier2pt,
        COUNT(IF(A.type_action='lancer'  AND A.id_joueur=J.id_joueur AND
            (SELECT type_lancer FROM lancer WHERE annee=A.annee AND num_partie = A.num_partie AND instant = A.instant AND est_panier=1) = '3pt'
            ,1,NULL)) AS panier3ptc,
        COUNT(IF(A.type_action='revirement' AND A.id_joueur=J.id_joueur AND
            (SELECT type_revirement FROM revirement WHERE annee=A.annee AND num_partie = A.num_partie AND instant = A.instant)='defensif'
            ,1,NULL)) AS nb_volballe
        FROM  concoure Cc, contrat Ct, participe PA, joueur J ,partie P LEFT JOIN  action A ON (P.annee, P.num_partie) = (A.annee, A.num_partie)
        WHERE P.annee = %s AND P.num_partie =%s AND
                Cc.annee= P.annee AND Cc.num_partie = P.num_partie
                AND PA.annee = P.annee AND PA.num_partie = P.num_partie
                AND J.id_joueur = PA.id_joueur
                AND Ct.id_joueur = J.id_joueur AND Ct.num_equipe = Cc.num_equipe_vis
                AND Ct.debut_incl <= P.date_partie AND P.date_partie < Ct.fin_excl
        GROUP BY J.id_joueur;"""
    cur.execute(cmd4,(annee,num))
    joueurs2 = cur.fetchall()
    #liste action
    cmd5="SELECT action.instant, action.type_action, equipe.nom_equipe, joueur.nom_famille, joueur.prenom FROM action, equipe, contrat, joueur WHERE action.id_joueur = contrat.id_joueur AND contrat.num_equipe = equipe.num_equipe AND joueur.id_joueur = action.id_joueur AND action.num_partie =%s AND action.annee=%s;"
    cur.execute(cmd5,(num,annee))
    actions = cur.fetchall()
    return render_template('partie.html', info=info,equipes=equipes, scores=scores ,joueurs1=joueurs1, joueurs2=joueurs2, actions = actions, type_partie = type_partie)
  
        

#=====================================

if __name__ == "__main__":
    app.run()




