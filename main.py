from flask import Flask, render_template, request
import pymysql 
import pymysql.cursors 

app = Flask(__name__) 

#==============================


@app.route("/") 
def accueil(id=None): 
    conn= pymysql.connect( 
        host='localhost', 
        user='root', 
        password='1994',
        db='basketballer' )
    cmd='SELECT nom_equipe FROM equipe;'
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
    conn= pymysql.connect( 
        host='localhost', 
        user='root', 
        password='1994',
        db='basketballer' )
    if(nom and prenom): 
        cmd="SELECT joueur.id_joueur, joueur.nom_famille, joueur.prenom, equipe.nom_equipe FROM joueur, equipe, contrat WHERE equipe.num_equipe = contrat.num_equipe AND contrat.id_joueur=joueur.id_joueur AND contrat.fin_excl = '9999-12-31' AND joueur.nom_famille= '"+nom+"' AND joueur.prenom= '"+prenom+"';"
        cur=conn.cursor()
        cur.execute(cmd)
        info = cur.fetchall()
    elif(nom):
        cmd="SELECT joueur.id_joueur, joueur.nom_famille, joueur.prenom, equipe.nom_equipe FROM joueur, equipe, contrat WHERE equipe.num_equipe = contrat.num_equipe AND contrat.id_joueur=joueur.id_joueur AND contrat.fin_excl = '9999-12-31' AND joueur.nom_famille= '"+nom+"';"
        cur=conn.cursor()
        cur.execute(cmd)
        info = cur.fetchall()
    elif(prenom):
        cmd="SELECT joueur.id_joueur, joueur.nom_famille, joueur.prenom, equipe.nom_equipe FROM joueur, equipe, contrat WHERE equipe.num_equipe = contrat.num_equipe AND contrat.id_joueur=joueur.id_joueur AND contrat.fin_excl = '9999-12-31' AND joueur.prenom= '"+prenom+"';"
        cur=conn.cursor()
        cur.execute(cmd)
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
        user='root', 
        password='1994',
        db='basketballer' )
    if (dateDebut or dateFin):
        if not(dateDebut): 
            dateDebut='0000-00-00'
        if not(dateFin): 
            dateFin='9999-12-31'
        cmd="SELECT partie.annee, partie.num_partie, partie.date_partie, E1.nom_equipe, E2.nom_equipe from partie,equipe E1, equipe E2, concoure WHERE E1.num_equipe= concoure.num_equipe_loc AND E2.num_equipe= concoure.num_equipe_vis AND concoure.annee = partie.annee AND concoure.num_partie = partie.num_partie AND (E1.nom_equipe= '"+equipelocal+"'OR E2.nom_equipe= '"+equipelocal+"') AND (E2.nom_equipe ='"+equipevisiteur+"' OR E1.nom_equipe ='"+equipevisiteur+"') AND partie.date_partie BETWEEN '" +dateDebut+"' AND '"+ dateFin+"';"
        cur=conn.cursor()
        cur.execute(cmd)
        info = cur.fetchall()
    else : 
        cmd2="SELECT partie.annee, partie.num_partie, partie.date_partie, E1.nom_equipe, E2.nom_equipe from partie,equipe E1, equipe E2, concoure WHERE E1.num_equipe= concoure.num_equipe_loc AND E2.num_equipe= concoure.num_equipe_vis AND concoure.annee = partie.annee AND concoure.num_partie = partie.num_partie AND (E1.nom_equipe= '"+equipelocal+"'OR E2.nom_equipe= '"+equipelocal+"') AND (E2.nom_equipe ='"+equipevisiteur+"' OR E1.nom_equipe ='"+equipevisiteur+"');"
        cur=conn.cursor()
        cur.execute(cmd2)
        info = cur.fetchall()
    return render_template('resultsearchpartie.html',info=info)
        
#====================


