CREATE TABLE Adherent( login VARCHAR(100) PRIMARY KEY, mdp VARCHAR(100) NOT NULL, nom VARCHAR(100) NOT NULL, prenom VARCHAR(100) NOT NULL, date_naissance DATE, code_postal CHAR(5), adresse_rue VARCHAR(100), ville VARCHAR(100), adresse_mail VARCHAR(100) NOT NULL, num_tel VARCHAR(100) NOT NULL, actif BOOLEAN, droit_emprunt BOOLEAN );
INSERT INTO Adherent VALUES ('apple', '123456', 'Steve', 'Jobs', '1955-02-24', '60200', '1 Rue des Bonnetiers', 'Compiègne', 'steve.jobs@gmail.com', '(800)275-2273', True, True);
INSERT INTO Adherent VALUES ('otari', 'oTsuv471', 'Tari', 'Ousmane', '1998-07-15', '60200', '4 Rue Carnot', 'Compiègne', 'ousmane.tari@gmail.com', '0685967412', True, True);
INSERT INTO Adherent VALUES('asifflet', 'Lutr47j', 'Sifflet', 'Armin', '1990-10-25', '60200', '1 Rue Michelet', 'Compiègne', 'armin.sifflet@gmail.com', '0548963124', True, True);

CREATE TABLE MembrePersonnel( login VARCHAR(100) PRIMARY KEY, mdp VARCHAR(100) NOT NULL, nom VARCHAR(100) NOT NULL, prenom VARCHAR(100) NOT NULL, code_postal CHAR(5), adresse_rue VARCHAR(100), ville VARCHAR(100), adresse_mail VARCHAR(100) NOT NULL );
INSERT INTO MembrePersonnel VALUES('Chris', '654321', 'LU', 'Maybe', '13100', '13 Fleury val', 'Aix-en-provence', 'Fendi@outlook.com');
INSERT INTO MembrePersonnel VALUES('mazir', 'mA12ghuylm', 'Azir', 'Mohammed', '60000', '2 Avenue de la Paix', 'Beauvais', 'mohammed.azir@gmail.com');
INSERT INTO MembrePersonnel VALUES('eiro', 'yu45sdq', 'Iro', 'Esteban', '60200', '10 Rue Louis Armand', 'Compiègne', 'esteban.iro@gmail.com');

CREATE TABLE Contributeur( nom VARCHAR(100), prenom VARCHAR(100), date_naissance DATE, nationalite VARCHAR(100), PRIMARY KEY (nom, prenom) );
INSERT INTO Contributeur VALUES ('Pior Ilitch', 'Tchaïkovski', '1840-04-25', 'russe'), ('Maalouf', 'Ibrahim', '1980-11-05', 'française, libanaise'), ('Tarantino', 'Quentin', '1963-03-27', 'américaine'), ('Robert', 'Yves', '1920-06-19', 'française'), ('Travolta', 'John', '1954-02-18', 'américaine'), ('Richard', 'Pierre', '1934-08-16', 'française'), ('Beyle', 'Henri', '1783-01-23', 'française'), ('Orwell', 'Georges', '1903-06-25', 'britannique');

CREATE TABLE Retard( id INT PRIMARY KEY, personnel VARCHAR(100) REFERENCES MembrePersonnel(login), fin BOOLEAN );
INSERT INTO Retard VALUES ('1', 'Chris', '0');

CREATE TABLE Deterioration( id INT PRIMARY KEY, personnel VARCHAR(100) REFERENCES MembrePersonnel(login) remboursement BOOLEAN, );
INSERT INTO Deterioration VALUES ('1', 'eiro', '0');

CREATE TABLE OeuvreMusicale( code VARCHAR(100) PRIMARY KEY, titre VARCHAR(100) NOT NULL, date_apparition DATE, editeur VARCHAR(100), genre VARCHAR(100) NOT NULL, code_classification VARCHAR(100) NOT NULL, longueur TIME );
INSERT INTO OeuvreMusicale VALUES ('LLDCT38', 'Le Lac des cygnes', TO_DATE('1877', 'YYYY'), NULL, 'ballet classique', 'LEL134', '02:30:00');
INSERT INTO OeuvreMusicale VALUES ('TDCAU41', 'They Don’t Care About Us', TO_DATE('2011', 'YYYY'), NULL, 'mélange de styles', 'TDC123', '00:04:28');

