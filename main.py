import tkinter as tk
import random

WIDTH = 800
HEIGHT = 700

root = tk.Tk()
root.title("Фрактал: Папоротник Барнсли")
root.resizable(False, False)

canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="black", highlightthickness=0)
canvas.pack()

x, y = 0.0, 0.0
total_points = 0
running = True

def get_next_point(x, y):
    r = random.random()

    if r < 0.01:
        next_x = 0.0
        next_y = 0.16 * y
    elif r < 0.86:
        next_x = 0.85 * x + 0.04 * y
        next_y = -0.04 * x + 0.85 * y + 1.6
    elif r < 0.93:
        next_x = 0.2 * x - 0.26 * y
        next_y = 0.23 * x + 0.22 * y + 1.6
    else:
        next_x = -0.15 * x + 0.28 * y
        next_y = 0.26 * x + 0.24 * y + 0.44
        
    return next_x, next_y

def draw_step():
    global x, y, total_points, running
    
    if not running:
        return

    for _ in range(150):
        x, y = get_next_point(x, y)
        total_points += 1

        screen_x = int(WIDTH / 2 + x * 90)
        screen_y = int(HEIGHT - y * 65 - 20)

        canvas.create_rectangle(screen_x, screen_y, screen_x + 1, screen_y + 1, fill="#39FF14", outline="")

    canvas.delete("info_text")
    canvas.create_text(
        15, 15,
        anchor="nw",
        text=f"Отрисовано точек: {total_points}",
        fill="white",
        font=("Arial", 12),
        tags="info_text"
    )
    canvas.create_text(
        15, 40,
        anchor="nw",
        text="Пробел — Пауза/Старт | R — Перезапуск   :)",
        fill="gray",
        font=("Arial", 10),
        tags="info_text"
    )

    root.after(10, draw_step)

def toggle_pause(event):
    global running
    running = not running
    if running:
        draw_step()

def reset_fractal(event):
    global x, y, total_points
    canvas.delete("all")
    x, y = 0.0, 0.0
    total_points = 0
    if not running:
        toggle_pause(None)
    else:
        draw_step()

root.bind("<space>", toggle_pause)
root.bind("<r>", reset_fractal)
root.bind("<R>", reset_fractal)

draw_step()
root.mainloop()

