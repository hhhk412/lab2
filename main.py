import tkinter as tk
import settings.config as config
from core.fractal import get_next_point

# Инициализация окна
root = tk.Tk()
root.title("Фрактал: Папоротник Барнсли")
root.resizable(False, False)

canvas = tk.Canvas(
    root, 
    width=config.WIDTH, 
    height=config.HEIGHT, 
    bg=config.BG_COLOR, 
    highlightthickness=0
)
canvas.pack()

# Состояние анимации
x, y = 0.0, 0.0
total_points = 0
running = True

def draw_step():
    global x, y, total_points
    
    if not running:
        return

    # Отрисовка порции точек
    for _ in range(config.POINTS_PER_STEP):
        x, y = get_next_point(x, y)
        total_points += 1

        # Расчет экранных координат с использованием конфига
        screen_x = int(config.WIDTH / 2 + x * config.SCALE_X)
        screen_y = int(config.HEIGHT - y * config.SCALE_Y - config.OFFSET_Y)

        canvas.create_rectangle(
            screen_x, screen_y, 
            screen_x + 1, screen_y + 1, 
            fill=config.LEAF_COLOR, 
            outline=""
        )

    # Обновление счетчиков и инструкций на экране
    canvas.delete("info_text")
    canvas.create_text(
        15, 15,
        anchor="nw",
        text=f"Отрисовано точек: {total_points}",
        fill=config.TEXT_MAIN_COLOR,
        font=("Arial", 12),
        tags="info_text"
    )
    canvas.create_text(
        15, 40,
        anchor="nw",
        text="Пробел — Пауза/Старт | R — Перезапуск   :)",
        fill=config.TEXT_SUB_COLOR,
        font=("Arial", 10),
        tags="info_text"
    )

    root.after(config.DELAY_MS, draw_step)

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

# Привязка клавиш управления
root.bind("<space>", toggle_pause)
root.bind("<r>", reset_fractal)
root.bind("<R>", reset_fractal)

# Запуск
draw_step()
root.mainloop()
