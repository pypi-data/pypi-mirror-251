
class classe:
    def __init__(self, type, coefs):
        self.type = type #="Triangulaire ou Trapézoïdale
        self.coefs = coefs #lise des coefs en notation Kaufmann avec la hauteur en dernier (triangulaire 4 coefs, trapez. 5 coefs)


    def __str__(self):
        return f"Cette classe est un inevalle flou {self.type} et a comme coefficients en notation de Kaufmann : {self.coefs}"


class entree:
    def __init__(self, name, borneInf, borneSup, classes = {}):
        self.name = name #str du nom de l'entrée
        self.classes = classes #dico de toutes les classes, la clé est le nom de la classe
        self.borneSup = borneSup #born de l'univers des classes
        self.borneInf = borneInf


    def __str__(self):
        print( f"Le nom de l'entrée est '{self.name}', ses bornes : {[self.borneInf, self.borneSup]} et ses classes sont :")
        for classe in self.classes :
            print(f"    {classe}: ", end="")
            print(self.classes[classe])
        return ""


    def ajouter_classe(self, classe, nameClasse):
        self.classes[nameClasse]=classe



class sortie:
    def __init__(self, name, consequence):
        self.name = name #str du nom de la sortie
        self.consequence = consequence #liste de toutes les conséquences



    def __str__(self):
        return f"Le nom de la sortie est '{self.name}' et les conséquences sont : {self.consequence}"



class regle:
    def __init__(self, consequence, antecedents):
        self.antecedents = antecedents #dico des antécédents de la règles avec comme clé le nom de l'entrée et comme valeur le nom de la classe
        self.consequence = consequence #str de la conséquence en sortie



    def __str__(self):
        return f"Les antécédants de cette règle sont : {self.antecedents} et la conséquence est : {self.consequence}"



class SF:
    def __init__(self, name, entrees, sortie, regles = []):
        self.entrees = entrees #dico de toutes les entrées (classes), avec comme clé le nom de l'entrée
        self.sortie = sortie #classe sortie
        self.regles = regles #liste de classe règle
        self.name = name


    def __str__(self):
        print(f"Le nom de ce système flou est '{self.name}' et ses entrées sont :")
        print("")
        for entree in self.entrees:
            print(self.entrees[entree])
        print("")
        print("")
        print("La sortie de ce système flou est :")
        print("")
        print(self.sortie)
        print("")
        print("")
        print("")
        print("Les règles de ce système flou sont :")
        for i in range(len(self.regles)):
            print("")
            print(self.regles[i])
        return ""



































def trouverYTriangle(x,coefs):
    if x<coefs[0]:
        return 0
    elif x<coefs[1]:
        return (coefs[3]/(coefs[1]-coefs[0]))*x-(coefs[3]/(coefs[1]-coefs[0]))*coefs[0]
    elif x<coefs[2]:
        return (coefs[3]/(coefs[1]-coefs[2]))*x-(coefs[3]/(coefs[1]-coefs[2]))*coefs[2]
    else :
        return 0



def trouverYTrapeze(x,coefs):
    if x<coefs[0]:
        return 0
    elif x<coefs[1]:
        return (coefs[4]/(coefs[1]-coefs[0]))*x-(coefs[4]/(coefs[1]-coefs[0]))*coefs[0]
    elif x<coefs[2]:
        return coefs[4]
    elif x<coefs[3]:
        return (coefs[4]/(coefs[2]-coefs[3]))*x-(coefs[4]/(coefs[2]-coefs[3]))*coefs[3]
    else :
        return 0



def trouverYGauss(x,coefs):
    from math import exp
    if x>coefs[2]:
        return coefs[4]*exp(-((x-coefs[2])/(2*coefs[3]))**2)
    elif x>coefs[0]:
        return coefs[4]
    else:
        return coefs[4]*exp(-((x-coefs[0])/(2*coefs[1]))**2)


def saturation(valeur, borneInf, borneSup):
    a = min(borneSup, valeur)
    return max(a, borneInf)







