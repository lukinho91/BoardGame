import pygame
import sys
import math

pygame.init()



# státuszok:
# 0 - nincsen még készen
# 1 - készen van
# 2 - kirobbant egy tömegverekedés

# körök
# 1: piros -> páratlan      counter % 2 != 0
# 2: kék1 -> osztható 2vel de nem osztahtó 4gyel   counter % 2 = 0 and counter % 4 != 0
# 3: piros -> páratlan
# 4: kék2 -> osztható 4gyel   counter % 4 = 0




# --- Ablak ---
screen = pygame.display.set_mode((700, 700))
pygame.display.set_caption("Kattintható pontok – 1 piros, max 2 kék (három szín)")

# --- Beállítások ---
line_color = (0, 255, 0)
line_width = 2
point_radius = 15
font = pygame.font.SysFont("Arial", 18)

# --- Pontok ---
points = [
    {"pos": [50, 50], "color": (200, 200, 200), "label": "Müpa", "ertek": 0, "status": 0, "goal": 4, "point_radius": 15},
    {"pos": [350, 50], "color": (200, 200, 200), "label": "Deák", "ertek": 0, "status": 0,  "goal": 4,  "point_radius": 15},
    {"pos": [50, 350], "color": (200, 200, 200), "label": "Blaha", "ertek": 0, "status": 0,  "goal": 4, "point_radius": 15},
    {"pos": [350, 350], "color": (200, 200, 200), "label": "Astoria", "ertek": 0, "status": 0,  "goal": 4, "point_radius": 15},
    {"pos": [200, 200], "color": (200, 200, 200), "label": "Corvin", "ertek": 0, "status": 0, "goal": 4, "point_radius": 15},
    {"pos": [450, 400], "color": (200, 200, 200), "label": "Parlamant", "ertek": 0, "status": 0, "goal": 4, "point_radius": 15},
    {"pos": [450, 650], "color": (200, 200, 200), "label": "BME", "ertek": 0, "status": 0, "goal": 4, "point_radius": 15},
    {"pos": [600, 400], "color": (200, 200, 200), "label": "ELTE", "ertek": 0, "status": 0, "goal": 4, "point_radius": 15},
    {"pos": [600, 300], "color": (200, 200, 200), "label": "Újpest", "ertek": 0, "status": 0, "goal": 4, "point_radius": 15},
    {"pos": [50, 500], "color": (200, 200, 200), "label": "Kispest", "ertek": 0, "status": 0, "goal": 4, "point_radius": 15},
    {"pos": [200, 400], "color": (200, 200, 200), "label": "Psukás", "ertek": 0, "status": 0, "goal": 4, "point_radius": 15},
]

# --- Vonalak ---
lines = [
    (points[0]["pos"], points[1]["pos"]),
    (points[0]["pos"], points[2]["pos"]),
    (points[1]["pos"], points[3]["pos"]),
    (points[2]["pos"], points[3]["pos"]),
    (points[4]["pos"], points[0]["pos"]),
    (points[9]["pos"], points[6]["pos"]),
    (points[6]["pos"], points[7]["pos"]),
    (points[1]["pos"], points[8]["pos"]),
    (points[4]["pos"], points[10]["pos"]),
    (points[5]["pos"], points[10]["pos"]),
    (points[4]["pos"], points[3]["pos"]),
    (points[2]["pos"], points[9]["pos"]),
    (points[10]["pos"], points[9]["pos"]),
    (points[7]["pos"], points[8]["pos"]),
    (points[7]["pos"], points[5]["pos"]),
]

click_count = 0
running = True
red_point = None
blue1_point = None
blue2_point = None

def is_neighbor(p1, p2):
    pos1 = p1["pos"]
    pos2 = p2["pos"]
    for start, end in lines:
        if (start == pos1 and end == pos2) or (start == pos2 and end == pos1):
            return True
    return False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            # --- Szín kiválasztása kattintásszám alapján ---
            if click_count % 2 == 1:
                target_color = (255, 0, 0)  # piros
            elif click_count % 4 == 2:
                target_color = (0, 0, 255)  # kék1
            else:
                target_color = (0, 1, 255)  # kék2

            for p in points:
                dx = mouse_pos[0] - p["pos"][0]
                dy = mouse_pos[1] - p["pos"][1]
                distance = math.hypot(dx, dy)

                if distance <= point_radius and ((target_color == (255,0,0)) or p["color"] == (200,200,200)):

                    # --- Szomszédság ellenőrzés ---
                    if target_color == (255, 0, 0):
                        if red_point and p != red_point and not is_neighbor(red_point, p):
                            continue
                    elif target_color == (0, 0, 255):
                        if blue1_point and not is_neighbor(blue1_point, p):
                            continue
                    else:  # kék2
                        if blue2_point and not is_neighbor(blue2_point, p):
                            continue

                                        # --- Piros pont kezelése ---
                    if target_color == (255, 0, 0):

                        # Ha már van piros, és most másikra lép → előző visszaszürkül
                        if red_point and p != red_point:
                            red_point["color"] = (200, 200, 200)
                            p["status"] = 0  # új piros pontnál státusz vissza 0-ra]

                        red_point = p

                        # Ha piros újra rálép ugyanarra → pontot kap
                        if p["status"] == 1:
                            p["ertek"] += 1

                            # Ha eléri a 4-et → nőjön a kör
                            if p["ertek"] >= p["goal"]:
                                p["point_radius"] = 25     # ✔️ most már jó

                        # Első kattintás után státusz 1 lesz
                        p["status"] = 1
                    # --- Kék pont kezelése ---
                    elif target_color == (0, 0, 255):
                        if blue1_point and p != blue1_point:
                            blue1_point["color"] = (200, 200, 200)
                        blue1_point = p
                    else:  # kék2
                        if blue2_point and p != blue2_point:
                            blue2_point["color"] = (200, 200, 200)
                        blue2_point = p

                    p["color"] = target_color
                    click_count += 1
                    break

    # --- Háttér ---
    screen.fill((0, 0, 0))

    # --- Vonalak ---
    for start, end in lines:
        pygame.draw.line(screen, line_color, start, end, line_width)

    # --- Pontok kirajzolása ---
    for p in points:
        pygame.draw.circle(screen, p["color"], p["pos"], p["point_radius"])
        label_surface = font.render(f"{p['label']} ({p['ertek']})", True, (255, 255, 255))
        label_rect = label_surface.get_rect(center=(p["pos"][0], p["pos"][1] - point_radius - 10))
        screen.blit(label_surface, label_rect)

    # --- Kattintásszámláló ---
    counter_surface = font.render(f"Kattintások: {click_count}", True, (255, 255, 0))
    screen.blit(counter_surface, (150, 10))

    pygame.display.flip()

pygame.quit()
sys.exit()