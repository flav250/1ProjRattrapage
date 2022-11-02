import pygame
from pygame.locals import *

pygame.init()

game = pygame.display.set_mode((600, 602))
pygame.display.set_caption("Alquerque")
pionN = pygame.image.load("Image/pion1.png")
pionB = pygame.image.load("Image/pion2.png")


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


class fonctiongame:

    def __init__(self):
        self.tableau = [[Player(2), Player(2), Player(2), Player(2), Player(2)],
           [Player(2), Player(2), Player(2), Player(2), Player(2)],
           [Player(2), Player(2), Player(0), Player(1), Player(1)],
           [Player(1), Player(1), Player(1), Player(1), Player(1)],
           [Player(1), Player(1), Player(1), Player(1), Player(1)]]

    def getTableau(self):
        return self.tableau

    def InitBoard(self):
        board = pygame.image.load("Image/alquerque1.png")
        board_rect = board.get_rect(center=(300, 298.5))
        game.blit(board, board_rect)

        for i in range(len(self.tableau)):
            for j in range(len(self.tableau[i])):
                if self.tableau[i][j].image is not None:
                    self.tableau[i][j].rect = self.tableau[i][j].image.get_rect(center=(122 * (j + 0.46), 122 * (i + 0.47)))
                    if self.tableau[i][j].player != 0:
                        game.blit(self.tableau[i][j].image, self.tableau[i][j].rect)
        pygame.display.flip()

    def position(self,event: MOUSEMOTION):
        for y in range(len(self.tableau)):
            for x in range(len(self.tableau[y])):
                if self.tableau[y][x].rect.collidepoint(event.pos[0], event.pos[1]) is True:
                    return y, x
        return None

    def case(self, pion):
        x = pion[0]
        y = pion[1]
        voisin = []
        try:
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if (x + y) % 2 == 0:
                        if 0 <= x + i <= len(self.tableau) - 1 and 0 <= y + j <= len(self.tableau) - 1 and (i != 0 or j != 0):
                            voisin.append((x + i, y + j))
                    else:
                        if 0 <= x + i <= len(self.tableau) - 1 and 0 <= y + j <= len(self.tableau) - 1 and (
                                (x + i == x) != (y + j == y)):
                            voisin.append((x + i, y + j))
        except IndexError:
            pass
        return voisin

    def movepos(self, pion1: tuple, pion2: tuple):
        if pion2 in self.case(pion1) and self.tableau[pion2[0]][pion2[1]].player == 0 and self.tableau[pion1[0]][
            pion1[1]].player == turnplayer:
            return True
        else:
            return False

    def capture(self, pion1: tuple, pion2: tuple):
        for items in self.case(pion1):
            if self.tableau[pion1[0]][pion1[1]].player == turnplayer and self.tableau[pion2[0]][
                pion2[1]].player == 0 and items in self.case(pion2) and self.tableau[items[0]][
                items[1]].player == self.pionadverse() and (
                    (((pion1[0] + pion2[0]) / 2, (pion1[1] + pion2[1]) / 2) == items) or (
                    pion1[0] == pion2[0] == items[0] or pion1[1] == pion2[1] == items[1])):
                return items
        return None

    def capturer(self, pion1: tuple, pion2: tuple, pion3: tuple):
        self.tableau[pion1[0]][pion1[1]].set(0)
        self.tableau[pion2[0]][pion2[1]].set(turnplayer)
        self.tableau[pion3[0]][pion3[1]].set(0)

    def secondcapture(self):
        for i in range(len(self.tableau)):
            for j in range(len(self.tableau[i])):
                for k in self.case((i, j)):
                    for l in self.case((k[0], k[1])):
                        if self.tableau[i][j].player == turnplayer and l not in self.case((i, j)) and self.capture((i, j),
                                                                                                              l) is not None:
                            return True
        return False

    def pionadverse(self):
        if turnplayer == 1:
            return 2
        else:
            return 1

    def endgame(self):
        for i in range(len(self.tableau)):
            for j in range(len(self.tableau[i])):
                if self.tableau[i][j].player == turnplayer:
                    return False
        return True


continuer = True
case_nei, second_nei = None, None
turnplayer = 1
plateau = fonctiongame()
while continuer:
    plateau.InitBoard()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            continuer = False
        elif event.type == MOUSEBUTTONDOWN:
            click = plateau.position(event)
            if click is None:
                break
            if case_nei is None:
                case_nei = click
            elif case_nei is not None and click != case_nei and second_nei is None:
                second_nei = click
            if case_nei is not None and second_nei is not None:
                mp = plateau.movepos(case_nei, second_nei)
                if mp is True and plateau.secondcapture() is True:
                    plateau.getTableau()[case_nei[0]][case_nei[1]].set(0)
                    plateau.getTableau()[second_nei[0]][second_nei[1]].set(0)
                    turnplayer = plateau.pionadverse()
                elif mp is True and plateau.secondcapture() is False:
                    plateau.getTableau()[second_nei[0]][second_nei[1]].set(turnplayer)
                    plateau.getTableau()[case_nei[0]][case_nei[1]].set(0)
                    turnplayer = plateau.pionadverse()
                if mp is False and plateau.capture(case_nei, second_nei) is not None:
                    plateau.capturer(case_nei, second_nei, plateau.capture(case_nei, second_nei))
                    turnplayer = plateau.pionadverse()

                case_nei, second_nei = None, None

            if plateau.endgame() is True:
                tableau = [[Player(2), Player(2), Player(2), Player(2), Player(2)],
                           [Player(2), Player(2), Player(2), Player(2), Player(2)],
                           [Player(2), Player(2), Player(0), Player(1), Player(1)],
                           [Player(1), Player(1), Player(1), Player(1), Player(1)],
                           [Player(1), Player(1), Player(1), Player(1), Player(1)]]
                turnplayer = 1
pygame.quit()
