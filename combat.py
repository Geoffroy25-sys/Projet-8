# Bloc 3: ARCHITECTURE POO
def tour_de_combat(attaquant, defenseur, log_fn=print):
    """ Un tour complet: l'attaquant attaque, le défenseur tente de parer.
    - Si le defenseur pare → contre-attaque avec bonus
    - Sinon → il subit les dégâts normalement
    Retourne les dégâts infligés."""
    import random
    
    if defenseur.tenter_parade():
        log_fn(f"{defenseur.get_nom()} pare l'attaque de {attaquant.get_nom()}")
        degats_contre = int(defenseur.get_attaque()* 1.3) + random.randint(-2, 2)
        degats_contre = max(0, degats_contre - attaquant.get_defense())
        log_fn(f"{defenseur.get_nom()} contre-attaque → {degats_contre} degats")
        attaquant.subir_degats(degats_contre)
        return 0
    else:
        if not defenseur.est_vivant():
            return 0
        degats = attaquant.attaquer(defenseur)
        return degats
def combat(joueur, monstre, log_fn=print):
    """ Boucle de combat entre joueur et monstre.
    Les deux s'attaquent en alternance jusqu'à ce que l'un tombe.
    Retourne: 
        True si le joueur a gagné
        False si le joueur est mort """ 
    log_fn(f"\n{'='*40}")
    log_fn(f"Combat{joueur.get_nom()} vs {monstre.get_nom()}")
    log_fn(f"{'='*40}")

    while joueur.est_vivant() and monstre.est_vivant():
        log_fn(f"\n [Tour de {joueur.get_nom()}]")
        tour_de_combat(joueur, monstre, log_fn)

        if not monstre.est_vivant():
            break

        log_fn(f"\n [Tour de {monstre.get_nom}]") 
        tour_de_combat(monstre, joueur, log_fn)

    if joueur.est_vivant():
       xp = monstre.get_xp_recompense()
       joueur.gagner_xp(xp)
       log_fn(f"{joueur.get_nom()} remporte le combat (+{xp} XP)")
       return True
    else:
        log_fn(f"{joueur.get.nom()} est mort")
        log_fn("YOU DIED")
        return False

if __name__ == "__main__":
    from personnages import Joueur, Monstre
    Arthur = Joueur("Arthur", 100, 50, 20)
    Ogre = Monstre("Ogre", 50, 10, 5, 100)
    print("Combat")
    resultat = combat(Arthur, Ogre)
    print(f"\nArthur a gagné : {resultat}")
    Arthur.afficher_stats()

             
    