"""
Project: NF18
Group number: 05
"""

# variable globale pour stocker l'objet de connexion avec base de donnee
conn = None

# variable globale pour indiquer le role de utilisateur
# si token == 1 il est membrePersonnel, si token == 2 il est aderent
# mais avant notre utilisateur se connecter, token = None
role = None

def connect_to_db():
    """return connection of the postresql, if login successfully else return None"""
    pass

def login():
    """verification de role de utilisateur"""
    pass

def loop(conn):
    """main loop of the program"""
    print("Bonjour, bienvenue a base de donnee biblio")
    print("Appuyez 1 pour afficher vos emprunts")
    print("Appuyez 2 pour afficher des exemplaires de auteur")
    print("Appuyez 3 pour afficher tous les livres")
    print("Appuyez 4 pour afficher des emprunts des Adherents")
    print("Appuyez 5 pour afficher des emprunts des Adherents")
    print("Appuyez 6 pour afficher des emprunts des Adherents")
    print("Appuyez 7 pour afficher des emprunts des Adherents")
    print("Appuyez 8 pour afficher des emprunts des Adherents")
    print("Appuyez 9 pour afficher des emprunts des Adherents")
    print("Appuyez 10 pour afficher des emprunts des Adherents")
    print("Appuyez 11 pour afficher des emprunts des Adherents")
    print("Appuyez 12 pour afficher des emprunts des Adherents")
    choix = input()
    if choix == "1":
        print("1")
    elif choix == "2":
        print("2")
    else:
        print("input invalide")

"""choix pour les adherents"""
def affichage_emprunts():
    """afficher tous les lignes de emprunts liee a cet utilisateur"""
    pass

def exemplairesPop():
    pass

def affichageDesGenres():
    pass

"""choix pour les membrePersonnels"""
def ajouterDesDocuments():
    pass

def modifierDesDiscription():
    pass

def ajouterDesExemplaires():
    pass

def gestionDesPrets():
    pass

def gestionDesSactions():
    pass


if __name__ == "__main__":
    conn = connect_to_db()
    uid = login()
    while conn is not None:
        loop(conn)

    print("Connextion not exists")
