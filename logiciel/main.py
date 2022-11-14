"""
Project: NF18
Group number: 05
"""

# variable globale pour stocker l'objet de connexion avec base de donnee
conn = None

# variable globale pour indiquer le role de utilisateur
# si token == 2 il est membrePersonnel, si token == 1 il est aderent
# mais avant notre utilisateur se connecter, token = None
role = None
uid = None

def sqlExecute(sql: string)->list:
    """cette methode est destine a simplifier le processus de sql, retourner un liste de tuple"""
    return []

def connect_to_db():
    """return connection of the postresql, if login successfully else return None"""
    conn = None
    try:
        conn = psycopg2.connect(
            host = "",
            database = "",
            user = "",
            password = ""
        )
        cur = conn.cursor()
        print('Postgres version: ')
        cur.execute('SELECT version()')
        db_version = cur.fetchone()
        print(db_version)
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

def login():
    """verification de role de utilisateur"""
    role = None
    uid = None
    
    print("Vous etes adherent ou membrePersonnel?")
    print("1: adherent")
    print("2: membrePersonnel")
    response = input("Vous etes: 1/2")
    if response == '1':
        role = 1
    elif response == '2':
        role = 2
    else:
        print("input invalide")
        return
    
    print("\nenterez votre username et mot de passe")
    username = input("username: ")
    pwd = input("mot de passe: ")
    
    if role == 1:
        sql = """
        
        """
    else:
        sql = """
        
        """
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
    if conn is None:
        pass
    else:
        while uid is None:
            login()
        while conn is not None:
            loop(conn)
