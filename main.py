import pygame
import config
import random
from bot import Bot, DiedBot


def get_iterator_to_preset_bots() -> tuple[int, int]:
    for i in range(config.WindowX):
        for j in range(config.WindowY):
            yield i, j


def draw_world():
    sc.fill(config.BackGroundColour)


def draw_bot(bot: Bot | DiedBot | None, mode="eat"):
    if bot is None:
        return
    bot_rect = pygame.Rect(
        bot.x * (config.SquareSize + config.Indent) + config.Indent,
        bot.y * (config.SquareSize + config.Indent) + config.Indent,
        config.SquareSize,
        config.SquareSize
    )
    if isinstance(bot, Bot):
        match mode:
            case "eat":
                pygame.draw.rect(sc, bot.eat_rgb, bot_rect)
            case "rasa":
                pygame.draw.rect(sc, bot.rasa_rgb, bot_rect)
    else:
        pygame.draw.rect(sc, bot.rgb, bot_rect)


def check_mode():
    global mode
    key = pygame.key.get_pressed()
    if key[pygame.K_e]:
        mode = "eat"
    elif key[pygame.K_r]:
        mode = "rasa"


pygame.init()
sc = pygame.display.set_mode((config.Indent + (config.SquareSize + config.Indent) * config.WindowX,
                              config.Indent + (config.SquareSize + config.Indent) * config.WindowY))

clock = pygame.time.Clock()

mode = "eat"


def f():
    list_of_bots: list[list[Bot | None | DiedBot]]
    list_of_bots = [[None for _ in range(config.WindowY)] for _ in range(config.WindowX)]

    for i, j in random.sample([i for i in get_iterator_to_preset_bots()], config.StartBotCount):
        list_of_bots[i][j] = Bot(i, j)

    while True:
        flag = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
        check_mode()
        draw_world()
        moved = [[False for _ in range(config.WindowY)] for _ in range(config.WindowX)]
        for x in range(config.WindowX):
            for y in range(config.WindowY):
                if isinstance(list_of_bots[x][y], Bot) and not moved[x][y]:
                    bot = list_of_bots[x][y]
                    bot.move(list_of_bots)
                    moved[bot.x][bot.y] = True
                    flag = True
                draw_bot(list_of_bots[x][y], mode=mode)

        if not flag:
            return
        pygame.display.flip()
        clock.tick(config.FPS)


if __name__ == "__main__":
    i = 0
    while True:
        f()
        print(f"Сдохло поколение №{i + 1}")
        i += 1
