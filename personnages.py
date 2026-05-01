# Bloc 3 : ARCHITECTURE POO
import random

class Personnage:
    def __init__(self, nom, pv_max, attaque, defense, chance_parade=0.15):
        self._nom = nom
        self._pv = pv_max
        self._pv_max = pv_max
        self._attaque = attaque
        self._defense = defense
        self._chance_parade = chance_parade
        
# Getters
    def get_nom(self):
        return self._nom
    def get_pv(self): 
        return self._pv
    def get_pv_max(self): 
        return self._pv_max
    def get_attaque(self):
        return self._attaque
    def get_defense(self):
        return self._defense
    def get_chance_parade(self): 
        return self._chance_parade

    # Setters
    def set_pv(self, valeur):
        if valeur <= 0:
         self._pv = 0
        elif valeur > self._pv_max:                                                             
            self._pv = self._pv_max        
        else:
         self._pv = valeur 

    def est_vivant(self) :
        return self._pv > 0
    
    def tenter_parade(self):
        "Retourne True si le personnage pare l'attaque."
        return random.random() < self._chance_parade
    
    # MODULARITE
    def attaquer(self,cible):
        from exceptions import CibleDejaMorteErreur
        if not cible.est_vivant(): 
            raise CibleDejaMorteErreur(f"{cible.get_nom()} est déjà morte ")
        degats = self._attaque + random.randint(-2, 2)
        degats_finaux = max(0, degats - cible.get_defense())
        print(f"{self._nom} attaque {cible.get_nom()} et lui inflige {degats_finaux} dégâts")
        cible.subir_degats(degats_finaux)
        return degats_finaux
        
    def subir_degats(self, degats):
            self.set_pv(self._pv - degats)
            if not self.est_vivant():
                print(f"{self._nom} est vaincu ")
            else:   
                print(f"{self._nom} : {self._pv}/{self._pv_max} PV")

    def afficher_stats(self):
        barre = "#" * int(self._pv / self._pv_max * 20 )   
        print(f"{self._nom:10} : {self._pv:3}/{self._pv_max} PV [{barre:20}]")    

class Joueur(Personnage):
    def __init__(self, nom, pv_max, attaque, defense, nb_potion_soin = 7):
        super().__init__(nom, pv_max, attaque, defense, chance_parade=0.20)
        self._xp = 0
        self._level_up = 0
        self._inventaire = {"potion_soin": nb_potion_soin}
        self._zone_actuelle = 1
        
  # Getters
    def get_xp(self): return self._xp
    def get_inventaire(self):  return self._inventaire
    def get_potion_soin(self): return self._inventaire.get("potion_soin", 0)
    def get_zone_actuelle(self): return self._zone_actuelle
    def get_level_up(self): return self._level_up

    #Setters
    def set_zone_actuelle(self, zone): 
        self._zone_actuelle = zone
    
    def gagner_xp(self, montant):
        self._xp += montant
        print(f"{self._nom} gagne {montant} XP (Total : {self._xp})")
        self._verifier_level_up()

    def _verifier_level_up(self):
        """Arthur monte de level tous les 500 XP"""    
        level = self._xp // 500
        if level > self._level_up:
            self._level_up = level
            self._pv_max += 10
            self._pv = self._pv_max
            self._attaque += 3
            self._defense += 2
            print(f"LEVEL UP ! Level {self._level_up} | PV:{self._pv_max} ATK:{self._attaque} DEF:{self._defense}")

    def ajouter_item(self, item, quantite = 1):
        "Ajoute un objet à l'inventaire. si déjà présent augmenter la qunatité."
        if item in self._inventaire:
            self._inventaire[item] += quantite
        else:
            self._inventaire[item] = quantite    
        print(f"Objet obtenu : {item}(*{self._inventaire[item]})")

    def utiliser_potion_soin(self):
            "Boit une potion_soin depuis l'inventaire pour récupérer des PV"
            if self.get_potion_soin() <= 0:
                print("Plus de potions de soins dans l'inventaire")
                return False
            soin = 80
            self._inventaire["potion_soin"] -= 1 
            self.set_pv(self._pv + soin)
            print(f"{self._nom} boit une potion de soin ( + {soin} PV) | Potions restantes : {self.get_potion_soin}")
            return True

    def afficher_stats(self):
        super().afficher_stats()
        inv_str = ", ".join(f"{obj}(*{qte})" for obj, qte in self._inventaire.items())
        print(f"XP: {self._xp} | Level: {self._level_up} | Inv: [{inv_str}]")
        print(f" XP: {self._xp} | Inv: [{inv_str}]")

class Monstre(Personnage):
    def __init__(self, nom, pv_max, attaque, defense, xp_recompense=200):
        super().__init__(nom, pv_max, attaque, defense, chance_parade=0.05)
        self._xp_recompense = xp_recompense 

    def get_xp_recompense(self): return self._xp_recompense

    def afficher_stats(self):
        barre = "#" * int(self._pv / self._pv_max * 20)
        print(f"{self._nom:10} : {self._pv:3}/{self._pv_max} PV [{barre:20}]")
   
class Boss(Monstre): 
    def __init__(self, nom, pv_max, attaque, defense, cri_de_guerre, xp_recompense:500, est_boss_final=False):
        super().__init__(nom, pv_max, attaque, defense, xp_recompense)
        self._cri = cri_de_guerre
        self.est_boss_final = est_boss_final

    def get_est_boss_final(self): return self.est_boss_final
    def get_cri(self): return self._cri    

    def attaquer(self, cible):
     if random.random() < 0.2:
       print(f"{self._nom.upper()} CRI : {self._cri}")
       original_attaque = self._attaque 
       self._attaque =int(self._attaque * 1.5)
       super().attaquer(cible)
       self._attaque = original_attaque
     else:
      super().attaquer(cible) 
    def afficher_stats(self):
        barre = "#" * int(self._pv / self._pv_max * 20)
        label = "BOSS FINAL" if self.est_boss_final else "BOSS"
        print(f"[{label}] {self._nom:10} : {self._pv:3} / {self._pv_max} PV [{barre:20}]") 
if __name__ == "__main__":
    Arthur = Joueur("Arthur", 100, 50, 20)
    Ogre = Monstre("Ogre", 50, 10, 5, 100)
    Seigneur_des_Ogres = Boss("Seigneur des Ogres", 300, 60, 40, "ARGH", 500)

    print("Test")
    Arthur.afficher_stats()
    Ogre.afficher_stats()
    Seigneur_des_Ogres.afficher_stats()

    print("Combat")
    while Ogre.est_vivant() and Arthur.est_vivant():
         Arthur.attaquer(Ogre)
         if Ogre.est_vivant():
             Ogre.attaquer(Arthur)

         if not Ogre.est_vivant():    
             Arthur.gagner_xp(Ogre.get_xp_recompense())

    Arthur.afficher_stats





      
      