def dichotomie (coefs1, forme1, coefs2, forme2):
    if forme1 == "Triangulaire":
        coefs1 = [coefs1[0], coefs1[1], coefs1[1], coefs1[2], coefs1[3]]
        forme1 = "Trapézoïdale"
    if forme2 == "Triangulaire":
        coefs2 = [coefs2[0], coefs2[1], coefs2[1], coefs2[2], coefs2[3]]
        forme2 = "Trapézoïdale"

    if forme1 == "Trapézoïdale" and forme2 == "Trapézoïdale" :
        res = dichotomieTrapezoidale(coefs1, coefs2)
    elif forme1 == "Gaussienne" and forme2 == "Gaussienne" :
        res = dichotomieGauss(coefs1, coefs2)
    elif (forme1 == "Gaussienne" and forme2 == "Trapézoïdale"):
        res = dichotomieTrapezGauss (coefs1, coefs2) #tourjours la forme gaussienne en première
    elif (forme2 == "Gaussienne" and forme1 == "Trapézoïdale"):
        res = dichotomieTrapezGauss (coefs2, coefs1) #tourjours la forme gaussienne en première

    return res





def dichotomieTrapezGauss(coefsGauss, coefsTrap):#tourjours la forme gaussienne en première

    def dichoto(deb, fin, coefsGauss, coefsTrap):
        delta = 1
        while delta > 0.001:
            m = (deb + fin) / 2
            delta = abs(fin - deb)
            fonctionM = trouverYGauss(m, coefsGauss) - trouverYTrapeze(m, coefsTrap)
            fonctionA = trouverYGauss(deb, coefsGauss) - trouverYTrapeze(deb, coefsTrap)
            if fonctionM == 0:
                return m
            elif fonctionM * fonctionA > 0:
                deb = m
            else:
                fin = m
        return trouverYTrapeze(deb, coefsTrap)




    if coefsTrap[1]>=coefsGauss[2]:
        return dichoto(coefsGauss[2], coefsTrap[1], coefsGauss, coefsTrap)

    elif  coefsTrap[2]<=coefsGauss[0]:
        return dichoto(coefsTrap[2], coefsGauss[0], coefsGauss, coefsTrap)

    else :
        return min(coefsTrap[4], coefsGauss[4])






def dichotomieTrapezoidale(coefs1, coefs2):
    if coefs1[1]!=coefs1[0]:
        a11=coefs1[4]/(coefs1[1]-coefs1[0])
        b11=-(coefs1[4]/(coefs1[1]-coefs1[0]))*coefs1[0]
    if coefs1[2]!=coefs2[3]:
        a12=(coefs1[4]/(coefs1[2]-coefs1[3]))
        b12=-(coefs1[4]/(coefs1[2]-coefs1[3]))*coefs1[3]

    if coefs2[1]!=coefs2[0]:
        a21=coefs2[4]/(coefs2[1]-coefs2[0])
        b21=-(coefs2[4]/(coefs2[1]-coefs2[0]))*coefs2[0]
    if coefs2[2]!=coefs2[3]:
        a22=(coefs2[4]/(coefs2[2]-coefs2[3]))
        b22=-(coefs2[4]/(coefs2[2]-coefs2[3]))*coefs2[3]





    def dichoto(a,b,a1,b1,a2,b2):
        delta = 1
        while delta > 0.001:
            m = (a + b) / 2
            delta = abs(b - a)
            if (a1-a2)*m+b1-b2 == 0:
                return m
            elif ((a1-a2)*a+b1-b2)*((a1-a2)*m+b1-b2) > 0:
                a = m
            else:
                b = m
        return a





    if coefs1[0]>=coefs2[3] or coefs1[3]<=coefs2[0]:
        return 0

    elif coefs1[1]>coefs2[2]:
        x=dichoto(coefs1[0], coefs1[1], a11, b11, a22, b22)
        y=x*a11+b11
        return y

    elif coefs1[1]<=coefs2[2] and coefs2[1]<=coefs1[2]:
        return min(coefs1[4],coefs2[4])

    elif coefs2[1]>coefs1[2]:
        x=dichoto(coefs1[2], coefs1[3], a21, b21, a12, b12)
        y=x*a21+b21
        return y








