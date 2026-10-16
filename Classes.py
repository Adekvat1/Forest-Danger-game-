import math

class Enemy:
    def __init__(self, name, atk, max_hp, exp):
        self.name = name
        self.atk = atk
        self.hp = max_hp
        self.max_hp = max_hp
        self.exp = exp
        self.is_playable = False
        self.kills = 0

    def set_max_stats(self):
        if self.hp < 0: self.hp = 0

class Game:
    def __init__(self):
        "difficulty:"
        "1.1 -> infinity, for correct work"
        self.difficulty = 1.1
        self.show_info = True
        self.easy_mode = False
        self.enemy_max_hp = 30
        self.enemy_min_hp = 10

    def update_text(self, player):
        text = {
            "level_up_buy": f"\nПовышение уровня: Стоимость {player.exp_to_next_level}EXP. Увеличивает вашу ATK на +10\n",
            "level_up": f"\nВы успешно повысили уровень! Текущий уровень: {player.level}",
            "help": "---\n[Пример: Space + Enter чтобы применить]\n[Enter чтобы пропустить]\n",
            "atk": "\nНажмите Enter чтобы ударить врага!\nИли Space + Enter чтобы убежать."
        }
        return text

    def difficulty_up(self, items, player):
        self.enemy_min_hp = int(self.enemy_min_hp + (player.atk / 2))
        self.enemy_max_hp = int(self.enemy_max_hp + (player.atk / 2))
        for i in items:
            i.difficulty_up(self.difficulty)

class Player:
    def __init__(self, name, atk, max_hp, stm):
        self.name = name
        self.atk = atk
        self.max_atk = atk
        self.hp = max_hp
        self.max_hp = max_hp
        self.exp = 0
        self.is_playable = True
        self.score = 0
        self.kills = 0
        self.level = 1
        self.stm = stm
        self.stm_max = stm
        self.atk_up_step = 10
        self.exp_to_next_level = 100
        self.arm = 0
        self.inv = []
        self.inv_max = 2

    def level_up(self, game):
        self.atk += self.atk_up_step
        self.exp -= self.exp_to_next_level
        self.level += 1
        self.exp_to_next_level = int(self.exp_to_next_level * game.difficulty)

    def reset(self):
        self.hp = self.max_hp
        self.exp = 0
        self.atk = self.max_atk
        self.score = 0
        self.kills = 0
        self.stm = self.stm_max
        self.exp_to_next_level = 100

    def min_max(self):
        if self.hp > self.max_hp: self.hp = self.max_hp
        if self.stm > self.stm_max: self.stm = self.stm_max

class Items:
    def __init__(self, name, meta, link):
        self.name = name
        self.meta = meta
        self.link = link

    def activate_item(self, player):
        self.link(player, self)

    def difficulty_up(self, difficulty):
        self.meta["cost"] = math.ceil(self.meta["cost"] * difficulty)

class Effect:
    def __init__(self, name, meta, effect):
        self.name = name
        self.meta = meta
        self.effect = effect