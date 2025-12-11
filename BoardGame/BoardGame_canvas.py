import tkinter as tk
import math
import random
import sqlite3
import tkinter.messagebox as messagebox

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
    (points[7]["pos"], points[5]["pos"]), 
    #(points[11]["pos"], points[5]["pos"])
]

goal = 2
click_count = 0
red_point = None
active_blue = None
blue3 = None
extra_blue_used = False
kuldetes1 = None
kuldetes2 = None
kuldetes3 = None


# Kezdeti szürke pontok kivétele, kivéve a 12. elemet (index 11)
initial_gray_points = [p for i, p in enumerate(points) if p["color"] == (200,200,200) and i != 11]

# Két különböző kék pont kiválasztása
blue1, blue2 = random.sample(initial_gray_points, 2)

blue1["color"] = (0, 0, 255)
blue2["color"] = (0, 0, 255)


# ========================
# SEGÉDFÜGGVÉNYEK
# ========================

def show_rules():
    rules_window = tk.Toplevel()
    rules_window.title("Játékszabályok")
    rules_window.geometry("500x400")

    text = tk.Text(rules_window, wrap="word", font=("Arial", 12))
    text.pack(expand=True, fill="both")

    try:
        with open("szabalyok.txt", "r", encoding="utf-8") as f:
            rules = f.read()
    except FileNotFoundError:
        rules = "Nem található a rules.txt fájl!"

    text.insert("1.0", rules)
    text.config(state="disabled")


def kuldetes():
    global kuldetes1, kuldetes2, kuldetes3
    kuldetes1, kuldetes2, kuldetes3 = random.sample(initial_gray_points, 3)
    print(kuldetes1["label"], kuldetes2["label"], kuldetes3["label"])


def color_to_hex(c):
    if isinstance(c, tuple):
        return '#{:02x}{:02x}{:02x}'.format(*c)
    return c

def is_neighbor(p1, p2):
    for start, end in lines:
        if (start==p1["pos"] and end==p2["pos"]) or (start==p2["pos"] and end==p1["pos"]):
            return True
    return False


def add_police_line():
    if blue3 is not None:
        lines.append((points[11]["pos"], points[5]["pos"]))
        return