def dichotomieTriangulaire(coefs1, coefs2):
    if coefs1[1]!=coefs1[0]:
        a11=coefs1[4]/(coefs1[1]-coefs1[0])
        b11=-(coefs1[4]/(coefs1[1]-coefs1[0]))*coefs1[0]
    if coefs1[2]!=coefs2[3]:
        a12=(coefs1[4]/(coefs1[2]-coefs1[3]))
        b12=-(coefs1[4]/(coefs1[2]-coefs1[3]))*coefs1[3]

    if coefs2[1]!=coefs2[0]:
        a21=coefs2[4]/(coefs2[1]-coefs2[0])
        b21=-(coefs2[4]/(coefs2[1]-coefs2[0]))*coefs2[0]
    if coefs2[2]!=coefs2[3]:
        a22=(coefs2[4]/(coefs2[2]-coefs2[3]))
        b22=-(coefs2[4]/(coefs2[2]-coefs2[3]))*coefs2[3]





    def dichoto(a,b,a1,b1,a2,b2):
        delta = 1
        while delta > 0.001:
            m = (a + b) / 2
            delta = abs(b - a)
            if (a1-a2)*m+b1-b2 == 0:
                return m
            elif ((a1-a2)*a+b1-b2)*((a1-a2)*m+b1-b2) > 0:
                a = m
            else:
                b = m
        return a





    if coefs1[0]>=coefs2[2] or coefs1[2]<=coefs2[0]:
        return 0

    elif coefs1[1]>coefs2[1]:
        x=dichoto(coefs1[0], coefs1[1], a11, b11, a22, b22)
        y=x*a11+b11
        return y

    elif coefs1[1]==coefs2[1]:
        return min(coefs1[3],coefs2[3])

    elif coefs2[1]>coefs1[1]:
        x=dichoto(coefs2[0], coefs2[1], a21, b21, a12, b12)
        y=x*a21+b21
        return y


def dichotomieGauss(coefs1, coefs2):


    def dichoto(a, b, coefs1, coefs2):
        delta = 1
        while delta > 0.001:
            m = (a + b) / 2
            delta = abs(b - a)
            fonctionM = trouverYGauss(m, coefs1) - trouverYGauss(m, coefs2)
            fonctionA = trouverYGauss(a, coefs1) - trouverYGauss(a, coefs2)
            if fonctionM == 0:
                return trouverYGauss(m, coefs1)
            elif fonctionM * fonctionA > 0:
                a = m
            else:
                b = m
        return trouverYGauss(a, coefs1)





    if coefs1[0]>=coefs2[2]:
        return dichoto(coefs2[2], coefs1[0], coefs1, coefs2)

    elif coefs1[2]<=coefs2[0]:
        return dichoto(coefs1[2], coefs2[0], coefs1, coefs2)
    else:
        return min(coefs1[4], coefs2[4])

















## Création d'un excel pour remplir les infos d'un SF

def ajoutExcel ():
    import pandas as pd
    import warnings
    warnings.simplefilter("ignore", category=UserWarning)


    df = pd.read_excel('C:/Users/Utilisateur/Documents/utc/pypl/bibliFuzzy/fuzzyMath/fuzzy/Feuil1.xlsm')

    df.to_excel('C:/Users/Utilisateur/Documents/utc/pypl/bibliFuzzy/fuzzyMath/fuzzy/' + "exemple.xlsx", index=False)



