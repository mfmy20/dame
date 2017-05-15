from tkinter import *
from random import *
from copy import *
launcher = Tk()
launcher.title('Launcher')
launcher.geometry('200x100+900+450') #le 200*100 représente la taille tandis que 900+450 répresente la postion de départ

player = "white" #variable de début pour éviter tout bug
profondeur = 5
premier_coup = True
     
menubar = Menu(launcher) #obligé pour crée un menu glissant
def facile():              # fonction transformant les variables de bases
    global profondeur
    profondeur = 4

def moyen():
    global profondeur
    profondeur = 5

def difficile():
    global profondeur
    profondeur = 6
    
def impossible():
    global profondeur
    profondeur = 7

def joueur():
    global player
    player = Value.get()

def launch(): #permet de lancer le jeu en fermant le launcher
    launcher.quit()
    launcher.destroy()
    
difficulte = Menu(menubar, tearoff=0)
difficulte.add_command(label="Facile", command=facile)
difficulte.add_command(label="Moyen", command=moyen)
difficulte.add_command(label="Difficile", command=difficile)
difficulte.add_command(label="Impossible", command=impossible)
menubar.add_cascade(label="Difficulté", menu=difficulte) #crée le menu glissant

label = Label(launcher, text="choisissez votre couleur:")
label.pack()

Value = StringVar() 
bouton1 = Radiobutton(launcher, text="Blanc", variable=Value, value="white", command=joueur) #groupe de boutton
bouton2 = Radiobutton(launcher, text="Noir", variable=Value, value="black", command = joueur)
bouton1.pack()
bouton2.pack()

bouton=Button(launcher, text="Lance le jeu", command=launch)
bouton.pack()

launcher.config(menu=menubar)
launcher.mainloop()
fenetre = Tk()
fenetre.title('Plateau')
list_jeton_noir = []   #valeur de base
list_jeton_blanc = []
list_jeton = []
case = []
jeton_doit_joue = []

def MinMax(Rafle): #Lancement de l'IA
    IA = True             #valeur de base de l'IA
    list_jeton_simule = []
    jeton_blanc_simule = []
    jeton_noir_simule = []
    alpha = -100000000
    beta = 100000000
    for i in list_jeton_blanc:      #générent les listes de simulations 
        coord = plateau.coords(i)
        tag = plateau.gettags(i)
        if tag.count('dame'):
            tag = 'dame'
        else:
            tag = None
        jeton = []
        jeton.append(i)
        jeton.append(coord[0])
        jeton.append(coord[1])
        jeton.append("white")
        jeton.append(tag)
        jeton_blanc_simule.append(jeton)
        list_jeton_simule.append(jeton)
    for i in list_jeton_noir:
        coord = plateau.coords(i)
        tag = plateau.gettags(i)
        if tag.count('dame'):
            tag = 'dame'
        else:
            tag = None
        jeton = []
        jeton.append(i)
        jeton.append(coord[0])
        jeton.append(coord[1])
        jeton.append("black")
        jeton.append(tag)
        jeton_noir_simule.append(jeton)      
        list_jeton_simule.append(jeton)
    doit_IA_manger(IA,list_jeton_simule,jeton_blanc_simule,jeton_noir_simule) #permet de choisir quel action à simuler
    if a_manger:
        for d in a_manger:
            if Rafle:
                if d[0][0] == Rafle:
                    list_jeton_simule2 = deepcopy(list_jeton_simule)
                    jeton_blanc_simule2 = deepcopy(jeton_blanc_simule)
                    jeton_noir_simule2 = deepcopy(jeton_noir_simule)
                    d2 = deepcopy(d)
                    val = Min(d2,list_jeton_simule2,jeton_blanc_simule2,jeton_noir_simule2,profondeur-1,alpha,beta)
                    if val > alpha or (val == alpha and randint(1,2) == 2):
                        alpha = val
                        MeilleurCoup = d
            else:
                list_jeton_simule2 = deepcopy(list_jeton_simule)
                jeton_blanc_simule2 = deepcopy(jeton_blanc_simule)
                jeton_noir_simule2 = deepcopy(jeton_noir_simule)
                d2 = deepcopy(d)
                val = Min(d2,list_jeton_simule2,jeton_blanc_simule2,jeton_noir_simule2,profondeur-1,alpha,beta)
                if val > alpha or (val == alpha and randint(1,2) == 2):
                    alpha = val
                    MeilleurCoup = d
    else:
        if player == "white":
            jeton_doit_joue = jeton_noir_simule.copy()
        else:
            jeton_doit_joue = jeton_blanc_simule.copy()
        jeton_doit_joue = verification_IA(jeton_doit_joue,list_jeton_simule,jeton_blanc_simule,jeton_noir_simule)
        for c in jeton_doit_joue:
            case_possible = case_jouable_IA(c,list_jeton_simule,jeton_blanc_simule,jeton_noir_simule)
            for d in case_possible:
                action = []
                action.append(c)
                action.append(None)
                action.append(d[0])
                action.append(d[1])
                list_jeton_simule2 = deepcopy(list_jeton_simule)#permet de sauvegarder l’intérieur des listes
                jeton_blanc_simule2 = deepcopy(jeton_blanc_simule)
                jeton_noir_simule2 = deepcopy(jeton_noir_simule)
                action2 = deepcopy(action)
                val = Min(action2,list_jeton_simule2,jeton_blanc_simule2,jeton_noir_simule2,profondeur-1,alpha,beta)#la valeur retourner par la fonction min sera égale à val
                if val > alpha or (val == alpha and randint(1,2) == 2):
                    alpha = val
                    MeilleurCoup = action
    return MeilleurCoup #renvoie le coup à joué

