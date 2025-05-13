import pygame, sys, random, time
from pygame.math import Vector2

class RETURNTOMENU(Exception):
    pass

class SNAKE:
    def __init__(self):
        self.body = [Vector2(5,10), Vector2(4,10), Vector2(3,10)] 
        self.direction = Vector2(1,0)
        self.new_block = False

        self.head_up = pygame.image.load('sprites/head_up.png').convert_alpha()
        self.head_down = pygame.image.load('sprites/head_down.png').convert_alpha()
        self.head_right = pygame.image.load('sprites/head_right.png').convert_alpha()
        self.head_left = pygame.image.load('sprites/head_left.png').convert_alpha()

        self.tail_up = pygame.image.load('sprites/tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load('sprites/tail_down.png').convert_alpha()
        self.tail_right = pygame.image.load('sprites/tail_right.png').convert_alpha()
        self.tail_left = pygame.image.load('sprites/tail_left.png').convert_alpha()

        self.body_vertical = pygame.image.load('sprites/body_vertical.png').convert_alpha()
        self.body_horizontal = pygame.image.load('sprites/body_horizontal.png').convert_alpha()

        self.body_tr = pygame.image.load('sprites/body_tr.png').convert_alpha()
        self.body_tl = pygame.image.load('sprites/body_tl.png').convert_alpha()
        self.body_br = pygame.image.load('sprites/body_br.png').convert_alpha()
        self.body_bl = pygame.image.load('sprites/body_bl.png').convert_alpha()

        self.crunch_sound = pygame.mixer.Sound('sound/crunch.wav')
        self.life_sound = pygame.mixer.Sound('sound/life.wav')
        


    def draw_snake(self):
       
        self.update_head_graphics()
        self.update_tail_graphics()

        for index,block in enumerate(self.body):
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)

            if index == 0:
                screen.blit(self.head,block_rect)
            elif index == len(self.body) - 1:
                screen.blit(self.tail,block_rect)
            
            else: 
                previous_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block
                if previous_block.x == next_block.x:
                    screen.blit(self.body_vertical,block_rect)
                elif previous_block.y == next_block.y:
                    screen.blit(self.body_horizontal,block_rect)
                else: 
                    if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
                        screen.blit(self.body_tl,block_rect)
                    elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
                        screen.blit(self.body_bl,block_rect)
                    elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
                        screen.blit(self.body_tr,block_rect)
                    elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
                        screen.blit(self.body_br,block_rect)
            
        
    def update_head_graphics(self):
        head_relation = self.body[1] - self.body[0]
        if head_relation == Vector2(1,0):self.head = self.head_left
        elif head_relation == Vector2(-1,0):self.head = self.head_right
        elif head_relation == Vector2(0,1):self.head = self.head_up
        elif head_relation == Vector2(0,-1):self.head = self.head_down


    def update_tail_graphics(self):
        tail_relation = self.body[-2] - self.body[-1]
        if tail_relation == Vector2(1,0):self.tail = self.tail_left
        elif tail_relation == Vector2(-1,0):self.tail = self.tail_right
        elif tail_relation == Vector2(0,1):self.tail = self.tail_up
        elif tail_relation == Vector2(0,-1):self.tail = self.tail_down
    
    def move_snake(self):
        if self.new_block == True:
            body_copy = self.body[:] 
            body_copy.insert(0,body_copy[0] + self.direction) 
            self.new_block = False
        else:
            body_copy = self.body[:-1] 
            body_copy.insert(0,body_copy[0] + self.direction) 
            self.body = body_copy[:]

    def add_block(self):
        self.new_block = True

    def play_crunch_sound(self):
        self.crunch_sound.play()
    
    def play_life_sound(self):
        self.life_sound.play()

    def reset(self):
        self.body = [Vector2(5,10), Vector2(4,10), Vector2(3,10)] 
        self.direction = Vector2(0,0)
        
