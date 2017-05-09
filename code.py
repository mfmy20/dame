from tkinter import *
from random import *
from copy import *
launcher = Tk()
launcher.title('Launcher')
launcher.geometry('200x100+900+450')

player = "white"
profondeur = 3
premier_coup = True
     
menubar = Menu(launcher)
def facile():
    global profondeur
    profondeur = 2

def moyen():
    global profondeur
    profondeur = 3

def difficile():
    global profondeur
    profondeur = 4
    
def impossible():
    global profondeur
    profondeur = 5

def joueur():
    global player
    player = Value.get()

def launch():
    launcher.quit()
    launcher.destroy()
    
difficulte = Menu(menubar, tearoff=0)
difficulte.add_command(label="Facile", command=facile)
difficulte.add_command(label="Moyen", command=moyen)
difficulte.add_command(label="Difficile", command=difficile)
difficulte.add_command(label="Impossible", command=impossible)
menubar.add_cascade(label="Difficulté", menu=difficulte)

label = Label(launcher, text="choisissez votre couleur:")
label.pack()

Value = StringVar() 
bouton1 = Radiobutton(launcher, text="Blanc", variable=Value, value="white", command=joueur)
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
    IA = True
    list_jeton_simule = []
    jeton_blanc_simule = []
    jeton_noir_simule = []
    maxval = -100000000             
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
    doit_IA_manger(IA,list_jeton_simule,jeton_blanc_simule,jeton_noir_simule)
    if a_manger:
        for d in a_manger:
            if Rafle:
                if d[0][0] == Rafle:
                    list_jeton_simule2 = deepcopy(list_jeton_simule)
                    jeton_blanc_simule2 = deepcopy(jeton_blanc_simule)
                    jeton_noir_simule2 = deepcopy(jeton_noir_simule)
                    d2 = deepcopy(d)
                    val = Min(d2,list_jeton_simule2,jeton_blanc_simule2,jeton_noir_simule2,profondeur-1)
                    if val > maxval or (val == maxval and randint(1,2) == 2):
                        maxval = val
                        MeilleurCoup = d
            else:
                list_jeton_simule2 = deepcopy(list_jeton_simule)
                jeton_blanc_simule2 = deepcopy(jeton_blanc_simule)
                jeton_noir_simule2 = deepcopy(jeton_noir_simule)
                d2 = deepcopy(d)
                val = Min(d2,list_jeton_simule2,jeton_blanc_simule2,jeton_noir_simule2,profondeur-1)
                if val > maxval or (val == maxval and randint(1,2) == 2):
                    maxval = val
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
                list_jeton_simule2 = deepcopy(list_jeton_simule)
                jeton_blanc_simule2 = deepcopy(jeton_blanc_simule)
                jeton_noir_simule2 = deepcopy(jeton_noir_simule)
                action2 = deepcopy(action)
                val = Min(action2,list_jeton_simule2,jeton_blanc_simule2,jeton_noir_simule2,profondeur-1)
                if val > maxval or (val == maxval and randint(1,2) == 2):
                    maxval = val
                    MeilleurCoup = action
    return MeilleurCoup

def Min(d,list_jeton_simule,jeton_blanc_simule,jeton_noir_simule,profondeur):
    IA = False
    minval = 10000000000
    maxval = -10000000000
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
            for d in a_manger:
                list_jeton_simule2 = deepcopy(list_jeton_simule)
                jeton_blanc_simule2 = deepcopy(jeton_blanc_simule)
                jeton_noir_simule2 = deepcopy(jeton_noir_simule)
                d2 = deepcopy(d)
                val = Min(d2,list_jeton_simule2,jeton_blanc_simule2,jeton_noir_simule2,profondeur)
                if val > maxval or (val == maxval and randint(1,2) == 2):
                    maxval = val
            return maxval
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
                val = Min(d2,list_jeton_simule2,jeton_blanc_simule2,jeton_noir_simule2,profondeur-1)
                if val > maxval or (val == maxval and randint(1,2) == 2):
                    minval = val
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
                    val = Max(action2,list_jeton_simule2,jeton_blanc_simule2,jeton_noir_simule2,profondeur-1)
                    if val < minval or (val == minval and randint(1,2) == 2):
                        minval = val
    return minval

