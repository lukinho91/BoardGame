import pygame
import sys
import math
import random

pygame.init()

# --- Ablak ---
screen = pygame.display.set_mode((700, 700))
pygame.display.set_caption("Kattintható pontok – piros + 3 kék")

# --- Beállítások ---
line_color = (0, 255, 0)
line_width = 2
font = pygame.font.SysFont("Arial", 18)

# --- Pontok ---
points = [
    {"pos": [50, 50], "color": (200, 200, 200), "label": "Müpa", "ertek": 0, "status": 0, "goal": 4, "point_radius": 15, "activate": False},
    {"pos": [350, 50], "color": (200, 200, 200), "label": "Deák", "ertek": 0, "status": 0, "goal": 4, "point_radius": 15, "activate": False},
    {"pos": [50, 350], "color": (200, 200, 200), "label": "Blaha", "ertek": 0, "status": 0, "goal": 4, "point_radius": 15, "activate": False},
    {"pos": [350, 350], "color": (200, 200, 200), "label": "Astoria", "ertek": 0, "status": 0, "goal": 4, "point_radius": 15, "activate": False},
    {"pos": [200, 200], "color": (200, 200, 200), "label": "Corvin", "ertek": 0, "status": 0, "goal": 4, "point_radius": 15, "activate": False},
    {"pos": [450, 400], "color": (200, 200, 200), "label": "Parlament", "ertek": 0, "status": 0, "goal": 4, "point_radius": 15, "activate": False},
    {"pos": [450, 650], "color": (200, 200, 200), "label": "BME", "ertek": 0, "status": 0, "goal": 4, "point_radius": 15, "activate": False},
    {"pos": [600, 400], "color": (200, 200, 200), "label": "ELTE", "ertek": 0, "status": 0, "goal": 4, "point_radius": 15, "activate": False},
    {"pos": [600, 300], "color": (200, 200, 200), "label": "Újpest", "ertek": 0, "status": 0, "goal": 4, "point_radius": 15, "activate": False},
    {"pos": [50, 500], "color": (200, 200, 200), "label": "Kispest", "ertek": 0, "status": 0, "goal": 4, "point_radius": 15, "activate": False},
    {"pos": [200, 400], "color": (200, 200, 200), "label": "Puskás", "ertek": 0, "status": 0, "goal": 4, "point_radius": 15, "activate": False},
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

# --- Segédfüggvény: szomszéd vizsgálat ---
def is_neighbor(p1, p2):
    pos1 = p1["pos"]
    pos2 = p2["pos"]
    for start, end in lines:
        if (start == pos1 and end == pos2) or (start == pos2 and end == pos1):
            return True
    return False

# --- Segédfüggvény: harmadik kék létrehozása ---
def add_third_blue_if_needed(p):
    if p and p["ertek"] > 0:
        gray_points = [x for x in points if x["color"] == (200, 200, 200)]
        if gray_points:
            extra_blue = random.choice(gray_points)
            extra_blue["color"] = (0, 0, 255)
            return extra_blue
    return None

# --- Játékállapot ---
click_count = 0
red_point = None
blue1_point = None
blue2_point = None
blue3_point = None
active_blue = None  # aktivált kék, csak ez léphet

# --- Véletlenszerűen elhelyezett első 2 kék ---
initial_gray_points = [p for p in points if p["color"] == (200,200,200)]
if len(initial_gray_points) >= 2:
    blue1_point = random.choice(initial_gray_points)
    blue1_point["color"] = (0,0,255)
    initial_gray_points.remove(blue1_point)
    
    blue2_point = random.choice(initial_gray_points)
    blue2_point["color"] = (0,0,255)
    initial_gray_points.remove(blue2_point)

running = True

# =====================================================================
#                           FŐ CIKLUS
# =====================================================================
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            if click_count % 2 == 0:
                target = "red"   # piros kezd minden kör elején páros szám
            else:
                target = "blue"  # kék jön utána

            # --- Pontok vizsgálata ---
            for p in points:
                dx = mouse_pos[0] - p["pos"][0]
                dy = mouse_pos[1] - p["pos"][1]
                distance = math.hypot(dx, dy)

                # Rákattintottál-e a körre?
                if distance > p["point_radius"]:
                    continue

                # --- PIROS LÉPÉS ---
                if target == "red":
                    if red_point and p != red_point and not is_neighbor(red_point, p):
                        continue

                    # ha volt régi piros → visszaszürkül
                    if red_point and p != red_point:
                        red_point["color"] = (200,200,200)
                        red_point["status"] = 0

                    # új piros
                    red_point = p

                    # pontgyűjtés ha status=1 volt
                    if p["status"] == 1:
                        p["ertek"] += 1
                        if p["ertek"] >= p["goal"]:
                            p["point_radius"] = 25

                    p["status"] = 1
                    p["color"] = (255,0,0)
                    click_count += 1
                    break

                # --- KÉK LÉPÉS ---
                else:
                    # Ha kék pontra kattintottál → aktiválás
                    if p["color"] == (0,0,255):
                        active_blue = p
                        p["color"] = (0,150,255)  # vizuális visszajelzés
                        print("Kék aktiválva:", p["label"])
                        break  # ne lépjen, csak aktiválódjon

                    # Ha nincs aktivált kék → nem léphet
                    if active_blue is None:
                        continue

                    # Csak szomszédos mezőre léphet
                    if not is_neighbor(active_blue, p):
                        continue

                    # Ha lép, az előző hely visszaszürkül
                    if active_blue != p:
                        active_blue["color"] = (200,200,200)
                        # Harmadik kék logika
                        add_third_blue_if_needed(p)

                    # Új pozíció kékre vált
                    p["color"] = (0,0,255)
                    # Frissítjük az aktivált kék referenciát
                    if blue1_point == active_blue:
                        blue1_point = p
                    elif blue2_point == active_blue:
                        blue2_point = p
                    else:
                        blue3_point = p
                    active_blue = p

                    click_count += 1
                    break

    # --- Rajzolás ---
    screen.fill((0,0,0))

    # Vonalak
    for start,end in lines:
        pygame.draw.line(screen, line_color, start, end, line_width)

    # Pontok
    for p in points:
        pygame.draw.circle(screen, p["color"], p["pos"], p["point_radius"])
        txt = f"{p['label']} ({p['ertek']}) st:{p['status']}"
        label_surface = font.render(txt, True, (255,255,255))
        label_rect = label_surface.get_rect(center=(p["pos"][0], p["pos"][1]-p["point_radius"]-10))
        screen.blit(label_surface, label_rect)

    # Click counter
    counter_surface = font.render(f"Kattintások: {click_count}", True, (255,255,0))
    screen.blit(counter_surface, (150,10))

    pygame.display.flip()

pygame.quit()
sys.exit()