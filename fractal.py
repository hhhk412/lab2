#Вычисление координаты следующей точки папоротника 
import random

def get_next_point(x: float, y: float) -> tuple[float, float]:
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
