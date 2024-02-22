import pygame
import sys
from random import randint
from math import sqrt
from time import sleep
from pygame import mixer

#Initialisation
pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((800,600))

#Titre et icone
pygame.display.set_caption("Solitaire AI")
icon = pygame.image.load("images/icon.jpeg")
pygame.display.set_icon(icon)