def add_third_blue(p):
    global blue3, extra_blue_used
    if extra_blue_used or blue3 is not None: return
    if p["ertek"]>0 and p["ertek"] != goal:
        blue3 =points[11]
        blue3["color"]=(0,0,255)
        extra_blue_used=True
        add_police_line()


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
        LIMIT 1 OFFSET 2
    """)
    row = c.fetchone()
    if row:
        x, y, ertek = row
        return [{"pos": [x, y], "ertek": ertek}]
    return []


def red_can_move():
    if not red_point:
        return True  # Ha még nincs piros pont, léphet
    for p in points:
        if p["color"] in [(0,0,255), (0,150,255)]:  # kék pontok
            continue
        if is_neighbor(red_point, p):
            return True
    return False  # nincs elérhető szomszéd

def check_red_blocked():
    if not red_can_move():
        messagebox.showinfo("Játék vége", "A Kék nyert!!", parent=window1)
        messagebox.showinfo("Játék vége", "A Kék nyert!!", parent=window2)
        return True
    return False

def game_ended():
    if ((kuldetes1["status"] == 2 and kuldetes2["status"] == 2) or
        (kuldetes1["status"] == 2 and kuldetes3["status"] == 2) or
        (kuldetes3["status"] == 2 and kuldetes2["status"] == 2)):
        
        # Pop-up mindkét ablakon
        messagebox.showinfo("Játék vége", "A Piros nyert!!", parent=window1)
        messagebox.showinfo("Játék vége", "A Piros nyert!!", parent=window2)
        
        return True
    return False

 

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
                p["status"] = 2

        # --- KÖR RAJZOLÁS ---
        canvas.create_oval(
            x-radius, y-radius, x+radius, y+radius,
            fill=color_to_hex(color), outline="black"
        )
        canvas.create_text(
            x, y-radius-10,
            text=f"{p['label']} ({p['ertek']})",
            fill="green"
        )


# ========================
#  KÉK MEGJELENÍTÉS
# ========================
def draw_blue(canvas):
    canvas.delete("all")

    # vonalak kirajzolása
    for start, end in lines:
        canvas.create_line(start[0], start[1], end[0], end[1], fill="green", width=2)

    # utolsó előtti piros pont betöltése DB-ből
    red_pos = get_penultimate_red_from_db()
    red_dict = {tuple(r["pos"]): r["ertek"] for r in red_pos}

    for p in points:
        x, y = p["pos"]
        radius = p["point_radius"]
        color = p["color"]

        # Ha a pont kék, vagy aktív kék
        if color == (0,0,255) or color == (0,150,255):
            if color == (0,150,255):
                radius += 5  # aktív kék nagyobb kör
        # Ha pont az utolsó előtti piros DB-ben és nem kék, marad piros
        elif tuple(p["pos"]) in red_dict:
            color = (255,0,0)
        # Egyébként szürke
        else:
            color = (200,200,200)

        canvas.create_oval(
            x-radius, y-radius, x+radius, y+radius,
            fill=color_to_hex(color), outline="black"
        )
        # Csak a label jelenik meg, sem érték, sem státusz
        canvas.create_text(
            x, y-radius-10,
            text=f"{p['label']}",
            fill="green"
        )
# ========================
#  REFRESH
# ========================
def refresh():

    draw_red(canvas1)
    draw_blue(canvas2)
    if check_red_blocked():
        return  # megállítja a piros lépését, mert a kék nyert
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
    moved = False  # <<< itt kell definiálni, minden esetben

    for p in points:
        px, py = p["pos"]
        distance = math.hypot(mouse_pos[0]-px, mouse_pos[1]-py)
        if distance > p["point_radius"]:
            continue

        # --- Nem lehet kék pontokra lépni ---
        if p["color"] == (0,0,255) or p["color"] == (0,150,255):
            continue

        # Ha piros már van és nem szomszédos, tovább
        if red_point and p != red_point and not is_neighbor(red_point, p):
            continue

        if red_point and p != red_point:
            red_point["color"] = (200,200,200)

        red_point = p
        red_point["color"] = (255,0,0)

        if game_ended():
            return

        if p.get("status", 0) == 1:
            p["ertek"] += 1
            if p["ertek"] >= goal:
                p["status"] = 2

        p["status"] = 1
        click_count += 1

        update_labels()
        insert_red_position(p)

        moved = True
        break

    # Ha nem tudott lépni a piros (minden szomszéd kék), kék nyert
    if not moved:
        messagebox.showinfo("Játék vége", "A Kék nyert!!", parent=window1)
        messagebox.showinfo("Játék vége", "A Kék nyert!!", parent=window2)

def on_click_blue(event):
    global click_count, active_blue

    if click_count % 2 != 1:
        return

    mouse_pos = (event.x, event.y)

    for p in points:
        px, py = p["pos"]
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

        if not is_neighbor(active_blue, p):
            continue

        #Kék rálép a piros jelenlegi pozíciójára → kék nyer
        last_red = get_red_positions_from_db()
        if last_red:
            red_x, red_y = last_red[0]["pos"]
            if p["pos"][0] == red_x and p["pos"][1] == red_y:
                messagebox.showinfo("Játék vége", "A Kék nyert!!", parent=window1)
                messagebox.showinfo("Játék vége", "A Kék nyert!!", parent=window2)
                return

        active_blue["color"] = (200,200,200)
        add_third_blue(p)

        p["color"] = (0,0,255)
        active_blue = p
        click_count += 1

        update_labels()
        break


# ========================
#  PIROS ABLAK
# ========================
window1 = tk.Tk()
window1.title("Piros-1")
kuldetes()
# Küldetés felirat
kuldetes_label = tk.Label(window1, text=f"Küldetés: {kuldetes1['label']} és {kuldetes2['label']} és {kuldetes3['label']}", font=("Arial", 12))
kuldetes_label.pack()

label_red = tk.Label(window1, text="Következő: Piros", font=("Arial",14))
label_red.pack()

bomb_button_red = tk.Button(window1, text="Játékszabályok", font=("Arial",12), command=show_rules)
bomb_button_red.pack()

canvas1 = tk.Canvas(window1, width=700, height=700, bg="white")
canvas1.pack()
canvas1.bind("<Button-1>", on_click_red)


# ========================
#  KÉK ABLAK
# ========================

window2 = tk.Toplevel(window1)
window2.title("Kék-2")

label_blue = tk.Label(window2, text="Következő: Piros", font=("Arial",14))
label_blue = tk.Label(window2, text="Következő: Piros", font=("Arial",14))
#current_target_label = tk.Label(window2, text="Célpont: ---", font=("Arial", 12))
label_blue.pack()

bomb_button_blue = tk.Button(window2, text="Játékszabályok", font=("Arial",12), command=show_rules)
bomb_button_blue.pack()

canvas2 = tk.Canvas(window2, width=700, height=700, bg="white")
canvas2.pack()


canvas1.bind("<Button-1>", on_click_red)
canvas2.bind("<Button-1>", on_click_blue)

refresh()
window1.mainloop()
conn.close()