def Min(d,list_jeton_simule,jeton_blanc_simule,jeton_noir_simule,profondeur,alpha,beta):
    IA = False
    if d[1]:
        color = d[1][3]
        d[0][1] = d[2]
        d[0][2] = d[3]
        if color == "white":
            jeton_blanc_simule.remove(d[1])
            list_jeton_simule.remove(d[1])
        elif color == "black":
            jeton_noir_simule.remove(d[1])
            list_jeton_simule.remove(d[1])
        dames_IA(d[0])
        jeton_doit_joue = doit_IA_manger(not IA,list_jeton_simule,jeton_blanc_simule,jeton_noir_simule)
        if a_manger:
            for d in a_manger: #au cas ou un il y a une rafle on reste sur une fonction max
                list_jeton_simule2 = deepcopy(list_jeton_simule)
                jeton_blanc_simule2 = deepcopy(jeton_blanc_simule)
                jeton_noir_simule2 = deepcopy(jeton_noir_simule)
                d2 = deepcopy(d)
                val = Min(d2,list_jeton_simule2,jeton_blanc_simule2,jeton_noir_simule2,profondeur-1,alpha,beta)
                if val > alpha or (val == alpha and randint(1,2) == 2):
                    alpha = val
                if beta <= alpha:
                    return alpha
            return alpha
    else:
        d[0][1] = d[2]
        d[0][2] = d[3]
        dames_IA(d[0])
    jeton_doit_joue = doit_IA_manger(IA,list_jeton_simule,jeton_blanc_simule,jeton_noir_simule)
    if not jeton_doit_joue:
        if player == "white":
            jeton_doit_joue = jeton_blanc_simule.copy()
        else:
            jeton_doit_joue = jeton_noir_simule.copy()
        jeton_doit_joue = verification_IA(jeton_doit_joue,list_jeton_simule,jeton_blanc_simule,jeton_noir_simule)
    if profondeur == 0 or not jeton_blanc_simule or not jeton_noir_simule or not jeton_doit_joue:
        if (player == "white" and not jeton_noir_simule) or (player == "black" and not jeton_blanc_simule):
            evalu = -5000
        elif (player == "white" and (not jeton_blanc_simule or not jeton_doit_joue)) or (player == "black" and (not jeton_blanc_simule or not jeton_doit_joue)):
            evalu = 5000
        else:
            evalu = 0
        return evaluer(list_jeton_simule,jeton_blanc_simule,jeton_noir_simule,evalu)
    else:
        if a_manger:
            for d in a_manger:
                list_jeton_simule2 = deepcopy(list_jeton_simule)
                jeton_blanc_simule2 = deepcopy(jeton_blanc_simule)
                jeton_noir_simule2 = deepcopy(jeton_noir_simule)
                d2 = deepcopy(d)
                val = Min(d2,list_jeton_simule2,jeton_blanc_simule2,jeton_noir_simule2,profondeur-1,alpha,beta)
                if val < beta or (val == beta and randint(1,2) == 2):
                    beta = val
                if beta <= alpha:
                    return beta
        else:
            for c in jeton_doit_joue:
                case_possible = case_jouable_IA(c,list_jeton_simule,jeton_blanc_simule,jeton_noir_simule)
                for d in case_possible:
                    action = []
                    action.append(c)
                    action.append(None)
                    action.append(d[0])
                    action.append(d[1])
                    list_jeton_simule2 = deepcopy(list_jeton_simule)
                    jeton_blanc_simule2 = deepcopy(jeton_blanc_simule)
                    jeton_noir_simule2 = deepcopy(jeton_noir_simule)
                    action2 = deepcopy(action)
                    val = Max(action2,list_jeton_simule2,jeton_blanc_simule2,jeton_noir_simule2,profondeur-1,alpha,beta)
                    if val < beta or (val == beta and randint(1,2) == 2):
                        beta = val
                    if beta <= alpha:
                        return beta
    return beta

def Max(d,list_jeton_simule,jeton_blanc_simule,jeton_noir_simule,profondeur,alpha,beta): #même chose que les deux précedents
    IA = True
    if d[1]:
        d[0][1] = d[2]
        d[0][2] = d[3]
        if color == "white":
            jeton_blanc_simule.remove(d[1])
        else:
            jeton_noir_simule.remove(d[1])
        list_jeton_simule.remove(d[1])
        dames_IA(d[0])
        jeton_doit_joue = doit_IA_manger(not IA,list_jeton_simule,jeton_blanc_simule,jeton_noir_simule)
        if a_manger:
            for d in a_manger:
                list_jeton_simule2 = deepcopy(list_jeton_simule)
                jeton_blanc_simule2 = deepcopy(jeton_blanc_simule)
                jeton_noir_simule2 = deepcopy(jeton_noir_simule)
                d2 = deepcopy(d)
                val = Min(d2,list_jeton_simule2,jeton_blanc_simule2,jeton_noir_simule2,profondeur-1,alpha,beta)
                if val < beta or (val == beta and randint(1,2) == 2):
                    beta = val
                if beta <= alpha:
                    return beta
            return beta
    else:
        d[0][1] = d[2]
        d[0][2] = d[3]
        dames_IA(d[0])
    jeton_doit_joue = doit_IA_manger(IA,list_jeton_simule,jeton_blanc_simule,jeton_noir_simule)
    if not jeton_doit_joue:
        if player == "white":
            jeton_doit_joue = jeton_noir_simule.copy()
        else:
            jeton_doit_joue = jeton_blanc_simule.copy()
        jeton_doit_joue = verification_IA(jeton_doit_joue,list_jeton_simule,jeton_blanc_simule,jeton_noir_simule)
    if profondeur == 0 or not jeton_blanc_simule or not jeton_noir_simule or not jeton_doit_joue:
        if (player == "white" and not jeton_blanc_simule) or (player == "black" and not jeton_noir_simule):
            evalu = 5000
        elif (player == "white" and (not jeton_noir_simule or not jeton_doit_joue)) or (player == "black" and (not jeton_noir_simule or not jeton_doit_joue)):
            evalu = -5000
        else:
            evalu = 0
        return evaluer(list_jeton_simule,jeton_blanc_simule,jeton_noir_simule,evalu)
    else:
        if a_manger:
            for d in a_manger:
                list_jeton_simule2 = deepcopy(list_jeton_simule)
                jeton_blanc_simule2 = deepcopy(jeton_blanc_simule)
                jeton_noir_simule2 = deepcopy(jeton_noir_simule)
                d2 = deepcopy(d)
                val = Min(d2,list_jeton_simule2,jeton_blanc_simule2,jeton_noir_simule2,profondeur-1,alpha,beta)
                if val > alpha or (val == alpha and randint(1,2) == 2):
                    alpha = val
                if beta <= alpha:
                    return alpha
        else:
            for c in jeton_doit_joue:
                case_possible = case_jouable_IA(c,list_jeton_simule,jeton_blanc_simule,jeton_noir_simule)
                for d in case_possible:
                    action = []
                    action.append(c)
                    action.append(None)
                    action.append(d[0])
                    action.append(d[1])
                    list_jeton_simule2 = deepcopy(list_jeton_simule)
                    jeton_blanc_simule2 = deepcopy(jeton_blanc_simule)
                    jeton_noir_simule2 = deepcopy(jeton_noir_simule)
                    action2 = deepcopy(action)
                    val = Min(action2,list_jeton_simule2,jeton_blanc_simule2,jeton_noir_simule2,profondeur-1,alpha,beta)
                    if val > alpha or (val == alpha and randint(1,2) == 2):
                        alpha = val
                    if beta <= alpha:
                        return alpha
    return alpha

