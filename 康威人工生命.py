import pygame
import objects
from random import randint
import numpy as np
import numba 

#主程式變數
running = True
playing = False
game_status = 0
tick = 0
dashboard = 0
teams = 2
teams_num = [0, 0, 0, 0, 0, 0, 0, 0]
reinforcement = [1, 0, 0, 0, 0, 0, 0, 0]
size = 10
color = 0
reset = 0

#主畫面
pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
width = screen.get_width()//size
height = screen.get_height()//size
pygame.display.set_caption("Conway's Game of Life")

#主視窗
bg = pygame.Surface(screen.get_size())
bg.fill((0, 0, 0))
clock = pygame.time.Clock()

#雜七雜八的東西
cover = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
cover.set_alpha(150)
cover.fill((20, 20, 20))
cover = cover.convert_alpha()

pencils = []
for i in range(7):
    pencil = pygame.image.load(f"圖片\\pencil_{i+1}.png")
    pencil = pygame.transform.scale(pencil, (50, 50))
    pencils.append(pencil)

#文字
font1 = pygame.font.Font("FFFFORWA.ttf", 40)
q_word = font1.render("Conway's Game of Life", True, (255, 255, 255))

#生命體的家
colors = [(0, 0, 0), (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 120, 40), (255, 255, 100), (100, 255, 255), (255, 100, 255)]
list_of_life = []
sur_cells = []

#物件都在這裡
start_button = objects.Button("start_button", width*size/2-100, height*size/2-30, 50, 15, 2, 4)
clear_button = objects.Button("clear_button", width*size/2-100, height*size/2+50, 50, 15, 2, 4)
setting_button = objects.Button("setting_button", width*size/2-100, height*size/2+130, 50, 15, 2, 4)
reset_button = objects.Button("reset_button", width*size/2-100+230, height*size/2-30, 15, 15, 2, 4)
pause_button = objects.Button("pause_button", width*size-100, 40, 15, 15, 2, 4)
edit_button = objects.Button("edit_button", width*size/2-100-90, height*size/2-30, 15, 15, 2, 4)
leave_button = objects.Button("leave_button", width*size-100, 40, 15, 15, 2, 4)
quit_button = objects.Button("quit_button", width*size-100, 40, 15, 15, 2, 4)

db = objects.Dashboard(-400, 30, 300, height*size-60)

team_config = objects.Slider("Number of Team(s)", width*size/2-300, 130, 600, 50, 7, 1, teams)
pixel_config = objects.Slider("Size of Cells", width*size/2-300, 280, 600, 50, 50, 1, 10)

reinforce_config = objects.Checkbox("Reinforcement", width*size/2-300, 430, 15, 15, 3)

#物件群組
menu = pygame.sprite.Group()
menu.add(start_button)
menu.add(reset_button)
menu.add(edit_button)
menu.add(clear_button)
menu.add(quit_button)
menu.add(setting_button)
menu.add(db)
ingame = pygame.sprite.Group()
ingame.add(db)
ingame.add(pause_button)
edit = pygame.sprite.Group()
edit.add(leave_button)
edit.add(db)
setting = pygame.sprite.Group()
setting.add(team_config)
setting.add(pixel_config)
setting.add(leave_button)
setting.add(reinforce_config)

#清除全部
def clear():
    
    global list_of_life

    teams_num[1] = 0
    teams_num[2] = 0

    for i in range(height):
        for j in range(width):
            list_of_life[i][j] = 0
            pygame.draw.rect(bg, (0, 0, 0), [j*size, i*size, size, size], 0)

        screen.blit(bg, (0, 0))
        menu.draw(screen)

        pygame.display.update()


