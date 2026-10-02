import getpass
from auth import creer_utilisateur

nom = input("Nom d'utilisateur: ")
mdp = getpass.getpass("Mot de passe (ma yبانش fil ecran): ")
creer_utilisateur(nom, mdp)
print("Utilisateur cree:", nom)