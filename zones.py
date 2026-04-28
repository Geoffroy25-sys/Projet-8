# Bloc 3 : ARCHITECTURE POO
from personnages import Monstre, Boss

def creer_zones():
    "Retourne la liste de toutes les zones du jeu. CHaque zone contient des monstres et un boss."

    zones = [
        # Zone 1 
        {
            "nom": "Forêt des Ogres",
            "description": "Une forêt sombre peuplée d'Ogre sauvage",
            "monstres": [
                Monstre("Ogre", 50, 10, 5, xp_recompense=100),
                Monstre("Ogre", 50, 10, 5, xp_recompense=100),
                Monstre("Grand Ogre", 70, 15, 8, xp_recompense=300),
            ],    
            "boss": Boss(
                "Chef des Ogres", 250, 35, 15, "JE VAIS T'ECRASER", xp_recompense=1000, est_boss_final=False
            ),
            "recompense_boss": "Massue du chef"
        },
         # Zone 2 
        {
            "nom": "Cavernes Maudites",
            "description": "Des cavernes profondes où les Ogres se terrent",
            "monstres": [
                Monstre("Ogre Armé", 80, 18, 10, xp_recompense=200),
                Monstre("Ogre Armé", 80, 18, 10, xp_recompense=200),
                Monstre("Ogre Mage", 85, 22, 8, xp_recompense=400),
            ],    
            "boss": Boss(
                "Gardien des cavernes", 400, 50, 25, "PERSONNE NE PASSE", xp_recompense=2500, est_boss_final=False
            ),
            "recompense_boss": "Armure des Cavernes"
        }, 
         # Zone 3 
        {
            "nom": "Trône des Ogres",
            "description": "Le repaire du Seigneur des Ogres",
            "monstres": [
                Monstre("Garde Ogre", 100, 30, 15, xp_recompense=500),
                Monstre("Garde Ogre", 100, 30, 15, xp_recompense=500),
                Monstre("Ogre d'Elite", 90, 30, 12, xp_recompense=800),
            ],    
            "boss": Boss(
                "Seigneur des Ogres", 250, 35, 15, "ARGH", xp_recompense=5000, est_boss_final=True
            ),
            "recompense_boss": "Couronne du Seigneur"
        },
    ]