def evaluer(list_jeton_simule,jeton_blanc_simule,jeton_noir_simule,val): 
    for c in jeton_blanc_simule: 
        tag = c[4] #on prend le tag du jeton
        if player == "white":
            if tag == 'dame': #on comptabilise les jetons dames et normaux
                val -= 3 #avec des valeurs négatives si c'est les jetons du joueurs 
            else:
                val -= 1
        else:
            if tag == 'dame':
                val += 3 #avec des valeurs positives positives si c'est les jetons de l'IA
            else:
                val += 1
    for c in jeton_noir_simule:
        tag = c[4]
        if player == "white":
            if tag == 'dame':
                val += 3
            else:
                val += 1
        else:
            if tag == 'dame':
                val -= 3
            else:
                val -= 1
    return val

def doit_IA_manger(IA,list_jeton_simule,jeton_blanc_simule,jeton_noir_simule):
    global a_manger #exectement le même principe que les fonctions doit_noir_manger et doit_blanc_manger
    a_manger = []
    jeton_doit_joue = []
    if (IA and player == "white") or (not IA and player == "black"):
        for c in jeton_noir_simule:
            coord_noir  = []
            coord_noir.append(c[1])
            coord_noir.append(c[2])
            tag = c[4]
            for d in jeton_blanc_simule:
                coord_blanc = []
                coord_blanc.append(d[1])
                coord_blanc.append(d[2])
                k = 1
                while k <= 9:
                    ne_peu = False
                    if (coord_noir[0] == coord_blanc[0]-100*k or coord_noir[0] == coord_blanc[0]+100*k) and (coord_noir[1] == coord_blanc[1]-100*k or coord_noir[1] == coord_blanc[1]+100*k):
                        if (coord_noir[0]+100*k == coord_blanc[0]  and coord_noir[0]+100*(k+1) <= 900) or (coord_noir[0]-100*k == coord_blanc[0] and coord_noir[0]-100*(k+1 ) >= 0) or (coord_noir[1]+100*k == coord_blanc[0] and coord_noir[1]+100*(k+1) <= 900) or (coord_noir[1]+100*k == coord_blanc[0] and coord_noir[1]-100*(k+1) >= 0):
                            for e in list_jeton_simule:
                                coord_sec = []
                                coord_sec.append(e[1])
                                coord_sec.append(e[2])
                                if (coord_noir[0] == coord_blanc[0]-100*k == coord_sec[0]-100*(k+1) or coord_noir[0] == coord_blanc[0]+100*k == coord_sec[0]+100*(k+1)) and (coord_noir[1] == coord_blanc[1]-100*k == coord_sec[1]-100*(k+1) or coord_noir[1] == coord_blanc[1]+100*k == coord_sec[1]+100*(k+1)):
                                    ne_peu = True
                                if k > 1 and (coord_noir[0] == coord_blanc[0]-100*k == coord_sec[0]-100*(k-1) or coord_noir[0] == coord_blanc[0]+100*k == coord_sec[0]+100*(k-1)) and (coord_noir[1] == coord_blanc[1]-100*k == coord_sec[1]-100*(k-1) or coord_noir[1] == coord_blanc[1]+100*k == coord_sec[1]+100*(k-1)):
                                    ne_peu = True
                            if not ne_peu:
                                if coord_blanc[0] == coord_noir[0]-100*k:
                                    X = coord_noir[0]-100*(k+1)
                                else:
                                    X = coord_noir[0]+100*(k+1)
                                if coord_blanc[1] == coord_noir[1]-100*k:
                                    Y = coord_noir[1]-100*(k+1)
                                else:
                                    Y = coord_noir[1]+100*(k+1)
                                C = []
                                C.append(c)
                                C.append(d)
                                C.append(X)
                                C.append(Y)
                                a_manger.append(C)
                                jeton_doit_joue.append(c)
                                if X < 0 or Y < 0 or X > 900 or Y > 900:
                                    a_manger.remove(C)
                                    jeton_doit_joue.remove(c)
                    if tag == 'dame':
                        k += 1
                    else:
                        break
        return jeton_doit_joue
    else:
        for c in jeton_blanc_simule:
            coord_blanc  = []
            coord_blanc.append(c[1])
            coord_blanc.append(c[2])
            tag = c[4]
            for d in jeton_noir_simule:
                coord_noir = []
                coord_noir.append(d[1])
                coord_noir.append(d[2])
                k = 1
                while k <= 9:
                    ne_peu = False
                    if (coord_blanc[0] == coord_noir[0]-100*k or coord_blanc[0] == coord_noir[0]+100*k) and (coord_blanc[1] == coord_noir[1]-100*k or coord_blanc[1] == coord_noir[1]+100*k):
                        if (coord_blanc[0]+100*k == coord_noir[0]  and coord_blanc[0]+100*(k+1) <= 900) or (coord_blanc[0]-100*k == coord_noir[0] and coord_blanc[0]-100*(k+1 ) >= 0) or (coord_blanc[1]+100*k == coord_noir[0] and coord_blanc[1]+100*(k+1) <= 900) or (coord_blanc[1]+100*k == coord_noir[0] and coord_blanc[1]-100*(k+1) >= 0):
                            for e in list_jeton_simule:
                                coord_sec = []
                                coord_sec.append(e[1])
                                coord_sec.append(e[2])
                                if (coord_blanc[0] == coord_noir[0]-100*k == coord_sec[0]-100*(k+1) or coord_blanc[0] == coord_noir[0]+100*k == coord_sec[0]+100*(k+1)) and (coord_blanc[1] == coord_noir[1]-100*k == coord_sec[1]-100*(k+1) or coord_blanc[1] == coord_noir[1]+100*k == coord_sec[1]+100*(k+1)):
                                    ne_peu = True
                                if k > 1 and (coord_blanc[0] == coord_noir[0]-100*k == coord_sec[0]-100*(k-1) or coord_blanc[0] == coord_noir[0]+100*k == coord_sec[0]+100*(k-1)) and (coord_blanc[1] == coord_noir[1]-100*k == coord_sec[1]-100*(k-1) or coord_blanc[1] == coord_noir[1]+100*k == coord_sec[1]+100*(k-1)):
                                    ne_peu = True
                            if not ne_peu:
                                if coord_noir[0] == coord_blanc[0]-100*k:
                                    X = coord_blanc[0]-100*(k+1)
                                else:
                                    X = coord_blanc[0]+100*(k+1)
                                if coord_noir[1] == coord_blanc[1]-100*k:
                                    Y = coord_blanc[1]-100*(k+1)
                                else:
                                    Y = coord_blanc[1]+100*(k+1)
                                C = []
                                C.append(c)
                                C.append(d)
                                C.append(X)
                                C.append(Y)
                                a_manger.append(C)
                                jeton_doit_joue.append(c)
                                if X < 0 or Y < 0 or X > 900 or Y > 900:
                                    a_manger.remove(C)
                                    jeton_doit_joue.remove(c)
                    if tag == 'dame':
                        k += 1
                    else:
                        break
        return jeton_doit_joue