@app.route("/joueur/<id>")
def getJoueur(id=None):
    conn= pymysql.connect( 
        host='localhost', 
        user='root', 
        password='1994',
        db='basketballer' )
    cmd='SELECT * FROM joueur WHERE id_joueur='+id+';'
    cur=conn.cursor()
    cur.execute(cmd)
    info = cur.fetchone()
    cmd2="SELECT * FROM contrat WHERE fin_excl='9999-12-31'AND id_joueur="+id+";"
    cur.execute(cmd2)
    info2 = cur.fetchone()
    if (info2) :
        cmd3="SELECT * FROM equipe WHERE num_equipe="+str(info2[0])+";"
        cur.execute(cmd3)
        info3 = cur.fetchone()
    else : 
        info3=("inconnu","inconnu","inconnu","inconnu")
        info2=("inconnu","inconnu","inconnu","inconnu","inconnu")

    #Tout init à 0
    nb_revirement_p = 0
    nb_revirement_n = 0
    nb_lancer_1pt = 0
    nb_lancer_2pt = 0
    nb_lancer_3pt = 0
    nb_panier_1pt = 0
    nb_panier_2pt = 0
    nb_panier_3pt = 0
    moy_assiste = 0
    moy_vol_balle = 0
    moy_revirement = 0
    nb_point =  0
    moy_point = 0
    pourcentage_lancer_franc = 0
    pourcentage_2pt = 0
    pourcentage_3pt = 0
    moy_min = 0
    moy_rebond = 0
    moy_faute = 0

    #nombre de match joués dans la saison. Enregistré dans variable nb_partie */
    cmd4="SELECT COUNT(*), SUM(P.minutes) FROM participe P WHERE P.id_joueur =" +id+ " AND P.annee=2018;"
    cur.execute(cmd4)
    infoParticipe = cur.fetchone()
    nb_partie = infoParticipe[0]
    nb_minute = infoParticipe[1] #
    if(nb_partie) :
        moy_min = nb_minute / nb_partie
        #Moyenne des assists  par partie
        cmd5='SELECT COUNT(*) FROM  assiste A WHERE A.annee=2018 AND A.id_joueur='+id+';'
        cur.execute(cmd5)
        nb_assiste = cur.fetchone()[0]
        #action
        cmd6 = 'SELECT * FROM  action A WHERE A.annee=2018 AND A.id_joueur='+id+';'
        cur.execute(cmd6)
        action = cur.fetchall()
        #Moyenne des rebonds et fautes par partie
        nb_rebond = 0
        nb_faute = 0
        for Tuple in action:
            if Tuple[3] == "rebond":
                nb_rebond +=1
            if Tuple[3] == "faute" :
                nb_faute +=1
        moy_rebond = nb_rebond / nb_partie
        moy_faute = nb_faute / nb_partie
        #lancers e trevirements:
        for Tuple in action :
            if Tuple[3] == "lancer" :
                cmd7 = 'SELECT L.type_lancer, L.est_panier FROM lancer L WHERE L.annee='+str(Tuple[0])+' AND L.num_partie='+str(Tuple[1])+' AND L.instant= "'+str(Tuple[2])+'";'
                cur.execute(cmd7)
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
                cmd8 = 'SELECT R.type_revirement FROM revirement R WHERE R.annee='+str(Tuple[0])+' AND R.num_partie='+str(Tuple[1])+' AND R.instant= "'+str(Tuple[2])+'";'
                cur.execute(cmd8)
                revirement = cur.fetchone()
                if revirement[0] == "offensif":
                    nb_revirement_p +=1
                elif revirement[0] == "defensif":
                    nb_revirement_n +=1

        moy_assiste = nb_assiste / nb_partie
        moy_vol_balle = nb_revirement_p / nb_partie
        moy_revirement = nb_revirement_n / nb_partie
        nb_point =  1*nb_panier_1pt + 2*nb_panier_2pt +3*nb_panier_3pt
        moy_point = nb_point / nb_partie
        if(nb_lancer_1pt) :
            pourcentage_lancer_franc = (nb_panier_1pt / nb_lancer_1pt) * 100 #prob de division par zéro hahaha
        if(nb_lancer_2pt) :
            pourcentage_2pt = (nb_panier_2pt / nb_lancer_2pt) * 100
        if (nb_lancer_3pt):
            pourcentage_3pt = (nb_panier_3pt / nb_lancer_3pt) * 100

    return render_template('joueur.html', prenom=info[1], nom=info[2],
                           naissance= info[3], taille=info[4], poids=info[5], 
                           position= info[6], bras=info[8], numero=info2[4],equipe=info3[1],
                           pays=info3[3], nb_partie=nb_partie, moy_assiste=moy_assiste, 
                           moy_rebond=moy_rebond, moy_faute = moy_faute, moy_vol_balle=moy_vol_balle,
                           moy_revirement=moy_revirement,moy_point=moy_point,
                           pourcentage_lancer_franc=pourcentage_lancer_franc,
                           pourcentage_2pt=pourcentage_2pt,pourcentage_3pt=pourcentage_3pt,
                           moy_min = moy_min)
  


