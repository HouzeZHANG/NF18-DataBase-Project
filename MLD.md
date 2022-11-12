# 1. Justification choix des transformations des héritages 

## Ressource - OeuvreMusicale|Film|Livre : 
- Cet héritage sera explicité dans le modèle relationnel comme un héritage par les classes filles car c'est un héritage exclusif. 
- Ainsi, chaque classe fille héritera de la classe mère la clé et ses attributs. 
- Les clés primaires des classes filles ne sont donc pas retenues comme clé primaire.

## Sanction - Retard|Détérioration : 
- Cet héritage sera explicité dans le modèle relationnel comme un héritage par les classes filles car c'est un héritage exclusif. 
- Ainsi, chaque classe fille héritera de la classe mère la clé et ses attributs. 
- Les clés primaires des classes filles ne sont donc pas retenues comme clé primaire.

# 2. Classes

## Adherent
Adherent(#login: varchar, mdp:varchar, nom: varchar, prenom: varchar, date_naissance: date, code_postal: varchar, adresse_rue: varchar, ville: varchar, adresse_mail: varchar,num_tel: varchar, actif: bool, droit_emprunt: bool)
- avec mdp, nom, prenom, adresse_mail et num_tel NOT NULL

## MembrePersonnel
MembrePersonnel(#login:varchar, mdp:varchar, nom: varchar, prenom: varchar, code_postal: varchar, adresse_rue: varchar, ville: varchar, adresse_mail: varchar)
- avec mdp, nom, prenom, adresse_mail NOT NULL

## Exemplaire
Exemplaire(#id: int, etat : {neuf, bon, abîmé, perdu}, disponible :  bool, code_oeuvre⇒OeuvreMusicale, code_film⇒Film, code_livre⇒Livre)
- clé artificielle id implémentée car chaque exemplaire est unique et on va utiliser cette clé pour la classe emprunt
- code_oeuvre OR code_film OR code_livre (dû à la transformation d’héritage par classes filles)

## Contributeur
Contributeur(#nom: varchar, #prenom: varchar, date_naissance: date, nationalite: varchar)
- avec nom, prenom clé

# 3. Classes issues des association

## Emprunt
Emprunt(#id : int, exemplaire⇒Exemplaire, date_pret: date, date_retour : date, date_rendu: date, personnel⇒ MembrePersonnel, retard⇒Retard, deterioration⇒Deterioration)
- date_pret, date_retour NOT NULL
- id clé artificielle
- date_rendu et date_retour>date_pret
- deterioration OR retard

## Emprunter
Emprunter(#adherent⇒Adherent, #emprunt⇒Emprunt)

- Contraintes:
Projection(Emprunt, id) = Projection(Emprunter, emprunt)
- En général, une entrée de la table d'emprunt correspond à un enregistrement emprunteur, mais tous les enregistrements adhérents ne correspondent pas à des enregistrements emprunteurs.

## Composer
Composer(#contrib⇒Contributeur, #code⇒OeuvreMusicale)

## Interpréter
Interpréter(#contrib⇒Contributeur, #code⇒OeuvreMusicale.code)

## Réaliser
Réaliser(#contrib⇒Contributeur, #code⇒Film.code)

## Acteur
Acteur(#contrib⇒Contributeur, #code⇒Film.code)

## Auteur
Auteur(#contrib⇒Contributeur, #code⇒Livre.code)

# 4. Transformations d’héritage

## Ressource
Ressourse - transformation par classes filles

## OeuvreMusicale
OeuvreMusicale(#code: varchar, titre: varchar, date_apparition: date, editeur: varchar, genre : varchar, code_classification : varchar, longueur : time)
- titre, genre, code_classification NOT NULL

## Film
Film(#code: varchar, titre: varchar, date_apparition: date, editeur: varchar, genre : varchar, code_classification : varchar, longueur : time, synopsis : varchar)
- titre, genre, code_classification NOT NULL

## Livre
Livre(#code: varchar, titre: varchar, date_apparition: date, editeur: varchar, genre : varchar, code_classification : varchar, ISBN : varchar, resume : varchar, langue : varchar)
- titre, genre, code_classification NOT NULL
- ISBN unique NOT NULL

Contraintes:
INTERSECTION(Projection(OeuvreMusicale, code), Projection(Film, code)) UNION 
INTERSECTION(Projection(Film, code), Projection(Livre, code)) UNION
INTERSECTION(Projection(Livre, code), Projection(OeuvreMusicale, code)) UNION = {}

# Sanction - transformation par classes filles

## Retard
Retard(#id : int, personnel⇒MembrePersonnel, fin : bool)
- fin : méthode

## Deterioration
Deterioration(#id : int, remboursement : bool, personnel⇒MembrePersonnel)
