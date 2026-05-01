#Bloc 4: PERSISTANCE
import json
import os

Sauvegarde = "sauvegarde.json"
def sauvegarder (Joueur, log_fn = print):
    "Sauvegarde l'état du joueur"
    données = {
        "nom":          Joueur.get_nom(),
        "pv":           Joueur.get_pv(),
        "pv_max":       Joueur.get_pv_max(),
        "attaque":      Joueur.get_attaque(),
        "defense":      Joueur.get_defense(),
        "XP":           Joueur.get_xp(),
        "level_up":     Joueur.get_level_up(),
        "inventaire":   Joueur.get_inventaire(),
        "potion_soin":  Joueur.get_potion_soin(),
        "zone":         Joueur.get_zone_actuelle()
    }
    with open(Sauvegarde, "w", encoding="utf-8") as f:
        json.dump(données, f, ensure_ascii=False, indent=4)
    log_fn("Partie sauvegardée au feu de camp")
def sauvegarder_avant_boss(joueur, nom_boss, log_fn=print):
    "Sauvegarde automatique avant un combat de boss"
    log_fn(f"Sauvegarde automatique avant {nom_boss}")
    sauvegarder(joueur, log_fn)

def charger(Classe_Joueur, log_fn=print):
    "Charge et retourne le joueur depuis la dernière sauvegarde"
    if not os.path.exists(Sauvegarde):
        log_fn("Aucune sauvegarde trouvée")
        return None
    with open(Sauvegarde, "r", encoding="utf-8") as f:
        données=json.load(f)
    joueur=Classe_Joueur(
        données["nom"],
        données["pv_max"],
        données["attaque"],
        données["defense"],
        données.get("potion_soin", 3)
    )
    joueur.set_pv(données["pv"])
    joueur._inventaire = données["inventaire"]
    joueur._xp = données["XP"]
    joueur.set_zone_actuelle(données.get("zone", 1))
    log_fn(f"Partie chargée, {joueur.get_nom()} (Zone {joueur.get_zone_actuelle()})")
    return joueur

if __name__=="__main__":
    from personnages import Joueur

    Arthur = Joueur("Arthur", 100, 50, 20)
    Arthur.gagner_xp(100)
    Arthur.ajouter_item("Epée")

    print ("Bloc 4: Persistance")
    sauvegarder(Arthur)
    Arthur2 = charger(Joueur)
    Arthur2.afficher_stats
    os.remove(Sauvegarde)