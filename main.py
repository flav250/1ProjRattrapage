import pygame
from pygame.locals import *

pygame.init()

game = pygame.display.set_mode((600, 602))
pygame.display.set_caption("Alquerque")


# ---------------------------------------------------------------------------------------------------------

# La class

# ---------------------------------------------------------------------------------------------------------

class Player(pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__()
        self.player = player
        self.image = None
        if player == 2:
            self.image = pygame.transform.scale(pygame.image.load("Image/pion1.png"), (60, 60))
        if player == 1:
            self.image = pygame.transform.scale(pygame.image.load("Image/pion2.png"), (60, 60))
        elif player == 0:
            self.image = pygame.transform.scale(pygame.image.load("Image/pion2.png"), (60, 60))

    def set(self, player):
        self.player = player
        if player == 2:
            self.image = pygame.transform.scale(pygame.image.load("Image/pion1.png"), (60, 60))
        if player == 1:
            self.image = pygame.transform.scale(pygame.image.load("Image/pion2.png"), (60, 60))
        elif player == 0:
            self.image = pygame.transform.scale(pygame.image.load("Image/pion2.png"), (60, 60))


# Cette class va permettre de définir les pions avec la couleur noir et blanc
# Un pion qui égale à 0 c'est un pion invisible qui sera cliquable pour nous aider au déplacement

# ---------------------------------------------------------------------------------------------------------

# Tableau

# ---------------------------------------------------------------------------------------------------------

tableau = [[Player(2), Player(2), Player(2), Player(2), Player(2)],
           [Player(2), Player(2), Player(2), Player(2), Player(2)],
           [Player(2), Player(2), Player(0), Player(1), Player(1)],
           [Player(1), Player(1), Player(1), Player(1), Player(1)],
           [Player(1), Player(1), Player(1), Player(1), Player(1)]]


# On crée le tableau en appelant pour chaque pion la class "Player" avec un numéro définit dans la class pour donner
# la couluer des pions

# ---------------------------------------------------------------------------------------------------------

# Placement des pions

# ---------------------------------------------------------------------------------------------------------

def InitBoard():
    board = pygame.image.load("Image/alquerque1.png")
    board_rect = board.get_rect(center=(300, 298.5))
    game.blit(board, board_rect)

    for i in range(len(tableau)):
        for j in range(len(tableau[i])):
            if tableau[i][j].image is not None:
                tableau[i][j].rect = tableau[i][j].image.get_rect(center=(122 * (j + 0.46), 122 * (i + 0.47)))
                if tableau[i][j].player != 0:
                    game.blit(tableau[i][j].image, tableau[i][j].rect)
    pygame.display.flip()


# InitBoard permet de placer les pions sur le plateau en créant une doule iste à parcourir le tableau pour placer les
# pions


# ---------------------------------------------------------------------------------------------------------

# Test de click sur un pion

# ---------------------------------------------------------------------------------------------------------

def move(event: MOUSEMOTION):
    for y in range(len(tableau)):
        for x in range(len(tableau[y])):
            if tableau[y][x].rect.collidepoint(event.pos[0], event.pos[1]) is True:
                return y, x
    return None


# Cette fonction va donner les coordonnées de chaque pion quand on clique dessus qui va nous aider pour le déplacement


# ---------------------------------------------------------------------------------------------------------

# Mouvement des pions

# ---------------------------------------------------------------------------------------------------------

def case(player: tuple):
    voisin = []
    try:
        if player[0] - 1 >= 0 and tableau[player[0] - 1][player[1]]:
            voisin.append((player[0] - 1, player[1]))
        if player[0] + 1 >= 0 and tableau[player[0] + 1][player[1]]:
            voisin.append((player[0] + 1, player[1]))
        if player[1] - 1 >= 0 and tableau[player[0]][player[1] - 1]:
            voisin.append((player[0], player[1] - 1))
        if player[1] + 1 >= 0 and tableau[player[0]][player[1] + 1]:
            voisin.append((player[0], player[1] + 1))
        if (player[0] % 2 != 0 and player[1] % 2 != 0) or (player[0] % 2 == 0 and player[1] % 2 == 0):
            if player[0] - 1 >= 0 and player[1] - 1 >= 0 and tableau[player[0] - 1][player[1] - 1]:
                voisin.append((player[0] - 1, player[1] - 1))
            if player[0] + 1 >= 0 and player[1] + 1 >= 0 and tableau[player[0] + 1][player[1] + 1]:
                voisin.append((player[0] + 1, player[1] + 1))
            if player[0] + 1 >= 0 and player[1] - 1 >= 0 and tableau[player[0] + 1][player[1] - 1]:
                voisin.append((player[0] + 1, player[1] - 1))
            if player[0] - 1 >= 0 and player[1] + 1 >= 0 and tableau[player[0] - 1][player[1] + 1]:
                voisin.append((player[0] - 1, player[1] + 1))
    except IndexError:
        pass
    return voisin


# ---------------------------------------------------------------------------------------------------------

# Alternance de joueur

# ---------------------------------------------------------------------------------------------------------

def movepos(pion1: tuple, pion2: tuple):
    if pion2 in case(pion1) and tableau[pion2[0]][pion2[1]].player == 0 and tableau[pion1[0]][pion1[1]].player == turnplayer:
        return True
    else:
        return False


# ---------------------------------------------------------------------------------------------------------

# Capture des pions

# ---------------------------------------------------------------------------------------------------------

def capture(pion1: tuple, pion2: tuple):
    for items in case(pion1):
        if tableau[pion1[0]][pion1[1]].player == turnplayer and tableau[pion2[0]][
            pion2[1]].player == 0 and items in case(pion2) and tableau[items[0]][
            items[1]].player == pionadverse() and (
                (((pion1[0] + pion2[0]) / 2, (pion1[1] + pion2[1]) / 2) == items) or (
                pion1[0] == pion2[0] == items[0] or pion1[1] == pion2[1] == items[1])):
            return items
    return None


# ---------------------------------------------------------------------------------------------------------

# Changer de pions

# ---------------------------------------------------------------------------------------------------------

def capturer(pion1: tuple, pion2: tuple, pion3: tuple):
    tableau[pion1[0]][pion1[1]].set(0)
    tableau[pion2[0]][pion2[1]].set(turnplayer)
    tableau[pion3[0]][pion3[1]].set(0)


# ---------------------------------------------------------------------------------------------------------

# Tentative de capture

# ---------------------------------------------------------------------------------------------------------

def secondcapture():
    for i in range(len(tableau)):
        for j in range(len(tableau[i])):
            for k in case((i, j)):
                for l in case((k[0], k[1])):
                    if tableau[i][j].player == turnplayer and l not in case((i, j)) and capture((i, j), l) is not None:
                        return True
    return False


# ---------------------------------------------------------------------------------------------------------

# Alternance de joueur

# ---------------------------------------------------------------------------------------------------------

def pionadverse():
    if turnplayer == 1:
        return 2
    else:
        return 1


# ---------------------------------------------------------------------------------------------------------

# fin de jeux

# ---------------------------------------------------------------------------------------------------------

def endgame():
    for i in range(len(tableau)):
        for j in range(len(tableau[i])):
            if tableau[i][j].player == turnplayer:
                return False
    return True


# ---------------------------------------------------------------------------------------------------------

# Lorque le jeux se lance

# ---------------------------------------------------------------------------------------------------------

continuer = True
case_nei, second_nei = None, None
turnplayer = 1
while continuer:
    InitBoard()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            continuer = False
        elif event.type == MOUSEBUTTONDOWN:
            click = move(event)
            if click is None:
                break
            if case_nei is None:
                case_nei = click
            elif case_nei is not None and click != case_nei and second_nei is None:
                second_nei = click
            if case_nei is not None and second_nei is not None:
                mp = movepos(case_nei, second_nei)
                if mp is True and secondcapture() is True:
                    tableau[case_nei[0]][case_nei[1]].set(0)
                    tableau[second_nei[0]][second_nei[1]].set(0)
                elif mp is True and secondcapture() is False:
                    tableau[second_nei[0]][second_nei[1]].set(turnplayer)
                    tableau[case_nei[0]][case_nei[1]].set(0)
                if mp is False and capture(case_nei, second_nei) is not None:
                    capturer(case_nei, second_nei, capture(case_nei, second_nei))

                turnplayer = pionadverse()

                case_nei, second_nei = None, None

            if endgame() is True:
                tableau = [[Player(2), Player(2), Player(2), Player(2), Player(2)],
                           [Player(2), Player(2), Player(2), Player(2), Player(2)],
                           [Player(2), Player(2), Player(0), Player(1), Player(1)],
                           [Player(1), Player(1), Player(1), Player(1), Player(1)],
                           [Player(1), Player(1), Player(1), Player(1), Player(1)]]
                turnplayer = 1
pygame.quit()
