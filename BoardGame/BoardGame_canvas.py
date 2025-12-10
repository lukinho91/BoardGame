import tkinter as tk
import math
import random
import sqlite3

# ========================
#       ADATBÁZIS
# ========================
conn = sqlite3.connect("game.db")
c = conn.cursor()

c.execute("DROP TABLE IF EXISTS red_positions")
c.execute("""
CREATE TABLE red_positions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    x INTEGER,
    y INTEGER,
    ertek INTEGER
)
""")
conn.commit()

# Fix első sor beszúrása
c.execute("INSERT INTO red_positions (x, y, ertek) VALUES (?, ?, ?)", (70, 130, 0))
conn.commit()

# ========================
#       PONTOK
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

goal = 2
click_count = 0
red_point = None
active_blue = None
blue3 = None
extra_blue_used = False

# Kezdeti kéket kiválasztjuk
initial_gray_points = [p for i,p in enumerate(points) if p["color"]==(200,200,200) and i!=10]
blue1 = random.choice(initial_gray_points); blue1["color"]=(0,0,255); initial_gray_points.remove(blue1)
blue2 = random.choice(initial_gray_points); blue2["color"]=(0,0,255); initial_gray_points.remove(blue2)


# ========================
# SEGÉDFÜGGVÉNYEK
# ========================
def color_to_hex(c):
    if isinstance(c, tuple):
        return '#{:02x}{:02x}{:02x}'.format(*c)
    return c

def is_neighbor(p1, p2):
    for start, end in lines:
        if (start==p1["pos"] and end==p2["pos"]) or (start==p2["pos"] and end==p1["pos"]):
            return True
    return False

def add_third_blue(p):
    global blue3, extra_blue_used
    if extra_blue_used or blue3 is not None: return
    if p["ertek"]>0 and p["ertek"] != goal:
        blue3 = points[11]
        blue3["color"]=(0,0,255)
        extra_blue_used=True

def insert_red_position(p):
    x, y = p["pos"]
    ertek = p["ertek"]
    c.execute("INSERT INTO red_positions (x, y, ertek) VALUES (?, ?, ?)", (x, y, ertek))
    conn.commit()

def get_red_positions_from_db():
    c.execute("""
        SELECT x, y, ertek
        FROM red_positions
        ORDER BY id DESC
        LIMIT 1
    """)

    row = c.fetchone()
    if row:
        x, y, ertek = row
        return [{"pos": [x,y], "ertek": ertek}]
    return []

def get_penultimate_red_from_db():
    c.execute("""
        SELECT x, y, ertek
        FROM red_positions
        ORDER BY id DESC
        LIMIT 1 OFFSET 1
    """)
    row = c.fetchone()
    if row:
        x, y, ertek = row
        return [{"pos": [x, y], "ertek": ertek}]
    return []


# ========================
#  PIROS MEGJELENÍTÉS
# ========================
def draw_red(canvas):
    canvas.delete("all")

    # vonalak
    for start, end in lines:
        canvas.create_line(start[0], start[1], end[0], end[1], fill="green", width=2)

    # legutóbbi piros
    red_pos = get_red_positions_from_db()
    red_dict = {tuple(r["pos"]): r["ertek"] for r in red_pos}

    for p in points:
        x, y = p["pos"]
        radius = p["point_radius"]

        # --- SZÍNKEZELÉS ---  
        color = p["color"]   # EREDETI SZÍN (kék is megmarad!)

        # Ha ez a pont a DB szerinti piros → átfestjük pirosra
        if tuple(p["pos"]) in red_dict:
            color = (255,0,0)
            p["ertek"] = red_dict[tuple(p["pos"])]
            if p["ertek"] >= goal:
                radius = 25

        # --- KÖR RAJZOLÁS ---
        canvas.create_oval(
            x-radius, y-radius, x+radius, y+radius,
            fill=color_to_hex(color), outline="black"
        )
        canvas.create_text(
            x, y-radius-5,
            text=f"{p['label']} ({p['ertek']})",
            fill="green"
        )


