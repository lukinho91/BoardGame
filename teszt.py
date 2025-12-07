import pygame
import sys
import math
import random

pygame.init()

# --- Ablak ---
screen = pygame.display.set_mode((700, 700))
pygame.display.set_caption("Kattintható pontok – piros + 2 kék")

# --- Beállítások ---
line_color = (0, 255, 0)
line_width = 2
point_radius = 15
font = pygame.font.SysFont("Arial", 18)
