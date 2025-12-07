import pygame
import sys
import random

pygame.init()

# --- Ablak ---
screen = pygame.display.set_mode((700, 700))
pygame.display.set_caption("Kattintható pontok – rácsos, összefüggő")
line_color = (0, 255, 0)
line_width = 2
font = pygame.font.SysFont("Arial", 18)

# --- Beállítások ---
rows = 4
cols = 4
spacing = 150
max_blue = 3
point_radius = 20

# --- Csúcsok létrehozása rácsban ---
nodes = []
for i in range(rows):
    for j in range(cols):
        node = {
            "id": i*cols + j,
            "pos": (100 + j*spacing, 100 + i*spacing),
            "color": (0, 0, 255),
            "label": f"P{i*cols+j+1}",
            "ertek": 0,
            "point_radius": point_radius,
            "edges": 0,
            "max_edges": random.choice([2,3])
        }
        nodes.append(node)

# --- Szomszédsági függvény ---
def get_neighbors(node, all_nodes):
    x, y = node["pos"]
    neighbors = []
    for n in all_nodes:
        if n != node and ((abs(n["pos"][0]-x) == spacing and n["pos"][1]==y) or (abs(n["pos"][1]-y) == spacing and n["pos"][0]==x)):
            neighbors.append(n)
    return neighbors

# --- Élek generálása ---
lines = []

# Először minden csúcsnak legalább 2 él
for node in nodes:
    neighbors = get_neighbors(node, nodes)
    random.shuffle(neighbors)
    for neighbor in neighbors:
        if node["edges"] < 2 and neighbor["edges"] < neighbor["max_edges"] and (node["pos"], neighbor["pos"]) not in lines and (neighbor["pos"], node["pos"]) not in lines:
            lines.append((node["pos"], neighbor["pos"]))
            node["edges"] += 1
            neighbor["edges"] += 1

# További élek maximumig
for node in nodes:
    neighbors = get_neighbors(node, nodes)
    random.shuffle(neighbors)
    for neighbor in neighbors:
        if node["edges"] < node["max_edges"] and neighbor["edges"] < neighbor["max_edges"] and (node["pos"], neighbor["pos"]) not in lines:
            if random.random() < 0.5:
                lines.append((node["pos"], neighbor["pos"]))
                node["edges"] += 1
                neighbor["edges"] += 1

# --- Fő ciklus ---
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for node in nodes:
                dx = mouse_pos[0] - node["pos"][0]
                dy = mouse_pos[1] - node["pos"][1]
                if (dx**2 + dy**2) <= node["point_radius"]**2:
                    node["color"] = (255, 0, 0)

    # --- Kék pontok korlátozása ---
    blue_nodes = [n for n in nodes if n["color"] == (0,0,255)]
    if len(blue_nodes) > max_blue:
        for n in blue_nodes[max_blue:]:
            n["color"] = (200,200,200)

    # --- Rajzolás ---
    screen.fill((0,0,0))
    for start, end in lines:
        pygame.draw.line(screen, line_color, start, end, line_width)
    for node in nodes:
        pygame.draw.circle(screen, node["color"], node["pos"], node["point_radius"])
        txt = f"{node['label']} ({node['ertek']})"
        label_surface = font.render(txt, True, (255,255,255))
        label_rect = label_surface.get_rect(center=(node["pos"][0], node["pos"][1]-node["point_radius"]-10))
        screen.blit(label_surface, label_rect)

    pygame.display.flip()

pygame.quit()
sys.exit()