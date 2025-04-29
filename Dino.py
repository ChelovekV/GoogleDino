import pygame
import random
import os

pygame.init()

#GLOBAL CONST
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
RUNNING = [pygame.image.load(os.path.join("Assets/Dino", "DinoRun1.png")),
           pygame.image.load(os.path.join("Assets/Dino", "DinoRun2.png"))]
JUMPING = pygame.image.load(os.path.join("Assets/Dino", "DinoJump.png"))
SMALL_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus1.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus2.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus3.png"))]
LARGE_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus1.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus2.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus3.png"))]
BG = pygame.image.load(os.path.join("Assets/Other", "Track.png"))

BIRD = [pygame.image.load(os.path.join("Assets/Bird", "Bird1.png")),
        pygame.image.load(os.path.join("Assets/Bird", "Bird2.png"))]

CLOUD = pygame.image.load(os.path.join("Assets/Other", "Cloud.png"))

RESET = pygame.image.load(os.path.join("Assets/Other", "Reset.png"))

DUCKING = [pygame.image.load(os.path.join("Assets/Dino", "DinoDuck1.png")),
           pygame.image.load(os.path.join("Assets/Dino", "DinoDuck2.png"))]
class Dinosaur():
    X_POS = 80
    Y_POS = 310
    JUMP_VEL = 8.5
    Y_POS_DUCK = 340
    def __init__(self):
        self.run_img = RUNNING
        self.jump_img = JUMPING
        self.duck_img = DUCKING

        #флажки
        self.dino_run = True
        self.dino_jump = False
        self.dino_duck = False
        self.step_index = 0 #счётчик шагов
        self.jump_vel = self.JUMP_VEL
        self.image = self.run_img[0] #первый спрайт
        self.dino_rect = self.image.get_rect()
        #задали коорд.
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS

    def update(self, userInput):

        if self.dino_run:
            self.run()

        if self.dino_jump:
            self.jump()
            
        if self.dino_duck:
            self.duck()

        if self.step_index >= 10:
            self.step_index = 0

        if (userInput[pygame.K_UP] or userInput[pygame.K_SPACE]) and not self.dino_jump:
            self.dino_duck = False
            self.dino_run = False
            self.dino_jump = True
        elif userInput[pygame.K_DOWN] and not self.dino_jump:
            self.dino_duck = True
            self.dino_run = False
            self.dino_jump = False
        elif not (self.dino_jump or userInput[pygame.K_DOWN]):
            self.dino_duck = False
            self.dino_run = True
            self.dino_jump = False

    def run(self):
        self.image = self.run_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.step_index += 1

    def jump(self):
        self.image = self.jump_img
        if self.dino_jump:
            self.dino_rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8
        if self.jump_vel < -self.JUMP_VEL:
            self.dino_jump = False
            self.jump_vel = self.JUMP_VEL

    def duck(self):
        self.image = self.duck_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS_DUCK
        self.step_index += 1

    def draw(self):
        SCREEN.blit(self.image, (self.dino_rect.x, self.dino_rect.y))
class Cloud():
    def __init__(self):
        self.x = SCREEN_WIDTH + random.randint(800,1000)
        self.y = random.randint(50,100)
        self.image = CLOUD
        self.width = self.image.get_width()

    def update(self):
        self.x -= game_speed
        if self.x <= -self.image.get_width():
            self.x = SCREEN_WIDTH + random.randint(800, 1000)
            self.y = random.randint(50, 100)
    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.x, self.y))
class Obstacle():
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH
    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop()

    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)

class SmallCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 325
class LargeCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 300
class Bird(Obstacle):
    def __init__(self,image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = 250
        self.index = 0
    def draw(self, SCREEN):
        if self.index >= 9:
            self.index = 0
        SCREEN.blit(self.image[self.index // 5], self.rect)
        self.index += 1
#Основная игровая функция
def main():
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles
    run = True
    clock = pygame.time.Clock()
    player = Dinosaur()
    cloud = Cloud()
    game_speed = 20
    #коорд. для дороги
    x_pos_bg = 0
    y_pos_bg = 380
    points = 0
    font = pygame.font.Font('freesansbold.ttf', 20)
    obstacles = [] #Список для препядствий на экране
    death_count = 0 #счётчик смертей
    x_white_box = 200
    y_white_box = 0
    height_white_box = 600
    wight_white_box = 900

    def score():
        global points, game_speed
        points += 1
        if points % 100 == 0:
            game_speed += 1
        text = font.render("Points: " + str(points), True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (1000, 40)
        SCREEN.blit(text, textRect)
    def background():
        global x_pos_bg, y_pos_bg
        image_width = BG.get_width()
        SCREEN.blit(BG, (x_pos_bg, y_pos_bg))
        SCREEN.blit(BG, (x_pos_bg +image_width, y_pos_bg))
        if x_pos_bg <= -image_width:
            SCREEN.blit(BG, (x_pos_bg + image_width, y_pos_bg))
            x_pos_bg = 0
        x_pos_bg -= game_speed
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        SCREEN.fill((255, 255 ,255))

        if len(obstacles) == 0:
            rand = random.randint(0,2)
            if rand == 0:
                obstacles.append(SmallCactus(SMALL_CACTUS))
            elif rand == 1:
                obstacles.append(LargeCactus(LARGE_CACTUS))
            else:
                obstacles.append((Bird(BIRD)))
        for obstacle in obstacles:
            obstacle.draw(SCREEN)
            obstacle.update()
            if player.dino_rect.colliderect(obstacle.rect):
                pygame.time.delay(2000)
                death_count += 1
                menu(death_count)
                # Получить знач. с клавиш
        userInput = pygame.key.get_pressed()
        player.draw()
        player.update(userInput)
        cloud.draw(SCREEN)
        cloud.update()
        pygame.draw.rect(SCREEN, (255, 255, 255), (x_white_box, y_white_box,
                                                   wight_white_box, height_white_box))
        x_white_box += 25
        score()
        background()
        pygame.display.update()
        clock.tick(30)

#Меню для запуска
def menu(death_count):
    global points
    x_pos_bg = 0
    y_pos_bg = 380
    x_white_box = 200
    y_white_box = 0
    height_white_box = 600
    wight_white_box = 900

    run = True
    while run:
        font = pygame.font.Font('freesansbold.ttf', 30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Если польщователь нажал выход:
                run = False
                return

            #обработка нажатия клавиш
            if event.type == pygame.KEYDOWN:
                main()
        SCREEN.fill((255,255,255))

        if death_count == 0:
            text = font.render("Press any Key to Start", True, (0, 0, 0))
            SCREEN.blit(BG, (x_pos_bg, y_pos_bg))
            pygame.draw.rect(SCREEN, (255, 255, 255), (x_white_box, y_white_box,
                                                       wight_white_box, height_white_box))
        elif death_count > 0:
            text = font.render("Press any Key to Restart", True, (0, 0, 0))
            score = font.render("Score: " + str(points), True, (0, 0,0))
            scoreRect = score.get_rect()
            scoreRect.center = (1000, 40)
            SCREEN.blit(score, scoreRect)
            SCREEN.blit(RESET,(500, 350))
            SCREEN.blit(BG, (x_pos_bg, y_pos_bg))
        textRect = text.get_rect()
        textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        SCREEN.blit(text, textRect)

        SCREEN.blit(RUNNING[0], (80, 310))
        pygame.display.update()

menu(death_count=0)

