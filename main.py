import pygame
import config
import random
from bot_and_square import Bot, Square


def get_iterator_to_preset_bots() -> tuple[int, int]:
    for i in range(config.WindowX):
        for j in range(config.WindowY):
            yield i, j


def draw_world():
    sc.fill(config.BackGroundColour)


def draw_bot(bot: Bot, mode="eat"):
    if bot is None:
        return
    bot_rect = pygame.Rect(
        bot.x * (config.SquareSize + config.Indent) + config.Indent,
        bot.y * (config.SquareSize + config.Indent) + config.Indent,
        config.SquareSize,
        config.SquareSize
    )

    match mode:
        case "eat":
            pygame.draw.rect(sc, bot.eat_rgb, bot_rect)
        case "rasa":
            pygame.draw.rect(sc, bot.rasa_rgb, bot_rect)


def check_mode():
    global mode
    key = pygame.key.get_pressed()
    if key[pygame.K_e]:
        mode = "eat"
    if key[pygame.K_r]:
        mode = "rasa"


def check_pause():
    global paused
    key = pygame.key.get_pressed()
    if key[pygame.K_SPACE]:
        paused = not paused


pygame.init()
sc = pygame.display.set_mode((config.Indent + (config.SquareSize + config.Indent) * config.WindowX,
                              config.Indent + (config.SquareSize + config.Indent) * config.WindowY))

clock = pygame.time.Clock()

mode = "eat"
paused = False


def f():
    list_of_bots = [[Square(x, y) for y in range(config.WindowY)] for x in range(config.WindowX)]

    for x, y in random.sample([i for i in get_iterator_to_preset_bots()], config.StartBotCount):
        list_of_bots[x][y].bot = Bot(x, y)

    while True:
        flag = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
        draw_world()
        moved = [[False for _ in range(config.WindowY)] for _ in range(config.WindowX)]
        for x in range(config.WindowX):
            for y in range(config.WindowY):
                if list_of_bots[x][y].bot is not None and not moved[x][y]:
                    if not paused:
                        bot = list_of_bots[x][y].bot
                        bot.move(list_of_bots)
                        moved[bot.x][bot.y] = True
                    flag = True
                    draw_bot(list_of_bots[x][y].bot, mode=mode)
        check_mode()
        check_pause()
        if not flag:
            return
        pygame.display.flip()
        clock.tick(config.FPS)


if __name__ == "__main__":
    gen = 1
    while True:
        f()
        print(f"Сдохло поколение №{gen}")
        gen += 1
