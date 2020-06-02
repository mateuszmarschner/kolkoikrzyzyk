import pygame
import sys
import random
from pygame.locals import * 

pygame.init()
pygame.display.set_caption("Kółko i krzyżyk")
OKNOGRY = pygame.display.set_mode((600, 600))


POLE_GRY = [0, 0, 0,
            0, 0, 0,
            0, 0, 0]

RUCH = 1  
WYGRANY = 0 
WYGRANA = False

# rysowanie planszy gry
def rysuj_plansze():
    for i in range(0, 3):
        for j in range(0, 3):
            pygame.draw.rect(OKNOGRY, (218,216,167),Rect((j * 200, i * 200), (200, 200)), 1)

# narysuj kółka
def rysuj_pole_gry():
    for i in range(0, 3):
        for j in range(0, 3):
            pole = i * 3 + j
            x = j * 200 + 100
            y = i * 200 + 100

            if POLE_GRY[pole] == 1:
                pygame.draw.circle(OKNOGRY, (255,158,157), (x, y), 50)
            elif POLE_GRY[pole] == 2:
                pygame.draw.circle(OKNOGRY, (63,184,175), (x, y), 50)
                y = i * 200 + 100

            if POLE_GRY[pole] == 1:
                pygame.draw.circle(OKNOGRY, (255,158,157), (x, y), 50)
            elif POLE_GRY[pole] == 2:
                pygame.draw.circle(OKNOGRY, (63,184,175), (x, y), 50)

# postaw znak
def postaw_znak(pole, RUCH):
    if POLE_GRY[pole] == 0:
        if RUCH == 1:
            POLE_GRY[pole] = 1
            return 2
        elif RUCH == 2:
            POLE_GRY[pole] = 2
            return 1

    return RUCH


# sprawdzanie, czy komputer może wygrać
def sprawdz_pola(uklad, wygrany=None):
    wartosc = None
    POLA_INDEKSY = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # indeksy pól w poziomie (wiersze)
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # indeksy pól w pionie (kolumny)
        [0, 4, 8], [2, 4, 6]  # indeksy pól na skos (przekątne)
    ]

    for lista in POLA_INDEKSY:
        kol = []
        for ind in lista:
            kol.append(POLE_GRY[ind])
        if (kol in uklad):
            wartosc = wygrany if wygrany else lista[kol.index(0)]
    return wartosc


# ruchy komputera
def ai_ruch(RUCH):
    pole = None


    uklady_wygrywam = [[2, 2, 0], [2, 0, 2], [0, 2, 2]]
    uklady_blokuje = [[1, 1, 0], [1, 0, 1], [0, 1, 1]]

    pole = sprawdz_pola(uklady_wygrywam)
    if pole is not None:
        return postaw_znak(pole, RUCH)

    pole = sprawdz_pola(uklady_blokuje)
    if pole is not None:
        return postaw_znak(pole, RUCH)

    while pole is None:
        pos = random.randrange(0, 9)
        if POLE_GRY[pos] == 0:
            pole = pos

    return postaw_znak(pole, RUCH)


def kto_wygral():
    uklad_gracz = [[1, 1, 1]]
    uklad_komp = [[2, 2, 2]]

    WYGRANY = sprawdz_pola(uklad_gracz, 1)
    if not WYGRANY: 
        WYGRANY = sprawdz_pola(uklad_komp, 2)

    if 0 not in POLE_GRY and WYGRANY not in [1, 2]:
        WYGRANY = 3

    return WYGRANY

def drukuj_wynik(WYGRANY, flaga):
    fontObj = pygame.font.Font('freesansbold.ttf', 60)
    if WYGRANY == 1:
        tekst = u'Wygrał Gracz'
    elif WYGRANY == 2 and flaga == 1:
        tekst = u'Wygrał Komputer!'
    elif WYGRANY == 2 and flaga == 2:
        tekst = u'Wygrał Gracz 2!'
    elif WYGRANY == 3:
        tekst = 'Remis!'
    tekst_obr = fontObj.render(tekst, True, (0,0,0))
    tekst_prost = tekst_obr.get_rect()
    tekst_prost.center = (300, 275)
    OKNOGRY.blit(tekst_obr, tekst_prost)


