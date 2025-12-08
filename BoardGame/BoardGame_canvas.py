import tkinter as tk
import math
import random

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
#       SEGÉDFÜGGVÉNYEK
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
    if p["ertek"]>0:
        blue3 = points[11]
        blue3["color"]=(0,0,255)
        extra_blue_used=True
        print("Harmadik kék létrejött:", blue3["label"])

def draw_points(canvas):
    canvas.delete("all")
    for start, end in lines:
        canvas.create_line(start[0]+15, start[1]+15, end[0]+15, end[1]+15, fill="green", width=2)
    for p in points:
        x, y = p["pos"]
        canvas.create_oval(x, y, x+p["point_radius"]*2, y+p["point_radius"]*2,
                           fill=color_to_hex(p["color"]), outline="black")
        canvas.create_text(x+p["point_radius"], y-5, text=f"{p['label']} ({p['ertek']})", fill="green")

# ========================
#       ESEMÉNY
# ========================
def on_click(event):
    global click_count, red_point, active_blue
    mouse_pos = (event.x, event.y)
    target = "red" if click_count%2==0 else "blue"

    for p in points:
        px, py = p["pos"]
        distance = math.hypot(mouse_pos[0]-px-p["point_radius"], mouse_pos[1]-py-p["point_radius"])
        if distance > p["point_radius"]: 
            continue

        # PIROS
        if target=="red":
            if red_point and p!=red_point and not is_neighbor(red_point,p): continue
            if red_point and p!=red_point: red_point["color"]=(200,200,200)
            red_point = p
            red_point["color"]=(255,0,0)
            if p.get("status",0)==1:
                p["ertek"] += 1
                if p["ertek"] >= goal:
                    p["point_radius"] = 25
            p["status"]=1
            click_count +=1

        # KÉK
        else:
            if p["color"]==(0,0,255):
                active_blue = p; p["color"]=(0,150,255); break
            if active_blue is None: continue
            if not is_neighbor(active_blue,p): continue
            active_blue["color"]=(200,200,200)
            add_third_blue(p)
            p["color"]=(0,0,255)
            active_blue = p
            click_count +=1
        break

# ========================
#       ABLAKOK
# ========================
window1 = tk.Tk()
window1.title("Pálya 1")
canvas1 = tk.Canvas(window1, width=700, height=700, bg="white")
canvas1.pack()

window2 = tk.Toplevel(window1)
window2.title("Pálya 2")
canvas2 = tk.Canvas(window2, width=700, height=700, bg="white")
canvas2.pack()

canvas1.bind("<Button-1>", on_click)
canvas2.bind("<Button-1>", on_click)

def refresh():
    draw_points(canvas1)
    draw_points(canvas2)
    window1.after(50, refresh)

refresh()
window1.mainloop()