import pygame
import sys
import grid_io as gr
import game_logic as gl
import display as disp

def main():
    rows,cols = 40,40
    cell = 20
    speed = 0.1
    running = False
    gen = 0

    screen_type = disp.SCREEN_MAIN_MENU
    shape = disp.SHAPE_SQUARE
    color_id = 0

    grid = gr.random_grid(rows,cols,0.3)

    screen,clock,w,h = disp.init_display(0,0)
    disp.load_music()
    bg = disp.load_background(screen)

    while True:
        if screen_type == disp.SCREEN_MAIN_MENU:
            buttons = disp.create_buttons(["Играть","Выход"],w,300)

        elif screen_type == disp.SCREEN_SHAPE_SELECT:
            buttons = disp.create_buttons(list(disp.SHAPE_NAMES.values()),w)

        elif screen_type == disp.SCREEN_COLOR_SELECT:
            buttons = disp.create_buttons([c[0] for c in disp.COLOR_SCHEMES],w)

        else:
            buttons = []

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

                if screen_type == disp.SCREEN_GAME:
                    if e.key == pygame.K_SPACE:
                        running = not running

                    elif e.key == pygame.K_s or e.key == pygame.K_RIGHT:
                        grid = gl.next_generation(grid)
                        gen += 1

                    elif e.key == pygame.K_r:
                        grid = gr.random_grid(rows,cols)
                        gen = 0
                        running = False

                    elif e.key == pygame.K_c:
                        grid = gr.create_empty_grid(rows,cols)
                        gen = 0
                        running = False

                    elif e.key == pygame.K_l:
                        try:
                            grid = gr.load_grid_from_file("save.txt")
                            rows,cols = len(grid),len(grid[0])
                            screen,clock,w,h = disp.init_display(rows,cols,cell)
                            gen = 0
                            running = False
                        except:
                            pass

                    elif e.key == pygame.K_f:
                        try:
                            gr.save_grid_to_file(grid,"save.txt")
                        except:
                            pass

                    elif e.key == pygame.K_EQUALS or e.key == pygame.K_PLUS:
                        speed = max(0.01, speed - 0.02)

                    elif e.key == pygame.K_MINUS:
                        speed = min(1.0, speed + 0.02)

            if screen_type != disp.SCREEN_GAME:
                for b in buttons:
                    if b.handle(e):
                        if screen_type == disp.SCREEN_MAIN_MENU:
                            if b.text == "Играть":
                                screen_type = disp.SCREEN_SHAPE_SELECT
                            else:
                                pygame.quit()
                                sys.exit()

                        elif screen_type == disp.SCREEN_SHAPE_SELECT:
                            for k,v in disp.SHAPE_NAMES.items():
                                if v == b.text:
                                    shape = k
                                    screen_type = disp.SCREEN_COLOR_SELECT

                        elif screen_type == disp.SCREEN_COLOR_SELECT:
                            for i,c in enumerate(disp.COLOR_SCHEMES):
                                if c[0] == b.text:
                                    color_id = i
                                    a,d,g = c[1],c[2],c[3]
                                    disp.handle_color_scheme(a,d,g)
                                    screen,clock,w,h = disp.init_display(rows,cols,cell)
                                    grid = gr.random_grid(rows,cols,0.3)
                                    gen = 0
                                    running = False
                                    screen_type = disp.SCREEN_GAME

        if screen_type == disp.SCREEN_GAME and running:
            grid = gl.next_generation(grid)
            gen += 1
            pygame.time.delay(int(speed*1000))

        if screen_type == disp.SCREEN_MAIN_MENU:
            if bg:
                screen.blit(bg,(0,0))
            else:
                screen.fill((20,20,40))
            for b in buttons:
                b.draw(screen)

        elif screen_type == disp.SCREEN_SHAPE_SELECT:
            screen.fill((30,30,50))
            for b in buttons:
                b.draw(screen)

        elif screen_type == disp.SCREEN_COLOR_SELECT:
            screen.fill((30,30,50))
            for b in buttons:
                b.draw(screen)

        elif screen_type == disp.SCREEN_GAME:
            screen.fill((0,0,0))
            disp.draw_grid(screen,grid,shape)
            disp.draw_ui(screen,gen,speed,running)

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()