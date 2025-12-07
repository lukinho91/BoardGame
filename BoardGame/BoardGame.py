import pygame
import sys
import math
import random
import sqlite3
from datetime import datetime

# ========================
#      ADATBÁZIS
# ========================
conn = sqlite3.connect("game.db")
c = conn.cursor()

c.execute("DROP TABLE IF EXISTS points")
c.execute("DROP TABLE IF EXISTS moves")
c.execute("DROP TABLE IF EXISTS positions")

c.execute('''CREATE TABLE points (
    id INTEGER PRIMARY KEY,
    label TEXT
)''')

c.execute('''CREATE TABLE moves (
    id INTEGER PRIMARY KEY,
    timestamp TEXT,
    player TEXT,
    from_point_id INTEGER,
    point_id INTEGER,
    new_color TEXT,
    new_ertek INTEGER
)''')

c.execute('''CREATE TABLE positions (
    point_id INTEGER,
    timestamp TEXT,
    x INTEGER,
    y INTEGER,
    color TEXT,
    ertek INTEGER,
    radius INTEGER,
    move_id INTEGER
)''')
conn.commit()

# ========================
#       PYGAME
# ========================
pygame.init()
screen = pygame.display.set_mode((1000, 700))
pygame.display.set_caption("Kattintható pontok – piros + 3 kék")
line_color = (0, 255, 0)
line_width = 2
font = pygame.font.SysFont("Arial", 18)

# ========================
#        PONTOK
# ========================
points = [
    {"id":0, "pos":[50,50], "label":"Müpa", "color":(200,200,200), "ertek":0, "point_radius":15, "status":0},
    {"id":1, "pos":[350,50], "label":"Deák", "color":(200,200,200), "ertek":0, "point_radius":15, "status":0},
    {"id":2, "pos":[50,350], "label":"Blaha", "color":(200,200,200), "ertek":0, "point_radius":15, "status":0},
    {"id":3, "pos":[350,350], "label":"Astoria", "color":(200,200,200), "ertek":0, "point_radius":15, "status":0},
    {"id":4, "pos":[200,200], "label":"Corvin", "color":(200,200,200), "ertek":0, "point_radius":15, "status":0},
    {"id":5, "pos":[450,400], "label":"Parlament", "color":(200,200,200), "ertek":0, "point_radius":15, "status":0},
    {"id":6, "pos":[450,650], "label":"BME", "color":(200,200,200), "ertek":0, "point_radius":15, "status":0},
    {"id":7, "pos":[600,400], "label":"ELTE", "color":(200,200,200), "ertek":0, "point_radius":15, "status":0},
    {"id":8, "pos":[600,300], "label":"Újpest", "color":(200,200,200), "ertek":0, "point_radius":15, "status":0},
    {"id":9, "pos":[50,500], "label":"Kispest", "color":(200,200,200), "ertek":0, "point_radius":15, "status":0},
    {"id":10,"pos":[200,400], "label":"Puskás", "color":(200,200,200), "ertek":0, "point_radius":15, "status":0},
    {"id":11,"pos":[350,500], "label":"Rendőrség", "color":(200,200,200), "ertek":0, "point_radius":15, "status":0},
]

for p in points:
    c.execute("INSERT INTO points (id,label) VALUES (?,?)",(p["id"],p["label"]))
    color_str = ','.join(map(str,p["color"]))
    c.execute("INSERT INTO positions (point_id,timestamp,x,y,color,ertek,radius,move_id) VALUES (?,?,?,?,?,?,?,?)",
              (p["id"], datetime.now().isoformat(), p["pos"][0], p["pos"][1], color_str, p["ertek"], p["point_radius"], None))
conn.commit()

# ========================
#        VONALAK
# ========================
lines = [
    (points[0]["pos"], points[1]["pos"]), (points[0]["pos"], points[2]["pos"]),
    (points[1]["pos"], points[3]["pos"]), (points[2]["pos"], points[3]["pos"]),
    (points[4]["pos"], points[0]["pos"]), (points[9]["pos"], points[6]["pos"]),
    (points[6]["pos"], points[7]["pos"]), (points[1]["pos"], points[8]["pos"]),
    (points[4]["pos"], points[10]["pos"]), (points[5]["pos"], points[10]["pos"]),
    (points[4]["pos"], points[3]["pos"]), (points[2]["pos"], points[9]["pos"]),
    (points[10]["pos"], points[9]["pos"]), (points[7]["pos"], points[8]["pos"]),
    (points[7]["pos"], points[5]["pos"]), (points[11]["pos"], points[5]["pos"])
]

def is_neighbor(p1,p2):
    for start,end in lines:
        if (start==p1["pos"] and end==p2["pos"]) or (start==p2["pos"] and end==p1["pos"]):
            return True
    return False

