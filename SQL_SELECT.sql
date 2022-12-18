--Affichage des Emprunts des Adhérents (exemple : 'apple')--
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
WHERE Emprunt.adherent = 'apple';
--Affichage des Exemplaires de tel auteur - réalisateur - compositeur aux Adhérents--
SELECT  Livre.titre
       ,Auteur.contrib_nom    AS Nom
       ,Auteur.contrib_prenom AS Prénom
       ,COUNT(Exemplaire.id)  AS NbExemplaires
FROM Auteur
JOIN Livre
ON Auteur.code = Livre.code
JOIN Exemplaire
ON Livre.code = Exemplaire.code_livre
WHERE Auteur.contrib_nom = 'Beyle'
AND Auteur.contrib_prenom = 'Henri'
GROUP BY  Livre.titre
         ,Auteur.contrib_nom
         ,Auteur.contrib_prenom
ORDER BY NbExemplaires ASC;

SELECT  Film.titre
       ,Acteur.contrib_nom    AS Nom
       ,Acteur.contrib_prenom AS Prénom
       ,COUNT(Exemplaire.id)  AS NbExemplaires
FROM Acteur
JOIN Film
ON Acteur.code = Film.code
JOIN Exemplaire
ON Film.code = Exemplaire.code_film
WHERE Acteur.contrib_nom = 'Travolta'
AND Acteur.contrib_prenom = 'John'
GROUP BY  Film.titre
         ,Acteur.contrib_nom
         ,Acteur.contrib_prenom
ORDER BY NbExemplaires ASC;

SELECT  OeuvreMusicale.titre
       ,Composer.contrib_nom    AS Nom
       ,Composer.contrib_prenom AS Prénom
       ,COUNT(Exemplaire.id)    AS NbExemplaires
FROM Composer
JOIN OeuvreMusicale
ON Composer.code = OeuvreMusicale.code
JOIN Exemplaire
ON OeuvreMusicale.code = Exemplaire.code_oeuvre
WHERE Composer.contrib_nom = 'Maalouf'
AND Composer.contrib_prenom = 'Ibrahim'
GROUP BY  OeuvreMusicale.titre
         ,Composer.contrib_nom
         ,Composer.contrib_prenom
ORDER BY NbExemplaires ASC;
--Affichage des Livres - Films - Oeuvres musicales aux Adhérents--
SELECT  *
FROM Livre;

SELECT  *
FROM Film;

SELECT  *
FROM OeuvreMusicale;
--Ajouter des documents--
INSERT INTO Livre VALUES (code, titre, date_apparition, editeur, genre, code_classification, ISBN, resume, langue); {pour le programme en python, affectation aux variables}
INSERT INTO Film VALUES (code, titre, date_apparition, editeur, genre, code_classification, longueur, synopsis);
INSERT INTO OeuvreMusicale VALUES(code, titre, date_apparition, editeur, genre, code_classification, longueur);
--Modifier leur description-- UPDATE Film

SET synopsis = {}
WHERE code = {} UPDATE Livre

SET resume = {}
WHERE code = {}
--Ajouter des exemplaires d'une Ressource--
INSERT INTO Exemplaire VALUES (etat,disponible,code_oeuvre,code_film,code_livre);
--Gestion des Prêts par un MembrePersonnel--
SELECT  Film.titre
       ,Emprunt.date_pret
       ,Emprunt.date_retour
FROM Emprunt
JOIN Exemplaire
ON Emprunt.exemplaire = Exemplaire.id
JOIN Film
ON Film.code = Exemplaire.code_film
WHERE Emprunt.personnel = 'mazir';
--Gestion des sanctions par MembrePersonnel--
SELECT  Livre.titre
       ,Emprunt.date_pret
       ,Emprunt.date_retour
       ,Emprunt.adherent
       ,Retard.personnel
FROM Retard
JOIN Emprunt
ON Emprunt.retard = Retard.id
JOIN Exemplaire
ON Emprunt.exemplaire = Exemplaire.id
JOIN Livre
ON Livre.code = Exemplaire.code_livre;

SELECT  Film.titre
       ,Emprunt.date_pret
       ,Emprunt.date_retour
       ,Emprunt.adherent
       ,Deterioration.personnel
