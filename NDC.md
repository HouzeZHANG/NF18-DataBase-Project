# NDC - sujet Bibliothèque

**Préambule**

**Client : **(Bibliothèque municipale), M. Alessandro Victorino 
**Livrables : **
→ README (avec le sujet du projet et les noms des membres du groupe) lors de la création du Gitlab du projet
→ NDC + première version du MCD : date du TD de la semaine 7 + 2 jours avant 23h59
→ MCD corrigé + première version du MLD : date du TD de la semaine 9 + 2 jours avant 23h59
→ MLD corrigé + SQL (CREATE et INSERT) : date du TD de la semaine 10 + 2 jours avant 23h59
→ SQL (SELECT, GROUP BY) +première applic. python : date du TD de la semaine 11 + 2 jours avant 23h59
→ Application python finalisée : date du TD de la semaine 15 + 2 jours avant 23h59
→ NoSQL R-JSON : date du TD de la semaine 17 + 2 jours avant 23h59


**Liste des objets, associations et contraintes**

**Ressource** (classe mère abstraite) : code (clé), titre, date d’apparition, éditeur, genre, code de classification
→ est disponible en 1 Exemplaire (1 - *)
→ est classe mère de Oeuvre musicale, Film et Livre

**Livre** : ISBN, résumé, langue
→ classe fille exclusive de Ressource

**Film** : langue, longueur, synopsis
→ classe fille exclusive de Ressource

**OeuvreMusicale** : longueur
→ classe fille exclusive de Ressource

**Contributeur** : nom, prénom, date de naissance, nationalité
→ compose une OeuvreMusicale(1..* - *)
→ interprète une OeuvreMusicale(1..* - *) 
→ réalise un Film(1..* - *) 
→ est acteur d'un Film(1..* - *) 
→ est auteur d'un Livre(1..* - *) 

**Membre du personnel** : compte utilisateur login, compte utilisateur mdp, nom, prénom, date de naissance, rue, ville, code postal, adresse mail
→ gère les Emprunts (* - *)
→ gère les Sanctions (* - *) 

**Sanction** : 
→ est associée à un ou plusieurs Emprunts (1 - *)

**Retard** : durée du retard
→ classe fille exclusive de Sanction

**Détérioration** : droit
→ classe fille exclusive de Sanction

**Adhérent** : compte utilisateur login, compte utilisateur mdp, nom, prénom, date de naissance, rue, ville, code postal, adresse mail, téléphone, droit à l'emprunt, actif, nombre d'emprunts
→ emprunte un ou plusieurs Exemplaire (* — *)
→ le nombre d'emprunts est limité
→ pour tenir compte des adhérences passées : on ajoute un booléen « actif » qui permet de dire au système s’il est encore adhérent et permet ainsi de ne pas le supprimer de la base de données
→ pour interdire les emprunts, on choisit de mettre un autre booléen « droit_emprunt » 

**Emprunt** : date de prêt, durée de prêt
⇒ classe d'association entre Adhérent et Exemplaire
→ la durée de prêt est limitée

**Exemplaire** : état, disponible
→ appartient à une Ressource (* - 1)
→ l’exemplaire peut être neuf, en bon état, abîmé ou perdu
→ disponible est un booléen


**Description des utilisateurs**

Les administrateurs de la base de données, qui sont les Membres du personnel , gèrent les emprunts, les sanctions, ajoutent des documents, des exemplaires, modifient des descriptions. Les utilisateurs, qui sont les Adhérents, peuvent avoir acccès à leurs données et aux documents.


**Requêtes statistiques**

Il faut aussi être capable de forunir des statistiques sur les documents empruntés par les utilisateurs, pour que les administrateurs puissent établir la liste des documents populaires et étudier le profil des utilisateurs pour suggérer des documents.