def verification_IA(jeton_doit_joue,list_jeton_simule,jeton_blanc_simule,jeton_noir_simule): #meme principe que la fonction vérifié
    jeton_suppr = []
    for c in jeton_doit_joue:
        coord = []
        coord.append(c[1])
        coord.append(c[2])
        couleur_jeton1 = c[3]
        tag = c[4]
        nbr_case = 0
        if tag == 'dame':
            possibilite = 4
            for e in list_jeton_simule:
                couleur_jeton2 = e[3]
                coord_2 = []
                coord_2.append(e[1])
                coord_2.append(e[2])
                if couleur_jeton1 == couleur_jeton2 and (coord[0] == coord_2[0]-100 or coord[0] == coord_2[0]+100) and (coord[1] == coord_2[1]-100 or coord[1] == coord_2[1]+100):
                    possibilite -= 1
                elif couleur_jeton1 != couleur_jeton2 and (coord[0] == coord_2[0]-100 or coord[0] == coord_2[0]+100) and (coord[1] == coord_2[1]-100 or coord[1] == coord_2[1]+100):
                    if coord[0]+200 == coord_2[0]+100 <= 900 or coord[0]-200 == coord_2[0]-100 >= 0 or coord[1]+200 == coord_2[1]+100 <= 900 or coord[1]-200 == coord_2[1]-100 >= 0:
                        for f in list_jeton_simule:
                            coord_sec = []
                            coord_sec.append(f[1])
                            coord_sec.append(f[2])
                            if (coord[0] == coord_2[0]-100 == coord_sec[0]-200 or coord[0] == coord_2[0]+100 == coord_sec[0]+200) and (coord[1] == coord_2[1]-100 == coord_sec[1]-200 or coord[1] == coord_2[1]+100 == coord_sec[1]+200):
                                possibilite -= 1
        else:
            possibilite = 2
            for e in list_jeton_simule:
                couleur_jeton2 = e[3]
                coord_2 = []
                coord_2.append(e[1])
                coord_2.append(e[2])
                if couleur_jeton1 == "white" and (coord[0] == coord_2[0]-100 or coord[0] == coord_2[0]+100) and coord[1] == coord_2[1]+100:
                    if couleur_jeton2 == "white":
                        possibilite -= 1
                elif couleur_jeton1 == "black" and (coord[0] == coord_2[0]-100 or coord[0] == coord_2[0]+100) and coord[1] == coord_2[1]-100:
                    if couleur_jeton2 == "black":
                        possibilite -= 1
                if couleur_jeton1 != couleur_jeton2 and (coord[0] == coord_2[0]-100 or coord[0] == coord_2[0]+100) and (coord[1] == coord_2[1]-100 or coord[1] == coord_2[1]+100):
                    if couleur_jeton1 == "white" and coord[1] == coord_2[1]-100 and coord[1]-200 >= 0:
                        possibilite += 1
                    if couleur_jeton1 == "black" and coord[1] == coord_2[1]+100 and coord[1]+200 <= 900:
                        possibilite += 1
                    if (coord[0]+200 == coord_2[0]+100 <= 900 or coord[0]-200 == coord_2[0]-100 >= 0) and (coord[1]+200 == coord_2[1]+100 <= 900 or coord[1]-200 == coord_2[1]-100 >= 0):
                        for f in list_jeton_simule:
                            coord_sec = []
                            coord_sec.append(f[1])
                            coord_sec.append(f[2])
                            if (coord[0] == coord_2[0]-100 == coord_sec[0]-200 or coord[0] == coord_2[0]+100 == coord_sec[0]+200) and (coord[1] == coord_2[1]-100 == coord_sec[1]-200 or coord[1] == coord_2[1]+100 == coord_sec[1]+200):
                                possibilite -= 1
                    else:
                        possibilite -= 1
        for g in case:
                coord_case = plateau.coords(g)
                if (coord[0]-100 == coord_case[0] or coord[0]+100 == coord_case[0]) and (coord[1]-100 == coord_case[1] or coord[1]+100 == coord_case[1]):
                    nbr_case += 1
        if (couleur_jeton1 == "white" and coord[1] == 900) or (couleur_jeton1 == "black" and coord[1] == 0):
            possibilite += 1
        if nbr_case != 4:
            possibilite -= 1
        if nbr_case == 1:
            possibilite -= 1
        if possibilite <= 0:
                jeton_suppr.append(c)
    for c in jeton_suppr:
        jeton_doit_joue.remove(c)
    return jeton_doit_joue

def case_jouable_IA(d,list_jeton_simule,jeton_blanc_simule,jeton_noir_simule): #même principe que la fonction case_jouable
    color = d[3]
    tag = d[4]
    case_possible =[]
    coord = []
    coord.append(d[1])
    coord.append(d[2])
    k = 1
    while k < 10:
        if color == "white":
            add_XY = []
            add_XY.append(coord[0]-100*k)
            add_XY.append(coord[1]-100*k)
            case_possible.append(add_XY)
            add_XY = []
            add_XY.append(coord[0]+100*k)
            add_XY.append(coord[1]-100*k)
            case_possible.append(add_XY)
        else:
            add_XY = []
            add_XY.append(coord[0]-100*k)
            add_XY.append(coord[1]+100*k)
            case_possible.append(add_XY)
            add_XY = []
            add_XY.append(coord[0]+100*k)
            add_XY.append(coord[1]+100*k)
            case_possible.append(add_XY)
        if tag == 'dame':
            if color == "white":
                add_XY = []
                add_XY.append(coord[0]-100*k)
                add_XY.append(coord[1]+100*k)
                case_possible.append(add_XY)
                add_XY = []
                add_XY.append(coord[0]+100*k)
                add_XY.append(coord[1]+100*k)
                case_possible.append(add_XY)
            else:
                add_XY = []
                add_XY.append(coord[0]-100*k)
                add_XY.append(coord[1]-100*k)
                case_possible.append(add_XY)
                add_XY = []
                add_XY.append(coord[0]+100*k)
                add_XY.append(coord[1]-100*k)
                case_possible.append(add_XY)
            k += 1
        else:
            break
    for c in case_possible:
        for d in list_jeton_simule:
            coord2 = []
            coord2.append(d[1])
            coord2.append(d[2])
            if coord2[0] == c[0] and coord2[1] == c[1]:
                case_possible.remove(c)
    for c in case_possible:
        if c[0] < 0 or c[0] > 900 or c[1] < 0 or c[1] > 900:
            case_possible.remove(c)
    return case_possible

