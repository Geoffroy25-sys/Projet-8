# Bloc 5: Qualité
class JeuErreur(Exception):
    "Classe de base pour les erreurs du jeu"
    pass
class CibleDejaMorteErreur(JeuErreur):
    "Levée quand on attaque une cible déjà morte"
    pass
class InventairePleinErreur(JeuErreur):
    "Levée quand l'inventaire est plein"
    pass
class SauvegardeErreur(JeuErreur):
    "Levée quand la sauvegarde est absente ou corrompue"    
    pass   
if __name__ == "__main__":
    from personnages import Joueur, Monstre
    from exceptions import CibleDejaMorteErreur
    Arthur = Joueur("Arthur", 100, 50, 20)
    Ogre = Monstre("Ogre", 50, 10, 5)
    print("Exception")
    try:
        Ogre.set_pv(0)
        Arthur.attaquer(Ogre)
    except CibleDejaMorteErreur as e: 
        print(f"CibleDejaMorteErreur :{e}")    
    try:
        Arthur.utiliser_potion_soin()
        Arthur.utiliser_potion_soin()
        Arthur.utiliser_potion_soin()
        Arthur.utiliser_potion_soin()
    except Exception as e:
        print(f"Erreur potion soin :{e}") 