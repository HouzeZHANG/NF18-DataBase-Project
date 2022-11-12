# NDC - sujet Bibliothèque

**Préambule**


**Client :** M. Alessandro Victorino 

**Livrables :**

→ README (avec le sujet du projet et les noms des membres du groupe) lors de la création du Gitlab du projet

→ NDC + première version du MCD : date du TD de la semaine 7 + 2 jours avant 23h59

→ MCD corrigé + première version du MLD : date du TD de la semaine 9 + 2 jours avant 23h59

→ MLD corrigé + SQL (CREATE et INSERT) : date du TD de la semaine 10 + 2 jours avant 23h59

→ SQL (SELECT, GROUP BY) +première applic. python : date du TD de la semaine 11 + 2 jours avant 23h59

→ Application python finalisée : date du TD de la semaine 15 + 2 jours avant 23h59

→ NoSQL R-JSON : date du TD de la semaine 17 + 2 jours avant 23h59




**Liste des objets, associations et contraintes**  


**Ressource** : code {key}, titre (NOT NULL), date d’apparition, éditeur, genre (NOT NULL), code de classification (NOT NULL)  
 
→ est disponible en un ou plusieurs Exemplaire (1 - 1...n)
 
→ est classe mère de Oeuvre musicale, Film et Livre
 
 
**Livre** : ISBN {key}, résumé, langue
 
→ classe fille exclusive de Ressource
 
 
**Film** : langue, longueur, synopsis
 
→ classe fille exclusive de Ressource
 
 
**OeuvreMusicale** : longueur
 
→ classe fille exclusive de Ressource  

 
→ Cet héritage sera explicité dans le modèle relationnel comme un héritage par les classes filles car c'est un héritage exclusif. Ainsi, chaque classe fille héritera de la classe mère la clé et ses attributs. Les clés primaires des classes filles ne sont donc pas retenues comme clé primaire.
 
 
 
**Contributeur** : nom (NOT NULL), prénom (NOT NULL), date de naissance, nationalité
 
→ compose une OeuvreMusicale(1..n - 0...n)
 
→ interprète une OeuvreMusicale(1..n - 0...n)
 
→ réalise un Film(1..n - 0...n)
 
→ est acteur d'un Film(1..n - 0...n)
 
→ est auteur d'un Livre(1...n - 0...n)
 
→ un Contributeur contribue au moins une fois et il peut contribuer sur plusieurs Ressources et plusieurs fois dans des rôles différents sur une même Ressource.
 
 
 
**Membre du personnel** : compte utilisateur login {key}, compte utilisateur mdp (NOT NULL), nom (NOT NULL), prénom (NOT NULL), rue, ville, code postal, adresse mail (NOT NULL)
 
→ gère les Emprunts (1 - 0...n) 
 
→ gère les Sanctions (1 - 0...n)
 
 
 
**Sanction** :
 
→ peut être associée à un ou plusieurs Emprunts (0...1 - 0...n)  

→ est classe mère de Retard et Détérioration
 
 
**Retard** :  fin (0 ou 1)
 
→ classe fille exclusive de Sanction
 
→ Méthode : fin = date du jour < date de rendu + (date de rendu - date de retour), date de rendu, date de retour et date de rendu proviennent de la classe Emprunt.
 
 
 
**Détérioration** : remboursement (0 ou 1)
 
→ classe fille exclusive de Sanction
 
→ remboursement est un booléen qui indique si l'Exemplaire a été remboursé  

 
→ Cet héritage sera explicité dans le modèle relationnel comme un héritage par les classes filles car c'est un héritage exclusif. Ainsi, chaque classe fille héritera de la classe mère la clé et ses attributs. Les clés primaires des classes filles ne sont donc pas retenues comme clé primaire.
 
 
**Adhérent** : compte utilisateur login {key}, compte utilisateur mdp (NOT NULL), nom (NOT NULL), prénom (NOT NULL), date de naissance, rue, ville, code postal, adresse mail (NOT NULL), téléphone (NOT NULL), droit à l'emprunt (0 ou 1), actif (0 ou 1)
 
→ peut effectuer un ou plusieurs Emprunts (1 — 0...n)
 
→ le nombre d'emprunts est limité et il est calculé dans une requête à l'aide de la classe Emprunt, cela apparaîtra dans l'application.
 
→ pour tenir compte des adhérences passées : on ajoute un booléen « actif » qui permet de dire au système s’il est encore adhérent (1) et permet ainsi de ne pas le supprimer de la base de données. Si actif vaut 0, cela signifie que soit l'Adhérent est inactif soit l'Adhérent est blacklisté.
 
→ pour interdire les emprunts, on choisit de mettre un autre booléen « droit_emprunt ». Si cet Adhérent est associé à une Sanction de valeur 1, alors droit d'emprunt prendra la valeur 0. De même, si l’Adhérent a atteint sa limite d’Emprunts, droit d’emprunt prendra la valeur 0.
 
 
 
**Emprunt** : date de prêt (NOT NULL), date de retour (NOT NULL), date de rendu (> date de prêt)
 
 
→ la date de prêt peut être ultérieure à la date du jour en cas de réservation
 
→ la date de retour est la date à laquelle l'Exemplaire doit être rendu
 
→ la date de rendu est la date à laquelle l'Exemplaire a été rendu
 
 
 
 
**Exemplaire** : état(NOT NULL), disponible (0 ou 1)
 
→ appartient à une Ressource (1...n - 1)
 
→ peut être dans un ou plusieurs Emprunt (1 - 0...n)
 
→ l’exemplaire peut être neuf, en bon état, abîmé ou perdu
 
→ disponible est un booléen
 
 
 
 
**Description des utilisateurs**
 
 
Les administrateurs de la base de données, qui sont les Membres du personnel , gèrent les emprunts, les sanctions, ajoutent des documents, des exemplaires, modifient des descriptions. Les utilisateurs, qui sont les Adhérents, peuvent avoir acccès à leurs données et aux documents.
 
 
 
 
**Requêtes statistiques**
 
 
Il faut aussi être capable de fournir des statistiques sur les documents empruntés par les utilisateurs, pour que les administrateurs puissent établir la liste des documents populaires et étudier le profil des utilisateurs pour suggérer des documents.