CREATE TABLE Film( code VARCHAR(100) PRIMARY KEY, titre VARCHAR(100) NOT NULL, date_apparition DATE, editeur VARCHAR(100), genre VARCHAR(100) NOT NULL, code_classification VARCHAR(100) NOT NULL, longueur TIME, synopsis VARCHAR(100) );
INSERT INTO Film VALUES ('PULFI96', 'Pulp Fiction', TO_DATE('1994', 'YYYY'), NULL, 'gangsters', 'PUF932', '02:45:00');
INSERT INTO Film VALUES ('LGBCN96', 'Le Grand Blond avec une chaussure noire', TO_DATE('1972', 'YYYY'), NULL, 'espionnage parodique', 'LBB1325', '01:30:00');

CREATE TABLE Livre( code VARCHAR(100) PRIMARY KEY, titre VARCHAR(100) NOT NULL, date_apparition DATE, editeur VARCHAR(100), genre VARCHAR(100) NOT NULL, code_classification VARCHAR(100) NOT NULL, ISBN VARCHAR(100) UNIQUE NOT NULL, resume VARCHAR(100), langue VARCHAR(100) );
INSERT INTO Livre VALUES ('LRELN69', 'Le Rouge et le Noir', TO_DATE('1830', 'YYYY'), 'Poche', 'roman' , 'REN699', '978-2253077497', 'L’énergie d’un jeune homme ardent, exigeant et pauvre dans la société de la Restauration.', 'française');
INSERT INTO Livre VALUES ('AIHDA98', '1984', TO_DATE('1949', 'YYYY'), 'Penguin Random House Children’s UK', 'roman' , 'AIH984', '978-0241430972', 'Big Brother and the Thought Police watch everyone for signs of Thought Crime.', 'anglaise');

CREATE TABLE Exemplaire( id INT PRIMARY KEY, etat VARCHAR(100) NOT NULL CHECK (etat IN ('neuf', 'bon', 'abîmé', 'perdu')), disponible BOOLEAN, code_oeuvre VARCHAR(100) REFERENCES OeuvreMusicale(code), code_film VARCHAR(100) REFERENCES Film(code), code_livre VARCHAR(100) REFERENCES Livre(code), CHECK(((code_oeuvre <> NULL) AND (code_film = NULL) AND (code_livre = NULL)) OR ((code_oeuvre = NULL) AND (code_film <> NULL) AND (code_livre = NULL)) OR ((code_oeuvre = NULL) AND (code_film = NULL) AND (code_livre <> NULL))) );
INSERT INTO Exemplaire VALUES ('1', 'neuf', '1', NULL, 'PULFI96', NULL);
INSERT INTO Exemplaire VALUES ('2', 'bon', '0', NULL, NULL, 'LRELN69');

CREATE TABLE Emprunt( exemplaire INT REFERENCES Exemplaire (id), date_pret DATE NOT NULL, date_retour DATE NOT NULL CHECK (date_retour > date_pret), date_rendu DATE CHECK (date_rendu > date_pret), personnel VARCHAR(100) REFERENCES MembrePersonnel (login), adherent VARCHAR(100) REFERENCES Adherent (login), retard INT REFERENCES Retard(id), deterioration INT REFERENCES Deterioration(id), CHECK(((deterioration <> NULL) AND (retard = NULL)) OR ((retard <> NULL) AND (deterioration = NULL)) OR ((deterioration = NULL) AND (retard = NULL))), PRIMARY KEY (exemplaire, date_pret) );
INSERT INTO Emprunt VALUES ('1', TO_DATE('11-01-2022', 'DD-MM-YYYY'), TO_DATE('11-02-2022', 'DD-MM-YYYY'), TO_DATE('25-01-2022', 'DD-MM-YYYY'), 'mazir', 'apple', NULL, '1');
INSERT INTO Emprunt VALUES ('2', TO_DATE('04-06-2022', 'DD-MM-YYYY'), TO_DATE('04-07-2022', 'DD-MM-YYYY'), TO_DATE('07-07-2022', 'DD-MM-YYYY'), 'eiro', 'otari', '1', NULL);
INSERT INTO Emprunt VALUES ('2', TO_DATE('25-10-2022', 'DD-MM-YYYY'), TO_DATE('25-11-2022', 'DD-MM-YYYY'), NULL, 'eiro', 'asifflet', NULL, NULL);

CREATE TABLE Composer( contrib_nom VARCHAR(100), contrib_prenom VARCHAR(100), code VARCHAR(100) REFERENCES OeuvreMusicale (code), FOREIGN KEY (contrib_nom, contrib_prenom) REFERENCES Contributeur(nom, prenom), PRIMARY KEY(contrib_nom, contrib_prenom, code) );
INSERT INTO Composer VALUES ('Pior Ilitch', 'Tchaïkovski', 'LLDCT38');
INSERT INTO Composer VALUES ('Maalouf', 'Ibrahim', 'TDCAU41');