# ========================
#  KÉK MEGJELENÍTÉS
# ========================
def draw_blue(canvas):  # Kék pontok kirajzolása
    canvas.delete("all")  # Canvas törlése

    # vonalak kirajzolása
    for start, end in lines:
        canvas.create_line(start[0], start[1], end[0], end[1], fill="green", width=2)

    # utolsó előtti piros betöltése
    red_pos = get_penultimate_red_from_db()
    red_dict = {tuple(r["pos"]): r["ertek"] for r in red_pos}

    for p in points:
        x, y = p["pos"]
        radius = p["point_radius"]
        color = p["color"]

        # ----- KÉKEK ELŐNYBEN -----
        if color == (0,0,255) or color == (0,150,255):  # Ha kék pont, ne fessük pirosra
            if color == (0,150,255):
                radius += 5  # Aktív kék nagyobb kör
        else:
            # Csak szürke pontok esetén festjük pirosra DB alapján
            if tuple(p["pos"]) in red_dict:
                color = (255,0,0)
                radius = 25 if p["ertek"] >= goal else radius
            else:
                color = (200,200,200)  # Szürke pont

        canvas.create_oval(
            x-radius, y-radius, x+radius, y+radius,
            fill=color_to_hex(color), outline="black"
        )
        canvas.create_text(
            x, y-radius-5,
            text=f"{p['label']} ({p['ertek']})",
            fill="green"
        )

# ========================
#  REFRESH
# ========================
def refresh():
    draw_red(canvas1)
    draw_blue(canvas2)
    window1.after(50, refresh)

def update_labels():
    text = "Következő: Piros" if click_count % 2 == 0 else "Következő: Kék"
    label_red.config(text=text)
    label_blue.config(text=text)


# ========================
#       ESEMÉNYEK
# ========================
def on_click_red(event):
    global click_count, red_point

    if click_count % 2 != 0:
        return

    mouse_pos = (event.x, event.y)

    for p in points:
        px, py = p["pos"]
        center = (px, py)
        distance = math.hypot(mouse_pos[0]-px, mouse_pos[1]-py)
        if distance > p["point_radius"]:
            continue

        if red_point and p!=red_point and not is_neighbor(red_point,p):
            continue

        if red_point and p!=red_point:
            red_point["color"] = (200,200,200)

        red_point = p
        red_point["color"] = (255,0,0)

        if p.get("status",0)==1:
            p["ertek"] += 1
            if p["ertek"] >= goal:
                p["point_radius"] = 25

        p["status"]=1
        click_count += 1

        update_labels()

        # DB mentés
        insert_red_position(p)

        break


def on_click_blue(event):
    global click_count, active_blue
    
    if click_count % 2 != 1:
        return

    mouse_pos = (event.x, event.y)

    for p in points:
        px, py = p["pos"]
        center = (px, py)
        distance = math.hypot(mouse_pos[0]-px, mouse_pos[1]-py)
        if distance > p["point_radius"]:
            continue

        # kék kiválasztása
        if p["color"] == (0,0,255):
            active_blue = p
            p["color"] = (0,150,255)
            break

        if active_blue is None:
            continue

        if not is_neighbor(active_blue,p):
            continue

        active_blue["color"] = (200,200,200)
        add_third_blue(p)

        p["color"] = (0,0,255)
        active_blue = p
        click_count += 1

        update_labels()
        break


# ========================
#       ABLAKOK
# ========================
window1 = tk.Tk()
window1.title("Piros-1")

label_red = tk.Label(window1, text="Következő: Piros", font=("Arial",14))
label_red.pack()

canvas1 = tk.Canvas(window1, width=700, height=700, bg="white")
canvas1.pack()


window2 = tk.Toplevel(window1)
window2.title("Kék-2")

label_blue = tk.Label(window2, text="Következő: Piros", font=("Arial",14))
label_blue.pack()

canvas2 = tk.Canvas(window2, width=700, height=700, bg="white")
canvas2.pack()


canvas1.bind("<Button-1>", on_click_red)
canvas2.bind("<Button-1>", on_click_blue)

refresh()
window1.mainloop()
conn.close()