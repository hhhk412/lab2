import tkinter as tk
import settings.config as config
from core.fractal import get_next_point

# Инициализация главного окна приложения
root = tk.Tk()
root.title("Фрактал: Папоротник Барнсли")
root.resizable(False, False)  # запрет изменения размера окна

# Создание холста для отрисовки фрактала
# размеры, фон и толщина рамки берутся из config
canvas = tk.Canvas(
    root, 
    width=config.WIDTH, 
    height=config.HEIGHT, 
    bg=config.BG_COLOR, 
    highlightthickness=0
)
canvas.pack()

# Состояние анимации:
# x, y — текущая точка в фрактальных координатах (старт из начала координат)
# total_points — сколько точек уже нарисовано (для счётчика)
# running — флаг: идёт ли сейчас отрисовка (пауза/старт)
x, y = 0.0, 0.0
total_points = 0
running = True

def draw_step():
    """
    Один шаг анимации. Рисует порцию новых точек фрактала
    и планирует следующий шаг через root.after.
    """
    global x, y, total_points
    
    # Если стоит пауза — просто выходим, ничего не рисуем
    if not running:
        return

    # Отрисовка порции точек (POINTS_PER_STEP штук за кадр)
    for _ in range(config.POINTS_PER_STEP):
        # Получаем следующую точку фрактала через игру в хаос
        x, y = get_next_point(x, y)
        total_points += 1

        # Перевод фрактальных координат в экранные:
        # X: центр окна + смещение, умноженное на масштаб
        # Y: от низа окна вверх (ось Y инвертирована), с учётом отступа
        screen_x = int(config.WIDTH / 2 + x * config.SCALE_X)
        screen_y = int(config.HEIGHT - y * config.SCALE_Y - config.OFFSET_Y)

        # Рисуем точку как прямоугольник 1x1 пиксель
        canvas.create_rectangle(
            screen_x, screen_y, 
            screen_x + 1, screen_y + 1, 
            fill=config.LEAF_COLOR, 
            outline=""
        )

    # Обновление текста на экране (счётчик и подсказки)
    # Сначала удаляем старый текст по тегу "info_text"
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

    # Планируем следующий шаг через DELAY_MS миллисекунд
    root.after(config.DELAY_MS, draw_step)

def toggle_pause(event):
    """
    Обработчик пробела: ставит/снимает паузу.
    При возобновлении — заново запускает цикл отрисовки.
    """
    global running
    running = not running
    if running:
        draw_step()

def reset_fractal(event):
    """
    Обработчик клавиши R: полный сброс фрактала.
    Очищает холст, обнуляет координаты и счётчик, запускает заново.
    """
    global x, y, total_points
    canvas.delete("all")
    x, y = 0.0, 0.0
    total_points = 0
    if not running:
        toggle_pause(None)  # если была пауза — снимаем её
    else:
        draw_step()

# Привязка клавиш управления
root.bind("<space>", toggle_pause)   # пробел — пауза/старт
root.bind("<r>", reset_fractal)      # r — перезапуск
root.bind("<R>", reset_fractal)      # R — перезапуск (заглавная)

# Запуск анимации и главного цикла приложения
draw_step()
root.mainloop()