##Récupération infos
def creationSF (nomSF):

    import pandas as pd
    from math import isnan
    import warnings
    warnings.simplefilter("ignore", category=UserWarning)
    try :
        excel = pd.read_excel('C:/Users/Utilisateur/Documents/utc/pypl/bibliFuzzy/fuzzyMath/fuzzy/' + nomSF + '.xlsm')
    except:
        excel = pd.read_excel('C:/Users/Utilisateur/Documents/utc/pypl/bibliFuzzy/fuzzyMath/fuzzy/' + nomSF + '.xlsx')

    matrice = excel.values.tolist() #matrice de la page excel



    ##Création du dico des entrées
    nbEntree = int(matrice[0][1]) #nombre d'entrées de ce système flou
    entrees1 = {}

    for i in range (nbEntree):
        entrees1[str(matrice[3][i*8+1])] = entree(str(matrice[3][i*8+1]), float(matrice[4][i*8+1]), float(matrice[5][i*8+1]), {}) #création d'une entrée (nom, bornes sup et inf)

        j=0


        while matrice[8+j][i*8]!="XXX" and (isinstance(matrice[8+j][i*8], str) or not isnan(matrice[8+j][i*8])) :#pour tes les classes de cette entrée on créer un objet classe qu'on ajoute à enntree1
            nameClasse1 = str(matrice[8+j][i*8+1])
            type1 = matrice[8+j][i*8]

            if type1 == "Triangulaire" :

                coefs1 = [float(matrice[8+j][i*8+2]), float(matrice[8+j][i*8+3]), float(matrice[8+j][i*8+4]), float(matrice[8+j][i*8+6])] #on ajote les coefs de la classe

            elif type1 == "Trapézoïdale" :
                coefs1 = [float(matrice[8+j][i*8+2]), float(matrice[8+j][i*8+3]), float(matrice[8+j][i*8+4]), float(matrice[8+j][i*8+5]), float(matrice[8+j][i*8+6])] #on ajote les coefs de la classe

            classe1 = classe(type1, coefs1)
            entrees1[str(matrice[3][i*8+1])].ajouter_classe(classe1, nameClasse1)
            j+=1




    ##Suppression de la partie de la matrice que nous ne voulons plus
    xxx=0
    while xxx!=2 :
        if matrice[0][0]=='XXX':
            xxx+=1
        matrice.pop(0)
    matrice.pop(0) #enlever la ligne avec marqué "Sortie" en gros


    ##Création de l'objet sortie
    consequences = []

    j=2
    while isinstance(matrice[j][0], str) or not isnan(matrice[j][0]):
        consequences.append(str(matrice[j][0])) #on ajoute le nom de la conséquence j
        j+=1


    sortie1 = sortie(str(matrice[0][1]), consequences)



    ##Suppression de la partie de la matrice que nous ne voulons plus
    xxx=0
    while xxx!=1 :
        if matrice[0][0]=='XXX':
            xxx+=1
        matrice.pop(0)
    matrice.pop(0) #enlever la ligne avec marqué "Règles" en gros



    ##Création de la liste de toutes les règles

    regles1 = []

    nomsAntecedant = []
    for i in range (nbEntree):
        nomsAntecedant.append(str(matrice[0][i])) #ordre des entrées dans le tableau

    j=1
    nbLigne = len(matrice)

    while j < nbLigne and (isinstance(matrice[j][0], str) or not isnan(matrice[j][0])): #tant qu'il y a des règles écrites
        regleAntecedants = {}
        for i in range (nbEntree):
            regleAntecedants[nomsAntecedant[i]] = str(matrice[j][i]) #création du dico des antécédents de la règle (nom de l'entrée => nom de la classe)


        regle1 = regle(str(matrice[j][nbEntree]),regleAntecedants)
        regles1.append(regle1)

        j+=1


    SF1 = SF(nomSF, entrees1, sortie1, regles1)
    return SF1




