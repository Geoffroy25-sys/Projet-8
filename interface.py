# Bloc 6: Interface graphique
import tkinter as tk
from tkinter import scrolledtext, messagebox
import copy
import random

from personnages import Joueur, Monstre, Boss
from persistance import sauvegarder, sauvegarder_avant_boss, charger
from combat import tour_de_combat 
from zones import creer_zones
BG = "#1a1a1a"
BG_PANEL = "#222222"
OR = "#c9a84c"
ROUGE = "#8b0000"
BLANC = "#e8e8e8"
GRIS = "#555555"
VERT = "#2e6b2e"
POLICE = ("Courier New", 10)
POLICE_T = ("Courier New", 12, "bold")

class jeu_RPG(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("RPG-Projet 8")
        self.configure(bg = BG)
        self.resizable(False, False)
        self.Arthur = Joueur("Arthur", 100, 50, 20, nb_potion_soin=5)
        self._zones = creer_zones()
        self._idx_zones = 0
        self._idx_monstre = 0
        self._phase = "monstres"
        self._monstre_actuel = self._zones[0]["monstres"][0]
        self._construire_ui()
        self._actualiser()
        self._log(f"Bienvenue dans {self._zones[0]['nom']}")
        self._log(self._zones[0]["description"])
        self._log(f"\n{self._monstre_actuel.get_nom()} apparaît ")


    def _construire_ui(self):
        tk.Label(self, text="DARK_SOULS_RPG", 
                 font= ("Courier New", 14, "bold"),
                 fg=OR, bg= BG).grid(row=0, column=0, columnspan=3, pady=10)
        self._lbl_zone = tk.Label(self, font=("Courier New", 10, "italic"), fg=GRIS, bg=BG)
        self._lbl_zone.grid (row=1,  column=0, columnspan=3)    
        f_Arthur = tk.Frame(self, bg=BG_PANEL, bd=1, relief="solid")
        f_Arthur.grid(row=2, column=0, padx=12, pady=8, sticky="n")
        tk.Label(f_Arthur, text="--Arthur--", font=POLICE_T, fg=OR, bg=BG_PANEL).pack(pady=5)
        self._lbl_pv_a = tk.Label(f_Arthur, font=POLICE, fg=BLANC, bg=BG_PANEL)
        self._lbl_pv_a.pack()
        self._canvas_a = tk.Canvas(f_Arthur, width=160, height=14, bg=ROUGE, highlightthickness=0)
        self._canvas_a.pack(pady=2)
        self._barre_a = self._canvas_a.create_rectangle(0, 0, 160, 14, fill=VERT, width=0)
        self._lbl_xp_a = tk.Label(f_Arthur, font=POLICE, fg=OR, bg=BG_PANEL)
        self._lbl_xp_a.pack()
        self._lbl_est_a = tk.Label(f_Arthur, font=POLICE, fg=BLANC, bg=BG_PANEL)
        self._lbl_est_a.pack()
        self._lbl_inv_a = tk.Label(f_Arthur, font=("Courier New", 8), fg=GRIS, bg=BG_PANEL, wraplength=150)
        self._lbl_inv_a.pack(pady=(2, 8), padx=6)

        f_journal = tk.Frame(self, bg=BG)
        f_journal.grid(row=2, column=1, pady=8)
        tk.Label(f_journal, text="COMBAT", font=POLICE_T, fg=OR, bg=BG).pack()
        self._journal = scrolledtext.ScrolledText(
            f_journal, width=36, height=16, bg="#111111", fg=BLANC, font=POLICE, state="disabled", wrap="word", bd=1, relief="solid"
        )
        self._journal.pack()

        f_monstre = tk.Frame(self, bg=BG_PANEL, bd=1, relief="solid")
        f_monstre.grid(row=2, column=2, padx=12, pady=8, sticky="n")
        tk.Label(f_monstre, text="- MONSTRE-", font=POLICE_T, fg=ROUGE, bg=BG_PANEL).pack(pady=5)
        self._lbl_nom_e = tk.Label(f_monstre, font=POLICE, fg= BLANC, bg=BG_PANEL)
        self._lbl_nom_e.pack()
        self._canvas_e = tk.Canvas(f_monstre, width=160, height=14, bg="#3a0000", highlightthickness=0)
        self._canvas_e.pack(pady=2)
        self._barre_e = self._canvas_e.create_rectangle(0, 0, 160, 14, fill=ROUGE, width=0)
        self._lbl_pv_e = tk.Label(f_monstre, font=POLICE, fg=BLANC, bg=BG_PANEL)
        self._lbl_pv_e.pack(pady=(0, 8))

        f_btn=tk.Frame(self, bg=BG)
        f_btn.grid(row=3, column=0, columnspan=3, pady=10)
        boutons = [
           ("Attaquer", self._attaquer, OR),
           ("Potion", self._potion_soin, "#b56a00"),
           ("Sauvegarder", self._sauvegarder, GRIS),
           ("Charger", self._charger, GRIS),
           ("Recommencer", self._recommencer, ROUGE),

        ]
        for texte, cmd, couleur in boutons:
            tk.Button(f_btn, text=texte, command=cmd,
                      bg=couleur, fg=BG, font=POLICE,
                      relief="flat", padx=10, pady=5, 
                      cursor="hand2").pack(side="left",padx=5)
    def _actualiser(self):
        a = self.Arthur
        e = self._monstre_actuel
        zone = self._zones[self._idx_zones]        

        phase = "BOSS" if self._phase == "boss" else f"Monstre {self._idx_monstre + 1}/{len(zone['monstres'])}"
        self._lbl_zone.config(text=f"Zone{self._idx_zones + 1} : {zone['nom']} - {phase}")

        ratio_a = a.get_pv() / a.get_pv_max()
        self._canvas_a.coords( self._barre_a, 0, 0, int(160 * ratio_a), 14)
        self._lbl_pv_a.config(text=f"PV : {a.get_pv()} / {a.get_pv_max()}")
        self._lbl_xp_a.config(text=f"XP : {a.get_xp()}")
        self._lbl_est_a.config(text=f"Potion : {a.get_potion_soin()}")
        inv = a.get_inventaire()
        inv_str = ",".join(f"{obj}(*{qte})" for obj, qte in inv.items())
        self._lbl_inv_a.config(text="Inv : " + inv_str)

        ratio_e = e.get_pv() / e.get_pv_max()
        self._canvas_e.coords( self._barre_e, 0, 0, int(160 * ratio_e), 14)
        prefix = "Boss" if isinstance(e, Boss) else ""
        self._lbl_nom_e.config(text=prefix + e.get_nom())
        self._lbl_pv_e.config(text=f"pv : {e.get_pv()}/{e.get_pv_max()}")
        
    def _attaquer(self):
            Joueur = self.Arthur
            Monstre = self._monstre_actuel
            self._log(f"[tour d'Arthur]")
            tour_de_combat(Joueur, Monstre,self._log)
            if not Monstre.est_vivant():
                xp = Monstre.get_xp_recompense()
                level_avant = self.Arthur.get_level_up()
                Joueur.gagner_xp(xp)
                self._log(f"{Monstre.get_nom()} vaincu + {xp} XP ")
                if self.Arthur.get_level_up() > level_avant:
                    self._log(f"LEVEL UP ! Level {self.Arthur.get_level_up()}")
                    self._log(f"PV: {self.Arthur.get_pv_max()} ATK: {self.Arthur.get_attaque()} DEF: {self.Arthur.get_defense()}")
                self._actualiser()
                self._apres_victoire(Monstre)
                return
            self._log(f"\n[Tour de {Monstre.get_nom()}]")
            tour_de_combat(Monstre, Joueur, self._log)
            if not Joueur.est_vivant():
                self._log("\nTu es mort")
                self._mourir()
                return
            self._actualiser()

    def _apres_victoire(self, monstre_vaincu):
         """Gère la progression après une victoire."""
         zones = self._zones[self._idx_zones]
         if isinstance(monstre_vaincu, Boss):
            recompense = zones["recompense_boss"]
            self.Arthur.ajouter_item(recompense)
            self._log(f"Objet obtenu : {recompense} ")

            for item in zones.get("loot_boss", []):
                self.Arthur.ajouter_item(item["nom"], item["quantite"])
                self._log(f"+ {item['nom']} * {item['quantite']}")

            if monstre_vaincu.get_est_boss_final():
                self._log("\nVictoire finale")
                self._log("Le Seigneur des Ogres est vaincu")
                self._log("Arthur a sauvé le royaume")
                messagebox.showinfo("Victoire", "Félicitations\n Arthur a vaincu tous les boss")
                return
            self._idx_zones += 1
            self._idx_monstre = 0
            self._phase = "monstres"
            self._zones = creer_zones()
            nouvelle_zone = self._zones[self._idx_zones]
            self.Arthur.set_zone_actuelle(self._idx_zones + 1)
            self._monstre_actuel = nouvelle_zone["monstres"][0]
            self._log(f"\n{'=' * 40}")
            self._log(f"nouvelle zone : {nouvelle_zone['nom']}")
            self._log(nouvelle_zone["description"])
            self._log(f"{self._monstre_actuel.get_nom()} apparaît")
         else:
            self._idx_monstre +=1
            monstres=zones["monstres"]

            if random.random() < 0.3:
                loot_dispo = zones.get ("loot_chemin", [])
                if loot_dispo:
                    item = random.choice(loot_dispo)
                    self.Arthur.ajouter_item(item["nom"], item["quantite"])
                    self._log(f"Coffre trouvé + {item['nom']} * {item['quantite']}")
            if self._idx_monstre<len(monstres):
                self._monstre_actuel=monstres[self._idx_monstre]
                self._log(f"\n{self._monstre_actuel.get_nom()}apparaît")
            else :
                self._phase="boss"
                boss=zones["boss"]
                self._monstre_actuel=boss
                sauvegarder_avant_boss(self.Arthur,boss.get_nom(),self._log)
                self._log(f"\n{'='*40}")
                self._log(f"BOSS:{boss.get_nom()}")
                self._log(f"BOSS{boss.get_cri()}")
            
         self._actualiser()
    def _mourir(self):
        """Arthur est mort → recharge la dernière sauvegarde"""
        rep=messagebox.askretrycancel(
            "YOU DIED",
            "Arthur est mort \n Retry=reprendre sepuis la dernière sauvegarde \n cancel=quitter"

        )
        if rep:
            Joueur=charger(Joueur,self._log)
            if Joueur:
                self.Arthur = Joueur
                self._zones = creer_zones
                self._idx_zones = Joueur.get_zone_actuelle() - 1
                self._phase = "boss"
                self._monstre_actuel = self._zones[self._idx_zones]["boss"]
                self.Arthur.set_pv(self.Arthur.get_pv_max())
                self._log(f"\n Vous repartez du point de camp")
                self._log(f" {self._monstre_actuel.get_nom()} vous attend à nouveau")
                self._actualiser()
        else:
            self.destroy()    

    def _potion_soin(self):
        self.Arthur.utiliser_potion_soin()
        self._actualiser()        

    def _sauvegarder(self):
        sauvegarder(self.Arthur, self._log)   

    def _charger(self):
        Joueur = charger(Joueur, self._log)    
        if Joueur : 
            self.Arthur = Joueur
            self._zones = creer_zones()
            self._idx_zones = Joueur.get_zone_actuelle() - 1
            self._phase = "boss"
            self._monstre_actuel = self._zones[self._idx_zones]["boss"]
            self._actualiser()

    def _recommencer(self):
        if messagebox.askyesno("Recommencer", "Repartir depuis le début ?"):
            self.Arthur = Joueur("Arthur", 100, 50, 20, nb_potion_soin=5)        
            self._zones = creer_zones()
            self._idx_zones = 0
            self._idx_monstre = 0
            self._phase = "monstres"
            self._monstre_actuel = self._zones[0]["monstres"][0]
            self._journal.configure(state="normal")
            self._journal.delete("1.0", tk.END)
            self._journal.configure(state="disabled")
            self._log("Nouvelle partie\n")
            self._actualiser()

    def _log(self, texte):
            self._journal.configure(state="normal")     
            self._journal.insert(tk.END, texte + "\n")
            self._journal.see(tk.END)
            self._journal.configure(state="disabled")
    
            
         