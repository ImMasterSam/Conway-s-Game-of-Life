import pygame

import matplotlib
matplotlib.use("Agg")
import matplotlib.backends.backend_agg as agg
import pylab

pygame.init()

class Button(pygame.sprite.Sprite):

    #變數
    x = 0
    y = 0
    sprites = []
    width = 0
    height = 0

    def __init__(self, name, x, y, width, height, sp_num, scalex):

        pygame.sprite.Sprite.__init__(self)

        self.sprites = []
        for i in range(1, sp_num+1):
            pic = pygame.image.load(f"圖片\\{name}_{i}.png")
            self.sprites.append(pygame.transform.scale(pic, (width*scalex, height*scalex)).convert_alpha())

        self.image = self.sprites[0]
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.left = x
        self.rect.top = y
        self.width = width*scalex
        self.height = height*scalex
        self.show = 1

    def detect(self, pos):

        if(self.show==0):
            return False

        if(pos[0]>=self.x and pos[0]<=self.x+self.width) and (pos[1]>=self.y and pos[1]<=self.y+self.height):
            self.image = self.sprites[1]
            return True
        else:
            self.image = self.sprites[0]
            return False
        

class Dashboard(pygame.sprite.Sprite):

    #變數
    x = 0
    y = 0
    width = 0
    height = 0
    color_type = ["", "WHITE", "RED", "GREEN", "BLUE", "ORANGE", "YELLOW", "CYAN", "PINK"]

    font1 = pygame.font.Font("FFFFORWA.ttf", 30)
    font2 = pygame.font.Font("FFFFORWA.ttf", 20)
    name = font1.render("DASHBOARD", True, (255, 255, 255))

    def __init__(self, x, y, width, height):

        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface((width, height))
        self.image.fill((255, 255 ,255))
        self.bg = pygame.Surface((width-20, height-20))
        self.image.blit(self.bg, (10, 10))
        self.bg.blit(self.name, (20, 10))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.left = x
        self.rect.top = y
        self.width = width
        self.height = height

    def update(self, show, fps, color, teams_num, teams, reinforcement):
        
        self.fps = self.font2.render("FPS: "+fps, True, (255, 255, 255))
        self.image.blit(self.bg, (10, 10))
        self.image.blit(self.fps, (30, 85))

        for i in range(1, teams+1):
            if(reinforcement[i]*reinforcement[0]):
                pygame.draw.rect(self.image, color[i], [25, 100+50*i, 250, 35], 0)
                if(i == 1):
                    self.team_num = self.font2.render(f"{self.color_type[i]}: {int(teams_num[i])}", True, (0, 0, 0))
                else:
                    self.team_num = self.font2.render(f"{self.color_type[i]}: {int(teams_num[i])}", True, (255, 255, 255))
            else:
                self.team_num = self.font2.render(f"{self.color_type[i]}: {int(teams_num[i])}", True, color[i])
            self.image.blit(self.team_num, (30, 105+50*i))

        if(show == 0):
            if(self.rect.left>-300):
                self.x -= 10
                self.rect.left = self.x

        if(show == 1):
            if(self.rect.left<30):
                self.x += 10
                self.rect.left = self.x


class Slider(pygame.sprite.Sprite):

    #變數
    x = 0
    y = 0
    width = 0
    length = 0

    font1 = pygame.font.Font("FFFFORWA.ttf", 30)

    def __init__(self, name, x, y, length, width, max, min, init):

        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface((length, width+60))
        self.image.fill((0, 0, 0))
        self.bar = pygame.Surface((length, width-20))
        self.bar.fill((255, 255, 255))
        self.image.blit(self.bar, (0, 70))
        
        self.name = self.font1.render(name, True, (255, 255, 255))
        self.image.blit(self.name, (0, 5))

        self.rect = self.image.get_rect()
        self.x = (x*min+(x+length)*max)/max-min
        self.y = y
        self.x = x
        self.rect.left = x
        self.rect.top = y
        self.width = width
        self.length = length
        self.max = max
        self.min = min
        self.unit = (self.length-self.width)/(self.max-self.min)

        self.num = init
        self.num_word = self.font1.render(str(self.num), True, (255, 255, 255))
        self.image.blit(self.num_word, (550-10*(self.num+self.min>=100), 10))

        self.button = pygame.Surface((width, width))
        self.button.fill((255, 50, 50))
        self.image.blit(self.button, ((self.num-1)*self.unit, 60))

    def detect(self, pos):

        if(pos[0]>=self.x and pos[0]<self.x+self.length-self.width) and (pos[1]>=self.y+60 and pos[1]<=self.y+self.width+60):
            return True
        else:
            return False

    def move(self, pos):

        self.image.fill((0, 0, 0))
        self.image.blit(self.bar, (0, 70))
        self.num = (pos[0]-self.x+self.unit/2)//self.unit
        self.image.blit(self.button, (self.num*self.unit, 60))
        self.image.blit(self.name, (0, 5))

        self.num_word = self.font1.render(str(int(self.num+self.min)), True, (255, 255, 255))
        self.image.blit(self.num_word, (550-10*(self.num+self.min>=100), 10))

        return int(self.num+self.min)

        