def Max(d,list_jeton_simule,jeton_blanc_simule,jeton_noir_simule,profondeur):
    IA = True
    minval = 10000000000
    maxval = -10000000000
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
                val = Min(d2,list_jeton_simule2,jeton_blanc_simule2,jeton_noir_simule2,profondeur)
                if val < minval or (val == minval and randint(1,2) == 2):
                    minval = val
            return minval
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
                val = Min(d2,list_jeton_simule2,jeton_blanc_simule2,jeton_noir_simule2,profondeur-1)
                if val > maxval or (val == maxval and randint(1,2) == 2):
                    maxval = val
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
                    val = Min(action2,list_jeton_simule2,jeton_blanc_simule2,jeton_noir_simule2,profondeur-1)
                    if val > maxval or (val == maxval and randint(1,2) == 2):
                        maxval = val
    return maxval

def evaluer(list_jeton_simule,jeton_blanc_simule,jeton_noir_simule,val):
    for c in jeton_blanc_simule:
        tag = c[4]
        if player == "white":
            if tag == 'dame':
                val -= 3
            else:
                val -= 1
        else:
            if tag == 'dame':
                val += 3
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
    global a_manger
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

def verification_IA(jeton_doit_joue,list_jeton_simule,jeton_blanc_simule,jeton_noir_simule):
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

def case_jouable_IA(d,list_jeton_simule,jeton_blanc_simule,jeton_noir_simule):
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

def dames_IA(d):
    coord = []
    coord.append(d[1])
    coord.append(d[2])
    color = d[3]
    if color == "white" and coord[1] == 0:
        d[4] = 'dame'
    elif color == "black" and coord[1] == 900:
        d[4] = 'dame'

def doit_noir_manger():
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
    a_manger = []
    jeton_doit_joue = []
    for c in list_jeton_blanc:
        coord_blanc  = plateau.coords(c)
        tag = plateau.gettags(c)
        for d in list_jeton_noir:
            coord_noir = plateau.coords(d)
            k = 1
            while k <= 9:
                ne_peu = False
                if (coord_blanc[0] == coord_noir[0]-100*k or coord_blanc[0] == coord_noir[0]+100*k) and (coord_blanc[1] == coord_noir[1]-100*k or coord_blanc[1] == coord_noir[1]+100*k):
                    if (coord_blanc[0]+100*k == coord_noir[0]  and coord_blanc[0]+100*(k+1) <= 900) or (coord_blanc[0]-100*k == coord_noir[0] and coord_blanc[0]-100*(k+1 ) >= 0) or (coord_blanc[1]+100*k == coord_noir[0] and coord_blanc[1]+100*(k+1) <= 900) or (coord_blanc[1]+100*k == coord_noir[0] and coord_blanc[1]-100*(k+1) >= 0):
                        for e in list_jeton:
                            coord_sec = plateau.coords(e)
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
                if tag.count('dame'):
                    k += 1
                else:
                    break
    return jeton_doit_joue  

def verification_jeton(jeton_doit_joue):
    jeton_suppr = []
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
                if couleur_jeton1 == couleur_jeton2 and (coord[0] == coord_2[0]-100 or coord[0] == coord_2[0]+100) and (coord[1] == coord_2[1]-100 or coord[1] == coord_2[1]+100):
                    possibilite -= 1
                elif couleur_jeton1 != couleur_jeton2 and (coord[0] == coord_2[0]-100 or coord[0] == coord_2[0]+100) and (coord[1] == coord_2[1]-100 or coord[1] == coord_2[1]+100):
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
                        for f in list_jeton:
                            coord_sec = plateau.coords(f)
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
          
def grap(event):
    coord = []
    coord.append(event.x)
    coord.append(event.y)
    jeu(coord)

def jeu(coord):
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
        coord_jeton = plateau.coords(c)
        if coord_jeton[0] <= coord[0] <= coord_jeton[0]+100 and coord_jeton[1] <= coord[1] <= coord_jeton[1]+100:
            return c
    return None

def move(event):
    J_coord = plateau.coords(J)
    plateau.tag_raise(J)
    plateau.move(J,event.x-J_coord[0],event.y-J_coord[1])
    plateau.bind("<ButtonRelease>",poser_jeton)

