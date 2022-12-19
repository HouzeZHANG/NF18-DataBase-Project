"""
UV: NF18
Group number: 05
Subject: library management system
"""

import psycopg2
from enum import Enum


class Token(Enum):
    """_summary_
    Token enumaration shows the identification of the user, in this program 
    we have two cases, Adherent means visitors of the library, Member means
    librarians. Those two kinds of users have different authorities. 
    """
    ADHERENT = 'Adherent'
    MEMBER = 'Member'


class SqlType(Enum):
    """_summary_
    SqlType enumaration shows the type of the sql request. In this project
    we wiil use two different type of SQL: DML and DQL
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
    """_summary_
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
            # DML needs to use commit
            cur.commit()
            return []
    except (Exception, psycopg2.DatabaseError) as error:
        print('\n\nSQL_ERROR:\n' + sql)
        if error_message is None:
            print(error_message)
        else:
            print('ERROR: ' + str(error.__class__))

def res_print(ls: list):
    print("\n---SQL result: ---\n")
    if not ls:
        print("0 rows founded")
    else:
        for r in ls:
            s = ""
            for item in r:
                s = s + ("\t" + str(item))
            print(" -> " + s)
    print("-" * 18 + "\n")


class Program:
    """_summary_
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
        print('Bye...')

    def connect_to_db(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        try:
            print("Connect to postgresql...")
            
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
            print('Connection successful\n\n')
            return True
        except (Exception, psycopg2.DatabaseError) as error:
            print('Error name: ' + str(error.__class__))
            print("Database connection failure")
            return False

    def login(self) -> bool:
        """_summary_

        Returns:
            bool: return True when login succeeded, return False when login failed
        """
        # print(sql_execute(sql='select * from coating;', conn=self.connection, sql_type=SqlType.DQL))
        while self.user.token is None:
            role_str = input(Token.MEMBER.value + ' or ' + Token.ADHERENT.value + '?:M/A :')
            if role_str == 'M':
                self.user.token = Token.MEMBER
            elif role_str == 'A':
                self.user.token = Token.ADHERENT
        
        while self.user.uname is None:
            uname = input('Username: ')
            if uname != '':
                self.user.uname = uname
                
        pwd, sql = '', ''
        while pwd == '':
            pwd = input('Password: ')
        if self.user.token == Token.ADHERENT:
            sql = """select * from Adherent 
            where login = '{0}' and mdp = '{1}'
            """.format(self.user.uname, pwd)
        elif self.user.token == Token.MEMBER:
            # TODO
            sql = """
            select * from membrepersonnel
            where login = '{0}' and mdp = '{1}'
            """.format(self.user.uname, pwd)
        else:
            return False

        user_info_list = sql_execute(sql=sql, conn=self.connection, sql_type=SqlType.DQL)
        if not user_info_list:
            print("username or password not correct, please try again")
            self.user.uname, self.user.token = None, None
            return False
        elif len(user_info_list) > 1:
            self.user.uname, self.user.token = None, None
            return False
        else:
            print("Welcome " + self.user.token.value + ": " + user_info_list[0][2])
            return True

    def loop(self):
        print('Login successfully...\n')
        while True:
            if self.user.token is Token.MEMBER:
                # TODO menu for member user
                print('Welcome member...')
                print('Enter 1 for <Affichage des livres>')
                print('Enter q to quit')
                
                choice = input('# ')
                if choice == '1':
                    sql = """select * from Livre;"""
                    livres = sql_execute(sql=sql, conn=self.connection, sql_type=SqlType.DQL)
                    print("\n---Livres dans le biblo---")
                    res_print(livres)
                elif choice == '2':
                    pass
                elif choice == 'q':
                    return
                else:
                    print('Input invalid, wrong input: ' + choice)

            elif self.user.token is Token.ADHERENT:
                # TODO menu for adherent user
                print('Welcome adherent...')
                print('Enter 1 for <Affichage des Emprunts des Adhérents (exemple : "apple")>')
                print('Enter 2 for <Affichage des livres>')
                print('Enter q to quit')

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
                    print("\n---Empruntes de films---")
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
                    print("\n---Empruntes de musical---")
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
                    print("\n---Empruntes de livres---")
                    res_print(emprunt_of_livre)
                    
                elif choice == 'q':
                    return
                elif choice == '2':
                    sql = """select * from Livre;"""
                    livres = sql_execute(sql=sql, conn=self.connection, sql_type=SqlType.DQL)
                    print(livres)
                elif choice == '4':
                    # TODO
                    pass
                elif choice == 'q':
                    print('\nGoodbye\n')
                    return
                else:
                    print('Input invalid, wrong input: ' + choice)


class User:
    def __init__(self, uname=None, token=None):
        self.uname = uname
        self.token = token


if __name__ == "__main__":
    program = Program()
