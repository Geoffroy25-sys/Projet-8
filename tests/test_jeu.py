# Bloc 5: Qualité

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from personnages import Joueur, Monstre, Boss
from exceptions import CibleDejaMorteErreur, InventairePleinErreur

def test_set_pv_negatif():
    Arthur = Joueur("Arthur", 100, 50, 20)
    Arthur.set_pv(-10)
    assert Arthur.get_pv() == 0

def test_set_pv_trop_haut():
    Arthur = Joueur("Arthur", 100, 50, 20)
    Arthur.set_pv(9999)
    assert Arthur.get_pv() == 100

def test_est_vivant():
    Arthur = Joueur("Arthur", 100, 50, 20)
    assert Arthur.est_vivant() == True
    Arthur.set_pv(0)
    assert Arthur.est_vivant() == False

def test_gagner_xp():
    Arthur = Joueur("Arthur", 100, 50, 20)
    Arthur.gagner_xp(100)
    assert Arthur.get_xp() == 100
    
def test_joueur_inventaire():
    Arthur = Joueur("Arthur", 100, 50, 20)
    Arthur.ajouter_item("Epée")
    assert "Epée" in Arthur.get_inventaire()

def test_attaquer_cible_morte():
    Arthur = Joueur("Arthur", 100, 50, 20)
    Ogre = Monstre("Ogre", 50, 10, 5)
    Ogre.set_pv(0)
    with pytest.raises(CibleDejaMorteErreur):
        Arthur.attaquer(Ogre)

def test_degâts_jamais_negatifs():
    Arthur = Joueur("Arthur", 100, 1, 20)
    Ogre = Monstre("Ogre", 50, 10, 999)
    degâts = Arthur.attaquer(Ogre)
    assert degâts >= 0        