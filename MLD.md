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
- clé artificielle id implémentée car chaque exemplaire est unique et on va utiliser cette clé pour la classe Emprunt
- code_oeuvre OR code_film OR code_livre (dû à la transformation d’héritage par classes filles)

Contraintes :
- PROJECTION(Exemplaire, code_oeuvre) = PROJECTION(OeuvreMusicale, code) OR
- PROJECTION(Exemplaire, code_film) = PROJECTION(Film, code) OR
- PROJECTION(Exemplaire, code_livre) = PROJECTION(Livre, code)

## Contributeur
Contributeur(#nom: varchar, #prenom: varchar, date_naissance: date, nationalite: varchar)
- avec nom, prenom clé

# 3. Classes issues des association

## Emprunt
Emprunt(#exemplaire⇒Exemplaire, #date_pret: date, date_retour : date, date_rendu: date, personnel⇒ MembrePersonnel, retard⇒Retard, deterioration⇒Deterioration, adherent=>Adherent)
- (exemplaire,date_pret)  
- date_retour NOT NULL
- date_rendu et date_retour>date_pret
- deterioration OR retard
- adherent NOT NULL

Contraintes :
- PROJECTION(Emprunt, personnel) = PROJECTION(MembrePersonnel, login)
- PROJECTION(Emprunt, exemplaire) = PROJECTION(Exemplaire, id)
- PROJECTION(Emprunt, retard) = PROJECTION(Retard, id)
- PROJECTION(Emprunt, deterioration) = PROJECTION(Deterioration, id)

## Composer
Composer(#contrib⇒Contributeur, #code⇒OeuvreMusicale)
- avec (contrib, code) UNIQUE (déjà indiqué dans l'utilisation des clés ; pour obtenir un MLD explicite, cette précision a été rajoutée (un Contributeur ne compose qu'une seule fois une oeuvre))

## Interpréter
Interpréter(#contrib⇒Contributeur, #code⇒OeuvreMusicale.code)
- avec (contrib, code) UNIQUE

## Réaliser
Réaliser(#contrib⇒Contributeur, #code⇒Film.code)
- avec (contrib, code) UNIQUE

## Acteur
Acteur(#contrib⇒Contributeur, #code⇒Film.code)
- avec (contrib, code) UNIQUE

## Auteur
Auteur(#contrib⇒Contributeur, #code⇒Livre.code)
- avec (contrib, code) UNIQUE

Contraintes :
- INTERSECTION(Projection(Auteur, contrib), Projection(Acteur, contrib)) UNION INTERSECTION(Projection(Auteur, contrib), Projection(Réaliser, contrib)) UNION INTERSECTION(Projection(Auteur, contrib), Projection(Interpréter, contrib)) UNION INTERSECTION(Projection(Auteur, contrib), Projection(Composer, contrib)) UNION INTERSECTION(Projection(Acteur, contrib), Projection(Réaliser, contrib)) UNION INTERSECTION(Projection(Acteur, contrib), Projection(Interpréter, contrib)) UNION INTERSECTION(Projection(Acteur, contrib), Projection(Composer, contrib)) UNION INTERSECTION(Projection(Réaliser, contrib), Projection(Interpréter, contrib)) UNION INTERSECTION(Projection(Réaliser, contrib), Projection(Composer, contrib)) UNION INTERSECTION(Projection(Interpréter, contrib), Projection(Composer, contrib)) NULL OR NOT NULL, i.e. un contributeur peut contribuer plusieurs fois sur une même oeuvre avec des actions différentes.

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
- INTERSECTION(Projection(OeuvreMusicale, code), Projection(Film, code)) UNION INTERSECTION(Projection(Film, code), Projection(Livre, code)) UNION INTERSECTION(Projection(Livre, code), Projection(OeuvreMusicale, code)) UNION = {}

# Sanction - transformation par classes filles

## Retard
Retard(#id : int, personnel⇒MembrePersonnel, fin : bool)
- fin : méthode

## Deterioration
Deterioration(#id : int, remboursement : bool, personnel⇒MembrePersonnel)

Contraintes :
- INTERSECTION (PROJECTION(Retard, id), PROJECTION(Deterioration, id)) = {}
- PROJECTION(Retard, personnel) = PROJECTION(MembrePersonnel, login)
- PROJECTION(Deterioration, personnel) = PROJECTION(MembrePersonnel, login)
