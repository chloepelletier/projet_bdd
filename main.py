from flask import Flask, render_template, request


app = Flask(__name__) 




@app.route("/") 
def accueil(id=None): 
    return render_template('accueil.html') 


        
#====================
import pymysql 
import pymysql.cursors 

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
    return render_template('joueur.html', prenom=info[1], nom=info[2],
                           naissance= info[3], taille=info[4], poids=info[5], 
                           position= info[6], bras=info[8], numero=info2[4],equipe=info3[1],
                           pays=info3[3])
  
        

#=========================

@app.route("/equipe/<id>")
def getEquipe(id=None):
    conn= pymysql.connect( 
        host='localhost', 
        user='root', 
        password='1994',
        db='basketballer' )
    cmd='SELECT * FROM equipe WHERE num_equipe='+id+';'
    cur=conn.cursor()
    cur.execute(cmd)
    info = cur.fetchone()
    cmd4="SELECT num_partie, annee FROM concoure WHERE num_equipe_loc="+id+" OR num_equipe_vis="+id+";"
    cur.execute(cmd4)
    info4 = cur.fetchall()
    id_partie=()
    for i in range (0,len(info4)): 
        id_partie = id_partie + ((info4[i][0],info4[i][1], ),)
    if (id_partie) :
        cmd5="SELECT partie.date_partie, E1.nom_equipe, E2.nom_equipe, partie.annee,partie.num_partie FROM partie,concoure, equipe E1, equipe E2 WHERE partie.num_partie=concoure.num_partie AND partie.annee=concoure.annee AND E1.num_equipe = concoure.num_equipe_loc AND E2.num_equipe = concoure.num_equipe_vis AND (partie.num_partie,partie.annee) IN "+str(id_partie)+";"
        cur.execute(cmd5)
        infoPartie = cur.fetchall()
    else : 
        infoPartie = ("inconnu","inconnu","inconnu","inconnu","inconnu")
    cmd2="SELECT id_joueur FROM contrat WHERE fin_excl='9999-12-31'AND num_equipe="+id+";"
    cur.execute(cmd2)
    info2 = cur.fetchall()
    id_joueur=()
    for i in range (0,len(info2)): 
        id_joueur = id_joueur + (info2[i][0], )
    if(len(id_joueur)==1) : 
        id_joueur="("+ str(id_joueur[0])+")"
     if (id_joueur) :
        cmd3="SELECT joueur.id_joueur, joueur.nom_famille, joueur.prenom,joueur.role, contrat.dossard FROM joueur, contrat WHERE joueur.id_joueur = contrat.id_joueur AND joueur.id_joueur IN "+str(id_joueur)+";"
        cur.execute(cmd3)
        infoJoueur = cur.fetchall()
    else : 
        infoJoueur = ("inconnu","inconnu","inconnu","inconnu","inconnu")
    return render_template('equipe.html', nom=info[1], ville=info[2],pays=info[3],fondation=info[4],
                           infoPartie=infoPartie, infoJoueur=infoJoueur)


@app.route("/partie/<id>") 
def partie(id=None): 
    return render_template('partie.html')


if __name__ == "__main__":
    app.run()




