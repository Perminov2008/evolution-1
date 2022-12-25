import pygame
import config
import random
from bot import Bot, DiedBot


def get_iterator_to_preset_bots() -> tuple[int, int]:
    for i in range(config.WindowX):
        for j in range(config.WindowY):
            yield i, j


def draw_world():
    sc.fill("light grey")


def draw_bot(bot: None | Bot | DiedBot):
    if bot is None:
        return
    bot_rect = pygame.Rect(
        bot.x * (config.SquareSize + config.Indent)+config.Indent,
        bot.y * (config.SquareSize + config.Indent)+config.Indent,
        config.SquareSize,
        config.SquareSize
    )
    if isinstance(bot, Bot):
        pygame.draw.rect(sc, bot.eat_rgb, bot_rect)
    else:
        pygame.draw.rect(sc, bot.rgb, bot_rect)


pygame.init()
sc = pygame.display.set_mode((850, 350))

fps = 15
clock = pygame.time.Clock()


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
        draw_world()
        moved = [[False for _ in range(config.WindowY)] for _ in range(config.WindowX)]
        for x in range(config.WindowX):
            for y in range(config.WindowY):
                if isinstance(list_of_bots[x][y], Bot) and not moved[x][y]:
                    list_of_bots[x][y].move(list_of_bots)
                    moved[x][y]=True
                    flag = True
                draw_bot(list_of_bots[x][y])

        if not flag:
            f()
        pygame.display.flip()
        clock.tick(fps)


if __name__ == "__main__":
    f()
