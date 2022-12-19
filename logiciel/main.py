"""
UV: NF18
Group number: 05
Subject: library management system
"""

import psycopg2
from enum import Enum

class Token(Enum):
    """
    Token enumaration shows the identification of the user, Membre et Adhérent,
    those two kinds of users have different authorities. 
    """
    ADHERENT = 'Adherent'
    MEMBRE = 'Membre'


class SqlType(Enum):
    """
    SqlType enumaration shows the type of the sql request. In this project
    we will use two different type of SQL: DML and DQL
    (DML https://en.wikipedia.org/wiki/Data_manipulation_language and 
    DQL https://en.wikipedia.org/wiki/Data_query_language), 
    and as we all know DML needs COMMIT and ROLLBACK which are always 
    related to the TRANSACTION in database, so SqlType enumaration will 
    help us to simplify the design our interfaces. You will see more details 
    in the implementation of the function sql_execute() below. 
    """
    DML = 'dml'
    DQL = 'dql'


def sql_execute(sql, conn, sql_type: SqlType, error_message=None) -> list:
    """
    Method to execute sql requests, using strategy pattern
    
    Args:
        sql (string): the SQL you want to execute
        conn (connection object of psycopg2): generated by psycopg2.connect(...)
        sql_type (SqlType): DML or DQL
        error_message (string, optional): you can customize the error information
            for this sql. Defaults to None.

    Returns:
        list: return list of the sql executed, format like [[], [], ...] 
            and list = [] if there's no return
    """
    try:
        cur = conn.cursor()
        cur.execute(sql)
        if sql_type is SqlType.DQL:
            res = cur.fetchall()
            cur.close()
            return res
        elif sql_type is SqlType.DML:
            cur.commit()
            return []
    except (Exception, psycopg2.DatabaseError) as error:
        print('\n\nSQL_ERROR:\n' + sql)
        if error_message is None:
            print(error_message)
        else:
            print('ERROR: ' + str(error.__class__))

def res_print(ls: list):
    """_summary_

    Args:
        ls (list): 
    """
    print("\n---SQL result: ---\n")
    if not ls:
        print("La requête ne renvoie aucun résultat")
    else:
        for r in ls:
            s = ""
            for item in r:
                s = s + ("\t" + str(item))
            print(" -> " + s)
    print("-" * 18 + "\n")


