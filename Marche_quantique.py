import matplotlib.pyplot as plt

def h(t):
    """
    Application de la matrice d'Hadamar à un vecteur de deux éléments
    :param t: vecteur de deux éléments associé à un rang
    :return:
    """
    return t[0], (t[1][0]/2**0.5+t[1][1]/2**0.5, t[1][0]/2**0.5-t[1][1]/2**0.5)

def split_vector(t):
    """
    Décompose les vecteur selon leurs composantes
    :param t: vecteur de deux éléments associé à un rang
    :return: le vecteur décomposé
    """
    return (t[0],(t[1][0],0)), (t[0],(0,t[1][1]))

def add_vector(t1,t2):
    assert t1[0]==t2[0]
    """
    Additionne des vecteurs avec un même rang associé
    :param t1: vecteur de deux éléments associé à un rang
    :param t2: vecteur de deux éléments associé à un rang
    :return: retourne le vecteur résultant
    """
    return t1[0], (t1[1][0]+t2[1][0],t1[1][1]+t2[1][1])

def add_list_vector(L):
    """
    Additionne une liste de vecteurs avec un rang associé
    :param L: Liste de vecteurs avec un rang associé
    :return: Liste de vecteurs avec un rang associé
    """
    index={}
    results=[]
    i=0
    for t in L:
        if not(t[0] in index):
            index[t[0]]=i
            i+=1
            results.append(t)
        else:
            results[index[t[0]]]=add_vector(results[index[t[0]]],t)
    return results

def shift(L):
    """
    Effectue un shift
    :param L: Liste de vecteurs avec un rang associé
    :return: Liste de vecteurs avec un rang associé après le shift
    """
    results=[]
    for t in L:
        results.append((t[0]+1,(t[1][0],0)))
        results.append((t[0]-1, (0,t[1][1])))
    return add_list_vector(results)

def marche_quantique(v0, N):
    """
    Applique N fois la matrice d'Hadamar et le shift
    :param v0: Etat initial (pile ou face)
    :param N: Nombre d'étapes
    :return: Résultats de la marche quantique sous forme d'une liste de vecteurs avec un rang associé
    """
    results=[(0, v0)]
    for i in range(N):
        results=shift([h(e) for e in results])
    return results

def proba_marche_quantique(v0,N):
    """
    Effectue une marche quantique puis calcule les probabilités associés à chaque rang
    :param v0: Etat initial (pile ou face)
    :param N: Nombre d'étapes
    :return: Affichage d'un diagramme en barre
    """
    results=marche_quantique(v0, N)
    results.sort()
    x, y= [], []
    a=0
    for i in range(results[a][0],results[-1][0]+1):
        if i==results[a][0]:
            x.append(i)
            y.append(abs(results[a][1][0])**2+abs(results[a][1][1])**2)
            a+=1
        else:
            x.append(0)
            y.append(0)
    plt.bar(x,y)
    plt.title(f"Marche Quantique pour {N} étapes, de vecteur initial {str(v0)}")
    plt.ylabel('probabilité')
    plt.xlabel('rang')
    plt.show()

proba_marche_quantique((1/2**0.5,1j/2**0.5),50)