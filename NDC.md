NDC - sujet Bibliothèque
Ressource (classe mère abstraite) : code (clé), titre, date d’apparition, éditeur, genre, code_classification
→ comporte plusieurs Contributeurs (* — 1..n)

Classes filles de Ressource =
Livre : ISBN, résumé, langue
Film : langue, longueur, synopsis
Oeuvre musicale : longueur
→ ce sont des classes filles de Ressources

Exemplaire : état
→ appartient à une Ressource (association * — 1)

Contributeur : nom, prénom, date_naissance, nationalité, type_contrib ?
⇒ Comment gérer le fait qu’on ait soit ?
livre = auteur
film = acteur, réalisateur
oeuvre musicale = compositeur, interprète
Personne : compte_utilisateur_login, compte utilisateur_mdp, nom, prénom, date_naissance, rue, ville, code_postal, adresse_mail, num_tel
Membre_personnel : 
Adhérent :  carte_adherent
→ empruntent un ou plusieurs exemplaires d’une oeuvre (association n — m) ATTENTION nb limité et pour une durée limitée
ATTENTION on doit aussi tenir compte des adhérences passées

Prêt : date_prêt, durée_prêt
⇒ classe association entre adhérent et exemplaire ?
Contraintes :
code ressource unique
document ne peut être emprunté que si disponible + bon état
adhérent ne peut emprunter qu’un nb limité de documents + durée limitée
sanctions si retour en retard ⇒ suspension du même nombre de jour que le retard
sanctions si perte ou dégradation grave ⇒ suspension tant que le document n’est pas remboursé
ressources disponibles en plusieurs exemplaires, avec un état
possibilité de blacklister adhérents en cas de sanctions répétées

Remarques :
Faut-il décomposer adresse en code postal + ville + rue comme on avait fait en td une fois ? Oui
ATTENTION gestion adhérences passées et actuelles (concerne le prêt je pense)
