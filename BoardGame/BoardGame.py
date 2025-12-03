import pygame
import sys
import math

pygame.init()

# --- Ablak ---
screen = pygame.display.set_mode((400, 400))
pygame.display.set_caption("Kattintható pontok – válogatott vonalak")

# --- Beállítások ---
line_color = (0, 255, 0)
line_width = 2
point_radius = 15
font = pygame.font.SysFont("Arial", 18)

# --- Pontok: pozíció, szín, állapot, felirat, érték ---
points = [
    {"pos": [50, 50], "color": (200, 200, 200), "state": 0, "label": "0", "ertek": 0},
    {"pos": [350, 50], "color": (200, 200, 200), "state": 0, "label": "1", "ertek": 0},
    {"pos": [50, 350], "color": (200, 200, 200), "state": 0, "label": "2", "ertek": 0},
    {"pos": [350, 350], "color": (200, 200, 200), "state": 0, "label": "3", "ertek": 0},
    {"pos": [200, 200], "color": (200, 200, 200), "state": 0, "label": "4", "ertek": 0},
]

# --- Kézzel definiált vonalak ---
lines = [
    (points[0]["pos"], points[1]["pos"]),
    (points[0]["pos"], points[2]["pos"]),
    (points[1]["pos"], points[3]["pos"]),
    (points[2]["pos"], points[3]["pos"]),
    (points[4]["pos"], points[0]["pos"]),
    (points[4]["pos"], points[1]["pos"]),
    (points[4]["pos"], points[2]["pos"]),
    (points[4]["pos"], points[3]["pos"]),
]

click_count = 0
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            click_count += 1
            mouse_pos = pygame.mouse.get_pos()
           
            for p in points:
                dx = mouse_pos[0] - p["pos"][0]
                dy = mouse_pos[1] - p["pos"][1]
                distance = math.hypot(dx, dy)
                if distance <= point_radius and click_count % 2:
                    p[("ertek")] += 1
                    p["color"] = (255, 0, 0) if p["state"] == 0 else (200, 200, 200)
                elif distance <= point_radius and click_count % 2 !=0:
                    p["color"] = (255, 250, 0)                 
                    


    # --- Háttér kirajzolása ---
    screen.fill((0, 0, 0))

    # --- Vonalak kirajzolása ---
    for start, end in lines:
        pygame.draw.line(screen, line_color, start, end, line_width)

    # --- Pontok kirajzolása és érték felirata ---
    for p in points:
        pygame.draw.circle(screen, p["color"], p["pos"], point_radius)
        label_surface = font.render(str(p["ertek"]), True, (255, 255, 255))
        label_rect = label_surface.get_rect(center=(p["pos"][0], p["pos"][1] - point_radius - 10))
        screen.blit(label_surface, label_rect)

    # --- Teljes kattintásszámláló ---
    counter_surface = font.render(f"Kattintások: {click_count}", True, (255, 255, 0))
    screen.blit(counter_surface, (150, 10))

    pygame.display.flip()

pygame.quit()
sys.exit()