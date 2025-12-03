import pygame
import sys
import math

pygame.init()

# --- Ablak ---
screen = pygame.display.set_mode((400, 400))
pygame.display.set_caption("Kattintható pontok – 1 piros, max 2 kék (FIFO)")

# --- Beállítások ---
line_color = (0, 255, 0)
line_width = 2
point_radius = 15
font = pygame.font.SysFont("Arial", 18)

# --- Pontok ---
points = [
    {"pos": [50, 50], "color": (200, 200, 200), "label": "0", "ertek": 0},
    {"pos": [350, 50], "color": (200, 200, 200), "label": "1", "ertek": 0},
    {"pos": [50, 350], "color": (200, 200, 200), "label": "2", "ertek": 0},
    {"pos": [350, 350], "color": (200, 200, 200), "label": "3", "ertek": 0},
    {"pos": [200, 200], "color": (200, 200, 200), "label": "4", "ertek": 0},
]

# --- Vonalak ---
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
red_point = None
blue_points = []

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            # Piros pont: páros kattintás, Kék pont: páratlan
            target_color = (255, 0, 0) if (click_count % 2 == 0) else (0, 0, 255)

            for p in points:
                dx = mouse_pos[0] - p["pos"][0]
                dy = mouse_pos[1] - p["pos"][1]
                distance = math.hypot(dx, dy)

                # Csak szürkére lehet kattintani
                if distance <= point_radius and p["color"] == (200, 200, 200):

                    if target_color == (255, 0, 0):
                        # Pirosból egyszerre csak 1 lehet
                        if red_point:
                            red_point["color"] = (200, 200, 200)
                        red_point = p

                    else:  # Kék pont
                        if len(blue_points) >= 2:
                            # Ha már 2 kék van, az első visszaáll szürkére
                            first_blue = blue_points.pop(0)
                            first_blue["color"] = (200, 200, 200)
                        blue_points.append(p)

                    # Pont beállítása
                    p["color"] = target_color
                    p["ertek"] += 1
                    click_count += 1
                    break  # csak egy pont kattintása számít

    # --- Háttér ---
    screen.fill((0, 0, 0))

    # --- Vonalak ---
    for start, end in lines:
        pygame.draw.line(screen, line_color, start, end, line_width)

    # --- Pontok ---
    for p in points:
        pygame.draw.circle(screen, p["color"], p["pos"], point_radius)
        label_surface = font.render(str(p["ertek"]), True, (255, 255, 255))
        label_rect = label_surface.get_rect(center=(p["pos"][0], p["pos"][1] - point_radius - 10))
        screen.blit(label_surface, label_rect)

    # --- Kattintásszámláló ---
    counter_surface = font.render(f"Kattintások: {click_count}", True, (255, 255, 0))
    screen.blit(counter_surface, (150, 10))

    pygame.display.flip()

pygame.quit()
sys.exit()
