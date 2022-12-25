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

    def kill_me(self, list_of_bots: ["DiedBot", "Bot"]):
        list_of_bots[self.x][self.y] = None


class Bot:
    def __init__(self, x, y, from_bot: "Bot" = None, energy=100):
        if from_bot is not None:
            self.rgb = from_bot.rgb
            self._genom = from_bot._genom
            mutation_at = random.randint(0, config.GenomShape - 1)
            self._genom[mutation_at] = random.randint(*config.GenomItemsLen)
        else:
            self.rgb = [255, 255, 255]  # белый
            self._genom = [random.randint(*config.GenomItemsLen) for _ in range(config.GenomShape)]
        self.energy = energy
        self.age = 1
        self.x = x
        self.y = y
        self._genom_point = 0

    def move(self, list_of_bots: [DiedBot, "Bot"]):
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
                    self._change_genom_point(action - 28)
        else:
            self._get_energy_from_sun()
        if self.age >= config.MaxAge or self.energy <= 0:
            self.kill_me(list_of_bots)

    def _multiplicate(self, x: int, list_of_bots: ["Bot", DiedBot]):
        coordinates = (self.x, self.y)
        self._go(x, list_of_bots)
        if self.energy < config.MinEnergyToCreateBot:
            return
        list_of_bots[coordinates[0]][coordinates[1]] = Bot(*coordinates, self, energy=config.EnergyWhenBirth)
        self._add_energy(-max(config.KEnergyToCreateBot * self.energy, config.MinEnergyToCreateBot))

    def _add_energy(self, x: int):
        self.energy = min(self.energy + x, config.MaxEnergy)

    def _get_energy_from_sun(self):
        self._add_energy(config.EnergyFromSun[self.y])
        self._change_genom_point(1)
        self.rgb[1] = min(255, 1 + self.rgb[1])
        self.rgb[0] = min(255, -1 + self.rgb[0])
        self.rgb[2] = min(255, -1 + self.rgb[2])

    def _see(self, x: int, list_of_bots: ["Bot", DiedBot]):
        match x:
            case 0:
                entity = list_of_bots[(self.x - 1) % config.WindowX][(self.y - 1) % config.WindowY]
                if isinstance(entity, DiedBot):
                    self._change_genom_point(2)
                elif entity is not None:
                    self._change_genom_point(3)
                else:
                    self._change_genom_point(1)

            case 1:
                entity = list_of_bots[self.x % config.WindowX][(self.y - 1) % config.WindowY]
                if isinstance(entity, DiedBot):
                    self._change_genom_point(2)
                elif entity is not None:
                    self._change_genom_point(3)
                else:
                    self._change_genom_point(1)
            case 2:
                entity = list_of_bots[(self.x + 1) % config.WindowX][(self.y - 1) % config.WindowY]
                if isinstance(entity, DiedBot):
                    self._change_genom_point(2)
                elif entity is not None:
                    self._change_genom_point(3)
                else:
                    self._change_genom_point(1)
            case 3:
                entity = list_of_bots[(self.x + 1) % config.WindowX][self.y % config.WindowY]
                if isinstance(entity, DiedBot):
                    self._change_genom_point(2)
                elif entity is not None:
                    self._change_genom_point(3)
                else:
                    self._change_genom_point(1)
            case 4:
                entity = list_of_bots[(self.x + 1) % config.WindowX][(self.y + 1) % config.WindowY]
                if isinstance(entity, DiedBot):
                    self._change_genom_point(2)
                elif entity is not None:
                    self._change_genom_point(3)
                else:
                    self._change_genom_point(1)
            case 5:
                entity = list_of_bots[self.x % config.WindowX][(self.y + 1) % config.WindowY]
                if isinstance(entity, DiedBot):
                    self._change_genom_point(2)
                elif entity is not None:
                    self._change_genom_point(3)
                else:
                    self._change_genom_point(1)
            case 6:
                entity = list_of_bots[(self.x - 1) % config.WindowX][(self.y + 1) % config.WindowY]
                if isinstance(entity, DiedBot):
                    self._change_genom_point(2)
                elif entity is not None:
                    self._change_genom_point(3)
                else:
                    self._change_genom_point(1)
            case 7:
                entity = list_of_bots[(self.x - 1) % config.WindowX][self.y % config.WindowY]
                if isinstance(entity, DiedBot):
                    self._change_genom_point(2)
                elif entity is not None:
                    self._change_genom_point(3)
                else:
                    self._change_genom_point(1)

    def _move_me_at(self, x: int, y: int, list_of_bots: ["Bot", DiedBot]):
        list_of_bots[self.x][self.y] = None
        list_of_bots[x][y] = self
        self.x = x
        self.y = y

    def _eat_bot(self, entity: "Bot"):
        self._add_energy(entity.energy * config.WhenEatBot)
        self.rgb[1] = max(0, -1 + self.rgb[1])
        self.rgb[0] = max(0, -1 + self.rgb[0])
        self.rgb[2] = min(255, +1 + self.rgb[2])

    def _eat_die_bot(self, entity: DiedBot):
        self.energy += entity.energy
        self.rgb[1] = max(0, -1 + self.rgb[1])
        self.rgb[0] = min(255, +1 + self.rgb[0])
        self.rgb[2] = max(0, -1 + self.rgb[2])

    def _go(self, x: int, list_of_bots: ["Bot", DiedBot]):
        self._see(x, list_of_bots)
        self._add_energy(-config.MoveEnergy)
        match x:
            case 0:
                entity = list_of_bots[(self.x - 1) % config.WindowX][(self.y - 1) % config.WindowY]
                if isinstance(entity, DiedBot):
                    self._eat_die_bot(entity)
                elif entity is not None:
                    self._eat_bot(entity)
                self._move_me_at((self.x - 1) % config.WindowX, (self.y - 1) % config.WindowY, list_of_bots)
            case 1:
                entity = list_of_bots[self.x % config.WindowX][(self.y - 1) % config.WindowY]
                if isinstance(entity, DiedBot):
                    self._eat_die_bot(entity)
                elif entity is not None:
                    self._eat_bot(entity)
                self._move_me_at(self.x % config.WindowX, (self.y - 1) % config.WindowY, list_of_bots)
            case 2:
                entity = list_of_bots[(self.x + 1) % config.WindowX][(self.y - 1) % config.WindowY]
                if isinstance(entity, DiedBot):
                    self._eat_die_bot(entity)
                elif entity is not None:
                    self._eat_bot(entity)
                self._move_me_at((self.x + 1) % config.WindowX, (self.y - 1) % config.WindowY, list_of_bots)
            case 3:
                entity = list_of_bots[(self.x + 1) % config.WindowX][self.y % config.WindowY]
                if isinstance(entity, DiedBot):
                    self._eat_die_bot(entity)
                elif entity is not None:
                    self._eat_bot(entity)
                self._move_me_at((self.x + 1) % config.WindowX, self.y % config.WindowY, list_of_bots)
            case 4:
                entity = list_of_bots[(self.x + 1) % config.WindowX][(self.y + 1) % config.WindowY]
                if isinstance(entity, DiedBot):
                    self._eat_die_bot(entity)
                elif entity is not None:
                    self._eat_bot(entity)
                self._move_me_at((self.x + 1) % config.WindowX, (self.y + 1) % config.WindowY, list_of_bots)
            case 5:
                entity = list_of_bots[self.x % config.WindowX][(self.y + 1) % config.WindowY]
                if isinstance(entity, DiedBot):
                    self._eat_die_bot(entity)
                elif entity is not None:
                    self._eat_bot(entity)
                self._move_me_at(self.x % config.WindowX, (self.y + 1) % config.WindowY, list_of_bots)
            case 6:
                entity = list_of_bots[(self.x - 1) % config.WindowX][(self.y + 1) % config.WindowY]
                if isinstance(entity, DiedBot):
                    self._eat_die_bot(entity)
                elif entity is not None:
                    self._eat_bot(entity)
                self._move_me_at((self.x - 1) % config.WindowX, (self.y + 1) % config.WindowY, list_of_bots)
            case 7:
                entity = list_of_bots[(self.x - 1) % config.WindowX][self.y % config.WindowY]
                if isinstance(entity, DiedBot):
                    self._eat_die_bot(entity)
                elif entity is not None:
                    self._eat_bot(entity)
                self._move_me_at((self.x - 1) % config.WindowX, self.y % config.WindowY, list_of_bots)

    def _check_my_y_coordinate(self):
        self._change_genom_point(self.y + 1)

    def __eq__(self, other):
        return (self.x == other.x) and (self.y == other.y)

    def _check_my_energy(self):
        self._change_genom_point(self.energy)

    def _check_age(self):
        self._change_genom_point(self.age)

    def _change_genom_point(self, x: int):
        self._genom_point = (x + self._genom_point) % (config.GenomItemsLen[1] + 1)

    def copy_genom(self):
        return self._genom

    def kill_me(self, list_of_bots: ["Bot", DiedBot]):
        if self.energy <= 0:
            list_of_bots[self.x][self.y] = None
        list_of_bots[self.x][self.y] = DiedBot(self.x, self.y, self.energy * config.WhenDie)