CREATE TABLE Interpreter( contrib_nom VARCHAR(100), contrib_prenom VARCHAR(100), code VARCHAR(100) REFERENCES OeuvreMusicale (code), FOREIGN KEY (contrib_nom, contrib_prenom) REFERENCES Contributeur(nom, prenom), PRIMARY KEY(contrib_nom, contrib_prenom, code) );
INSERT INTO Interpreter VALUES ('Maalouf', 'Ibrahim', 'TDCAU41');

CREATE TABLE Realiser( contrib_nom VARCHAR(100), contrib_prenom VARCHAR(100), code VARCHAR(100) REFERENCES Film (code), FOREIGN KEY (contrib_nom, contrib_prenom) REFERENCES Contributeur(nom, prenom), PRIMARY KEY(contrib_nom, contrib_prenom, code) );
INSERT INTO Realiser VALUES ('Tarantino', 'Quentin', 'PULFI96');
INSERT INTO Realiser VALUES ('Robert', 'Yves', 'LGBCN96');

CREATE TABLE Acteur( contrib_nom VARCHAR(100), contrib_prenom VARCHAR(100), code VARCHAR(100) REFERENCES Film (code), FOREIGN KEY (contrib_nom, contrib_prenom) REFERENCES Contributeur(nom, prenom), PRIMARY KEY(contrib_nom, contrib_prenom, code) );
INSERT INTO Acteur VALUES ('Travolta', 'John', 'PULFI96');
INSERT INTO Acteur VALUES ('Richard', 'Pierre', 'LGBCN96');

CREATE TABLE Auteur( contrib_nom VARCHAR(100), contrib_prenom VARCHAR(100), code VARCHAR(100) REFERENCES Livre (code), FOREIGN KEY (contrib_nom, contrib_prenom) REFERENCES Contributeur(nom, prenom), PRIMARY KEY(contrib_nom, contrib_prenom, code) );
INSERT INTO Auteur VALUES ('Beyle', 'Henri', 'LRELN69');
INSERT INTO Auteur VALUES ('Orwell', 'Georges', 'AIHDA98'); Affichage des Emprunts des Adhérents (exemple : 'apple')

SELECT  Film.titre
       ,Emprunt.date_pret
       ,Emprunt.date_retour
FROM Emprunt
JOIN Exemplaire
ON Emprunt.exemplaire = Exemplaire.id
JOIN Film
ON Film.code = Exemplaire.code_film
WHERE Emprunt.adherent = 'apple';

SELECT  OeuvreMusicale.titre
       ,Emprunt.date_pret
       ,Emprunt.date_retour
FROM Emprunt
JOIN Exemplaire
ON Emprunt.exemplaire = Exemplaire.id
JOIN OeuvreMusicale
ON OeuvreMusicale.code = Exemplaire.code_oeuvre
WHERE Emprunt.adherent = 'apple';

SELECT  Livre.titre
       ,Emprunt.date_pret
       ,Emprunt.date_retour
FROM Emprunt
JOIN Exemplaire
ON Emprunt.exemplaire = Exemplaire.id
JOIN Livre
ON Livre.code = Exemplaire.code_livre
WHERE Emprunt.adherent = 'apple'; Affichage des Exemplaires de tel auteur aux Adhérents Affichage des Livres - Films - Oeuvres musicales aux Adhérents

SELECT  *
FROM Livre;

SELECT  *
FROM Film;

SELECT  *
FROM OeuvreMusicale; Ajouter des documents
INSERT INTO Livre VALUES (code, titre, date_apparition, editeur, genre, code_classification, ISBN, resume, langue); {pour le programme en python, affectation aux variables}
INSERT INTO Film VALUES (code, titre, date_apparition, editeur, genre, code_classification, longueur, synopsis);
INSERT INTO OeuvreMusicale VALUES(code, titre, date_apparition, editeur, genre, code_classification, longueur); Modifier leur description Ajouter des exemplaires d'une Ressource
INSERT INTO Exemplaire VALUES (etat,disponible,code_oeuvre,code_film,code_livre); Gestion des Prêts par MembrePersonnel Gestion des sanctions par MembrePersonnel Affichage des données des utilisateurs pour un Adhérent Profil des Adhérents Les exemplaires populaires Affichage des genres