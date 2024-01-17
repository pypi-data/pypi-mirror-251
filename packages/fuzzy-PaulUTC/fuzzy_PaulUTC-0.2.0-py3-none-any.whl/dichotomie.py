
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
    from trouverY import trouverYGauss


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













