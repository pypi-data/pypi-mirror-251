
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