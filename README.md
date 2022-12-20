# Project NF18 2022 Biblio

Group 5:
- [Cassandra Le Roux](https://gitlab.utc.fr/lerouxca)
- [Camille Josserand](https://gitlab.utc.fr/cjossera) 
- [Chloe Bolle-Reddat](https://gitlab.utc.fr/cbollere)
- [ZHANG Houze](https://github.com/HouzeZHANG)

Gestion d'une base de données pour une bibliothèque réalisée en pyhthon, dans le cadre d'un projet de NF18 A22

![Interactive library management system based on psycopg2 and python](doc/img/welcome.png)

## Fonctionnalités <!-- omit in toc -->

Ce projet est implémenté en [psycopg2](https://github.com/fuergaosi233/wechat-chatgpthttps://www.psycopg.org/docs/), [python3](https://www.python.org/downloads/) et [postgresql](https://www.postgresql.org/)

- Possibilité d'utilisation de JSON

## 0. Contenu de la base de données <!-- omit in toc -->

- [Project NF18 2022 Biblio](#project-nf18-2022-biblio)
  - [1. Comment utiliser la base de données dans une application Python ?](#1-comment-utiliser-la-base-de-données-dans-une-application-python-)

## 1. Comment utiliser la base de données dans une application Python ?

1. [Installer](https://www.postgresql.org/download/) Postgresql Client
2. Créer test_database sur une base de données locale ou sur un serveur de base de données à distance
```sql
CREATE DATABASE [testdb]
```
3. Copier/dupliquer ce dossier en local
```git
git clone git@gitlab.utc.fr:cjossera/nf18-td1_g5.git
```
4. Créer les tables et insérer des exemples de données
```cmd
psql -U [username] -d [testdb] -a -f SQL_CREATE_TABLE.sql
psql -U [username] -d [testdb] -a -f SQL_INSERT.sql
```
5. Configurer les paramètres dans [db_config.ini](.\logiciel\conf\db_config.ini)

![params of connection](doc/img/params.png)

6. Lancer [main.py](logiciel/main.py) dans le terminal
```cmd
python main.py
```
Si vous pouvez voir les lignes suivantes (cf ci-dessous), félicitations !
![connect successfully](doc/img/connect.png)
Si les lignes suivantes apparaissent (cf ci-dessous), cela signifie qu'il y a eu un problème avec la configuration, veuillez vérfier à nouveau que tous les paramètres ont été étbalis correctement.
![connect failure](doc/img/connectfailure.png)