class FRUIT:
    def __init__(self):
        self.randomize()
       
    def draw_fruit(self):
       fruit_rect = pygame.Rect(int(self.pos.x * cell_size),int(self.pos.y * cell_size),cell_size,cell_size)
       screen.blit(apple, fruit_rect)
       

    def randomize(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = pygame.math.Vector2(self.x,self.y)

class POWER:

    def __init__(self):
        self.active = False
        self.spawn_time = 0
        self.last_spawn = time.time()

    def draw_power(self):
       if self.active: 
        power_rect = pygame.Rect(int(self.pos.x * cell_size),int(self.pos.y * cell_size),cell_size,cell_size)
        screen.blit(power, power_rect)

    def spawn(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = pygame.math.Vector2(self.x,self.y)
        self.active = True
        self.spawn_time = time.time()
        self.last_spawn = self.spawn_time

    def update(self):
        current_time = time.time()

        if self.active and (current_time - self.spawn_time > 7):
            self.despawn()
        elif not self.active and (current_time - self.spawn_time > 20):
            self.spawn()


    def despawn(self):
        self.active = False
        self.last_spawn = time.time()
       
class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()
        self.power = POWER()
        self.lives = 0
        self.reset_time = None
        self.score = 0
    
    def update(self):
        if self.reset_time:
            if time.time() - self.reset_time < 1.5:
                return
            else:
                self.reset_time = None
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()
        self.power.update()
        

    def draw_elements(self):
        self.draw_grass()
        self.fruit.draw_fruit()
        self.power.draw_power()
        self.snake.draw_snake()
        self.draw_score()
        self.draw_life()

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.add_block()
            self.snake.play_crunch_sound()
            self.score += 1
        
        for block in self.snake.body[1:]:
            if block == self.fruit.pos:
                self.fruit.randomize()
        
        if self.power.active and self.power.pos == self.snake.body[0]:
            self.power.despawn()
            self.lives += 1
            self.snake.play_life_sound()
            
    def check_fail(self):
        
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            self.game_over()
        
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()
       
    def reset_snake(self):
        self.snake.reset()
        self.reset_time = time.time()


    def game_over(self):
        if self.lives > 0:
            self.lives -= 1
            self.reset_snake()
        else:
            self.score = 0
            raise RETURNTOMENU()
            
    
    def draw_grass(self):
        grass_color = (167,209,61) 
        for row in range(cell_number):
            if row % 2 == 0:
                for col in range(cell_number):
                    if col % 2 == 0:
                        grass_rect = pygame.Rect(col * cell_size,row * cell_size,cell_size,cell_size)
                        pygame.draw.rect(screen,grass_color,grass_rect)
            else:
                for col in range(cell_number):
                    if col % 2 != 0:
                        grass_rect = pygame.Rect(col * cell_size,row * cell_size,cell_size,cell_size)
                        pygame.draw.rect(screen,grass_color,grass_rect)
   
    def draw_score(self):
        score_text = str(self.score)
        score_surface = game_font.render(score_text,True,(56,74,12))
        score_x = int(cell_size * cell_number - 60)
        score_y = int(cell_size * cell_number - 40)
        score_rect = score_surface.get_rect(center = (score_x,score_y))
        apple_rect = apple.get_rect(midright = (score_rect.left,score_rect.centery))
        bg_rect = pygame.Rect(apple_rect.left,apple_rect.top,apple_rect.width + score_rect.width + 6,apple_rect.height)

        pygame.draw.rect(screen,(167,209,61), bg_rect)
        screen.blit(score_surface,score_rect)
        screen.blit(apple,apple_rect)
        pygame.draw.rect(screen,(56,74,12),bg_rect,2) 
    
    def draw_life(self):
        life_text = f"Lives: {self.lives + 1}"
        life_surface = game_font.render(life_text,True,(56,74,12))
        life_x = int(cell_size * cell_number - 730)
        life_y = int(cell_size * cell_number - 40)
        life_rect = life_surface.get_rect(center = (life_x,life_y))
        
        pygame.draw.rect(screen, (167,209,61), life_rect)
        screen.blit(life_surface, life_rect)
        pygame.draw.rect(screen,(56,74,12),life_rect,2)

class Button:
    def __init__(self, image, pos, text_input, font, base_color, hovering_color):
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input 
        self.text = self.font.render(self.text_input, True, self.base_color)
        if self.image is None:
            self.image = self.text
        self.rect = self.image.get_rect(center = (self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))
    
    def update(self,screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def checkForInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False
    
    def changeColor(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)
def main():
    while True:
        Menu(screen)
        game_loop(screen)

pygame.init()

cell_size = 40
cell_number = 20
screen_size = (cell_number * cell_size, cell_number * cell_size) 
screen = pygame.display.set_mode(screen_size)

clock = pygame.time.Clock()

applebig = pygame.image.load('sprites/apple.png').convert_alpha()
apple = pygame.transform.smoothscale(applebig, (cell_size, cell_size))
powerbig = pygame.image.load('sprites/life.png')
power = pygame.transform.smoothscale(powerbig, (cell_size, cell_size))
pygame.mixer.music.load('sound/music.wav')

game_font = pygame.font.Font('fonts/Howdy Frog.ttf', 25)

def Menu(screen):
    pygame.display.set_caption("Menu")
    running = True
    while running:
        
        screen.fill((0,0,0))
        MENU_MOUSE_POS = pygame.mouse.get_pos()

        title_surface = game_font.render("Snake Game", True, "White")
        title_rect = title_surface.get_rect(center=(screen.get_width() // 2, 100))
        screen.blit(title_surface, title_rect)

        PLAY_BUTTON = Button(image=None, pos=(screen.get_width() // 2,250),
                    text_input = "PLAY", font = game_font, base_color = (175,215,70), hovering_color = "White")
        QUIT_BUTTON = Button(image=None, pos=(screen.get_width() // 2,350),
                    text_input = "QUIT", font = game_font, base_color = (175,215,70), hovering_color = "White")

        for button in [PLAY_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)
        
        for event in pygame.event.get():
            if event.type ==pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    running = False
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()
        
        pygame.display.update()
        clock.tick(60)


def game_loop(screen):
    pygame.display.set_caption("Play")
    pygame.mixer.music.play(-1, 0.0) 
    running = True
    main_game = MAIN()
    SCREEN_UPDATE = pygame.USEREVENT
    pygame.time.set_timer(SCREEN_UPDATE, 150)
    
    try:
        while True: 
        
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == SCREEN_UPDATE:
                    main_game.update()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        if main_game.snake.direction.y != 1:
                            main_game.snake.direction = Vector2(0, -1)
                    if event.key == pygame.K_RIGHT:
                        if main_game.snake.direction.x != -1:
                            main_game.snake.direction = Vector2(1, 0)
                    if event.key == pygame.K_DOWN:
                        if main_game.snake.direction.y != -1:
                            main_game.snake.direction = Vector2(0, 1)
                    if event.key == pygame.K_LEFT:
                        if main_game.snake.direction.x != 1:
                            main_game.snake.direction = Vector2(-1, 0)

            screen.fill((175,215,70)) 
            main_game.draw_elements()
            pygame.display.update()
            clock.tick(60) 
    except RETURNTOMENU:
        pygame.mixer.music.stop()
        return
    
main()