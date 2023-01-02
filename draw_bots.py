import pygame
import random

# Поле получилось 20 на 15 (Вы просили уменьшить)

WIDTH = 1000
HEIGHT = 750
FPS = 10
pole_x = 20
pole_y = 15
move = 50

white = (255, 255, 255)
gray = (125, 125, 125)
black = (0, 0, 0)
red = (255, 0, 0)
yellow = (225, 225, 0)
blue = (0, 0, 255)
green = (0, 150, 75)

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
    x1 = -45
    y1 = -45
    x2 = -5
    y2 = -5
    screen.fill(green)
    pygame.draw.rect(screen, blue, (0, 0, WIDTH, HEIGHT), 2)
    for i in range(pole_x):
        x += move
        pygame.draw.line(screen, blue, [x, HEIGHT], [x, 0], 4)
    for i in range(pole_y):
        y += move
        pygame.draw.line(screen, blue, [0, y], [WIDTH, y], 4)
    # pygame.draw.rect(screen, white, (x1, y1, x2, y2))
    for i in range(pole_y):
        y1 += move
        y2 += move
        x1 = -45
        x2 = -5
        for j in range(pole_x):
            x1 += move
            x2 += move
            energy = random.randint(10, 100) # Пока что рандомное значение из-за этого на экране часто меняются цвета
            if i < pole_y / 2:  # Здесь должно быть условие на то что в этой клетке бот
                if energy <= 25:
                    pygame.draw.polygon(screen, white, [[x1, y1], [x1, y2], [x2, y2], [x2, y1]])
                elif energy <= 75:
                    pygame.draw.polygon(screen, yellow, [[x1, y1], [x1, y2], [x2, y2], [x2, y1]])
                else:
                    pygame.draw.polygon(screen, red, [[x1, y1], [x1, y2], [x2, y2], [x2, y1]])
                pygame.draw.circle(screen, gray, ((x1 + x2) / 2 + 0.25, (y1 + y2) / 2), 15)
                pygame.draw.polygon(screen, gray,
                                    [[x1 + 5, y1 + 20], [x1 + 5, y2 - 5], [x2 - 5, y2 - 5], [x2 - 5, y1 + 20]])
                pygame.draw.circle(screen, gray, ((x1 + x2) / 2 + 0.25, (y1 + y2) / 2), 15)
                pygame.draw.circle(screen, red, ((x1 + x2) / 2 + 10, (y1 + y2) / 2 - 2), 4)
                pygame.draw.circle(screen, red, ((x1 + x2) / 2 - 10, (y1 + y2) / 2 - 2), 4)
                pygame.draw.polygon(screen, black,
                                    [[x1 + 10, y1 + 27], [x1 + 10, y2 - 10], [x2 - 10, y2 - 10], [x2 - 10, y1 + 27]])
            else: # Здесь должно быть условие на то что в этой клетке яд
                pygame.draw.polygon(screen, white, [[x1, y1], [x1, y2], [x2, y2], [x2, y1]])
                pygame.draw.polygon(screen, green,
                                    [[x1 + 10, y1 + 5], [x1 + 10, y2 - 30], [x2 - 10, y2 - 30], [x2 - 10, y1 + 5]])
                pygame.draw.polygon(screen, green,
                                    [[x1 + 15, y1 + 10], [x1 + 15, y2 - 25], [x2 - 15, y2 - 25], [x2 - 15, y1 + 10]])
                pygame.draw.polygon(screen, green,
                                    [[x1 + 5, y1 + 15], [x1 + 5, y2 - 5], [x2 - 5, y2 - 5], [x2 - 5, y1 + 15]])
                pygame.draw.circle(screen, black, ((x1 + x2) / 2 + 8, (y1 + y2) / 2), 4)
                pygame.draw.circle(screen, black, ((x1 + x2) / 2 - 8, (y1 + y2) / 2), 4)
                pygame.draw.polygon(screen, black,
                                    [[x1 + 10, y1 + 27], [x1 + 10, y2 - 10], [x2 - 10, y2 - 10]])
                pygame.draw.polygon(screen, red,
                                    [[x1 + 10, y1 + 5], [x1 + 10, y2 - 33], [x2 - 10, y2 - 33], [x2 - 10, y1 + 5]])
    pygame.display.flip()
pygame.quit()