class Checkbox(pygame.sprite.Sprite):

    #變數
    x = 0
    y = 0
    sprites = []
    width = 0
    height = 0

    font1 = pygame.font.Font("FFFFORWA.ttf", 30)

    def __init__(self, name, x, y, width, height, scalex, init_on):

        pygame.sprite.Sprite.__init__(self)

        self.sprites = []
        for i in range(2):
            pic = pygame.image.load(f"圖片\\checkbox_{i}.png")
            self.sprites.append(pygame.transform.scale(pic, (width*scalex, height*scalex)).convert_alpha())

        self.image = pygame.Surface((600 ,50))
        self.image.fill((0, 0, 0))

        self.box = self.sprites[init_on]
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.left = x
        self.rect.top = y
        self.width = width*scalex
        self.height = height*scalex
        self.switch = init_on

        self.image.blit(self.box, (550, 5))

        self.name_word = self.font1.render(name, True, (255, 255, 255))
        self.image.blit(self.name_word, (0, 10))



    def press(self, pos):

        if(pos[0]>=self.x+550 and pos[0]<=self.x+self.width+550) and (pos[1]>=self.y+10 and pos[1]<=self.y+self.height+10):
            if(self.switch):
                self.switch = 0
                self.box = self.sprites[self.switch]
                self.image.blit(self.box, (550, 5))
            else:
                self.switch = 1
                self.box = self.sprites[self.switch]
                self.image.blit(self.box, (550, 5))
            return self.switch
        
        else:
            return self.switch


class Checkbox_list(pygame.sprite.Sprite):

    #變數
    x = 0
    y = 0
    sprites = []
    width = 0
    height = 0

    font1 = pygame.font.Font("FFFFORWA.ttf", 30)

    def __init__(self, name, x, y, width, height, scalex, n):

        pygame.sprite.Sprite.__init__(self)

        self.sprites = [[]]
        for i in range(1, n+1):
            pic_on = pygame.image.load(f"圖片\\checkbox_team_{i}_0.png")
            pic_off = pygame.image.load(f"圖片\\checkbox_team_{i}_1.png")
            self.sprites.append([pygame.transform.scale(pic_on, (width*scalex, height*scalex)).convert_alpha(), pygame.transform.scale(pic_off, (width*scalex, height*scalex)).convert_alpha()])

        self.image = pygame.Surface((600 ,140))
        self.image.fill((0, 0, 0))

        self.display = [[]]
        for i in range(1, n+1):
            self.display.append(self.sprites[i][1])
        
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.left = x
        self.rect.top = y
        self.width = width*scalex
        self.height = height*scalex
        self.n = n
        self.switchs = [x-x+1 for x in range(6)]

        for i in range(1, n+1):
            self.image.blit(self.sprites[i][self.switchs[i]], ((i-1)*135, 70))

        self.name_word = self.font1.render(name, True, (255, 255, 255))
        self.image.blit(self.name_word, (240, 10))


    def draw(self):
        for i in range(1, self.n+1):
            self.image.blit(self.sprites[i][self.switchs[i]], ((i-1)*135, 70))

    def press(self, pos):

        if(pos[0]>=self.x and pos[0]<=self.x + 600) and (pos[1]>=self.y+70 and pos[1]<=self.y+self.height+70):

            for i in range(1, self.n+1):

                if(pos[0]>=self.x+((i-1)*135) and pos[0]<=self.x+self.width+((i-1)*135)):
                    if(self.switchs[i]):
                        self.switchs[i] = 0
                        self.draw()
                    else:
                        self.switchs[i] = 1
                        self.draw()

        
        return self.switchs


class LineChart(pygame.sprite.Sprite):

    def __init__(self, x, y, scale_x, scale_y, set_dpi):

        pygame.sprite.Sprite.__init__(self)

        self.figure = pylab.figure(figsize=[scale_x, scale_y], dpi = set_dpi, facecolor="black")
        self.ax = self.figure.gca()
        self.ax.set_facecolor("black")
        self.ax.tick_params(axis='both', colors='white')
        self.ax.grid(color='gray', linestyle='--', linewidth=0.5)
        self.ax.set_title("Number of Cells", color="white")
        self.ax.set_xlabel("Generations", color="white")

        self.canvas = agg.FigureCanvasAgg(self.figure)
        self.canvas.draw()
        self.renderer = self.canvas.get_renderer()
        self.raw_data = self.renderer.tostring_rgb()

        self.canva_size = self.canvas.get_width_height()

        self.image = pygame.image.fromstring(self.raw_data, self.canva_size, "RGB").convert_alpha()

        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.left = x
        self.rect.top = y


    def update(self, datas, teams, colors):

        for i in range(1, teams+1):
            self.ax.plot(datas[i], color=(colors[i][0] / 255, colors[i][1] / 255, colors[i][2] / 255))
        self.canvas.draw()
        renderer = self.canvas.get_renderer()
        #raw_data = renderer.tostring_rgb()
        self.image = pygame.image.fromstring(renderer.tostring_rgb(), self.canva_size, "RGB").convert_alpha()


    def clear(self, datas, teams, colors):

        self.ax.cla()

        self.ax.set_facecolor("black")
        self.ax.tick_params(axis='both', colors='white')
        self.ax.grid(color='gray', linestyle='--', linewidth=0.5)
        self.ax.set_title("Number of Cells", color="white")
        self.ax.set_xlabel("Generations", color="white")

        for i in range(1, teams+1):
            self.ax.plot(datas[i], color=(colors[i][0] / 255, colors[i][1] / 255, colors[i][2] / 255))
        self.canvas.draw()
        renderer = self.canvas.get_renderer()
        #raw_data = renderer.tostring_rgb()
        self.image = pygame.image.fromstring(renderer.tostring_rgb(), self.canva_size, "RGB").convert()

