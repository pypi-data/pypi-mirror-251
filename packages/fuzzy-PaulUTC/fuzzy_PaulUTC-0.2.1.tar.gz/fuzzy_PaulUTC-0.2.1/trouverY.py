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
    if x>coefs[2]:
        return coefs[4]*math.exp(-((x-coefs[2])/(2*coefs[3]))**2)
    elif x>coefs[0]:
        return coefs[4]
    else:
        return coefs[4]*math.exp(-((x-coefs[0])/(2*coefs[1]))**2)


def saturation(valeur, borneInf, borneSup):
    a = min(borneSup, valeur)
    return max(a, borneInf)

































