import pygame, sys, random
from pygame.math import Vector2

class RETURNTOMENU(Exception):
    pass

class SNAKE:
    def __init__(self):
        self.body = [Vector2(5,10), Vector2(4,10), Vector2(3,10)] #starting pos of snake
        self.direction = Vector2(0,0)
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
        


    def draw_snake(self):
       
        self.update_head_graphics()
        self.update_tail_graphics()

        for index,block in enumerate(self.body):
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)

            #what direction is face heading

            if index == 0:
                screen.blit(self.head,block_rect)
            elif index == len(self.body) - 1:
                screen.blit(self.tail,block_rect)
            #what direction is body facing
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
    #moving the snake: the head is moved to a new block
    # the block before the head gets the position where the head used to be 
    # each block is moved to the position of the block that was there before it
    # "delete" the last block
        if self.new_block == True:
            body_copy = self.body[:] #copies entire self.body list 
            body_copy.insert(0,body_copy[0] + self.direction) #places the first element(head) one block ahead, based on the direction
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1] #copies entire self.body list except for last element
            body_copy.insert(0,body_copy[0] + self.direction) 
            self.body = body_copy[:]

    def add_block(self):
        self.new_block = True

    def play_crunch_sound(self):
        self.crunch_sound.play()

    def reset(self):
        self.body = [Vector2(5,10), Vector2(4,10), Vector2(3,10)] #starting pos of snake
        self.direction = Vector2(0,0)
        
class FRUIT:
    def __init__(self):
        self.randomize()
       
    def draw_fruit(self):
       fruit_rect = pygame.Rect(int(self.pos.x * cell_size),int(self.pos.y * cell_size),cell_size,cell_size)
       screen.blit(apple, fruit_rect)
       #pygame.draw.rect(screen, (126, 166, 114), fruit_rect)

    def randomize(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = pygame.math.Vector2(self.x,self.y)

class POWER:
    def __init__(self):
        self.spawn()

    def draw_power(self):
       power_rect = pygame.Rect(int(self.pos.x * cell_size),int(self.pos.y * cell_size),cell_size,cell_size)
       screen.blit(power, power_rect)

    def spawn(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = pygame.math.Vector2(self.x,self.y)
       
class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()
        self.power = POWER()
        self.lives = 1
    
    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()

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
        
        for block in self.snake.body[1:]:
            if block == self.fruit.pos:
                self.fruit.randomize()
        
        if self.power.pos == self.snake.body[0]:
            self.power.spawn()
            self.lives = self.lives + 1
            
    def check_fail(self):
        # check if the snake is outside the screen
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            self.game_over()
        #check if snake hits itself
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()
       
    def game_over(self):
        if self.lives > 0:
            self.lives -= 1
            self.snake.reset()
        else:
            #return to main menu
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
        score_text = str(len(self.snake.body) - 3)
        score_surface = game_font.render(score_text,True,(56,74,12))
        score_x = int(cell_size * cell_number - 60)
        score_y = int(cell_size * cell_number - 40)
        score_rect = score_surface.get_rect(center = (score_x,score_y))
        apple_rect = apple.get_rect(midright = (score_rect.left,score_rect.centery))
        bg_rect = pygame.Rect(apple_rect.left,apple_rect.top,apple_rect.width + score_rect.width + 6,apple_rect.height)

        pygame.draw.rect(screen,(167,209,61), bg_rect)
        screen.blit(score_surface,score_rect)
        screen.blit(apple,apple_rect)
        pygame.draw.rect(screen,(56,74,12),bg_rect,2) #frame of score box 2 is the line width
    
    def draw_life(self):
        life_text = str((self.lives + 1))
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
screen_size = (cell_number * cell_size, cell_number * cell_size) #size of window
screen = pygame.display.set_mode(screen_size)

clock = pygame.time.Clock()

applebig = pygame.image.load('sprites/apple.png').convert_alpha()
apple = pygame.transform.smoothscale(applebig, (cell_size, cell_size))
powerbig = pygame.image.load('sprites/powerboost.png')
power = pygame.transform.smoothscale(powerbig, (cell_size, cell_size))
pygame.mixer.music.load('sound/music.wav')
#SCREEN = pygame.display.set_mode((1280, 720))
game_font = pygame.font.Font('fonts/Howdy Frog.ttf', 25)



def Menu(screen):
    pygame.display.set_caption("Menu")
    running = True
    while running:
        
        screen.fill((0,0,0))
        MENU_MOUSE_POS = pygame.mouse.get_pos()

        #menu_text = str("Snake Game")
        #title_surface = game_font.render(menu_text,True,"White")
        #title_x = int(cell_size * cell_number // 2)
        #title_y = int(cell_size * cell_number - 500)
        #title_rect = title_surface.get_rect(center = (title_x,title_y))

        title_surface = game_font.render("Snake Game", True, "White")
        title_rect = title_surface.get_rect(center=(screen.get_width() // 2, 100))
        screen.blit(title_surface, title_rect)
        
        #pygame.draw.rect(SCREEN,(167,209,61), title_rect)
        #SCREEN.blit(title_surface,title_rect)
        
        #MENU_RECT = MENU_TEXT.get_rect(center=(640,100))

        PLAY_BUTTON = Button(image=None, pos=(screen.get_width() // 2,250),
                    text_input = "PLAY", font = game_font, base_color = (175,215,70), hovering_color = "White")
        QUIT_BUTTON = Button(image=None, pos=(screen.get_width() // 2,350),
                    text_input = "QUIT", font = game_font, base_color = (175,215,70), hovering_color = "White")

        #SCREEN.blit(MENU_TEXT, MENU_RECT)

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
    main_game = MAIN()
    SCREEN_UPDATE = pygame.USEREVENT
    pygame.time.set_timer(SCREEN_UPDATE, 150)
    pygame.mixer.music.play(-1, 0.0)
    
    try: 

        #cell_size = 40
        #cell_number = 20
        #screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size)) #size of window
        #clock = pygame.time.Clock()
        #applebig = pygame.image.load('sprites/apple.png').convert_alpha()
        #apple = pygame.transform.smoothscale(applebig, (cell_size, cell_size))
        #powerbig = pygame.image.load('sprites/powerboost.png')
        #power = pygame.transform.smoothscale(powerbig, (cell_size, cell_size))
        #game_font = pygame.font.Font('fonts/Howdy Frog.ttf', 25)
        #pygame.mixer.music.load('sound/music.wav')

        #SCREEN_UPDATE = pygame.USEREVENT
        #pygame.time.set_timer(SCREEN_UPDATE, 150)
        #pygame.mixer.music.play(-1, 0.0)

        #main_game = MAIN()

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

                screen.fill((175,215,70)) #screen color
                main_game.draw_elements()
                pygame.display.update()
                clock.tick(60) #framerate
    
    except RETURNTOMENU:
        return  
main()