def dames_IA(d): #même principe que dames
    coord = []
    coord.append(d[1])
    coord.append(d[2])
    color = d[3]
    if color == "white" and coord[1] == 0:
        d[4] = 'dame'
    elif color == "black" and coord[1] == 900:
        d[4] = 'dame'

def doit_noir_manger(): #même principe que doit_blanc_manger
    global a_manger
    a_manger = []
    jeton_doit_joue = []
    for c in list_jeton_noir:
        coord_noir  = plateau.coords(c)
        tag = plateau.gettags(c)
        for d in list_jeton_blanc:
            coord_blanc = plateau.coords(d)
            k = 1
            while k <= 9:
                ne_peu = False
                if (coord_noir[0] == coord_blanc[0]-100*k or coord_noir[0] == coord_blanc[0]+100*k) and (coord_noir[1] == coord_blanc[1]-100*k or coord_noir[1] == coord_blanc[1]+100*k):
                    if (coord_noir[0]+100*k == coord_blanc[0]  and coord_noir[0]+100*(k+1) <= 900) or (coord_noir[0]-100*k == coord_blanc[0] and coord_noir[0]-100*(k+1 ) >= 0) or (coord_noir[1]+100*k == coord_blanc[0] and coord_noir[1]+100*(k+1) <= 900) or (coord_noir[1]+100*k == coord_blanc[0] and coord_noir[1]-100*(k+1) >= 0):
                        for e in list_jeton:
                            coord_sec = plateau.coords(e)
                            if (coord_noir[0] == coord_blanc[0]-100*k == coord_sec[0]-100*(k+1) or coord_noir[0] == coord_blanc[0]+100*k == coord_sec[0]+100*(k+1)) and (coord_noir[1] == coord_blanc[1]-100*k == coord_sec[1]-100*(k+1) or coord_noir[1] == coord_blanc[1]+100*k == coord_sec[1]+100*(k+1)):
                                ne_peu = True
                            if k > 1 and (coord_noir[0] == coord_blanc[0]-100*k == coord_sec[0]-100*(k-1) or coord_noir[0] == coord_blanc[0]+100*k == coord_sec[0]+100*(k-1)) and (coord_noir[1] == coord_blanc[1]-100*k == coord_sec[1]-100*(k-1) or coord_noir[1] == coord_blanc[1]+100*k == coord_sec[1]+100*(k-1)):
                                ne_peu = True
                        if not ne_peu:
                            if coord_blanc[0] == coord_noir[0]-100*k:
                                X = coord_noir[0]-100*(k+1)
                            else:
                                X = coord_noir[0]+100*(k+1)
                            if coord_blanc[1] == coord_noir[1]-100*k:
                                Y = coord_noir[1]-100*(k+1)
                            else:
                                Y = coord_noir[1]+100*(k+1)
                            C = []
                            C.append(c)
                            C.append(d)
                            C.append(X)
                            C.append(Y)
                            a_manger.append(C)
                            jeton_doit_joue.append(c)
                            if X < 0 or Y < 0 or X > 900 or Y > 900:
                                a_manger.remove(C)
                                jeton_doit_joue.remove(c)
                if tag.count('dame'):
                    k += 1
                else:
                    break
    return jeton_doit_joue

def doit_blanc_manger():
    global a_manger
    a_manger = [] #création d'une liste vide pour contenir les pièces qui doivent mangent, celle qui seront manger et les coordonnées d'atterissage
    jeton_doit_joue = [] #création d'une liste vide pour contenir les jetons qui devront joué
    for c in list_jeton_blanc: #pour tout les jetons blancs
        coord_blanc  = plateau.coords(c) #leurs coordonnées
        tag = plateau.gettags(c) #et leurs tag (pour savoir si se sont des dames)
        for d in list_jeton_noir: #pour tout les jetons noirs
            coord_noir = plateau.coords(d)
            k = 1
            while k <= 9: #au cas où c'est une dame
                ne_peu = False #les 2 conditions suivantes permettent de vérifié que il y a bien un jeton noir à porté et que sa n'atterrisse pas dans une case hors du plateau
                if (coord_blanc[0] == coord_noir[0]-100*k or coord_blanc[0] == coord_noir[0]+100*k) and (coord_blanc[1] == coord_noir[1]-100*k or coord_blanc[1] == coord_noir[1]+100*k):
                    if (coord_blanc[0]+100*k == coord_noir[0]  and coord_blanc[0]+100*(k+1) <= 900) or (coord_blanc[0]-100*k == coord_noir[0] and coord_blanc[0]-100*(k+1 ) >= 0) or (coord_blanc[1]+100*k == coord_noir[0] and coord_blanc[1]+100*(k+1) <= 900) or (coord_blanc[1]+100*k == coord_noir[0] and coord_blanc[1]-100*(k+1) >= 0):
                        for e in list_jeton: #cette boucle permet de vérifié qu'il n'y pas un jeton derrière le jeton pouvant être pris
                            coord_sec = plateau.coords(e)
                            if (coord_blanc[0] == coord_noir[0]-100*k == coord_sec[0]-100*(k+1) or coord_blanc[0] == coord_noir[0]+100*k == coord_sec[0]+100*(k+1)) and (coord_blanc[1] == coord_noir[1]-100*k == coord_sec[1]-100*(k+1) or coord_blanc[1] == coord_noir[1]+100*k == coord_sec[1]+100*(k+1)):
                                ne_peu = True
                            if k > 1 and (coord_blanc[0] == coord_noir[0]-100*k == coord_sec[0]-100*(k-1) or coord_blanc[0] == coord_noir[0]+100*k == coord_sec[0]+100*(k-1)) and (coord_blanc[1] == coord_noir[1]-100*k == coord_sec[1]-100*(k-1) or coord_blanc[1] == coord_noir[1]+100*k == coord_sec[1]+100*(k-1)):
                                ne_peu = True
                        if not ne_peu: #si le jeton peut être pris le numéro du jeton prenant est enregistré ainsi que celui pris et avec les coordonnées d'atterrissage
                            if coord_noir[0] == coord_blanc[0]-100*k:
                                X = coord_blanc[0]-100*(k+1)
                            else:
                                X = coord_blanc[0]+100*(k+1)
                            if coord_noir[1] == coord_blanc[1]-100*k:
                                Y = coord_blanc[1]-100*(k+1)
                            else:
                                Y = coord_blanc[1]+100*(k+1)
                            C = []
                            C.append(c)
                            C.append(d)
                            C.append(X)
                            C.append(Y)
                            a_manger.append(C)
                            jeton_doit_joue.append(c)
                            if X < 0 or Y < 0 or X > 900 or Y > 900:
                                a_manger.remove(C)
                                jeton_doit_joue.remove(c)
                if tag.count('dame'): #si c'est une dame on vérifié pour les cases suivantes
                    k += 1
                else: #sinon on stop
                    break
    return jeton_doit_joue  #renvoie les jetons devants êtres jouent

