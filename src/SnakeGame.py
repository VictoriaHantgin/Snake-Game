import pygame, sys

class FRUIT:
    def __init__(self):
        # crearte an x and y pos
        # draw a square

pygame.init()
cell_size = 40
cell_number = 20
screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size)) #size of window
clock = pygame.time.Clock()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    screen.fill((175,215,70)) #screen color
    pygame.display.update()
    clock.tick(60) #framerate
