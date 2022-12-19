--suppression des tables au debut pour eviter les conflits de TABLE

DROP TABLE IF EXISTS Auteur;

DROP TABLE IF EXISTS Acteur;

DROP TABLE IF EXISTS Realiser;

DROP TABLE IF EXISTS Interpreter;

DROP TABLE IF EXISTS Composer;

DROP TABLE IF EXISTS Emprunt;

DROP TABLE IF EXISTS Exemplaire;

DROP TABLE IF EXISTS Livre;

DROP TABLE IF EXISTS Film;

DROP TABLE IF EXISTS OeuvreMusicale;

DROP TABLE IF EXISTS Deterioration;

DROP TABLE IF EXISTS Retard;

DROP TABLE IF EXISTS Contributeur;

DROP TABLE IF EXISTS MembrePersonnel;

DROP TABLE IF EXISTS Adherent;

CREATE TABLE Adherent( login VARCHAR(100) PRIMARY KEY, mdp VARCHAR(100) NOT NULL, nom VARCHAR(100) NOT NULL, prenom VARCHAR(100) NOT NULL, date_naissance DATE, code_postal CHAR(5), adresse_rue VARCHAR(100), ville VARCHAR(100), adresse_mail VARCHAR(100) NOT NULL, num_tel VARCHAR(100) NOT NULL, actif BOOLEAN, droit_emprunt BOOLEAN );

CREATE TABLE MembrePersonnel( login VARCHAR(100) PRIMARY KEY, mdp VARCHAR(100) NOT NULL, nom VARCHAR(100) NOT NULL, prenom VARCHAR(100) NOT NULL, code_postal CHAR(5), adresse_rue VARCHAR(100), ville VARCHAR(100), adresse_mail VARCHAR(100) NOT NULL );

CREATE TABLE Contributeur( nom VARCHAR(100), prenom VARCHAR(100), date_naissance DATE, nationalite VARCHAR(100), PRIMARY KEY (nom, prenom) );

CREATE TABLE Retard( id INT PRIMARY KEY, personnel VARCHAR(100) REFERENCES MembrePersonnel(login), fin BOOLEAN );

CREATE TABLE Deterioration( id INT PRIMARY KEY, personnel VARCHAR(100) REFERENCES MembrePersonnel(login), remboursement BOOLEAN );

CREATE TABLE OeuvreMusicale( code VARCHAR(100) PRIMARY KEY, titre VARCHAR(100) NOT NULL, date_apparition DATE, editeur VARCHAR(100), genre VARCHAR(100) NOT NULL, code_classification VARCHAR(100) NOT NULL, longueur TIME );

CREATE TABLE Film( code VARCHAR(100) PRIMARY KEY, titre VARCHAR(100) NOT NULL, date_apparition DATE, editeur VARCHAR(100), genre VARCHAR(100) NOT NULL, code_classification VARCHAR(100) NOT NULL, longueur TIME, synopsis VARCHAR(100) );

CREATE TABLE Livre( code VARCHAR(100) PRIMARY KEY, titre VARCHAR(100) NOT NULL, date_apparition DATE, editeur VARCHAR(100), genre VARCHAR(100) NOT NULL, code_classification VARCHAR(100) NOT NULL, ISBN VARCHAR(100) UNIQUE NOT NULL, resume VARCHAR(100), langue VARCHAR(100) );

CREATE TABLE Exemplaire( id INT PRIMARY KEY, etat VARCHAR(100) NOT NULL CHECK (etat IN ('neuf', 'bon', 'abîmé', 'perdu')), disponible BOOLEAN, code_oeuvre VARCHAR(100) REFERENCES OeuvreMusicale(code), code_film VARCHAR(100) REFERENCES Film(code), code_livre VARCHAR(100) REFERENCES Livre(code), CHECK(((code_oeuvre <> NULL) AND (code_film = NULL) AND (code_livre = NULL)) OR ((code_oeuvre = NULL) AND (code_film <> NULL) AND (code_livre = NULL)) OR ((code_oeuvre = NULL) AND (code_film = NULL) AND (code_livre <> NULL))) );

CREATE TABLE Emprunt( exemplaire INT REFERENCES Exemplaire (id), date_pret DATE NOT NULL, date_retour DATE NOT NULL CHECK (date_retour > date_pret), date_rendu DATE CHECK (date_rendu > date_pret), personnel VARCHAR(100) REFERENCES MembrePersonnel (login), adherent VARCHAR(100) REFERENCES Adherent (login), retard INT REFERENCES Retard(id), deterioration INT REFERENCES Deterioration(id), CHECK(((deterioration <> NULL) AND (retard = NULL)) OR ((retard <> NULL) AND (deterioration = NULL)) OR ((deterioration = NULL) AND (retard = NULL))), PRIMARY KEY (exemplaire, date_pret) );

CREATE TABLE Composer( contrib_nom VARCHAR(100), contrib_prenom VARCHAR(100), code VARCHAR(100) REFERENCES OeuvreMusicale (code), FOREIGN KEY (contrib_nom, contrib_prenom) REFERENCES Contributeur(nom, prenom), PRIMARY KEY(contrib_nom, contrib_prenom, code) );

CREATE TABLE Interpreter( contrib_nom VARCHAR(100), contrib_prenom VARCHAR(100), code VARCHAR(100) REFERENCES OeuvreMusicale (code), FOREIGN KEY (contrib_nom, contrib_prenom) REFERENCES Contributeur(nom, prenom), PRIMARY KEY(contrib_nom, contrib_prenom, code) );

CREATE TABLE Realiser( contrib_nom VARCHAR(100), contrib_prenom VARCHAR(100), code VARCHAR(100) REFERENCES Film (code), FOREIGN KEY (contrib_nom, contrib_prenom) REFERENCES Contributeur(nom, prenom), PRIMARY KEY(contrib_nom, contrib_prenom, code) );

CREATE TABLE Acteur( contrib_nom VARCHAR(100), contrib_prenom VARCHAR(100), code VARCHAR(100) REFERENCES Film (code), FOREIGN KEY (contrib_nom, contrib_prenom) REFERENCES Contributeur(nom, prenom), PRIMARY KEY(contrib_nom, contrib_prenom, code) );

CREATE TABLE Auteur( contrib_nom VARCHAR(100), contrib_prenom VARCHAR(100), code VARCHAR(100) REFERENCES Livre (code), FOREIGN KEY (contrib_nom, contrib_prenom) REFERENCES Contributeur(nom, prenom), PRIMARY KEY(contrib_nom, contrib_prenom, code) );

--création de vues
CREATE VIEW FinRetard AS
SELECT  Adherent.login                                                  AS Adhérent
       ,Emprunt.exemplaire                                              AS Exemplaire
       ,Emprunt.retard                                                  AS Retard
       ,Emprunt.date_rendu + (Emprunt.date_rendu - Emprunt.date_retour) AS DateDeFin
       ,DATE(NOW())                                                     AS DateDuJour
FROM Emprunt
JOIN Adherent
ON Emprunt.adherent = Adherent.login
WHERE Emprunt.retard IS NOT NULL;