def verification_jeton(jeton_doit_joue):
    jeton_suppr = [] #crée une liste qui supprimera les jetons de jeton_doit_joue
    for c in jeton_doit_joue:
        coord = plateau.coords(c)
        couleur_jeton1 = plateau.itemcget(c,"fill")
        tag = plateau.gettags(c)
        nbr_case = 0
        if tag.count('dame'): 
            possibilite = 4
            for e in list_jeton:
                couleur_jeton2 = plateau.itemcget(e,"fill")
                coord_2 = plateau.coords(e)
                if couleur_jeton1 == couleur_jeton2 and (coord[0] == coord_2[0]-100 or coord[0] == coord_2[0]+100) and (coord[1] == coord_2[1]-100 or coord[1] == coord_2[1]+100): #regarde si les cases disponnible pour la dame ne sont pas pris par des jetons allié
                    possibilite -= 1
                elif couleur_jeton1 != couleur_jeton2 and (coord[0] == coord_2[0]-100 or coord[0] == coord_2[0]+100) and (coord[1] == coord_2[1]-100 or coord[1] == coord_2[1]+100): #ou part des jetons ennemies imprennable
                    if coord[0]+200 == coord_2[0]+100 <= 900 or coord[0]-200 == coord_2[0]-100 >= 0 or coord[1]+200 == coord_2[1]+100 <= 900 or coord[1]-200 == coord_2[1]-100 >= 0:
                        for f in list_jeton:
                            coord_sec = plateau.coords(f)
                            if (coord[0] == coord_2[0]-100 == coord_sec[0]-200 or coord[0] == coord_2[0]+100 == coord_sec[0]+200) and (coord[1] == coord_2[1]-100 == coord_sec[1]-200 or coord[1] == coord_2[1]+100 == coord_sec[1]+200):
                                possibilite -= 1
        else:
            possibilite = 2
            for e in list_jeton:
                couleur_jeton2 = plateau.itemcget(e,"fill")
                coord_2 = plateau.coords(e)
                if couleur_jeton1 == "white" and (coord[0] == coord_2[0]-100 or coord[0] == coord_2[0]+100) and coord[1] == coord_2[1]+100: #regarde si le pions blanc peut avancé
                    if couleur_jeton2 == "white":
                        possibilite -= 1
                elif couleur_jeton1 == "black" and (coord[0] == coord_2[0]-100 or coord[0] == coord_2[0]+100) and coord[1] == coord_2[1]-100: #regarde si le pions noir peut avancé
                    if couleur_jeton2 == "black":
                        possibilite -= 1
                if couleur_jeton1 != couleur_jeton2 and (coord[0] == coord_2[0]-100 or coord[0] == coord_2[0]+100) and (coord[1] == coord_2[1]-100 or coord[1] == coord_2[1]+100): #vérifie si il peut prendre le jeton adverse ou pas
                    if couleur_jeton1 == "white" and coord[1] == coord_2[1]-100 and coord[1]-200 >= 0:
                        possibilite += 1
                    if couleur_jeton1 == "black" and coord[1] == coord_2[1]+100 and coord[1]+200 <= 900:
                        possibilite += 1
                    if (coord[0]+200 == coord_2[0]+100 <= 900 or coord[0]-200 == coord_2[0]-100 >= 0) and (coord[1]+200 == coord_2[1]+100 <= 900 or coord[1]-200 == coord_2[1]-100 >= 0):
                        for f in list_jeton:
                            coord_sec = plateau.coords(f)
                            if (coord[0] == coord_2[0]-100 == coord_sec[0]-200 or coord[0] == coord_2[0]+100 == coord_sec[0]+200) and (coord[1] == coord_2[1]-100 == coord_sec[1]-200 or coord[1] == coord_2[1]+100 == coord_sec[1]+200):
                                possibilite -= 1
                    else:
                        possibilite -= 1
        for g in case: #regarde si il à bien 4 case disponible autour de lui sinon, il lui enlève des possibilité
                coord_case = plateau.coords(g)
                if (coord[0]-100 == coord_case[0] or coord[0]+100 == coord_case[0]) and (coord[1]-100 == coord_case[1] or coord[1]+100 == coord_case[1]):
                    nbr_case += 1
        if (couleur_jeton1 == "white" and coord[1] == 900) or (couleur_jeton1 == "black" and coord[1] == 0):
            possibilite += 1
        if nbr_case != 4:
            possibilite -= 1
        if nbr_case == 1:
            possibilite -= 1
        if possibilite <= 0: #si le jetons n'a pas de possibilité de joué il l'enlève de se pouvant être joué
                jeton_suppr.append(c)
    for c in jeton_suppr:
        jeton_doit_joue.remove(c)
    return jeton_doit_joue
          
def grap(event): #prend les coordonné de l'endroit attrapé
    coord = []
    coord.append(event.x)
    coord.append(event.y)
    jeu(coord)

def jeu(coord): #vérifie qu'il clic bien sur un jeton et enléve le contour orange des autres
    global J,coord_J
    J = take_jeton(coord) 
    if J:
        coord_J = plateau.coords(J)
        for c in jeton_doit_joue:
            plateau.itemconfig(c,outline="",width = 0)
        plateau.itemconfig(J,outline="orange",width = 4)
        plateau.bind("<Motion>",move)

def take_jeton(coord):
    for c in jeton_doit_joue:
        coord_jeton = plateau.coords(c) #vérifie que les coordonnés du jeton correspond
        if coord_jeton[0] <= coord[0] <= coord_jeton[0]+100 and coord_jeton[1] <= coord[1] <= coord_jeton[1]+100:
            return c
    return None