#隨機生成
def random_reset():

    global width
    global height
    width = screen.get_width()//size
    height = screen.get_height()//size
    global list_of_life
    global sur_cells
    list_of_life = np.array([[x-x for x in range(width)] for y in range(height)])
    sur_cells = np.array([[[0, 0, 0, 0, 0, 0, 0, 0] for x in range(width)] for y in range(height)])
    global teams_num
    global reset
    reset = 0
    bg.fill((0, 0, 0))
    teams_num = [0, 0, 0, 0, 0, 0, 0, 0]

    for i in range(height):
        for j in range(width):

            x = randint(0, 5)
            if(x <2):
                k = randint(1, teams)
                list_of_life[i][j] = k
                teams_num[k] += 1
            else:
                list_of_life[i][j] = 0

            pygame.draw.rect(bg, colors[list_of_life[i][j]], [j*size, i*size, size, size], 0)

            
        screen.blit(bg, (0, 0))
        menu.draw(screen)

        pygame.display.update()

#更新生命體
@numba.njit(fastmath = True)
def update(sur_cells, list_of_life, temp, teams_num, teams, reinforcement, height, width):

    temp_num = [0, 0, 0, 0, 0, 0, 0, 0]
    
    for i in range(height):
        for j in range(width):

            sur_cells[i][j] = [0, 0, 0, 0, 0, 0, 0, 0]    
            alive = 0

            #上
            if(i>0 and list_of_life[i-1][j]):
                alive += 1
                sur_cells[i][j][list_of_life[i-1][j]] += 1
            #下
            if(i<height-1 and list_of_life[i+1][j]):
                alive += 1
                sur_cells[i][j][list_of_life[i+1][j]] += 1
            #左
            if(j>0 and list_of_life[i][j-1]):
                alive += 1
                sur_cells[i][j][list_of_life[i][j-1]] += 1
            #右
            if(j<width-1 and list_of_life[i][j+1]):
                alive += 1
                sur_cells[i][j][list_of_life[i][j+1]] += 1

            #左上
            if(j>0 and i>0 and list_of_life[i-1][j-1]):
                alive += 1
                sur_cells[i][j][list_of_life[i-1][j-1]] += 1
            #左下
            if(j>0 and i<height-1 and list_of_life[i+1][j-1]):
                alive += 1
                sur_cells[i][j][list_of_life[i+1][j-1]] += 1
            #右上
            if(i>0 and j<width-1 and list_of_life[i-1][j+1]):
                alive += 1
                sur_cells[i][j][list_of_life[i-1][j+1]] += 1
            #右下
            if(i<height-1 and j<width-1 and list_of_life[i+1][j+1]):
                alive += 1
                sur_cells[i][j][list_of_life[i+1][j+1]] += 1

            mate = 0
            rival = 0
            #print(surround_num)

            for k in range(1, teams+1):
                if(teams_num[k] < max(teams_num)//2):
                    reinforcement[k] = 1
                else:
                    reinforcement[k] = 0

                if(list_of_life[i][j] == k):
                    mate += sur_cells[i][j][k]
                else:
                    rival += sur_cells[i][j][k]

            #判斷存活or死亡
            if(list_of_life[i][j] > 0):
                if(rival - mate > 1 + reinforcement[list_of_life[i][j]]*reinforcement[0]):
                    temp[i][j] = 0
                elif(alive<2):
                    temp[i][j] = 0
                elif(alive>3):
                    temp[i][j] = 0
                else:
                    temp[i][j] = list_of_life[i][j]


            else:
                index = []
                for k in range(1, teams+1):
                    if(sur_cells[i][j][k] == 3 and sur_cells[i][j][k] == max(sur_cells[i][j])):
                        index.append(k)
                #print(index)

                if(len(index)==1):
                    temp[i][j] = index[0]
                    

            if(temp[i][j]):
                temp_num[temp[i][j]] += 1

    #teams_num = temp_num.copy()
    #list_of_life = temp.copy()

    return temp_num, temp, sur_cells, reinforcement

def draw():

    bg.fill((0, 0, 0))

    for i in range(height):
        for j in range(width):
            if(list_of_life[i][j]):
                pygame.draw.rect(bg, colors[list_of_life[i][j]], [j*size, i*size, size, size])

    
random_reset()
while running:

    fps = str(round(clock.get_fps(),2))
    pos = pos = pygame.mouse.get_pos()

    if(game_status == 0):
        clock.tick(60)
        db.update(dashboard, fps, colors, teams_num, teams, reinforcement)
        screen.blit(bg, (0, 0))
        screen.blit(cover, (0, 0))  
        screen.blit(q_word, (width*size/2-300, height*size-100))
        menu.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:
                    if(dashboard):
                        dashboard = 0
                    else:
                        dashboard = 1
                if event.key == pygame.K_RETURN:
                    game_status = 1
                if event.key == pygame.K_ESCAPE:
                    running = False

            if quit_button.detect(pos) and event.type == pygame.MOUSEBUTTONDOWN:
                running = False
            if start_button.detect(pos) and event.type == pygame.MOUSEBUTTONDOWN:
                game_status = 1
            if setting_button.detect(pos) and event.type == pygame.MOUSEBUTTONDOWN:
                game_status = 3
            if clear_button.detect(pos) and event.type == pygame.MOUSEBUTTONDOWN:
                clear()
            if reset_button.detect(pos) and event.type == pygame.MOUSEBUTTONDOWN:
                random_reset()
            if edit_button.detect(pos) and event.type == pygame.MOUSEBUTTONDOWN:
                pygame.mouse.set_visible(False)
                game_status = 2

    if(game_status == 1):
        db.update(dashboard, fps, colors, teams_num, teams, reinforcement)
        clock.tick(60)
        tick = (tick+1)%6
        if(tick == 0):
            teams_num, list_of_life, sur_cells, reinforcement = update(sur_cells, list_of_life, np.array([[x-x for x in range(width)] for y in range(height)]), teams_num, teams, reinforcement, height, width)
            draw()
        screen.blit(bg.convert(), (0, 0))
        ingame.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:
                    if(dashboard):
                        dashboard = 0
                    else:
                        dashboard = 1
                if event.key == pygame.K_ESCAPE:
                    game_status = 0

            if pause_button.detect(pos) and event.type == pygame.MOUSEBUTTONDOWN:
                game_status = 0

    if(game_status == 2):

        screen.blit(bg, (0, 0))
        db.update(dashboard, fps, colors, teams_num, teams, reinforcement)
        edit.draw(screen)
        screen.blit(pencils[color], (pos[0], pos[1]-50))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:
                    if(dashboard):
                        dashboard = 0
                    else:
                        dashboard = 1
                if event.key == pygame.K_ESCAPE:
                    pygame.mouse.set_visible(True)
                    game_status = 0

            if event.type == pygame.MOUSEWHEEL:
                color = (color + teams + event.y)%teams

            if(pygame.mouse.get_pressed()[0]):
                x = pos[0]//size
                y = pos[1]//size
                pygame.draw.rect(bg, colors[color+1], [x*size, y*size, size, size], 0)

                if(list_of_life[y][x] != color+1):
                    teams_num[list_of_life[y][x]] -= 1
                    list_of_life[y][x] = color+1
                    teams_num[color+1] += 1

            if(pygame.mouse.get_pressed()[2]):
                x = pos[0]//size
                y = pos[1]//size
                pygame.draw.rect(bg, colors[0], [x*size, y*size, size, size], 0)
                teams_num[list_of_life[y][x]] -= 1
                list_of_life[y][x] = 0

            if leave_button.detect(pos) and event.type == pygame.MOUSEBUTTONDOWN:
                pygame.mouse.set_visible(True)
                game_status = 0

    if(game_status == 3):
        
        screen.blit(bg, (0, 0))
        screen.blit(cover, (0, 0))
        pygame.draw.rect(screen, (0, 0, 0), [screen.get_size()[0]/2-400, 100, 800, screen.get_size()[1]-200])
        setting.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    random_reset()
                    game_status = 0
            if event.type == pygame.MOUSEBUTTONDOWN:
                reinforcement[0] = reinforce_config.press(pos)

            if team_config.detect(pos) and pygame.mouse.get_pressed()[0]:
                teams = team_config.move(pos)
            if pixel_config.detect(pos) and pygame.mouse.get_pressed()[0]:
                size = pixel_config.move(pos)
            if leave_button.detect(pos) and event.type == pygame.MOUSEBUTTONDOWN:
                random_reset()
                game_status = 0

    pygame.display.update()
pygame.quit()