# ========================
#      KEZDETI KÉKEK
# ========================
initial_gray_points = [p for i,p in enumerate(points) if p["color"]==(200,200,200) and i!=10]
blue1 = random.choice(initial_gray_points); blue1["color"]=(0,0,255); initial_gray_points.remove(blue1)
blue2 = random.choice(initial_gray_points); blue2["color"]=(0,0,255); initial_gray_points.remove(blue2)
blue3 = None
extra_blue_used = False
goal = 4

# ========================
#      JÁTÉKÁLLAPOT
# ========================
click_count = 0
red_point = None
active_blue = None

# ========================
#      HARMADIK KÉK
# ========================
def add_third_blue(p):
    global blue3, extra_blue_used
    if extra_blue_used or blue3 is not None: return
    if p["ertek"]>0:
        blue3 = points[11]
        blue3["color"]=(0,0,255)
        extra_blue_used=True
        print("Harmadik kék létrejött:", blue3["label"])
        color_str = ','.join(map(str,blue3["color"]))
        c.execute("INSERT INTO positions (point_id,timestamp,x,y,color,ertek,radius,move_id) VALUES (?,?,?,?,?,?,?,?)",
                  (blue3["id"], datetime.now().isoformat(), blue3["pos"][0], blue3["pos"][1],
                   color_str, blue3["ertek"], blue3["point_radius"], None))
        conn.commit()

# ========================
#       FŐ CIKLUS
# ========================
running = True
while running:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
        if event.type==pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            target = "red" if click_count%2==0 else "blue"

            for p in points:
                dx = mouse_pos[0]-p["pos"][0]; dy = mouse_pos[1]-p["pos"][1]
                if math.hypot(dx,dy)>p["point_radius"]: continue

                from_point_id = None

                # --- PIROS ---
                if target=="red":
                    if red_point and p!=red_point and not is_neighbor(red_point,p): continue
                    if red_point and p!=red_point: red_point["color"]=(200,200,200)
                    from_point_id = red_point["id"] if red_point else None
                    red_point = p
                    red_point["color"]=(255,0,0)

                    if p.get("status",0)==1:
                        p["ertek"] += 1
                        if p["ertek"] >= goal:
                            p["point_radius"] = 25
                    p["status"]=1
                    click_count += 1

                    # Mentés moves és positions
                    color_str = ','.join(map(str,p["color"]))
                    c.execute("INSERT INTO moves (timestamp,player,from_point_id,point_id,new_color,new_ertek) VALUES (?,?,?,?,?,?)",
                              (datetime.now().isoformat(),"red",from_point_id,p["id"],color_str,p["ertek"]))
                    move_id = c.lastrowid
                    c.execute("INSERT INTO positions (point_id,timestamp,x,y,color,ertek,radius,move_id) VALUES (?,?,?,?,?,?,?,?)",
                              (p["id"], datetime.now().isoformat(), p["pos"][0], p["pos"][1], color_str, p["ertek"], p["point_radius"], move_id))
                    conn.commit()
                    break

                # --- KÉK ---
                else:
                    if p["color"]==(0,0,255):
                        active_blue = p; p["color"]=(0,150,255); break
                    if active_blue is None: continue
                    if not is_neighbor(active_blue,p): continue
                    from_point_id = active_blue["id"]
                    active_blue["color"]=(200,200,200)
                    add_third_blue(p)
                    p["color"]=(0,0,255); active_blue=p; click_count+=1

                    color_str = ','.join(map(str,p["color"]))
                    c.execute("INSERT INTO moves (timestamp,player,from_point_id,point_id,new_color,new_ertek) VALUES (?,?,?,?,?,?)",
                              (datetime.now().isoformat(),"blue",from_point_id,p["id"],color_str,p["ertek"]))
                    move_id = c.lastrowid
                    c.execute("INSERT INTO positions (point_id,timestamp,x,y,color,ertek,radius,move_id) VALUES (?,?,?,?,?,?,?,?)",
                              (p["id"], datetime.now().isoformat(), p["pos"][0], p["pos"][1], color_str, p["ertek"], p["point_radius"], move_id))
                    conn.commit()
                    break

    # --- RAJZOLÁS ---
    screen.fill((0,0,0))
    for start,end in lines: pygame.draw.line(screen,line_color,start,end,line_width)
    for p in points:
        pygame.draw.circle(screen,p["color"],p["pos"],p["point_radius"])
        label_surface = font.render(f"{p['label']} ({p['ertek']})", True,(255,255,255))
        label_rect = label_surface.get_rect(center=(p["pos"][0],p["pos"][1]-p["point_radius"]-10))
        screen.blit(label_surface,label_rect)

    counter_surface = font.render(f"Kattintások: {click_count}",True,(255,255,0))
    screen.blit(counter_surface,(150,10))

    pygame.display.flip()

pygame.quit()
conn.close()
sys.exit()