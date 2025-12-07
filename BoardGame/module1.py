import pygame
import sys
import math

pygame.init()

# --- Ablak ---
screen = pygame.display.set_mode((700, 700))
pygame.display.set_caption("Kattintható pontok – piros + kék + zöld")

# --- Beállítások ---
line_color = (0, 255, 0)
line_width = 2
font = pygame.font.SysFont("Arial", 18)

# --- Pontok ---
points = [
    {"id": 1, "pos": [50, 50], "color": (200, 200, 200), "label": "Müpa", "activate": False},
    {"id": 2, "pos": [350, 50], "color": (200, 200, 200), "label": "Deák", "activate": False},
    {"id": 3, "pos": [50, 350], "color": (200, 200, 200), "label": "Blaha", "activate": False},
    {"id": 4, "pos": [350, 350], "color": (200, 200, 200), "label": "Astoria", "activate": False},
    {"id": 5, "pos": [200, 200], "color": (200, 200, 200), "label": "Corvin", "activate": False},
    {"id": 6, "pos": [450, 400], "color": (200, 200, 200), "label": "Parlament", "activate": False},
    {"id": 7, "pos": [450, 650], "color": (200, 200, 200), "label": "BME", "activate": False},
    {"id": 8, "pos": [600, 400], "color": (200, 200, 200), "label": "ELTE", "activate": False},
    {"id": 9, "pos": [600, 300], "color": (200, 200, 200), "label": "Újpest", "activate": False},
    {"id": 10, "pos": [50, 500], "color": (200, 200, 200), "label": "Kispest", "activate": False},
    {"id": 11, "pos": [200, 400], "color": (200, 200, 200), "label": "Puskás", "activate": False},
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


# --- Játékállapot ---
click_count = 0
red_point = None
blue1_point = None
blue2_point = None
blue3_point= None





# --- Függvény: szomszédok ID-ja ---
def get_neighbors_ids(point):
    neighbors = []
    for start, end in lines:
        if start == point["pos"]:
            for p in points:
                if p["pos"] == end:
                    neighbors.append(p["id"])

        elif end == point["pos"]:
            for p in points:
                if p["pos"] == start:
                    neighbors.append(p["id"])
    return neighbors

# --- Játék fő ciklus ---
click_count = 0
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


        # --- Piros vagy kék kör jön? ---
        if click_count % 2 == 1:
            target = "red"
        else:
            target = "blue"


        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for p in points:
                dx = mouse_pos[0] - p["pos"][0]
                dy = mouse_pos[1] - p["pos"][1]
                distance = math.hypot(dx, dy)

                if distance < 15:  # pont sugar
                    p["activate"] = True


        
                # Szürkére vagy pirosra kattinthatsz
                if p["color"] != (200,200,200) and target != "red":
                    continue

                if p["color"] == (0,0,255):
                    p["activate"] = True  # itt a helyes értékadás
                    print(p["label"], "activated")
                    






                    # szomszédok ID
                    neighbor_ids = get_neighbors_ids(p)
                    print(f"A {p['label']} szomszédainak ID-i: {neighbor_ids}")

                    click_count += 1
                    break  # csak egy pontot kattintunk egyszerre

    # --- Rajzolás ---
    screen.fill((0, 0, 0))

    # vonalak
    for start, end in lines:
        pygame.draw.line(screen, line_color, start, end, line_width)

    # pontok
    for p in points:
        pygame.draw.circle(screen, p["color"], p["pos"], 15)
        txt = f"{p['label']}"
        label_surface = font.render(txt, True, (255, 255, 255))
        label_rect = label_surface.get_rect(center=(p["pos"][0], p["pos"][1] - 20))
        screen.blit(label_surface, label_rect)

    # click counter
    counter_surface = font.render(f"Kattintások: {click_count}", True, (255, 255, 0))
    screen.blit(counter_surface, (10, 10))

    pygame.display.flip()

pygame.quit()
sys.exit()