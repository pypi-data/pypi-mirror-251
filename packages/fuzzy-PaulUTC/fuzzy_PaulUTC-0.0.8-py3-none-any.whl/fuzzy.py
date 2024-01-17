## Création d'un excel pour remplir les infos d'un SF

def ajoutExcel ():
    import pandas as pd
    import warnings

    # Ignorer les avertissements liés à openpyxl
    warnings.simplefilter("ignore", category=UserWarning)


    df = pd.read_excel('Feuil1.xlsm')

    df.to_excel("exemple.xlsx", index=False)



##Récupération infos
def creationSF (nomSF):
    import pandas as pd
    import warnings
    import math
    from classesObjets import SF
    from classesObjets import classe
    from classesObjets import entree
    from classesObjets import regle
    from classesObjets import sortie
    # Ignorer les avertissements liés à openpyxl
    warnings.simplefilter("ignore", category=UserWarning)



    try :
        excel = pd.read_excel(nomSF + '.xlsm')
    except:
        excel = pd.read_excel(nomSF + '.xlsx')

    matrice = excel.values.tolist() #matrice de la page excel



    ##Création du dico des entrées
    nbEntree = int(matrice[0][1]) #nombre d'entrées de ce système flou
    entrees1 = {}

    for i in range (nbEntree):
        entrees1[str(matrice[3][i*8+1])] = entree(str(matrice[3][i*8+1]), float(matrice[4][i*8+1]), float(matrice[5][i*8+1]), {}) #création d'une entrée (nom, bornes sup et inf)

        j=0


        while matrice[8+j][i*8]!="XXX" and (isinstance(matrice[8+j][i*8], str) or not math.isnan(matrice[8+j][i*8])) :#pour tes les classes de cette entrée on créer un objet classe qu'on ajoute à enntree1
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
    while isinstance(matrice[j][0], str) or not math.isnan(matrice[j][0]):
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

    while j < nbLigne and (isinstance(matrice[j][0], str) or not math.isnan(matrice[j][0])): #tant qu'il y a des règles écrites
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
    from trouverY import trouverYGauss
    from trouverY import trouverYTriangle
    from trouverY import trouverYTrapeze
    from trouverY import saturation
    from classesObjets import SF
    from classesObjets import classe
    from classesObjets import entree
    from classesObjets import regle
    from classesObjets import sortie


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
    from classesObjets import SF
    from classesObjets import classe
    from classesObjets import entree
    from classesObjets import regle
    from classesObjets import sortie
    from dichotomie import dichotomie
    from dichotomie import dichotomieTrapezGauss
    from dichotomie import dichotomieTrapezoidale
    from dichotomie import dichotomieGauss



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
    from classesObjets import SF
    from classesObjets import entree
    from classesObjets import sortie
    from classesObjets import regle
    from classesObjets import classe
    import importlib
    import sys


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







































