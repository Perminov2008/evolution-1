from __future__ import annotations
import random
import config


class Bot:
    def __init__(self, x, y, from_bot: Bot = None, energy=config.MaxEnergy):
        if from_bot is not None:
            self.eat_rgb = from_bot.eat_rgb
            self.rasa_rgb = from_bot.rasa_rgb
            self._genom = from_bot._genom
            if random.randint(1, config.MutationChance) == 1:
                mutation_at = random.randint(0, config.GenomShape - 1)
                self._genom[mutation_at] = random.randint(config.GenomItemsLen[0], config.GenomItemsLen[1] - 1)
        else:
            self.eat_rgb = [255, 255, 255]  # белый
            self.rasa_rgb = tuple([random.randint(1, 255) for _ in range(3)])
            self._genom = [random.randint(*config.GenomItemsLen) for _ in range(config.GenomShape)]
        self.energy = energy
        self.age = 1
        self.x = x
        self.y = y
        self._max_age = random.choice(config.MaxAges)
        self._genom_point = 0

    def move(self, list_of_bots: list[list[Square]]):
        self.age += 1
        for i in range(1000):
            action = self._genom[self._genom_point]
            match action:
                case 1:
                    self._get_energy_from_sun()
                    break
                case 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9:
                    self._go(action - 2, list_of_bots)
                    break
                case 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17:
                    self._see(action - 10, list_of_bots)
                case 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25:
                    self._multiplicate(action - 18, list_of_bots)
                    break
                case 26:
                    self._check_my_y_coordinate()
                case 27:
                    self._check_my_energy()
                case 28:
                    self._check_age()
                case 29 | 30 | 31 | 32 | 33 | 34 | 35 | 36:
                    self._check_poison(action - 29, list_of_bots)
                case 37 | 38 | 39 | 40 | 41 | 42 | 43 | 44:
                    self._convert_poison_to_energy(action - 37, list_of_bots)
                    break
                case _:
                    self._change_genom_point(action - 44)
        else:
            self.die(list_of_bots)
        if self.age >= self._max_age or self.energy <= 0 or \
                list_of_bots[self.x][self.y].poison >= config.PoisonCountToDie:
            self.die(list_of_bots)

    def _multiplicate(self, x: int, list_of_bots: list[list[Square]]):
        coordinates = (self.x, self.y)
        self._go(x, list_of_bots)
        if self.energy < config.EnergyToCreateBot:
            return
        list_of_bots[coordinates[0]][coordinates[1]].bot = Bot(*coordinates, self, energy=config.EnergyWhenBirth)
        self._add_energy(-config.EnergyToCreateBot)

    def _get_coordinates_to_move(self, a: int):
        match a:
            case 0:
                coordinates = [self.x - 1, self.y - 1]
            case 1:
                coordinates = [self.x, self.y - 1]
            case 2:
                coordinates = [self.x + 1, self.y - 1]
            case 3:
                coordinates = [self.x + 1, self.y]
            case 4:
                coordinates = [self.x + 1, self.y + 1]
            case 5:
                coordinates = [self.x, self.y + 1]
            case 6:
                coordinates = [self.x - 1, self.y + 1]
            case 7:
                coordinates = [self.x - 1, self.y]
            case _:
                raise Exception("Вы долбоеб, и передали в эту функцию неправильный a")
        return coordinates[0] % config.WindowX, coordinates[1] % config.WindowY

    def _get_square_at_pos_x(self, x: int, list_of_bots: list[list[Square]]):
        position_coordinates = self._get_coordinates_to_move(x)
        return list_of_bots[position_coordinates[0]][position_coordinates[1]]

    def _add_energy(self, x: int):
        self.energy = min(self.energy + x, config.MaxEnergy)

    def _get_energy_from_sun(self):
        self._add_energy(config.EnergyFromSun[self.y])
        self._change_genom_point(1)
        self.eat_rgb[0] = max(0, -1 + self.eat_rgb[0])
        self.eat_rgb[1] = min(255, 2 + self.eat_rgb[1])
        self.eat_rgb[2] = max(0, -1 + self.eat_rgb[2])

    def _see(self, x: int, list_of_bots: list[list[Square]]):
        sq = self._get_square_at_pos_x(x, list_of_bots)
        if sq.bot:
            if sq.bot.rasa_rgb == self.rasa_rgb:
                self._change_genom_point(2)
            else:
                self._change_genom_point(3)
        else:
            self._change_genom_point(1)

    def _move_me_at(self, x: int, y: int, list_of_bots: list[list[Square]]):
        list_of_bots[self.x][self.y].bot = None
        list_of_bots[x][y].bot = self
        self.x = x
        self.y = y

    def _eat_bot(self, bot: Bot):
        self._add_energy(int(bot.energy * config.WhenEatBot) - config.EnergyToEatBot)
        self.eat_rgb[0] = min(255, 2 + self.eat_rgb[0])
        self.eat_rgb[1] = max(0, -1 + self.eat_rgb[1])
        self.eat_rgb[2] = max(0, -1 + self.eat_rgb[2])

    def _check_poison(self, x: int, list_of_bots: list[list[Square]]):
        sq = self._get_square_at_pos_x(x, list_of_bots)
        self._change_genom_point(min(sq.poison, config.GenomShape))

    def _convert_poison_to_energy(self, x, list_of_bots: list[list[Square]]):
        sq = self._get_square_at_pos_x(x, list_of_bots)
        self._add_energy(-config.EnergyToConvertPoison)
        self._add_energy(int(min(sq.poison, config.MaxPoisonToConvertIntoEnergy) * config.PoisonToEnergy))
        self.eat_rgb[0] = max(0, -1 + self.eat_rgb[0])
        self.eat_rgb[1] = max(0, -1 + self.eat_rgb[1])
        self.eat_rgb[2] = min(255, 2 + self.eat_rgb[2])
        self._change_genom_point(1)

    def _go(self, x: int, list_of_bots: list[list[Square]]):
        self._change_genom_point(1)
        self._add_energy(-config.MoveEnergy)
        sq = self._get_square_at_pos_x(x, list_of_bots)
        if sq.bot is not None:
            self._eat_bot(sq.bot)
        self._move_me_at(sq.x, sq.y, list_of_bots)

    def _check_my_y_coordinate(self):
        self._change_genom_point(self.y + 1)

    def _check_my_energy(self):
        self._change_genom_point(min(self.energy, config.GenomShape))

    def _check_age(self):
        self._change_genom_point(self.age)

    def _change_genom_point(self, x: int):
        self._genom_point = (x + self._genom_point) % config.GenomShape

    def copy_genom(self):
        return self._genom

    def die(self, list_of_bots: list[list[Square]]):
        list_of_bots[self.x][self.y].bot = None
        for i in range(8):
            coordinates = self._get_coordinates_to_move(i)
            list_of_bots[coordinates[0]][coordinates[1]].add_poison(config.PoisonAddWhenBotDie)
        list_of_bots[self.x][self.y].add_poison(config.PoisonAddWhenBotDie)


class Square:
    def __init__(self, x, y, create_bot=False, poison: int = 0):
        self.x = x
        self.y = y
        if create_bot:
            self.bot = Bot(x, y)
        else:
            self.bot = None
        self.poison = poison

    def do_move(self, list_of_bots: list[list[Square]]):
        if self.bot is not None:
            if self.poison >= config.PoisonCountToDie:
                self.bot.die(list_of_bots)
            else:
                self.bot.move(list_of_bots)
        self.add_poison(-config.PoisonLostPerTurn)

    def add_poison(self, x):
        self.poison = max(0, min(x, config.MaxPoisonOnSquare))
