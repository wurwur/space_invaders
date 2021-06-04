## -*- coding: utf-8 -*-

import pygame
import time
from random import *

pygame.init()  # initialisation du module "pygame"

fenetre = pygame.display.set_mode((600, 600))  # Création d'une fenêtre graphique de taille 600x600 pixels
pygame.display.set_caption("Space Invader : Neowo's swag B)")  # Définit le titre de la fenêtre

## Chargement des images:
#    On définit et affecte les variables qui contiendront les images du vaisseau ou de l'alien
imageAlien = pygame.image.load("alien.png")
imageVaisseau = pygame.image.load("vaisseau.png")
imageVaisseau = pygame.transform.scale(imageVaisseau,(64, 64))  # On redimensionne l'image du vaisseau à une taille de 64x64 pixels
bomb = pygame.image.load("bomb.png")
star = pygame.image.load("star.png")
laser =  pygame.mixer.Sound('laser.wav')


# On définit les variables qui contiendront les positions des différents éléments (vaisseau, alien, projectile)
# Chaque position est un couple de valeur '(x,y)'
bomb_c,star_c = None, None
positionVaisseau = (300, 525)
AlienY = 65
positionAlien = [(150, AlienY),(200, AlienY),(250, AlienY),(300, AlienY),(350, AlienY),(400, AlienY),(450, AlienY)]
projectile = [(-1, -1)]
CadreProjectile = pygame.Rect((projectile[0][0] - 5, projectile[0][1] - 5), (10, 10))
for ele in positionAlien:
    CadreAlien = pygame.Rect((ele), (33, 37))

etoiles = [((randint(0,600),randint(0,600))) for x in range(100)]

Score = 0
Pr = 100
t = 0
m = True # aller à gauche
vie = 3
police = pygame.font.SysFont("arial", 20)

TexteScore = police.render('Score : ' + str(Score), True, (100, 255, 200))
TexteProjectile = police.render('Projectiles restants : ' + str(Pr), True, (100, 255, 200))


# Fonction en charge de dessiner tous les éléments sur notre fenêtre graphique.
# Cette fonction sera appelée depuis notre boucle infinie
def dessiner():
    global imageAlien, imageVaisseau, fenetre, projectile, vie, star, bomb, star_c, bomb_c
    # On remplit complètement notre fenêtre avec la couleur noire: (0,0,0)
    # Ceci permet de 'nettoyer' notre fenêtre avant de la dessiner
    fenetre.fill((0, 0, 0))
    fenetre.blit(imageVaisseau, positionVaisseau) # On dessine l'image du vaisseau à sa position
    for ele in positionAlien:
        fenetre.blit(imageAlien, ele)  # On dessine l'image de l'Alien à sa position
    fenetre.blit(TexteScore, (20, 10))
    fenetre.blit(TexteProjectile, (20, 30))
    imageVie = pygame.image.load("h"+str(vie)+".png")
    imageVie = pygame.transform.scale(imageVie, (135,35))
    if not bomb_c == None:
        fenetre.blit(bomb,bomb_c)
    if not star_c == None:
        fenetre.blit(star,star_c)
    fenetre.blit(imageVie, (20, 530))
    for ele in projectile:
        if projectile != (-1, -1):
            pygame.draw.circle(fenetre, (255, 255, 255), ele, 5) # On dessine le projectile (un simple petit cercle)
    for ele in etoiles:
        pygame.draw.circle(fenetre, (255, 255, 255), ele, 1)
    pygame.display.flip()  # Rafraichissement complet de la fenêtre avec les dernières opérations de dessin


# Fonction en charge de gérer les évènements clavier (ou souris)
# Cette fonction sera appelée depuis notre boucle infinie
def gererClavierEtSouris():
    global continuer, positionVaisseau, projectile, Pr, t, laser
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Permet de gérer un clic sur le bouton de fermeture de la fenêtre
            continuer = 0
    # Gestion du clavier: Quelles touches sont pressées ?
    touchesPressees = pygame.key.get_pressed()
    if touchesPressees[pygame.K_SPACE] == True and Pr > 0 and time.time() - t >= 0.5:
        projectile = projectile + [(positionVaisseau[0] + 32, positionVaisseau[1])]
        laser.play()
        Pr-=1
        t = time.time()
    if touchesPressees[pygame.K_RIGHT] == True and positionVaisseau[0] < 600 - 64:
        positionVaisseau = (positionVaisseau[0] + 5, positionVaisseau[1])
    if touchesPressees[pygame.K_LEFT] == True and positionVaisseau[0] > 0:
        positionVaisseau = (positionVaisseau[0] - 5, positionVaisseau[1])