##Fuzzifier
def fuzzifier(valeursAfuz, SF1): #valeursAfuz est un dico {nom de l'enntrée à fuzzifier => valeur) et SF est l'objet SF qui correspond
    res = {}
    for en in valeursAfuz:
        res[en] = {}
        classes = SF1.entrees[en].classes
        for classe in classes:
            valeursAfuz[en] = saturation(valeursAfuz[en], SF1.entrees[en].borneInf, SF1.entrees[en].borneSup)
            if classes[classe].type=="Triangulaire":
                res[en][classe] = trouverYTriangle(valeursAfuz[en], classes[classe].coefs)
            elif classes[classe].type=="Trapézoïdale":
                res[en][classe] = trouverYTrapeze(valeursAfuz[en], classes[classe].coefs)
            elif classes[classe].type=="Gaussienne":
                res[en][classe] = trouverYGauss(valeursAfuz[en], classes[classe].coefs)
            else :
                print(f"La fome de la classe : {classe} n'est pas reconnue.")
                return
    return res





def max_min_intersection (valeurAfuz, typeValeurAfuz, SF1):
#valeursAfuz est un dico {nom de l'enntrée à fuzzifier => liste des coefs en notation Kaufmann) et SF est l'objet SF qui correspond


    res = {}

    for en in valeurAfuz:
        res[en] = {}
        classes = SF1.entrees[en].classes


        for cl in classes:
            res[en][cl] = dichotomie(valeurAfuz[en], typeValeurAfuz[en], classes[cl].coefs, classes[cl].type)
    return res



##Algorithme Zalila

def probabiliste(liste):
    res = 1
    for val in liste :
        res *= val
    return res

def AlgoZalilaGeneralise(dicoValFuz, SF1, fonction, cheminAcces = '', AfficherResultat = True):
    import sys
    import importlib


    if fonction.upper() == 'MIN':
        fonction = min
    elif fonction.upper() == 'PROBABILISTE':
        fonction = probabiliste
    elif cheminAcces!='':
        sys.path.append(cheminAcces)
        module = importlib.import_module(fonction)

        if hasattr(module, fonction) and callable(getattr(module, fonction)):# Vérifiez si la fonction existe dans le module
            fonction = getattr(module, fonction)
    else :
        return "Fonction pas reconnue"
    # irr est la liste irr que l'on veut traiter
    # SF est le système flou utilisé
    # nomSyst est une chaîne de caractères du nom du système
    # le ET et la pseudo-implication sont modélisés par la T-norme min.
    # On calcule le degré de déclenchement de chaque règle



    csq = {}
    for conseq in SF1.sortie.consequence:
        csq[conseq] = []


    nbRegle = len(SF1.regles)  # Nombre de règles
    for i in range (nbRegle):
        ValAntecedent = []
        for nomEntree in SF1.regles[i].antecedents:
            val = dicoValFuz[nomEntree][SF1.regles[i].antecedents[nomEntree]] #val est la valeur d'un antécédent de la règle traitée
            ValAntecedent.append(val)
        csq[SF1.regles[i].consequence].append(ValAntecedent)



    for conseq in csq:
        for i in range(len(csq[conseq])):
            csq[conseq][i] = fonction(csq[conseq][i])

        csq[conseq] = round(max(csq[conseq]), 2)


    if AfficherResultat :# Affichage de la conséquence floue finale
        print(f"Les conséquence de '{SF1.name}' sont : {csq}")

    return csq


##Défuzzifier

def defuzzification_Barycentre (csq):
    defuzz = 0
    sommeCoefs = 0
    for conseq in csq:
        defuzz = defuzz + int(conseq)*csq[conseq]
        sommeCoefs +=  csq[conseq]
    defuzz = defuzz/sommeCoefs
    return defuzz


def defuzzification_Max (csq):
    maxi = None
    for conseq in csq:
        if maxi == None or maxi<csq[conseq]:
            maxi = csq[conseq]
            nomEntreeMax = conseq
        elif maxi == csq[conseq]:
            if isinstance(nomEntreeMax, list):
                nomEntreeMax.append(conseq)
            else :
                a = nomEntreeMax
                nomEntreeMax = [a,conseq]
    return nomEntreeMax







































