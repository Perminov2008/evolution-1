import pygame
WIDTH = 1000
HEIGHT = 600
FPS = 30
pole_x = 60
pole_y = 30
move = 25

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Evolution")
clock = pygame.time.Clock()

running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    x = 0
    y = 0
    pygame.draw.rect(screen, blue, (0, 0, WIDTH, HEIGHT), 2)
    for i in range(pole_x):
        x += move
        pygame.draw.line(screen, blue, [x, HEIGHT], [x, 0], 4)
    for i in range(pole_y):
        y += move
        pygame.draw.line(screen, blue, [0, y], [WIDTH, y], 4)
    # pygame.draw.rect(screen, white, (x1, y1, x2, y2))
    x1 = -20
    y1 = -20
    x2 = -5
    y2 = -5
    for i in range(pole_y):
        y1 += move
        y2 += move
        x1 = -20
        x2 = -5
        for j in range(pole_x):
            x1 += move
            x2 += move
            pygame.draw.polygon(screen, white, [[x1, y1], [x1, y2], [x2, y2], [x2, y1]])
    pygame.display.flip()
pygame.quit()