#=========================
@app.route("/equipe", methods=['POST'])
def equipe():
     equipe = request.form.get('equipeSearch')
     return getEquipe(equipe)


@app.route("/equipe")
def getEquipe(equipe):
    conn= pymysql.connect( 
        host='localhost', 
        user='root', 
        password='1994',
        db='basketballer' )
    cmd="SELECT num_equipe FROM equipe WHERE nom_equipe='"+equipe+"';"
    cur=conn.cursor()
    cur.execute(cmd)
    id = cur.fetchone()[0]
    cmd='SELECT * FROM equipe WHERE num_equipe='+str(id)+';'
    cur=conn.cursor()
    cur.execute(cmd)
    info = cur.fetchone()
    cmd4="SELECT num_partie, annee FROM concoure WHERE num_equipe_loc="+str(id)+" OR num_equipe_vis="+str(id)+";"
    cur.execute(cmd4)
    info4 = cur.fetchall()
    id_partie=()
    for i in range (0,len(info4)): 
        id_partie = id_partie + ((info4[i][0],info4[i][1], ),)
    if(len(id_partie)==1) : 
        id_partie="("+ str(id_partie[0])+")"
    if (id_partie) :
        cmd5="SELECT partie.date_partie, E1.nom_equipe, E2.nom_equipe, partie.annee,partie.num_partie FROM partie,concoure, equipe E1, equipe E2 WHERE partie.num_partie=concoure.num_partie AND partie.annee=concoure.annee AND E1.num_equipe = concoure.num_equipe_loc AND E2.num_equipe = concoure.num_equipe_vis AND (partie.num_partie,partie.annee) IN "+str(id_partie)+";"
        cur.execute(cmd5)
        infoPartie = cur.fetchall()
    else : 
        infoPartie = ("inconnu","inconnu","inconnu","inconnu","inconnu")
    cmd2="SELECT id_joueur FROM contrat WHERE fin_excl='9999-12-31'AND num_equipe="+str(id)+";"
    cur.execute(cmd2)
    info2 = cur.fetchall()
    id_joueur=()
    for i in range (0,len(info2)): 
        id_joueur = id_joueur + (info2[i][0], )
    if(len(id_joueur)==1) : 
        id_joueur="("+ str(id_joueur[0])+")"

    if (id_joueur) :
        cmd3="SELECT joueur.id_joueur, joueur.nom_famille, joueur.prenom,joueur.role, contrat.dossard FROM joueur," \
             "contrat WHERE joueur.id_joueur = contrat.id_joueur AND joueur.id_joueur IN "+str(id_joueur)+";"
        cur.execute(cmd3)
        infoJoueur = cur.fetchall()
    else : 
        infoJoueur = ("inconnu","inconnu","inconnu","inconnu","inconnu")
    return render_template('equipe.html', nom=info[1], ville=info[2],pays=info[3],fondation=info[4],
                           infoPartie=infoPartie, infoJoueur=infoJoueur)