def poser_jeton(event):
    global jeton_doit_joue
    X = event.x
    Y = event.y
    C = verification_case(X,Y)
    grapper = False
    case_possible = case_jouable()
    if a_manger:
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
            if a_manger:
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
    elif not a_manger and C:
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
    else:
        plateau.unbind("<ButtonRelease>")
        plateau.unbind("<Motion>")
        plateau.move(J,coord_J[0]-X,coord_J[1]-Y)
        for c in jeton_doit_joue:
            plateau.itemconfig(c,outline="orange",width = 4)
        plateau.bind("<Button-1>",grap) 
            
def verification_manger(X,Y,a_manger):
    for c in a_manger:
        if J == c[0] and c[2] <= X <= c[2] + 100 and c[3] <= Y <= c[3] + 100:
            return c
    return None

def case_jouable():
    color = plateau.itemcget(J,"fill")
    tag = plateau.gettags(J)
    case_possible =[]
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
            if coord2[0] == c[0] and coord2[1] == c[1]:
                case_possible.remove(c)
    return case_possible

def verification_case(X,Y):
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

def dames(d):
    coord = plateau.coords(d)
    color = plateau.itemcget(d,"fill")
    if color == "white" and coord[1] == 0:
        plateau.itemconfig(d,tag = "dame")
    elif color == "black" and coord[1] == 900:
        plateau.itemconfig(d,tag = "dame")
        
def fin_tour():
    global couleur,jeton_doit_joue,premier_coup
    if couleur == "white":
        couleur = "black"
        jeton_doit_joue = doit_noir_manger()
        if jeton_doit_joue:
            None
        else:
            jeton_doit_joue = list_jeton_noir.copy()       
    else:
        couleur = "white"
        jeton_doit_joue = doit_blanc_manger()
        if jeton_doit_joue:
            None
        else:
            jeton_doit_joue = list_jeton_blanc.copy()
    jeton_doit_joue = verification_jeton(jeton_doit_joue)
    if not list_jeton_blanc or (not jeton_doit_joue and couleur == "white"):
        perdant = "white"
        fin_jeu(perdant)
    elif not list_jeton_noir or (not jeton_doit_joue and couleur == "black"):
        perdant = "black"
        fin_jeu(perdant)
    else:
        if player == couleur:
            premier_coup = False
            plateau.bind("<Button-1>",grap)
            for c in jeton_doit_joue:
                plateau.itemconfig(c,outline="orange",width = 4)
        else:
            if premier_coup == True:
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
            else:
                Coup = MinMax(None)
                Poser_CoupIA(Coup)
    
def Poser_CoupIA(Coup):
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
    fin = Toplevel()
    fin.title("Fin")
    msg = Message(fin, text=text_gagnant)
    msg_2 = Message(fin, text=text_perdant)
    msg.pack()
    msg_2.pack()
    plateau.bind("<Button-1>",exit_game)

def exit_game(event):
    fenetre.destroy()
    exit()
          
plateau = Canvas(fenetre,width=1000,height=1000)
colone = 0
couleur = "#F6DDCC"
while colone < 10:
    ligne = 0
    while ligne < 10:
        if couleur == "#F6DDCC":
            plateau.create_rectangle(colone*100,ligne*100,colone*100+100,ligne*100+100,fill=couleur)
            couleur = "#873600"
        else:
            c = plateau.create_rectangle(colone*100,ligne*100,colone*100+100,ligne*100+100,fill=couleur)
            case.append(c)
            if ligne < 4 and couleur == "#873600":
                jeton = plateau.create_oval(colone*100,ligne*100,colone*100+100,ligne*100+100,fill="black",activefill="#2E2D2D")
                list_jeton_noir.append(jeton)
                list_jeton.append(jeton)
            elif ligne >= 6 and couleur == "#873600":
                jeton = plateau.create_oval(colone*100,ligne*100,colone*100+100,ligne*100+100,fill="white",activefill="#B0AFAD")
                list_jeton_blanc.append(jeton)
                list_jeton.append(jeton)
            couleur = "#F6DDCC"
        ligne += 1
    if couleur == "#F6DDCC":
        couleur = "#873600"
        plateau.create_rectangle(colone*100,ligne*100,colone*100+100,ligne*100+100,fill=couleur)
    else:
       couleur = "#F6DDCC"
       plateau.create_rectangle(colone*100,ligne*100,colone*100+100,ligne*100+100,fill=couleur)
    colone += 1
fin_tour()
plateau.pack()
fenetre.mainloop()
