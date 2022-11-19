"""
Project: NF18
Group number: 05
"""

import psycopg2
from enum import Enum


class Token(Enum):
    ADHERENT = 'Adherent'
    MEMBER = 'Member'


class SqlType(Enum):
    DML = 'dml'
    DQL = 'dql'


def sql_execute(sql, conn, sql_type: SqlType, error_message=None) -> list:
    """template pattern for sql execute"""
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


class Program:
    def __init__(self):
        self.user = None

        self.connection = None
        self.connect_to_db()
        if self.connection is None:
            return

        while not self.login():
            pass

        self.loop()

    def connect_to_db(self):
        """establish connection with postgresql using psycopg2, initialize self. Connection"""
        try:
            print("Connect to postgresql...")
            self.connection = psycopg2.connect(database='testdb',
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
        except (Exception, psycopg2.DatabaseError) as error:
            print('Error name: ' + str(error.__class__))

    def login(self) -> bool:
        """authentication, initialize self. User"""
        # print(sql_execute(sql='select * from coating;', conn=self.connection, sql_type=SqlType.DQL))
        role = ''
        while role != 'M' and role != 'A':
            role = input(Token.MEMBER.value + ' or ' + Token.ADHERENT.value + '?:M/A')
        uname = ''
        while uname == '':
            uname = input('Username: ')
        pwd = ''
        while pwd == '':
            pwd = input('Password: ')
        if role == 'M':
            # TODO
            sql = ''
        else:
            # TODO
            sql = ''

        user_info_list = sql_execute(sql=sql, conn=self.connection, sql_type=SqlType.DQL)
        # TODO
        #  if login success we initialize self. User and return True,
        #  else return False, let __init__ call login again
        # self.user = User()
        return False

    def loop(self):
        print('Login success...\n')

        while True:
            if self.user.token is Token.MEMBER:
                # TODO menu for member user
                print('Welcome member...')
            else:
                # TODO menu for adherent user
                print('Welcome adherent...')

            choice = input('# ')
            if choice == '1':
                # TODO
                pass
            elif choice == '2':
                # TODO
                pass
            elif choice == '3':
                # TODO
                pass
            elif choice == '4':
                # TODO
                pass
            elif choice == 'q':
                print('\nGoodbye\n')
                return
            else:
                print('Input invalid, wrong input: ' + choice)


class User:
    def __init__(self, uname='Unknow', token=Token.ADHERENT):
        self.uname = uname
        self.token = token


if __name__ == "__main__":
    program = Program()