# pętla główna programu
def intro():
    czcionka = pygame.font.SysFont("freesansbold.ttf",80)
    czcionka2 = pygame.font.SysFont("freesansbold.ttf",30)
    fps = pygame.time.Clock()
    intro = True
    
    while intro:
        for j in pygame.event.get():
            if j.type == QUIT:
                sys.exit(0)
                       
        OKNOGRY.fill((99,174,174))
        
        pygame.draw.rect(OKNOGRY, (15,71,71),(190,300,200,50))
        pygame.draw.rect(OKNOGRY, (15,71,71),(190,400,200,50))
        pygame.draw.rect(OKNOGRY, (15,71,71),(230,500,120,50))

        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        
        if 190+200 > mouse[0] > 190 and 300+50 > mouse[1] > 300:
            pygame.draw.rect(OKNOGRY, (4,40,40),(190,300,200,50))
            if click[0] == 1:
                gg()        
        elif 190+200 > mouse[0] > 190 and 400+50 > mouse[1] > 400:
            pygame.draw.rect(OKNOGRY, (4,40,40),(190,400,200,50))
            if click[0] == 1:
                gk()
        elif 230+120 > mouse[0] > 230 and 500+50 > mouse[1] > 500:
            pygame.draw.rect(OKNOGRY, (4,40,40),(230,500,120,50))
            if click[0] == 1:
                sys.exit(0)

        tekst = czcionka.render("Kółko i krzyżyk",True,(255,255,255))
        tekst1g = czcionka2.render("Gracz VS Gracz",True,(255,255,255))
        tekst2g = czcionka2.render("Gracz VS Komputer",True,(255,255,255))
        tekstw = czcionka2.render("WYJŚCIE",True,(255,255,255))
        
        tekst_dane = tekst.get_rect()
        tekst_dane.center = (290,90)
        OKNOGRY.blit(tekst,tekst_dane)

        tekst_1g = tekst1g.get_rect()
        tekst_1g.center = (290,325)
        OKNOGRY.blit(tekst1g,tekst_1g)

        tekst_2g = tekst2g.get_rect()
        tekst_2g.center = (290,425)
        OKNOGRY.blit(tekst2g,tekst_2g)

        tekst_w = tekstw.get_rect()
        tekst_w.center = (290,525)
        OKNOGRY.blit(tekstw,tekst_w)
        
        pygame.display.update()
        fps.tick(30)

def gg():
    RUCH = 1
    WYGRANY = 0 
    WYGRANA = False
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                #pygame.quit()
                sys.exit(0)

            if WYGRANA is False:
                if RUCH == 1:
                    if event.type == MOUSEBUTTONDOWN:
                        if event.button == 1:
                            mouseX, mouseY = event.pos
                            pole = (int(mouseY / 200) * 3) + int(mouseX / 200)
                            RUCH = postaw_znak(pole, RUCH)
                elif RUCH == 2:
                    if event.type == MOUSEBUTTONDOWN:
                        if event.button == 1:
                            mouseX, mouseY = event.pos
                            pole = (int(mouseY / 200) * 3) + int(mouseX / 200)
                            RUCH = postaw_znak(pole, RUCH)

                WYGRANY = kto_wygral()
                if WYGRANY is not None:
                    WYGRANA = True

        OKNOGRY.fill((251,246,144))
        rysuj_plansze()
        rysuj_pole_gry()
        if WYGRANA:
            drukuj_wynik(WYGRANY,2)
        pygame.display.update()
def gk():
    RUCH = 1 
    WYGRANY = 0 
    WYGRANA = False
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                #pygame.quit()
                sys.exit(0)

            if WYGRANA is False:
                if RUCH == 1:
                    if event.type == MOUSEBUTTONDOWN:
                        if event.button == 1:
                            mouseX, mouseY = event.pos
                            pole = (int(mouseY / 200) * 3) + int(mouseX / 200)
                            RUCH = postaw_znak(pole, RUCH)
                elif RUCH == 2:
                    RUCH = ai_ruch(RUCH)

                WYGRANY = kto_wygral()
                if WYGRANY is not None:
                    WYGRANA = True

        OKNOGRY.fill((251,246,144))
        rysuj_plansze()
        rysuj_pole_gry()
        if WYGRANA:
            drukuj_wynik(WYGRANY,1)
        pygame.display.update()

intro()
