import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from  random import randint
from scipy.integrate import quad

def simulation_marche(N,prec):
    """
    Réalise une simulation de la marche aléatoire
    :param N: nombre d'étapes
    :param prec:
    :return: Tableau des résultats
    """
    # N est le nombre d'étapes, qui est donc choisi impair
    # prec est le nombre d'itérations de la simulation
    resultat=np.zeros(N+1)
    # variable stockant les résultats pour chaque simulation, 'traque où la balle est tombé'
    for i in range(prec):
        pas=0
        # pas représente le rang de la balle sur l'ensemble des boîtes
        # si la balle tombe à gauche son range reste le même car on le dénombre à partir de la gauche
        # si la balle tombe à droite il augmente de 1
        for i in range(N):
            pas += randint(0,1)
        resultat[pas]+=1
    return resultat

def gauss(x, a, b, c):
    """
    Fonction gaussienne
    :param x: Abscisse
    :param a: Amplitude
    :param b: Milieu de la gaussienne
    :param c: Ecart type
    :return: image de l'abscisse par la gaussienne
    """
    y=a*np.exp(-(x-b)**2/(2*c**2))
    return y

def histogramme_marche(N, prec):
    """
    Retourne les résultats de la marche aléatoire sous forme d'un histogramme
    :param N: Nombre d'étapes de la marche aléatoire
    :param prec: Nombre de simulation
    :return: Rien
    """
    plage = np.array([i for i in range(N+1)])
    donnes = simulation_marche(N,prec)
    plt.bar(plage,donnes,1)
    plt.xlabel('rang')
    plt.ylabel('Nombre de simulations')
    plt.show()

def  courbe_marche(N,prec):
    """
    Retourn un graphique de la simulation et la modélisation des données
    :param N: Nombre d'étapes
    :param prec: Nombre de simulations
    :return: Rien
    """
    plage = np.array([i for i in range(N + 1)])
    donnes = simulation_marche(N, prec)
    plt.plot(plage, donnes, 'o', label='résultats expérimentaux')
    # Crée un modèle de courbe à partir des données experimental
    # on restreint les données autour du centre de la gaussienne pour améliorer le poids de ces données
    parametres, covariance = curve_fit(lambda x,a,c : gauss(x,a,N/2,c), plage, donnes, method='lm')
    # On connaît le milieu de la gaussienne donc on le fixe à N/2
    x = np.linspace(0,N,10*N)
    plt.plot(x, gauss(x, parametres[0], N/2, parametres[1]), color='yellow', label='modèle')
    plt.xlabel('rang')
    plt.ylabel('Nombre de simulations')
    plt.show()

def evolution_moyenne(debut, fin, prec):
    """
    Renvoie une courbe de l'évolution de la valeur moyenne en fonction du nombre d'étapes de la simulation
    :param debut: Nombre d'étapes initial
    :param fin: Nombre d'étapes  final
    :param prec: Nombre de simulation pour obtenir la valeur moyenne
    :return: Rien
    """
    # On crée la variable qui stockera les données
    moyenne = np.zeros(fin-debut+1)
    # Initialisation de la boucle pour calculer les valeurs moyennes en foncttion de N
    for N in range(debut, fin+1):
        plage = np.array([i for i in range(N + 1)])
        donnes = simulation_marche(N, prec)
        # On modeliise la courbe
        parametres, covariance = curve_fit(lambda x, a, c: gauss(x, a, N / 2, c),
                                           plage, donnes, method='lm')
        # Calcul de la valeur moyenne
        moyenne[N-debut]=quad(lambda x : gauss(x, parametres[0], N / 2, parametres[1]),0,N)[0]/N
    plage = np.array([i for i in range(debut, fin+1)])
    plt.plot(plage,moyenne)
    plt.show()

