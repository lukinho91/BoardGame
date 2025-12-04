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

# --- Pontok ---
points = [
    {"pos": [50, 50], "color": (200, 200, 200), "label": "Müpa", "ertek": 0, "status": 0, "goal": 4, "point_radius": 15},
    {"pos": [350, 50], "color": (200, 200, 200), "label": "Deák", "ertek": 0, "status": 0, "goal": 4, "point_radius": 15},
    {"pos": [50, 350], "color": (200, 200, 200), "label": "Blaha", "ertek": 0, "status": 0, "goal": 4, "point_radius": 15},
    {"pos": [350, 350], "color": (200, 200, 200), "label": "Astoria", "ertek": 0, "status": 0, "goal": 4, "point_radius": 15},
    {"pos": [200, 200], "color": (200, 200, 200), "label": "Corvin", "ertek": 0, "status": 0, "goal": 4, "point_radius": 15},
    {"pos": [450, 400], "color": (200, 200, 200), "label": "Parlament", "ertek": 0, "status": 0, "goal": 4, "point_radius": 15},
    {"pos": [450, 650], "color": (200, 200, 200), "label": "BME", "ertek": 0, "status": 0, "goal": 4, "point_radius": 15},
    {"pos": [600, 400], "color": (200, 200, 200), "label": "ELTE", "ertek": 0, "status": 0, "goal": 4, "point_radius": 15},
    {"pos": [600, 300], "color": (200, 200, 200), "label": "Újpest", "ertek": 0, "status": 0, "goal": 4, "point_radius": 15},
    {"pos": [50, 500], "color": (200, 200, 200), "label": "Kispest", "ertek": 0, "status": 0, "goal": 4, "point_radius": 15},
    {"pos": [200, 400], "color": (200, 200, 200), "label": "Puskás", "ertek": 0, "status": 0, "goal": 4, "point_radius": 15},
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

# --- Segédfüggvény ---
def is_neighbor(p1, p2):
    pos1 = p1["pos"]
    pos2 = p2["pos"]
    for start, end in lines:
        if (start == pos1 and end == pos2) or (start == pos2 and end == pos1):
            return True
    return False


#--- Ha a kék egy olyanra lép, ahol a piros már volt akkor legyen még egy kék ---#

def add_third_blue_if_needed(p):
    """
    Ha egy kék pont szürkére lép és annak az ertek > 0,
    akkor egy másik véletlenszerű szürke pont is kék lesz.
    """
    if p["color"] == (0, 0, 255) and p["ertek"] > 0:
        # szürke pontok listája
        gray_points = [x for x in points if x["color"] == (200, 200, 200)]
        if gray_points:
            extra_blue = random.choice(gray_points)
            extra_blue["color"] = (0, 0, 255)
            return extra_blue  # visszaadhatjuk az új kék pontot
    return None


           




# --- Játékállapot ---
click_count = 0
red_point = None
blue1_point = None
blue2_point = None
blue3_point= None

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

            # --- Piros vagy kék kör jön? ---
            if click_count % 2 == 1:
                target = "red"
            else:
                target = "blue"

            # --- Pontok vizsgálata ---
            for p in points:
                dx = mouse_pos[0] - p["pos"][0]
                dy = mouse_pos[1] - p["pos"][1]
                distance = math.hypot(dx, dy)

                # Rákattintottál-e a körre?
                if distance > p["point_radius"]:
                    continue

                # Szürkére vagy pirosra kattinthatsz
                if p["color"] != (200,200,200) and target != "red":
                    continue

                # =============================
                # ------- PIROS LÉP ---------
                # =============================
                if target == "red":

                    if red_point and p != red_point and not is_neighbor(red_point, p):
                        continue

                    # ha volt régi piros → visszaszürkül
                    if red_point and p != red_point:
                        red_point["color"] = (200,200,200)
                        red_point["status"] = 0

                    # új piros
                    red_point = p

                    # pontgyűjtés ha státusz 1 volt
                    if p["status"] == 1:
                        p["ertek"] += 1
                        if p["ertek"] >= p["goal"]:
                            p["point_radius"] = 25

                    p["status"] = 1
                    p["color"] = (255,0,0)

                # =============================
                # -------- KÉK LÉP ---------
                # =============================
                else:

                    # kék1 léphet?
                    kek1_valid = (blue1_point is None) or is_neighbor(blue1_point, p)

                    # kék2 léphet?
                    kek2_valid = (blue2_point is None) or is_neighbor(blue2_point, p)

                    #kek3 léphet?
                    kek3_valid = (blue3_point is None) or is_neighbor(blue3_point, p)

                    # melyik mozog?
                    if kek1_valid and not kek2_valid:
                        mover = "kek1"
                    elif kek2_valid and not kek1_valid:
                        mover = "kek2"
                    elif kek3_valid and not kek1_valid or kek2_valid:
                        mover = "kek3"
                    elif kek1_valid and kek2_valid and kek3_valid:
                        mover = "kek1"  # prioritás
                    else:
                        continue

                    # --- mozgatás ---
                    if mover == "kek1":
                        if blue1_point and p != blue1_point:
                            blue1_point["color"] = (200,200,200)

                        blue1_point = p
                        p["color"] = (0,0,255)
                        

                    else:  # kék2
                        if blue2_point and p != blue2_point:
                            blue2_point["color"] = (200,200,200)
                        blue2_point = p
                        p["color"] = (0,0,255)
                    
                    

                click_count += 1
                break

    # Háttér
    screen.fill((0, 0, 0))

    # Vonalak
    for start, end in lines:
        pygame.draw.line(screen, line_color, start, end, line_width)

    # Pontok
    for p in points:
        pygame.draw.circle(screen, p["color"], p["pos"], p["point_radius"])
        txt = f"{p['label']} ({p['ertek']}) st:{p['status']}"
        label_surface = font.render(txt, True, (255, 255, 255))
        label_rect = label_surface.get_rect(center=(p["pos"][0], p["pos"][1] - p["point_radius"] - 10))
        screen.blit(label_surface, label_rect)

    # Click counter
    counter_surface = font.render(f"Kattintások: {click_count}", True, (255, 255, 0))
    screen.blit(counter_surface, (150, 10))

    pygame.display.flip()

pygame.quit()
sys.exit()