class Program:
    """
    Basic class to represent the whole program.
    Don't forget to change the parameters in the connect_to_db function.
    """
    def __init__(self):
        self.user = User()
        self.connection = None
        
        if not self.connect_to_db():
            return

        while not self.login():
            pass
        
        self.loop()
        print('Au revoir...')

    def connect_to_db(self):
        try:
            print("Connection à postgresql...")
            
            # you should change the target database name, username and password
            self.connection = psycopg2.connect(database='nf18',
                                               user='postgres',
                                               password='123456',
                                               host='localhost',
                                               port='5432')
            cur = self.connection.cursor()
            print('Postgresql version: ')
            cur.execute('select version()')
            db_version = cur.fetchone()
            cur.close()
            print(db_version)
            print('Connection réussie\n\n')
            return True
        except (Exception, psycopg2.DatabaseError) as error:
            print('Erreur de type : ' + str(error.__class__))
            print("Echec de la connexion à la base de données")
            return False

    def login(self) -> bool:
        """
        Returns:
            bool: return True when login succeeded, return False when login failed
        """
        # print(sql_execute(sql='select * from coating;', conn=self.connection, sql_type=SqlType.DQL))
        while self.user.token is None:
            role_str = input(Token.MEMBRE.value + ' or ' + Token.ADHERENT.value + '?:M/A :')
            if role_str == 'M':
                self.user.token = Token.MEMBRE
            elif role_str == 'A':
                self.user.token = Token.ADHERENT
        
        while self.user.uname is None:
            uname = input("Nom d'utilisateur : ")
            if uname != '':
                self.user.uname = uname
                
        pwd, sql = '', ''
        while pwd == '':
            pwd = input('Mot de passe : ')
        if self.user.token == Token.ADHERENT:
            sql = """
            select nom,prenom,date_naissance,code_postal,adresse_rue,ville,adresse_mail,num_tel,actif,droit_emprunt
            from Adherent 
            where login = '{0}' and mdp = '{1}'
            """.format(self.user.uname, pwd)
        elif self.user.token == Token.MEMBRE:
            sql = """
            select nom,prenom,date_naissance,code_postal,adresse_rue,ville,adresse_mail,num_tel,actif,droit_emprunt 
            from membrepersonnel
            where login = '{0}' and mdp = '{1}'
            """.format(self.user.uname, pwd)
        else:
            return False

        user_info_list = sql_execute(sql=sql, conn=self.connection, sql_type=SqlType.DQL)
        if not user_info_list:
            print("Nom d'utilisateur ou mot de passe inccorecte, veuillez réessayer")
            self.user.uname = None
            self.user.token = None
            return False
        elif len(user_info_list) > 1:
            self.user.uname, self.user.token = None, None
            return False
        else:
            print("Bienvenue " + self.user.token.value + ": " + user_info_list[0][1])
            return True

    def loop(self):
        print('Connexion réussie...\n')
        while True:
            if self.user.token is Token.MEMBRE:
                print('Bienvenue...')
                print('Entrez 1 pour gérer les prêts des adhérents')
                print('Entrez 2 pour gérer les sanctions des adhérents')
                print('Entrez 3 pour mettre à jour les retards')
                print('Entrez q pour quitter')
                
                choice = input('# ')
                if choice == '1':
                    
                    sql = """
                    SELECT  Film.titre, Emprunt.date_pret, Emprunt.date_retour
                    FROM Emprunt
                    JOIN Exemplaire
                    ON Emprunt.exemplaire = Exemplaire.id
                    JOIN Film
                    ON Film.code = Exemplaire.code_film
                    WHERE Emprunt.personnel = '{0}';
                    """.format(self.user.uname)
                    films = sql_execute(sql=sql, conn=self.connection, sql_type=SqlType.DQL)
                    print("\n---Films dans le biblo---")
                    res_print(films)
                    
                    sql = """
                    SELECT  Livre.titre, Emprunt.date_pret, Emprunt.date_retour
                    FROM Emprunt
                    JOIN Exemplaire
                    ON Emprunt.exemplaire = Exemplaire.id
                    JOIN Livre
                    ON Livre.code = Exemplaire.code_livre
                    WHERE Emprunt.personnel = '{0}';
                    """.format(self.user.uname)
                    livres = sql_execute(sql=sql, conn=self.connection, sql_type=SqlType.DQL)
                    print("\n---Livres dans le biblo---")
                    res_print(livres)
                    
                elif choice == '2':
                    pass
                elif choice == 'q':
                    return
                else:
                    print('Choix invalide : ' + choice)

            elif self.user.token is Token.ADHERENT:
                print('Bienvenue...')
                print('Entrez 1 pour afficher vos emprunts')
                print('Entrez 2 pour rechercher les oeuvres d''un contributeur')
                print('Entrez 3 pour afficher les oeuvres par ordre de popularité')
                print('Entrez 4 si vous souhaitez des suggestions de films qui pourraient vous plaire')
                print('Entrez 5 si vous souhaitez des suggestions de livres qui pourraient vous plaire')
                print('Entrez 6 si vous souhaitez des suggestions d''oeuvres musicales qui pourraient vous plaire')
                print('Entrez q pour quitter')

                choice = input('# ')
                if choice == '1':
                    sql = """
                    SELECT  Film.titre, Emprunt.date_pret, Emprunt.date_retour
                    FROM Emprunt
                    JOIN Exemplaire
                    ON Emprunt.exemplaire = Exemplaire.id
                    JOIN Film
                    ON Film.code = Exemplaire.code_film
                    WHERE Emprunt.adherent = '{0}';
                    """.format(self.user.uname)
                    empruntes_of_film = sql_execute(sql=sql, conn=self.connection, sql_type=SqlType.DQL)
                    print("\n---Emprunts de films---")
                    res_print(empruntes_of_film)
                    
                    sql = """
                    SELECT  OeuvreMusicale.titre, Emprunt.date_pret, Emprunt.date_retour
                    FROM Emprunt
                    JOIN Exemplaire
                    ON Emprunt.exemplaire = Exemplaire.id
                    JOIN OeuvreMusicale
                    ON OeuvreMusicale.code = Exemplaire.code_oeuvre
                    WHERE Emprunt.adherent = '{0}';
                    """.format(self.user.uname)
                    emprunt_of_music = sql_execute(sql=sql, conn=self.connection, sql_type=SqlType.DQL)
                    print("\n---Emprunts d'oeuvres musicales---")
                    res_print(emprunt_of_music)
                    
                    sql = """
                    SELECT  Livre.titre, Emprunt.date_pret, Emprunt.date_retour
                    FROM Emprunt
                    JOIN Exemplaire
                    ON Emprunt.exemplaire = Exemplaire.id
                    JOIN Livre
                    ON Livre.code = Exemplaire.code_livre
                    WHERE Emprunt.adherent = '{0}';
                    """.format(self.user.uname)
                    emprunt_of_livre = sql_execute(sql=sql, conn=self.connection, sql_type=SqlType.DQL)
                    print("\n---Emprunts de livres---")
                    res_print(emprunt_of_livre)
                    
                elif choice == '2':
                    nom = input("Donnez le nom du contributeur (Auteur, Compositeur ou Acteur) : ")
                    prenom = input("Donnez le prénom nom du contributeur (Auteur, Compositeur ou Acteur) : ")
                    t = input("Veuillez entrez le type d'oeuvre (livre, oeuvre ou film) : ")
                    if t == 'oeuvre' :
                        sql = """
                        SELECT  OeuvreMusicale.titre,Composer.contrib_nom AS Nom,Composer.contrib_prenom AS Prénom,COUNT(Exemplaire.id)    AS NbExemplaires
                        FROM Composer
                        JOIN OeuvreMusicale
                        ON Composer.code = OeuvreMusicale.code
                        JOIN Exemplaire
                        ON OeuvreMusicale.code = Exemplaire.code_oeuvre
                        WHERE Composer.contrib_nom = '{0}'
                        AND Composer.contrib_prenom = '{1}'
                        GROUP BY  OeuvreMusicale.titre,Composer.contrib_nom,Composer.contrib_prenom
                        ORDER BY NbExemplaires ASC;
                        """.format(nom, prenom)
                        oeuvre = sql_execute(sql=sql, conn=self.connection, sql_type=SqlType.DQL)
                        print("\n---Oeuvres corespondantes à la recherche---")
                        res_print(oeuvre)

                    elif t == 'film' :
                        sql = """
                        SELECT  Film.titre,Acteur.contrib_nom AS Nom,Acteur.contrib_prenom AS Prénom,COUNT(Exemplaire.id)  AS NbExemplaires
                        FROM Acteur
                        JOIN Film
                        ON Acteur.code = Film.code
                        JOIN Exemplaire
                        ON Film.code = Exemplaire.code_film
                        WHERE Acteur.contrib_nom = '{0}'
                        AND Acteur.contrib_prenom = '{1}'
                        GROUP BY  Film.titre,Acteur.contrib_nom,Acteur.contrib_prenom
                        ORDER BY NbExemplaires ASC;
                        """.format(nom, prenom)
                        film = sql_execute(sql=sql, conn=self.connection, sql_type=SqlType.DQL)
                        print("\n---Films correspondants à la recherche---")
                        res_print(film)

                    elif t == 'livre' :
                        sql = """
                        SELECT  Livre.titre,Auteur.contrib_nom AS Nom,Auteur.contrib_prenom AS Prénom,COUNT(Exemplaire.id)  AS NbExemplaires
                        FROM Auteur
                        JOIN Livre
                        ON Auteur.code = Livre.code
                        JOIN Exemplaire
                        ON Livre.code = Exemplaire.code_livre
                        WHERE Auteur.contrib_nom = '{0}'
                        AND Auteur.contrib_prenom = '{1}'
                        GROUP BY  Livre.titre,Auteur.contrib_nom,Auteur.contrib_prenom
                        ORDER BY NbExemplaires ASC;
                        """.format(nom, prenom)
                        livre = sql_execute(sql=sql, conn=self.connection, sql_type=SqlType.DQL)
                        print("\n---Livres correspondants à la recherche---")
                        res_print(livre)
                        
                elif choice == '3':
                    
                    sql = """
                    SELECT  Film.titre, Film.genre, COUNT(*) AS Popularité
                    FROM Emprunt
                    JOIN Exemplaire
                    ON Exemplaire.id = Emprunt.exemplaire
                    JOIN Film
                    ON Exemplaire.code_film = Film.code
                    GROUP BY  titre, genre
                    ORDER BY Popularité ASC;
                    """
                    films_populaires = sql_execute(sql=sql, conn=self.connection, sql_type=SqlType.DQL)
                    print("\n---Films populaires dans la bibliothèque---")
                    res_print(films_populaires)
                    
                    sql = """
                    SELECT  OeuvreMusicale.titre, OeuvreMusicale.genre, COUNT(*) AS Popularité
                    FROM Emprunt
                    JOIN Exemplaire
                    ON Exemplaire.id = Emprunt.exemplaire
                    JOIN OeuvreMusicale
                    ON Exemplaire.code_oeuvre = OeuvreMusicale.code
                    GROUP BY  titre, genre
                    ORDER BY Popularité ASC;
                    """
                    oeuvres_populaires = sql_execute(sql=sql, conn=self.connection, sql_type=SqlType.DQL)
                    print("\n---Oeuvres musicales populaires dans la bibliothèque---")
                    res_print(oeuvres_populaires)
                    
                    sql = """
                    SELECT  Livre.titre, Livre.genre, COUNT(*) AS Popularité
                    FROM Emprunt
                    JOIN Exemplaire
                    ON Exemplaire.id = Emprunt.exemplaire
                    JOIN Livre
                    ON Exemplaire.code_livre = Livre.code
                    GROUP BY  titre, genre
                    ORDER BY Popularité ASC;
                    """
                    livres_populaires = sql_execute(sql=sql, conn=self.connection, sql_type=SqlType.DQL)
                    print("\n---Livres populaires dans la bibliothèque---")
                    res_print(livres_populaires)

                elif choice == '4':
                    sql = """
                    CREATE VIEW PopulariteFilm AS 
                    SELECT  Film.titre, Film.genre,COUNT(*) AS Popularite
                    FROM Emprunt
                    JOIN Exemplaire
                    ON Exemplaire.id = Emprunt.exemplaire
                    JOIN Film
                    ON Exemplaire.code_film = Film.code
                    WHERE Emprunt.adherent = '{0}'
                    GROUP BY  genre,titre
                    ORDER BY Popularite ASC;
                    """.format(self.user.uname)
                    genre = sql_execute(sql=sql, conn=self.connection, sql_type=SqlType.DQL)
                    if not genre :
                        print("Aucune suggestion à vous proposer."
                        "Si vous le souhaitez, il est possibe d'afficher les oeuvres par ordre de popularité.")
                    else :
                        genre = genre[0][1]
                        sql = """
                        SELECT  Film.titre
                        FROM Film
                        LEFT JOIN PopulariteFilm
                        ON Film.titre = PopulariteFilm.titre
                        WHERE PopulariteFilm.titre IS NULL 
                        AND Film.genre = '{0}'
                        GROUP BY  Film.titre;
                        """.format(genre)
                        films_populaires = sql_execute(sql=sql, conn=self.connection, sql_type=SqlType.DQL)
                        print("\n---Suggestions de films---")
                        res_print(films_populaires)
                    
                elif choice == '5' :
                    sql = """
                    CREATE VIEW PopulariteLivre AS 
                    SELECT  Livre.titre, Livre.genre,COUNT(*) AS Popularite
                    FROM Emprunt
                    JOIN Exemplaire
                    ON Exemplaire.id = Emprunt.exemplaire
                    JOIN Livre
                    ON Exemplaire.code_livre = Livre.code
                    WHERE Emprunt.adherent = '{0}'
                    GROUP BY  genre,titre
                    ORDER BY Popularite ASC;
                    """.format(self.user.uname)
                    
                    genre = sql_execute(sql=sql, conn=self.connection, sql_type=SqlType.DQL)
                    if not genre :
                        print("Aucune suggestion à vous proposer."
                        "Si vous le souhaitez, il est possibe d'afficher les oeuvres par ordre de popularité.")
                    else :  
                        genre = genre[0][1]
                        sql = """
                        SELECT  Livre.titre
                        FROM Livre
                        LEFT JOIN PopulariteLivre
                        ON Livre.titre = PopulariteLivre.titre
                        WHERE PopulariteLivre.titre IS NULL 
                        AND Livre.genre = '{0}'
                        GROUP BY  Livre.titre;
                        """.format(genre)
                        livres_populaires = sql_execute(sql=sql, conn=self.connection, sql_type=SqlType.DQL)
                        print("\n---Suggestions de livres---")
                        res_print(livres_populaires)

                elif choice == '6' :
                    sql = """
                    CREATE VIEW PopulariteOeuvre AS 
                    SELECT  OeuvreMusicale.titre, OeuvreMusicale.genre,COUNT(*) AS Popularite
                    FROM Emprunt
                    JOIN Exemplaire
                    ON Exemplaire.id = Emprunt.exemplaire
                    JOIN OeuvreMusicale
                    ON Exemplaire.code_oeuvre = OeuvreMusicale.code
                    WHERE Emprunt.adherent = '{0}'
                    GROUP BY  genre,titre
                    ORDER BY Popularite ASC;
                    """.format(self.user.uname)
                    
                    genre = sql_execute(sql=sql, conn=self.connection, sql_type=SqlType.DQL)
                    if not genre :
                        print("Aucune suggestion à vous proposer."
                        "Si vous le souhaitez, il est possibe d'afficher les oeuvres par ordre de popularité.")
                    else :
                        genre = genre[0][1]
                        sql = """
                        SELECT  OeuvreMusicale.titre
                        FROM OeuvreMusicale
                        LEFT JOIN PopulariteOeuvre
                        ON OeuvreMusicale.titre = PopulariteOeuvre.titre
                        WHERE PopulariteOeuvre.titre IS NULL 
                        AND Livre.genre = '{0}'
                        GROUP BY  OeuvreMusicale.titre;
                        """.format(genre)
                        oeuvres_populaires = sql_execute(sql=sql, conn=self.connection, sql_type=SqlType.DQL)
                        print("\n---Suggestions d'oeuvres musicales---")
                        res_print(oeuvres_populaires)
                    
                elif choice == 'q':
                    print('\nAu revoir\n')
                    return
                else:
                    print('Valeur invalide : ' + choice)


class User:
    def __init__(self, uname=None, token=None):
        self.uname = uname
        self.token = token


if __name__ == "__main__":
    program = Program()