FROM Deterioration
JOIN Emprunt
ON Emprunt.deterioration = Deterioration.id
JOIN Exemplaire
ON Emprunt.exemplaire = Exemplaire.id
JOIN Film
ON Film.code = Exemplaire.code_film;

SELECT  Adherent.nom
       ,Adherent.prenom
       ,Adherent.actif
       ,Deterioration.id
FROM Adherent
LEFT JOIN Emprunt
ON Emprunt.adherent = Adherent.login
LEFT JOIN Deterioration
ON Deterioration.id = Emprunt.deterioration;

SELECT  Adherent.nom
       ,Adherent.prenom
       ,Adherent.actif
       ,Retard.id
FROM Adherent
LEFT JOIN Emprunt
ON Emprunt.adherent = Adherent.login
LEFT JOIN Retard
ON Retard.id = Emprunt.retard;
--Affichage des données des utilisateurs pour un Adhérent--
SELECT  nom
       ,prenom
       ,date_naissance
       ,code_postal
       ,adresse_rue
       ,ville
       ,adresse_mail
       ,num_tel
       ,actif
       ,droit_emprunt
FROM Adherent
WHERE login = 'apple';
--Les genres populaires pour un adhérent (exemple d'apple Film)--

CREATE VIEW PopularitéFilmApple AS
SELECT  Film.titre
       ,Film.genre
       ,COUNT(*) AS Popularité
FROM Emprunt
JOIN Exemplaire
ON Exemplaire.id = Emprunt.exemplaire
JOIN Film
ON Exemplaire.code_film = Film.code
WHERE Emprunt.adherent = 'apple'
GROUP BY  genre
         ,titre
ORDER BY Popularité ASC;
--Profil des Adhérents (exemple d'apple pour Film)--
SELECT  Film.titre
FROM Film
LEFT JOIN PopularitéFilmApple
ON Film.titre = PopularitéFilmApple.titre
WHERE PopularitéFilmApple.titre IS NULL
AND Film.genre = 'gangsters'
GROUP BY  Film.titre;
--'gangsters' sera récupéré avec le code Python
--Les exemplaires populaires--

CREATE VIEW PopularitéFilm AS
SELECT  Film.titre
       ,Film.genre
       ,COUNT(*) AS Popularité
FROM Emprunt
JOIN Exemplaire
ON Exemplaire.id = Emprunt.exemplaire
JOIN Film
ON Exemplaire.code_film = Film.code
GROUP BY  titre
         ,genre
ORDER BY Popularité ASC;

CREATE VIEW PopularitéOeuvre AS
SELECT  OeuvreMusicale.titre
       ,OeuvreMusicale.genre
       ,COUNT(*) AS Popularité
FROM Emprunt
JOIN Exemplaire
ON Exemplaire.id = Emprunt.exemplaire
JOIN OeuvreMusicale
ON Exemplaire.code_oeuvre = OeuvreMusicale.code
GROUP BY  titre
         ,genre
ORDER BY Popularité ASC;

CREATE VIEW PopularitéLivre AS
SELECT  Livre.titre
       ,Livre.genre
       ,COUNT(*) AS Popularité
FROM Emprunt
JOIN Exemplaire
ON Exemplaire.id = Emprunt.exemplaire
JOIN Livre
ON Exemplaire.code_livre = Livre.code
GROUP BY  titre
         ,genre
ORDER BY Popularité ASC;
--Affichage des genres--
SELECT  *
FROM Livre
WHERE genre = {};

SELECT  *
FROM Film
WHERE genre = {};

SELECT  *
FROM OeuvreMusicale
WHERE genre = {};
--Update des Retards (avec comparaison avec DateDuJour)--

CREATE VIEW FinRetard AS
SELECT  Adherent.login                                                  AS Adhérent
       ,Emprunt.exemplaire                                              AS Exemplaire
       ,Emprunt.retard                                                  AS Retard
       ,Emprunt.date_rendu + (Emprunt.date_rendu - Emprunt.date_retour) AS DateDeFin
       ,DATE(NOW())                                                     AS DateDuJour
FROM Emprunt
JOIN Adherent
ON Emprunt.adherent = Adherent.login
WHERE retard = 1; UPDATE Retard

SET fin = '1'
WHERE Retard.id = 1; 