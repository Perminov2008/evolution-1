from __future__ import annotations
import random
import config


class DiedBot:
    def __init__(self, x, y, energy):
        self.x = x
        self.y = y
        self.energy = energy
        self.rgb = [0, 0, 0]

    def __eq__(self, other):
        return (self.x == other.x) and (self.y == other.y)

    def kill_me(self, list_of_bots: list[list[Bot | DiedBot | None]]):
        list_of_bots[self.x][self.y] = None


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

    def move(self, list_of_bots: list[list[Bot | DiedBot | None]]):
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
                case _:
                    self._change_genom_point(action)
        else:
            self.kill_me(list_of_bots)
        if self.age >= self._max_age or self.energy <= 0:
            self.kill_me(list_of_bots)

    def _multiplicate(self, x: int, list_of_bots: list[list[Bot | DiedBot | None]]):
        coordinates = (self.x, self.y)
        self._go(x, list_of_bots)
        if self.energy < config.EnergyToCreateBot:
            return
        list_of_bots[coordinates[0]][coordinates[1]] = Bot(*coordinates, self, energy=config.EnergyWhenBirth)
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
                raise Exception("Вы долбаеб, и передали в эту функцию неправельный a")
        return coordinates[0] % config.WindowX, coordinates[1] % config.WindowY

    def _get_entity_at_pos(self, x: int, list_of_bots: list[list[Bot | DiedBot | None]]):
        position_coordinates = self._get_coordinates_to_move(x)
        return list_of_bots[position_coordinates[0]][position_coordinates[1]]

    def _add_energy(self, x: int):
        self.energy = min(self.energy + x, config.MaxEnergy)

    def _get_energy_from_sun(self):
        self._add_energy(config.EnergyFromSun[self.y])
        self._change_genom_point(1)
        self.eat_rgb[1] = min(255, 1 + self.eat_rgb[1])
        self.eat_rgb[0] = max(0, -1 + self.eat_rgb[0])
        self.eat_rgb[2] = max(0, -1 + self.eat_rgb[2])

    def _see(self, x: int, list_of_bots: list[list[Bot | DiedBot | None]]):
        entity = self._get_entity_at_pos(x, list_of_bots)
        if isinstance(entity, DiedBot):
            self._change_genom_point(2)
        elif entity is not None:
            if entity.rasa_rgb is self.rasa_rgb:
                self._change_genom_point(3)
            else:
                self._change_genom_point(4)
        else:
            self._change_genom_point(1)

    def _move_me_at(self, x: int, y: int, list_of_bots: list[list[Bot | DiedBot | None]]):
        list_of_bots[self.x][self.y] = None
        list_of_bots[x][y] = self
        self.x = x
        self.y = y

    def _eat_bot(self, entity: Bot):
        self._add_energy(int(entity.energy * config.WhenEatBot))
        self.eat_rgb[1] = max(0, -1 + self.eat_rgb[1])
        self.eat_rgb[0] = max(0, -1 + self.eat_rgb[0])
        self.eat_rgb[2] = min(255, +1 + self.eat_rgb[2])

    def _eat_die_bot(self, entity: DiedBot):
        self._add_energy(entity.energy)
        self.eat_rgb[1] = max(0, -1 + self.eat_rgb[1])
        self.eat_rgb[0] = min(255, +1 + self.eat_rgb[0])
        self.eat_rgb[2] = max(0, -1 + self.eat_rgb[2])

    def _go(self, x: int, list_of_bots: list[list[Bot | DiedBot | None]]):
        self._see(x, list_of_bots)
        self._add_energy(-config.MoveEnergy)
        entity = self._get_entity_at_pos(x, list_of_bots)
        if isinstance(entity, DiedBot):
            self._eat_die_bot(entity)
        elif entity is not None:
            self._eat_bot(entity)
        self._move_me_at((self.x - 1) % config.WindowX, (self.y - 1) % config.WindowY, list_of_bots)

    def _check_my_y_coordinate(self):
        self._change_genom_point(self.y + 1)

    def __eq__(self, other):
        return (self.x == other.x) and (self.y == other.y)

    def _check_my_energy(self):
        self._change_genom_point(self.energy)

    def _check_age(self):
        self._change_genom_point(self.age)

    def _change_genom_point(self, x: int):
        self._genom_point = (x + self._genom_point) % config.GenomShape

    def copy_genom(self):
        return self._genom

    def kill_me(self, list_of_bots: list[list[Bot | DiedBot | None]]):
        if self.energy <= 0:
            list_of_bots[self.x][self.y] = None
        list_of_bots[self.x][self.y] = DiedBot(self.x, self.y, int(self.energy * config.WhenDie))