def move(event): #permet de déplacer le jeton
    J_coord = plateau.coords(J)
    plateau.tag_raise(J)
    plateau.move(J,event.x-J_coord[0],event.y-J_coord[1]) #certainement la fonction qui est la cause du bug d'avoir un jeton entre 4 cases
    plateau.bind("<ButtonRelease>",poser_jeton)

def poser_jeton(event): 
    global jeton_doit_joue
    X = event.x
    Y = event.y
    C = verification_case(X,Y)
    grapper = False
    case_possible = case_jouable()
    if a_manger: #si on peut manger effectue le mouvement dedié
        C = verification_manger(X,Y,a_manger)
        if C:
            plateau.unbind("<ButtonRelease>")
            plateau.unbind("<Motion>")
            coord = plateau.coords(C[0])
            plateau.move(C[0],C[2]-coord[0],C[3]-coord[1])
            color = plateau.itemcget(C[1],"fill")
            if color == "white":
                list_jeton_blanc.remove(C[1])
            else:
                list_jeton_noir.remove(C[1])
            list_jeton.remove(C[1])
            plateau.delete(C[1])
            plateau.itemconfig(C[0],outline="",width = 0)
            color = plateau.itemcget(C[0],"fill")
            if color == "black":
                jeton_doit_joue = doit_noir_manger()
            else:
                jeton_doit_joue = doit_blanc_manger()
            if a_manger: #vérifie si il y a une rafle
                for d in a_manger:
                    if C[0] == d[0]:
                        grapper = True
                        for c in jeton_doit_joue:
                            plateau.itemconfig(c,outline="orange",width = 4)
                        plateau.bind("<Button-1>",grap)
                if not grapper:
                    dames(J)
                    fin_tour()
            else:
                dames(J)
                fin_tour()
        else:
            plateau.unbind("<ButtonRelease>")
            plateau.unbind("<Motion>")
            plateau.move(J,coord_J[0]-X,coord_J[1]-Y)
            for c in jeton_doit_joue:
                plateau.itemconfig(c,outline="orange",width = 4)
            plateau.bind("<Button-1>",grap) 
    elif not a_manger and C: #si on peut pas manger effectue le mouvement dedié
        plateau.unbind("<ButtonRelease>")
        plateau.unbind("<Motion>")
        coord = plateau.coords(J)
        cursor = []
        cursor.append(C[0])
        cursor.append(C[1])
        if case_possible.count(cursor) >= 1:
            plateau.move(J,C[0]-coord[0],C[1]-coord[1])
            plateau.itemconfig(J,outline="",width = 0)
            dames(J)
            fin_tour()
        else:
            plateau.move(J,coord_J[0]-X,coord_J[1]-Y)
            for c in jeton_doit_joue:
                plateau.itemconfig(c,outline="orange",width = 4)
            plateau.bind("<Button-1>",grap) 
    else: #si le joueur à lâcher son jeton sur de mauvaise coordonnées
        plateau.unbind("<ButtonRelease>")
        plateau.unbind("<Motion>")
        plateau.move(J,coord_J[0]-X,coord_J[1]-Y)
        for c in jeton_doit_joue:
            plateau.itemconfig(c,outline="orange",width = 4)
        plateau.bind("<Button-1>",grap) 
            
def verification_manger(X,Y,a_manger): #vérifie que la position du jeton lâcher correspond avec l'une de celle où on peut mangé
    for c in a_manger:
        if J == c[0] and c[2] <= X <= c[2] + 100 and c[3] <= Y <= c[3] + 100:
            return c
    return None

def case_jouable():
    color = plateau.itemcget(J,"fill")
    tag = plateau.gettags(J)
    case_possible =[] #crée une liste avec les cases disponnibles pour le jeton
    k = 1
    while k < 10:
        if color == "white":
            add_XY = []
            add_XY.append(coord_J[0]-100*k)
            add_XY.append(coord_J[1]-100*k)
            case_possible.append(add_XY)
            add_XY = []
            add_XY.append(coord_J[0]+100*k)
            add_XY.append(coord_J[1]-100*k)
            case_possible.append(add_XY)
        else:
            add_XY = []
            add_XY.append(coord_J[0]-100*k)
            add_XY.append(coord_J[1]+100*k)
            case_possible.append(add_XY)
            add_XY = []
            add_XY.append(coord_J[0]+100*k)
            add_XY.append(coord_J[1]+100*k)
            case_possible.append(add_XY)
        if tag.count('dame'):
            if color == "white":
                add_XY = []
                add_XY.append(coord_J[0]-100*k)
                add_XY.append(coord_J[1]+100*k)
                case_possible.append(add_XY)
                add_XY = []
                add_XY.append(coord_J[0]+100*k)
                add_XY.append(coord_J[1]+100*k)
                case_possible.append(add_XY)
            else:
                add_XY = []
                add_XY.append(coord_J[0]-100*k)
                add_XY.append(coord_J[1]-100*k)
                case_possible.append(add_XY)
                add_XY = []
                add_XY.append(coord_J[0]+100*k)
                add_XY.append(coord_J[1]-100*k)
                case_possible.append(add_XY)
            k += 1
        else:
            break
    for c in case_possible:
        for d in list_jeton:
            coord2 = plateau.coords(d)
            if coord2[0] == c[0] and coord2[1] == c[1]: #supprimer les cases disponnible avec un jeton dessus
                case_possible.remove(c)
    return case_possible

def verification_case(X,Y): #renvoie la case sur laquel pose le jeton
    tag = plateau.gettags(J)
    k = 1
    c = []
    while k <= 9:
        if (coord_J[0] <= X-100*k <= coord_J[0]+100 or coord_J[0] <= X+100*k <= coord_J[0]+100) and (coord_J[1] <= Y-100*k <= coord_J[1]+100 or coord_J[1] <= Y+100*k <= coord_J[1]+100):
            if coord_J[0] <= X-100*k <= coord_J[0]+100:
                c.append(coord_J[0]+100*k)
            elif coord_J[0] <= X+100*k <= coord_J[0]+100:
                c.append(coord_J[0]-100*k)
            if coord_J[1] <= Y-100*k <= coord_J[1]+100:
                c.append(coord_J[1]+100*k)
            elif coord_J[1] <= Y+100*k <= coord_J[1]+100:
                c.append(coord_J[1]-100*k)
            return c
        if tag.count('dame'):
            k += 1
        else:
            break
    return None