@app.route("/partie/<annee>/<num>")
def getPartie(annee=None,num=None):
    conn= pymysql.connect( 
        host='localhost', 
        user='root', 
        password='1994',
        db='basketballer' )
    #recuperation des infos generales
    cmd='SELECT * FROM partie WHERE num_partie ='+num+' AND annee='+annee+';'
    cur=conn.cursor()
    cur.execute(cmd)
    info = cur.fetchone()
    #recuperation des noms d'equipe
    cmd2='SELECT E1.nom_equipe, E2.nom_equipe FROM concoure,equipe E1, equipe E2 WHERE E1.num_equipe = concoure.num_equipe_loc AND E2.num_equipe = concoure.num_equipe_vis AND num_partie ='+num+' AND annee='+annee+';'
    cur.execute(cmd2)
    equipes = cur.fetchone()
    #liste joueur equipe 1 
    cmd3="SELECT J.id_joueur, Ct.dossard,J.nom_famille, J.prenom, J.role, PA.minutes,"\
    "COUNT(IF(A.type_action='faute'  AND A.annee=P.annee AND A.num_partie=P.num_partie AND A.id_joueur=J.id_joueur,1,NULL)) AS nb_faute,"\
    "COUNT(IF(A.type_action='rebond' AND A.annee=P.annee AND A.num_partie=P.num_partie AND A.id_joueur=J.id_joueur,1,NULL)) AS nb_rebond,"\
    "COUNT(IF(A.type_action='revirement' AND A.annee=P.annee AND A.num_partie=P.num_partie AND A.id_joueur=J.id_joueur AND" \
    "(SELECT type_revirement FROM revirement WHERE annee=A.annee AND num_partie = A.num_partie AND instant = A.instant)='offensif'"\
    ",1,NULL)) AS nb_revirement ," \
    "COUNT(IF(A.type_action='lancer'  AND A.annee=P.annee AND A.num_partie=P.num_partie AND" \
    "(SELECT id_joueur FROM assiste WHERE annee=A.annee AND num_partie = A.num_partie AND instant = A.instant) = J.id_joueur" \
    ",1,NULL)) AS asisstance ," \
    "COUNT(IF(A.type_action='lancer' AND A.annee=P.annee AND A.num_partie=P.num_partie AND A.id_joueur=J.id_joueur AND" \
    "(SELECT type_lancer FROM lancer WHERE annee=A.annee AND num_partie = A.num_partie AND instant = A.instant AND est_panier=1) = '1pt'" \
    ",1,NULL)) AS lancerfranc, "\
    "COUNT(IF(A.type_action='lancer' AND A.annee=P.annee AND A.num_partie=P.num_partie AND A.id_joueur=J.id_joueur AND" \
    "(SELECT type_lancer FROM lancer WHERE annee=A.annee AND num_partie = A.num_partie AND instant = A.instant AND est_panier=1) = '2pt'"\
    ",1,NULL)) AS panier2pt," \
    "COUNT(IF(A.type_action='lancer' AND A.annee=P.annee AND A.num_partie=P.num_partie AND A.id_joueur=J.id_joueur AND" \
    "(SELECT type_lancer FROM lancer WHERE annee=A.annee AND num_partie = A.num_partie AND instant = A.instant AND est_panier=1) = '3pt'" \
    ",1,NULL)) AS panier3ptc," \
    "COUNT(IF(A.type_action='revirement' AND A.annee=P.annee AND A.num_partie=P.num_partie AND A.id_joueur=J.id_joueur AND"\
	 "(SELECT type_revirement FROM revirement WHERE annee=A.annee AND num_partie = A.num_partie AND instant = A.instant)='defensif'"\
    ",1,NULL)) AS nb_volballe"\
    " FROM  partie P,concoure Cc, contrat Ct, participe PA, joueur J, action A" \
    " WHERE P.annee ="+annee+" AND P.num_partie ="+num+" AND" \
    " Cc.annee= P.annee AND Cc.num_partie = P.num_partie" \
    " AND PA.annee = P.annee AND PA.num_partie = P.num_partie" \
    " AND J.id_joueur = PA.id_joueur" \
    " AND Ct.id_joueur = J.id_joueur AND Ct.num_equipe = Cc.num_equipe_loc" \
    " AND Ct.debut_incl <= P.date_partie AND P.date_partie < Ct.fin_excl" \
    " GROUP BY J.id_joueur;" 
    cur.execute(cmd3)
    joueurs1 = cur.fetchall()
    #liste joueur equipe 2 
    cmd4="SELECT J.id_joueur, Ct.dossard,J.nom_famille, J.prenom, J.role, PA.minutes,"\
    "COUNT(IF(A.type_action='faute'  AND A.annee=P.annee AND A.num_partie=P.num_partie AND A.id_joueur=J.id_joueur,1,NULL)) AS nb_faute,"\
    "COUNT(IF(A.type_action='rebond' AND A.annee=P.annee AND A.num_partie=P.num_partie AND A.id_joueur=J.id_joueur,1,NULL)) AS nb_rebond,"\
    "COUNT(IF(A.type_action='revirement' AND A.annee=P.annee AND A.num_partie=P.num_partie AND A.id_joueur=J.id_joueur AND" \
    "(SELECT type_revirement FROM revirement WHERE annee=A.annee AND num_partie = A.num_partie AND instant = A.instant)='offensif'"\
    ",1,NULL)) AS nb_revirement ," \
    "COUNT(IF(A.type_action='lancer'  AND A.annee=P.annee AND A.num_partie=P.num_partie AND" \
    "(SELECT id_joueur FROM assiste WHERE annee=A.annee AND num_partie = A.num_partie AND instant = A.instant) = J.id_joueur" \
    ",1,NULL)) AS asisstance ," \
    "COUNT(IF(A.type_action='lancer' AND A.annee=P.annee AND A.num_partie=P.num_partie AND A.id_joueur=J.id_joueur AND" \
    "(SELECT type_lancer FROM lancer WHERE annee=A.annee AND num_partie = A.num_partie AND instant = A.instant AND est_panier=1) = '1pt'" \
    ",1,NULL)) AS lancerfranc, "\
    "COUNT(IF(A.type_action='lancer' AND A.annee=P.annee AND A.num_partie=P.num_partie AND A.id_joueur=J.id_joueur AND" \
    "(SELECT type_lancer FROM lancer WHERE annee=A.annee AND num_partie = A.num_partie AND instant = A.instant AND est_panier=1) = '2pt'"\
    ",1,NULL)) AS panier2pt," \
    "COUNT(IF(A.type_action='lancer' AND A.annee=P.annee AND A.num_partie=P.num_partie AND A.id_joueur=J.id_joueur AND" \
    "(SELECT type_lancer FROM lancer WHERE annee=A.annee AND num_partie = A.num_partie AND instant = A.instant AND est_panier=1) = '3pt'" \
    ",1,NULL)) AS panier3ptc," \
    "COUNT(IF(A.type_action='revirement' AND A.annee=P.annee AND A.num_partie=P.num_partie AND A.id_joueur=J.id_joueur AND"\
	 "(SELECT type_revirement FROM revirement WHERE annee=A.annee AND num_partie = A.num_partie AND instant = A.instant)='defensif'"\
    ",1,NULL)) AS nb_volballe"\
    " FROM  partie P,concoure Cc, contrat Ct, participe PA, joueur J, action A" \
    " WHERE P.annee ="+annee+" AND P.num_partie ="+num+" AND" \
    " Cc.annee= P.annee AND Cc.num_partie = P.num_partie" \
    " AND PA.annee = P.annee AND PA.num_partie = P.num_partie" \
    " AND J.id_joueur = PA.id_joueur" \
    " AND Ct.id_joueur = J.id_joueur AND Ct.num_equipe = Cc.num_equipe_vis" \
    " AND Ct.debut_incl <= P.date_partie AND P.date_partie < Ct.fin_excl" \
    " GROUP BY J.id_joueur;" 
    cur.execute(cmd4)
    joueurs2 = cur.fetchall()
    #liste action
    cmd5="SELECT action.instant, action.type_action, equipe.nom_equipe, joueur.nom_famille, joueur.prenom FROM action, equipe, contrat, joueur WHERE action.id_joueur = contrat.id_joueur AND contrat.num_equipe = equipe.num_equipe AND joueur.id_joueur = action.id_joueur AND action.num_partie ="+num+" AND action.annee="+annee+";"
    cur.execute(cmd5)
    actions = cur.fetchall()
    return render_template('partie.html', info=info,equipes= equipes, joueurs1=joueurs1, joueurs2=joueurs2, actions = actions)
  
        

#=====================================

if __name__ == "__main__":
    app.run()




