# Bloc 2 : WORKFLOW & FONDATIONS
joueur = {
    "nom": "Arthur", 
    "pv" : 100,
    "attaque" : 50,
    "defense" : 20,
    "XP" : 0,
    "inventaire":[]
    
}
monstre = {
    "nom" : "Ogre",
    "pv" : 50,
    "attaque" : 10,
    "defense" : 5
}
boss ={
  "nom" : "Seigneur des Ogres",
    "pv" : 300,
    "attaque" : 60,
    "defense" : 40
}
import random

# Bloc 3 : ARCHITECTURE POO
class Personnage:
 def __init__(self, nom, pv_max, attaque, defense):
    self._nom = nom
    self._pv = pv_max
    self._pv_max = pv_max
    self._attaque = attaque
    self._defense = defense
def afficher_stats(self):  
# Getters
 def get_nom(self): return self._nom
def get_pv(self): return self._pv
def get_attaque(self): return self._attaque
def get_defense(self): return self._defense

# Setters
def set_pv(self, valeur):
    if valeur <= 0:
       self._pv = 0
    elif valeur > self._pv_max:
         self._pv = self._pv
    else:
         self._pv > 0      

# MODULARITE
def attaquer (self,cible):
      degats = self.attaque + random.randint(-2, 2)
      degats_finaux = degats - cible.get_defense()
      if degats_finaux < 0:
        degats_finaux = 0
      print(f"{self.nom} attaque {cible.nom} et lui inflige {degats_finaux} dégâts")
      cible.subir_degats(degats_finaux)
def subir_degats(self, degats):
          self.set_pv(self._pv - degats)
          if not self.est_vivant():
             print(f"{self.nom} est vaincu ")
          else:   
            print(f"{self._pv_max} PV")  
def afficher_stats(self):
        barre = "#" * int(self._pv / self._pv_max * 20 )   
        print(f"{self._nom:10} : {self.pv:3}/ {self._pv_max} PV [{barre:20}]")       
class Joueur(Personnage):
  def __init__(self, nom, pv_max, attaque, defense):
    super().__init__(nom, pv_max, attaque, defense)
    self.experience = 0
    self.inventaire = []
  def afficher_stats(self):
    print(f" XP: {self.experience} | Inv: {self.inventaire}")

class Monstre(Personnage):
  def __init__(self, nom, pv_max, attaque, defense):
    super().__init__(nom, pv_max, attaque, defense)
  def afficher_stats(self):
   print(f"PV:{self._pv}")
   
class Boss(Monstre): 
  def __init__(self, nom, pv_max, attaque, defense, cri_de_guerre):
    super().__init__(nom, pv_max, attaque, defense)
    self._cri = cri_de_guerre
    self.est_final = True
  def attaquer(self, cible):
    if random.random() < 0.2:
      print(f"{self._nom.upper()} CRI : {self._cri}")
      original_attaque = self._attaque = 1.5
      self._attaque *= 1.5
      super().attaquer(cible)
      self._attaque = original_attaque
    else:
      super().attaquer(cible) 
      
Arthur=Joueur("Arthur", 100, 50, 20)
Ogre=Monstre("Ogre", 50, 10, 5)
Seigneur_des_Ogres=Boss("Seigneur des Ogres", 300, 60, 40, "ARGH")
print(" TEST DE L'ARCHITECTURE")
Arthur.afficher_stats()
Seigneur_des_Ogres.afficher_stats()
print("\n Résultat final")
Arthur.afficher_stats()







      
      