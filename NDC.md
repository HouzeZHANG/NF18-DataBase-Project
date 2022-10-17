# NDC - sujet Bibliothèque



**Ressource** (classe mère abstraite) : code (clé), titre, date d’apparition, éditeur, genre, code de classification
→ est disponible en 1 Exemplaire (1 - *)
→ est classe mère de Oeuvre musicale, Film et Livre


**Livre** : ISBN, résumé, langue
→ classe fille exclusive de Ressource

**Film** : langue, longueur, synopsis
→ classe fille exclusive de Ressource

**Oeuvre musicale** : longueur
→ classe fille exclusive de Ressource


**Contributeur** : nom, prénom, date de naissance, nationalité
→ chaque contributeur ne contribue pas forcément à chaque type de ressources et chaque ressource a au moins 1 contributeur (*—1..n) 

**Membre_personnel** : compte utilisateur login, compte utilisateur mdp, nom, prénom, date de naissance, rue, ville, code postal, adresse mail

**Adhérent** : compte utilisateur login, compte utilisateur mdp, nom, prénom, date de naissance, rue, ville, code postal, adresse mail, téléphone
→ emprunte une ou plusieurs ressources (association n — n) ATTENTION nombre limité et pour une durée limitée
→ pour tenir compte des adhérences passées : on ajoute un booléen « actif » qui permet de dire au système s’il est encore adhérent et permet ainsi de ne pas le supprimer de la base de données
→  pour interdire les emprunts, on choisit de mettre un autre booléen « droit_emprunt » 

**Prêt** : date_prêt, durée_prêt
⇒ classe association entre adhérent et exemplaire

**Exemplaire** : état
→ l’exemplaire peut être neuf, en bon état, abîmé ou perdu

Contraintes :
- document ne peut être emprunté que si disponible et au minimum en bon état
- adhérent ne peut emprunter qu’un nombre limité de documents 
- sanctions si retour en retard ⇒ suspension du même nombre de jour que le retard (booléen droit_emprunt)
- sanctions si perte ou dégradation grave ⇒ suspension tant que le document n’est pas remboursé (booléen droit_emprunt)
- possibilité de blacklister adhérents en cas de sanctions répétées (booléen actif)
