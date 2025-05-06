import pygame, sys, random
from pygame.math import Vector2

class SNAKE:
    def __init__(self):
        self.body = [Vector2(5,10), Vector2(4,10), Vector2(3,10)] #starting pos of snake
        self.direction = Vector2(1,0)
        self.new_block = False


    def draw_snake(self):
        for block in self.body:
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)
            pygame.draw.rect(screen, (183, 111, 122), block_rect)
    
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
       
class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()
    
    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()

    def draw_elements(self):
        self.fruit.draw_fruit()
        self.snake.draw_snake()

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.add_block()

    def check_fail(self):
        # check if the snake is outside the screen
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            self.game_over()
        #check if snake hits itself
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()
       
       

    def game_over(self):
        pygame.quit()
        sys.exit()

pygame.init()
cell_size = 40
cell_number = 20
screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size)) #size of window
clock = pygame.time.Clock()
applebig = pygame.image.load('sprites/apple.png').convert_alpha()
apple = pygame.transform.smoothscale(applebig, (cell_size, cell_size))

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)

main_game = MAIN()

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
