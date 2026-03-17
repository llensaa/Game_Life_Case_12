# display.py
import pygame
import pygame.font

# Константы цветов по умолчанию
DEFAULT_ALIVE_COLOR = (255, 255, 255)  # Белый
DEFAULT_DEAD_COLOR = (0, 0, 0)         # Черный
DEFAULT_GRID_COLOR = (40, 40, 40)      # Темно-серый
DEFAULT_TEXT_COLOR = (0, 255, 0)       # Зеленый
DEFAULT_UI_BG_COLOR = (20, 20, 20)     # Очень темный серый

# Глобальные переменные для хранения цветов (чтобы не передавать их в каждую функцию)
_alive_color = DEFAULT_ALIVE_COLOR
_dead_color = DEFAULT_DEAD_COLOR
_grid_color = DEFAULT_GRID_COLOR
_text_color = DEFAULT_TEXT_COLOR
_ui_bg_color = DEFAULT_UI_BG_COLOR

# Глобальные переменные для шрифтов
_font_small = None
_font_medium = None


def init_display(rows: int, cols: int, cell_size: int = 20, 
                 alive_color: tuple = DEFAULT_ALIVE_COLOR,
                 dead_color: tuple = DEFAULT_DEAD_COLOR,
                 grid_color: tuple = DEFAULT_GRID_COLOR) -> tuple:
    """
    Инициализирует окно Pygame, задаёт размеры.
    
    Args:
        rows: количество строк сетки
        cols: количество столбцов сетки
        cell_size: размер клетки в пикселях
        alive_color: цвет живой клетки (RGB)
        dead_color: цвет мертвой клетки (RGB)
        grid_color: цвет линий сетки (RGB)
    
    Returns:
        tuple: (экран pygame, объект часов pygame, ширина окна, высота окна)
    """
    global _alive_color, _dead_color, _grid_color, _font_small, _font_medium
    
    # Устанавливаем цвета
    _alive_color = alive_color
    _dead_color = dead_color
    _grid_color = grid_color
    
    # Инициализация Pygame
    pygame.init()
    pygame.font.init()
    
    # Создаем шрифты
    _font_small = pygame.font.Font(None, 24)
    _font_medium = pygame.font.Font(None, 32)
    
    # Вычисляем размеры окна
    # Добавляем место для UI снизу
    ui_height = 60
    width = cols * cell_size
    height = rows * cell_size + ui_height
    
    # Создаем окно
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Conway's Game of Life")
    
    # Создаем объект для управления временем
    clock = pygame.time.Clock()
    
    return screen, clock, width, height


def draw_grid(screen, grid: list[list[int]], generation: int, speed: float) -> None:
    """
    Отрисовывает всю сетку.
    
    Args:
        screen: поверхность pygame для отрисовки
        grid: текущее состояние сетки
        generation: номер текущего поколения
        speed: скорость симуляции (задержка между поколениями)
    """
    if not grid:
        return
    
    rows = len(grid)
    cols = len(grid[0])
    
    # Получаем размер окна и вычисляем размер клетки
    screen_width, screen_height = screen.get_size()
    cell_size = screen_width // cols
    
    # Отрисовываем клетки
    for row in range(rows):
        for col in range(cols):
            # Определяем цвет клетки
            color = _alive_color if grid[row][col] == 1 else _dead_color
            
            # Вычисляем координаты прямоугольника клетки
            x = col * cell_size
            y = row * cell_size
            
            # Рисуем клетку
            pygame.draw.rect(screen, color, (x, y, cell_size, cell_size))
    
    # Рисуем линии сетки
    for x in range(0, screen_width, cell_size):
        pygame.draw.line(screen, _grid_color, (x, 0), (x, screen_height - 60))
    
    for y in range(0, rows * cell_size, cell_size):
        pygame.draw.line(screen, _grid_color, (0, y), (screen_width, y))
    
    # Рисуем UI
    draw_ui(screen, generation, speed, False)  # running будет обновлен в main


def get_cell_from_mouse(pos: tuple[int, int], cell_size: int, rows: int, cols: int) -> tuple[int, int] | None:
    """
    По координатам мыши возвращает индексы клетки (row, col).
    
    Args:
        pos: координаты мыши (x, y)
        cell_size: размер клетки в пикселях
        rows: количество строк в сетке
        cols: количество столбцов в сетке
    
    Returns:
        tuple[int, int] | None: (row, col) или None, если клик вне сетки
    """
    x, y = pos
    
    # Проверяем, не выходит ли клик за пределы сетки
    if y >= rows * cell_size:
        return None
    
    # Вычисляем индексы клетки
    col = x // cell_size
    row = y // cell_size
    
    # Проверяем, что индексы в допустимых пределах
    if 0 <= row < rows and 0 <= col < cols:
        return (row, col)
    
    return None