def dames(d): #transformer un pion en dame en ajoutant le tag dame (sans transformation de tag)
    coord = plateau.coords(d)
    color = plateau.itemcget(d,"fill")
    if color == "white" and coord[1] == 0:
        plateau.itemconfig(d,tag = "dame")
    elif color == "black" and coord[1] == 900:
        plateau.itemconfig(d,tag = "dame")
        
def fin_tour():
    global couleur,jeton_doit_joue,premier_coup
    if couleur == "white": #si avant c'était "les blancs" qui avait joué "les noirs" joue 
        couleur = "black"
        jeton_doit_joue = doit_noir_manger()
        if jeton_doit_joue:
            None
        else:
            jeton_doit_joue = list_jeton_noir.copy()       
    else:
        couleur = "white" #sinon c'est l'inverse
        jeton_doit_joue = doit_blanc_manger()
        if jeton_doit_joue:
            None
        else:
            jeton_doit_joue = list_jeton_blanc.copy()
    jeton_doit_joue = verification_jeton(jeton_doit_joue) #on vérifie qu'il n'y est pas de mauvais jetons dedans
    if not list_jeton_blanc or (not jeton_doit_joue and couleur == "white"): #on regarde si il y a une victoire
        perdant = "white"
        fin_jeu(perdant)
    elif not list_jeton_noir or (not jeton_doit_joue and couleur == "black"):
        perdant = "black"
        fin_jeu(perdant)
    else:
        if player == couleur: #on regarde si c'est le joueur qui joue 
            premier_coup = False
            plateau.bind("<Button-1>",grap)
            for c in jeton_doit_joue:
                plateau.itemconfig(c,outline="orange",width = 4)
        else:
            if premier_coup == True: #si c'est le premier coup pour éviter une attend il joura un coup pré-programmer
                premier_coup = False
                Coup = []
                jeton = []
                for c in list_jeton_blanc:
                    coord = plateau.coords(c)
                    if coord[0] == 900 and coord[1] == 600:
                        jeton.append(c)
                jeton.append(coord)
                Coup.append(jeton)
                Coup.append(None)
                Coup.append(800)
                Coup.append(500)
                Poser_CoupIA(Coup)
            else: #lance l'IA
                Coup = MinMax(None)
                Poser_CoupIA(Coup)
    
def Poser_CoupIA(Coup): #exactement comme Poser_Coup sauf qu'il n'y a pas toute les vérifications car les coordonnées sont parfaite
    global jeton_doit_joue
    grapper = False
    plateau.tag_raise(Coup[0][0])
    if Coup[1]:
        coord = plateau.coords(Coup[0][0])
        plateau.move(Coup[0][0],Coup[2]-coord[0],Coup[3]-coord[1])
        color = plateau.itemcget(Coup[1][0],"fill")
        if color == "white":
            list_jeton_blanc.remove(Coup[1][0])
        else:
            list_jeton_noir.remove(Coup[1][0])
        list_jeton.remove(Coup[1][0])
        plateau.delete(Coup[1][0])
        color = plateau.itemcget(Coup[0][0],"fill")
        if color == "black":
                jeton_doit_joue = doit_noir_manger()
        else:
            jeton_doit_joue = doit_blanc_manger()
        if a_manger:
            for d in a_manger:
                if Coup[0][0] == d[0]:
                    grapper = True
                    Coup = MinMax(Coup[0][0])
                    Poser_CoupIA(Coup)
            if not grapper:
                dames(Coup[0][0])
                fin_tour()
        else:
            dames(Coup[0][0])
            fin_tour()
    else:
        coord = plateau.coords(Coup[0][0])
        plateau.move(Coup[0][0],Coup[2]-coord[0],Coup[3]-coord[1])
        dames(Coup[0][0])
        fin_tour()    

def fin_jeu(perdant): 
    if perdant == "white":
        text_perdant="Les noirs ont gagné"
        text_perdant="Les blancs ont perdu"
    else:
        text_gagnant="Les blancs ont gagné"
        text_perdant="Les noirs ont perdu"
    fin = Toplevel() #crée une fenêtre au-dessus du canvas avec le message de victoire
    fin.title("Fin")
    msg = Message(fin, text=text_gagnant)
    msg_2 = Message(fin, text=text_perdant)
    msg.pack()
    msg_2.pack()
    plateau.bind("<Button-1>",exit_game)

def exit_game(event): #detruit toutes les fenêtres et éteint le programme
    fenetre.destroy()
    exit()
          
plateau = Canvas(fenetre,width=1000,height=1000) #création de la zone de dessin
colone = 0
couleur = "#F6DDCC" #couleur des cases blanches
while colone < 10:
    ligne = 0
    while ligne < 10: #créé en réaliter une case 
        if couleur == "#F6DDCC":
            plateau.create_rectangle(colone*100,ligne*100,colone*100+100,ligne*100+100,fill=couleur) #créé une case blanche stocker nulle part
            couleur = "#873600" #change de couleur pour une case noir
        else:
            c = plateau.create_rectangle(colone*100,ligne*100,colone*100+100,ligne*100+100,fill=couleur) #créé une case noir qui sera stocker dans case
            case.append(c)
            if ligne < 4 and couleur == "#873600":
                jeton = plateau.create_oval(colone*100,ligne*100,colone*100+100,ligne*100+100,fill="black",activefill="#2E2D2D") #sur les 4 première...
                list_jeton_noir.append(jeton) #...case noir de la colone, un jeton noir est créé et stocker dans 2 listes
                list_jeton.append(jeton)
            elif ligne >= 6 and couleur == "#873600": #même chose pour les blancs sauf que c'est sur les 4 dernières
                jeton = plateau.create_oval(colone*100,ligne*100,colone*100+100,ligne*100+100,fill="white",activefill="#B0AFAD")
                list_jeton_blanc.append(jeton)
                list_jeton.append(jeton)
            couleur = "#F6DDCC" #change de couleur pour blanc
        ligne += 1
    if couleur == "#F6DDCC":   #après avoir terminé une colone, la même chose se produit sur la colone suivant seulement c'est la même couleur que...
        couleur = "#873600"    #...la dernière case de la colone juste avant
        plateau.create_rectangle(colone*100,ligne*100,colone*100+100,ligne*100+100,fill=couleur)
    else:
       couleur = "#F6DDCC"
       plateau.create_rectangle(colone*100,ligne*100,colone*100+100,ligne*100+100,fill=couleur)
    colone += 1
fin_tour() #permet de passer à la suite du programme
plateau.pack() #importe pour que le canvas soit créé
fenetre.mainloop() #important pour que la fenêtre soit créé