# On crée une nouvelle horloge qui nous permettra de fixer la vitesse de rafraichissement de notre fenêtre
clock = pygame.time.Clock()

# La boucle infinie de pygame:
# On va continuellement dessiner sur la fenêtre, gérer les évènements et calculer certains déplacements
while True:
    # pygame permet de fixer la vitesse de notre boucle:
    # ici on déclare 50 tours par secondes soit une animation à 50 images par secondes
    clock.tick(50)
    dessiner()
    gererClavierEtSouris()

    fenetre.blit(TexteProjectile, (20, 30))
    # On fait avancer le projectile (si il existe)
    if len(positionAlien) == 0:
        print("Gagné")
        exit()
    elif AlienY >= positionVaisseau[1]:
        print("Noob")
        exit()
    if positionAlien[0][0] <= 10 or positionAlien[len(positionAlien)-1][0] >= 560:
        m = not m
        AlienY += 10
    if m is True:
        positionAlien = [(ele[0]-1, AlienY) for ele in positionAlien]
    else:
        positionAlien = [(ele[0] + 1, AlienY) for ele in positionAlien]

    if projectile != None:
        a = []
        for x, y in projectile:
            for i in range(len(positionAlien)):
                if positionAlien[i][0]-10 <= x <= positionAlien[i][0]+35 and positionAlien[i][1]-10 <= y <= positionAlien[i][1]+20:
                    Score += 1

                    positionAlien.pop(i)
                    break
            if not y - 5 <= 10:
                a = a + [(x, y - 5)]
        projectile = a
        for ele in projectile:
            CadreProjectile = pygame.Rect((ele[0], ele[1]), (10, 10))

    if randint(1,100) == 50 and bomb_c == None:
        x = randint(1,len(positionAlien)-1)
        print("aaa")
        bomb_c = (positionAlien[x][0],positionAlien[x][1])
    print(bomb_c, "             ", positionVaisseau)

    if randint(1,250) == 50 and star_c == None:
        star_c = (randint(15,585),0)
    if bomb_c != None:
        bomb_c = (bomb_c[0],bomb_c[1]+5)

        if bomb_c[0]-55 <= positionVaisseau[0] <= bomb_c[0]+35 and bomb_c[1]-35 <= positionVaisseau[1] <= bomb_c[1]+35:
            vie -= 1
            bomb_c = None
        try:
            if bomb_c[1] >= 600:
                bomb_c = None
        except:
            pass
    if star_c != None:
        star_c = (star_c[0],star_c[1]+5)

        if star_c[0]-55 <= positionVaisseau[0] <= star_c[0]+35 and star_c[1]-35 <= positionVaisseau[1] <= star_c[1]+35:
            Pr = 100
            star_c = None
        try:
            if star_c[1] >= 600:
                star_c = None
        except:
            pass


    if vie < 0:
        print("perdu")
        exit()
    a = []
    for x,y in etoiles:
        if y > 595:
            a.append((x,0))
        else:
            a.append((x,y+2))
    etoiles = a
        # projectile = (projectile[0], projectile[1] - 5) # le projectile "monte" vers le haut de la fenêtre
        # CadreProjectile=pygame.Rect((projectile[0],projectile[1]-5),(10,10))




    TexteScore = police.render('Score : ' + str(Score), True, (100, 255, 200))
    TexteProjectile = police.render('Projectiles restants : ' + str(Pr), True, (100, 255, 200))
    fenetre.blit(TexteScore, (20, 10))
    fenetre.blit(TexteProjectile, (20, 30))

## A la fin, lorsque l'on sortira de la boucle, on demandera à Pygame de quitter proprement
pygame.quit()