def draw_ui(screen, generation: int, speed: float, running: bool) -> None:
    """
    Отрисовывает текстовую информацию (поколение, скорость, статус паузы).
    
    Args:
        screen: поверхность pygame для отрисовки
        generation: номер текущего поколения
        speed: скорость симуляции (задержка между поколениями)
        running: флаг запущена ли симуляция
    """
    global _font_small, _font_medium
    
    if _font_small is None or _font_medium is None:
        return
    
    screen_width, screen_height = screen.get_size()
    
    # Область для UI (нижняя панель)
    ui_rect = pygame.Rect(0, screen_height - 60, screen_width, 60)
    pygame.draw.rect(screen, _ui_bg_color, ui_rect)
    pygame.draw.line(screen, _grid_color, (0, screen_height - 60), 
                    (screen_width, screen_height - 60), 2)
    
    # Текст с номером поколения
    gen_text = f"Generation: {generation}"
    gen_surface = _font_medium.render(gen_text, True, _text_color)
    gen_rect = gen_surface.get_rect()
    gen_rect.topleft = (10, screen_height - 50)
    screen.blit(gen_surface, gen_rect)
    
    # Текст со скоростью
    speed_text = f"Speed: {speed:.2f}s"
    speed_surface = _font_medium.render(speed_text, True, _text_color)
    speed_rect = speed_surface.get_rect()
    speed_rect.topleft = (10, screen_height - 25)
    screen.blit(speed_surface, speed_rect)
    
    # Статус симуляции
    status_text = "RUNNING" if running else "PAUSED"
    status_color = (0, 255, 0) if running else (255, 255, 0)
    status_surface = _font_medium.render(status_text, True, status_color)
    status_rect = status_surface.get_rect()
    status_rect.topright = (screen_width - 10, screen_height - 50)
    screen.blit(status_surface, status_rect)
    
    # Подсказки по управлению (можно добавить)
    if not running:
        hint_text = "SPACE: Start | S: Step | R: Reset | C: Clear | L: Load | F: Save | +/-: Speed"
        hint_surface = _font_small.render(hint_text, True, (150, 150, 150))
        hint_rect = hint_surface.get_rect()
        hint_rect.center = (screen_width // 2, screen_height - 15)
        screen.blit(hint_surface, hint_rect)


def handle_color_scheme(alive_color: tuple, dead_color: tuple, grid_color: tuple, 
                        text_color: tuple = None, ui_bg_color: tuple = None) -> None:
    """
    Настройка цветов интерфейса.
    
    Args:
        alive_color: цвет живой клетки (RGB)
        dead_color: цвет мертвой клетки (RGB)
        grid_color: цвет линий сетки (RGB)
        text_color: цвет текста (RGB)
        ui_bg_color: цвет фона UI панели (RGB)
    """
    global _alive_color, _dead_color, _grid_color, _text_color, _ui_bg_color
    
    _alive_color = alive_color
    _dead_color = dead_color
    _grid_color = grid_color
    
    if text_color:
        _text_color = text_color
    
    if ui_bg_color:
        _ui_bg_color = ui_bg_color


def draw_with_custom_cell_size(screen, grid: list[list[int]], cell_size: int, 
                               generation: int, speed: float) -> None:
    """
    Альтернативная функция отрисовки с возможностью указать размер клетки.
    Полезно для изменения масштаба.
    
    Args:
        screen: поверхность pygame для отрисовки
        grid: текущее состояние сетки
        cell_size: размер клетки в пикселях
        generation: номер текущего поколения
        speed: скорость симуляции
    """
    if not grid:
        return
    
    rows = len(grid)
    cols = len(grid[0])
    
    # Отрисовываем клетки
    for row in range(rows):
        for col in range(cols):
            color = _alive_color if grid[row][col] == 1 else _dead_color
            x = col * cell_size
            y = row * cell_size
            pygame.draw.rect(screen, color, (x, y, cell_size, cell_size))
    
    # Рисуем линии сетки
    grid_width = cols * cell_size
    grid_height = rows * cell_size
    
    for x in range(0, grid_width + 1, cell_size):
        pygame.draw.line(screen, _grid_color, (x, 0), (x, grid_height))
    
    for y in range(0, grid_height + 1, cell_size):
        pygame.draw.line(screen, _grid_color, (0, y), (grid_width, y))
    
    # Рисуем UI
    draw_ui(screen, generation, speed, False)


def cleanup() -> None:
    """Завершает работу с Pygame (освобождает ресурсы)."""
    pygame.quit()