def evolution_ecart_type_N(debut,fin,prec, seuil=0):
    """
    Evolution de l'écart type en fonction du nombre détape
    :param debut: Nombre d'étapes initial
    :param fin: Nombre d'étapes  final
    :param prec: Nombre de simulation pour obtenir la valeur moyenne
    :return: Rien
    """
    # Tableau des resultats
    ecarts = np.zeros(fin - debut + 1)
    # Initialisation de la boucle en fonction de N
    for N in range(debut, fin+1):
        plage = np.array([i for i in range(N + 1)])
        donnes = simulation_marche(N, prec)
        # Modélisation de la courbe
        parametres, covariance = curve_fit(lambda x, a, c: gauss(x, a, N / 2, c),
                                           plage, donnes, method='lm')
        # Calcul de l'écart-type
        somme = 0
        for x in range(len(donnes)):
            somme+=(donnes[x]-gauss(plage[x], parametres[0], N/2, parametres[1]))**2
        ecarts[N-debut]=(somme/(fin-debut))**0.5 # calcul de sigma_{n-1}
    # Affichage des resultats
    plage = np.array([i for i in range(debut, fin + 1)])
    plt.plot(plage, ecarts)
    plt.show()

def evolution_ecart_type_prec(debut,fin, ref, N, seuil=0):
    """
    Renvoie l'evolution de l'écart type en fonction du nombre de simulations
    :param debut: Nombre de simulation initial
    :param fin: Nombre de simulation final
    :param ref: Nombre de simulation pour obtenir les valeurs moyennes
    :param N: Nombre d'étapes
    :param seuil: Ajout d'un seuil de valeur moyenne des données pris en compte
    :return: Rien
    """
    # On fit la courbe en se centrant sur les valeurs du milieu à partir d'une valeur moyenne valant seuil
    # On la fit avec une précision donnée par la valeur de référence
    plage = np.array([i for i in range(N + 1)])  # creation des abscisses
    donnes = simulation_marche(N, ref)
    parametres, covariance = curve_fit(lambda x, a, c: gauss(x, a, N / 2, c),
                                       plage, donnes, method='lm')
    ecarts = np.zeros(fin - debut + 1)
    # Initialisation de la boucle pour calculer les écarts types en fonction de la précision
    for prec in range(debut, fin+1):
        donnes = simulation_marche(N, prec)  # Resultats experimentaux
        #calcul de l'écart-type
        somme = 0
        for x in range(len(donnes)):
            somme+=(donnes[x]-gauss(plage[x], parametres[0], N/2, parametres[1]))**2
        ecarts[prec-debut]=(somme/(fin-debut))**0.5 # calcul de sigma_{n-1}
    # Affichage des résultats
    plage = np.array([i for i in range(debut, fin + 1)])
    plt.scatter(plage, ecarts, marker='+', linewidths=0.5)
    plt.show()

def comp(N, prec):
    plage = np.array([i for i in range(N + 1)])
    donnes = simulation_marche(N, prec)
    plt.bar(plage, donnes, 1)
    plt.xlabel('rang')
    plt.ylabel('Nombre de simulations')
    plt.show()
    plt.clf()
    plt.plot(plage, donnes, 'o', label='résultats expérimentaux')
    # Crée un modèle de courbe à partir des données experimental
    # on restreint les données autour du centre de la gaussienne pour améliorer le poids de ces données
    parametres, covariance = curve_fit(lambda x, a, c: gauss(x, a, N / 2, c), plage, donnes, method='lm')
    # On connaît le milieu de la gaussienne donc on le fixe à N/2
    x = np.linspace(0, N, 10 * N)
    plt.plot(x, gauss(x, parametres[0], N / 2, parametres[1]), color='yellow', label='modèle')
    plt.xlabel('rang')
    plt.ylabel('Nombre de simulations')
    plt.show()

comp(100,10000)
#evolution_ecart_type_prec(10, 1000, 10000, 10)
# evolution_ecart_type_prec(100,10000,10)
#donnes=simulation_marche(100,1000)
#double_check(donnes, 100, 1)
#evolution_ecart_type_N(10,100,10000)
#evolution_ecart_type_N(10,100,1000,0.1)
#evolution_moyenne(10,100,1000)