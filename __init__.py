import pygame, sys, os
from pygame.locals import *
from tkinter import Tk
from tkinter.filedialog import askopenfilename
pygame.init()

cls = lambda: os.system("cls")
held = True

width = 1920
height = 1080
cls()
pygame.display.set_caption("EZ Refs - 1.0.0")
DISPLAY = pygame.display.set_mode((0, 0), RESIZABLE)
Tk().withdraw()
path = askopenfilename()
image = pygame.image.load(path)
boxx = width / 2
boxy = height / 2
imgWidth = pygame.Surface.get_width(image)
imgHeight = pygame.Surface.get_height(image)
imageRect = image.get_rect()
imageRect.center = (boxx, boxy)
mouse = pygame.mouse.get_pos()
black = (0, 0, 0)
mouseClicked = pygame.mouse.get_pressed()
mousePos = pygame.mouse.get_pos()
DISPLAY.fill(black)
while True:
    image = pygame.image.load(path)
    imageRect = image.get_rect()
    imageRect.center = (int(width / 2), int(height / 2))
    DISPLAY.blit(image, imageRect)
    cls()
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if mouse[0] >= imageRect.center[0] - imgWidth / 2 and mouse[0] <= imageRect.center[0] + imgWidth / 2:
                if mouse[1] >= imageRect.center[1] + imgHeight / 2 and mouse[1] <= imageRect.center[1] + imgHeight / 2:
                    if held:
                        imageRect.center = (mouse[0], mouse[1])
                    else:
                        imageRect.center = (boxx, boxy)
        mouseClicked = pygame.mouse.get_pressed()
        mousePosBefore = pygame.mouse.get_pos()[1]
        if event.type == mouseClicked[1]:
            if mouse[1] > mousePosBefore:
                boxy += 1
        else:
            imageRect.center = (boxx, boxy)
        if event.type == mouseClicked[1]:
            if mouse[1] < mousePosBefore:
                boxy -= 1
            else:
                imageRect.center = (boxx, boxy)
            