# main.py
import pygame
import sys
import grid_io as gr
import game_logic as gl
import display as disp

def main():
    # ========== НАСТРОЙКИ ==========
    rows, cols = 40, 40  # размер сетки
    cell_size = 20        # размер клетки в пикселях
    speed = 0.1           # скорость (задержка между поколениями в секундах)
    running = False       # флаг автоматической симуляции
    generation = 0        # номер текущего поколения
    drawing = False       # флаг для рисования мышкой
    current_tool = 1      # 1 - рисовать живые, 0 - рисовать мертвые
    
    # ========== ИНИЦИАЛИЗАЦИЯ ==========
    # Создаем начальную сетку (случайное заполнение)
    grid = gr.random_grid(rows, cols, prob=0.3)
    
    # Настраиваем цвета
    disp.handle_color_scheme(
        alive_color=(255, 255, 255),  # Белые живые
        dead_color=(0, 0, 0),         # Черные мертвые
        grid_color=(60, 60, 60),      # Серые линии
        text_color=(0, 255, 0)        # Зеленый текст
    )
    
    # Инициализируем дисплей
    screen, clock, width, height = disp.init_display(rows, cols, cell_size)
    
    # Для сохранения/загрузки файлов
    current_file = "save.txt"
    
    print("Игра 'Жизнь' запущена!")
    print("Управление:")
    print("  SPACE - пуск/пауза")
    print("  S - шаг (одно поколение)")
    print("  R - сброс к случайной конфигурации")
    print("  C - очистить всё")
    print("  L - загрузить из файла")
    print("  F - сохранить в файл")
    print("  +/- - увеличить/уменьшить скорость")
    print("  Левая кнопка мыши - нарисовать живую клетку")
    print("  Правая кнопка мыши - нарисовать мертвую клетку")
    print("  Q - выход")
    print("-" * 50)
    
    # ========== ГЛАВНЫЙ ЦИКЛ ==========
    while True:
        # ========== ОБРАБОТКА СОБЫТИЙ ==========
        for event in pygame.event.get():
            # Выход из программы
            if event.type == pygame.QUIT:
                disp.cleanup()
                sys.exit()
            
            # Обработка нажатий клавиш
            if event.type == pygame.KEYDOWN:
                # Выход по Q
                if event.key == pygame.K_q:
                    disp.cleanup()
                    sys.exit()
                
                # Пробел - пуск/пауза
                elif event.key == pygame.K_SPACE:
                    running = not running
                    print(f"{'Запущено' if running else 'Пауза'}")
                
                # S - шаг (одно поколение)
                elif event.key == pygame.K_s:
                    if not running:  # Работает только на паузе
                        grid = gl.next_generation(grid)
                        generation += 1
                        print(f"Шаг: поколение {generation}")
                
                # R - сброс к случайной конфигурации
                elif event.key == pygame.K_r:
                    grid = gr.random_grid(rows, cols, prob=0.3)
                    generation = 0
                    running = False
                    print("Сброс к случайной конфигурации")
                
                # C - очистить всё
                elif event.key == pygame.K_c:
                    grid = gr.create_empty_grid(rows, cols)
                    generation = 0
                    running = False
                    print("Сетка очищена")
                
                # L - загрузить из файла
                elif event.key == pygame.K_l:
                    try:
                        grid = gr.load_grid_from_file(current_file)
                        # Обновляем размеры сетки
                        rows = len(grid)
                        cols = len(grid[0]) if rows > 0 else 0
                        generation = 0
                        running = False
                        print(f"Загружено из файла {current_file}")
                    except FileNotFoundError:
                        print(f"Файл {current_file} не найден")
                    except Exception as e:
                        print(f"Ошибка загрузки: {e}")
                
                # F - сохранить в файл
                elif event.key == pygame.K_f:
                    try:
                        gr.save_grid_to_file(grid, current_file)
                        print(f"Сохранено в файл {current_file}")
                    except Exception as e:
                        print(f"Ошибка сохранения: {e}")
                
                # + (плюс) - увеличить скорость (уменьшить задержку)
                elif event.key == pygame.K_EQUALS or event.key == pygame.K_PLUS:
                    speed = max(0.05, speed - 0.05)
                    print(f"Скорость: {speed:.2f}с")
                
                # - (минус) - уменьшить скорость (увеличить задержку)
                elif event.key == pygame.K_MINUS:
                    speed = min(1.0, speed + 0.05)
                    print(f"Скорость: {speed:.2f}с")
            
            # Обработка мыши
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Получаем клетку под мышью
                cell = disp.get_cell_from_mouse(event.pos, cell_size, rows, cols)
                if cell:
                    row, col = cell
                    if event.button == 1:  # Левая кнопка - живая
                        gr.set_cell(grid, row, col, 1)
                        current_tool = 1
                        drawing = True
                    elif event.button == 3:  # Правая кнопка - мертвая
                        gr.set_cell(grid, row, col, 0)
                        current_tool = 0
                        drawing = True
            
            elif event.type == pygame.MOUSEBUTTONUP:
                drawing = False
            
            elif event.type == pygame.MOUSEMOTION and drawing:
                # Рисование при зажатой кнопке
                cell = disp.get_cell_from_mouse(event.pos, cell_size, rows, cols)
                if cell:
                    row, col = cell
                    gr.set_cell(grid, row, col, current_tool)
        
        # ========== ЛОГИКА ИГРЫ ==========
        if running:
            # Вычисляем следующее поколение
            grid = gl.next_generation(grid)
            generation += 1
            
            # Небольшая задержка для визуализации
            pygame.time.delay(int(speed * 1000))
        
        # ========== ОТРИСОВКА ==========
        # Очищаем экран
        screen.fill((0, 0, 0))
        
        # Рисуем сетку
        disp.draw_grid(screen, grid, generation, speed)
        
        # Обновляем экран
        pygame.display.flip()
        
        # Ограничиваем FPS
        clock.tick(60)

if __name__ == "__main__":
    main()