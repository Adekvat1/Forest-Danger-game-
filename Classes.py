import math, os, random
import text_data, names
from colorama import Fore, Style

def clear(): os.system('cls') if os.name == 'nt' else os.system('clear')

class Enemy:
    def __init__(self, name, atk, hp, arm, exp):
        self.name = name
        self.atk = atk
        self.hp = hp
        self.max_hp = hp
        self.exp = exp
        self.arm = arm
        self.max_arm = 50
        self.is_playable = False
        self.kills = 0

        if self.arm > self.max_arm: self.arm = self.max_arm

    def min_max(self):
        if self.hp < 0: self.hp = 0

class Game:
    def __init__(self):
        "difficulty:"
        "1.1 -> infinity, for correct work"
        self.difficulty = 1.1
        self.show_info = True
        self.easy_mode = False
        self.enemy_min_hp = 10
        self.enemy_max_hp = 30
        self.enemy_min_arm = 0
        self.enemy_max_arm = 5

    def update_text(self, player):
        text = {
            "level_up_buy": f"\n\nПовышение уровня: Стоимость {player.exp_to_next_level}EXP. Даёт +{player.atk_up_step} к ATK\n(Нажмите пробел чтобы принять)",
            "level_up": f"\nВы успешно повысили уровень! Текущий уровень: {player.level}",
            "help": f"{Fore.LIGHTBLACK_EX}\n[Пример: Space + Enter чтобы применить]\n[Enter чтобы пропустить]\n{Style.RESET_ALL}",
            "atk": f"\n{Fore.LIGHTBLACK_EX}Нажмите Enter чтобы ударить врага!\nИли Space + Enter чтобы убежать.{Style.RESET_ALL}"
        }
        return text

    def difficulty_up(self, items, player):
        addition = random.randint(5, 10)

        self.enemy_min_hp = int(self.enemy_min_hp + (player.atk / 2))
        self.enemy_max_hp = int(self.enemy_max_hp + (player.atk / 2))

        self.enemy_min_arm = self.enemy_min_arm + addition
        self.enemy_max_arm = self.enemy_max_arm + addition
        if self.enemy_min_arm >= self.enemy_max_arm: self.enemy_min_arm = self.enemy_max_arm - 5

        for i in items:
            i.difficulty_up(self.difficulty)

    def generate_enemy(self):
        enemy_names = names.get_names()
        new_hp = random.randint(self.enemy_min_hp, self.enemy_max_hp)
        new_atk = int(new_hp / 2)
        new_arm = random.randint(self.enemy_min_arm, self.enemy_max_arm)
        new_exp = new_atk * 3 + new_arm

        enemy = Enemy(random.choice(enemy_names), atk=new_atk, hp=new_hp, arm=new_arm, exp=new_exp)
        return enemy

    def reset_enemy_stats(self):
        self.enemy_min_arm = 0
        self.enemy_max_arm = 5
        self.enemy_min_hp = 10
        self.enemy_max_hp = 30

class Player:
    def __init__(self, name, atk, hp, stm):
        self.name = name
        self.atk = atk
        self.max_atk = atk
        self.hp = hp
        self.max_hp = hp
        self.exp = 0
        self.is_playable = True
        self.score = 0
        self.kills = 0
        self.level = 1
        self.stm = stm
        self.max_stm = stm
        self.atk_up_step = 5
        self.exp_to_next_level = 75
        self.arm = 0
        self.max_arm = 50
        self.inv = []
        self.inv_max = 2

    def level_up(self, game):
        self.atk += self.atk_up_step
        self.exp -= self.exp_to_next_level
        self.level += 1
        self.exp_to_next_level = int(self.exp_to_next_level * game.difficulty)

    def reset(self, game):
        self.hp = self.max_hp
        self.exp = 0
        self.atk = self.max_atk
        self.score = 0
        self.kills = 0
        self.stm = self.max_stm
        self.exp_to_next_level = 75
        game.reset_enemy_stats()

    def min_max(self):
        self.hp = min(self.hp, self.max_hp)
        self.stm = min(self.stm, self.max_stm)

    def try_lvlup(self, game, all_items, text):
        if self.exp >= self.exp_to_next_level:
            clear()
            print(
                text_data.get_current_stats(self, game),
                text["level_up_buy"]
            )
            choice = input()
            if choice != "":
                self.level_up(game)
                game.difficulty_up(all_items, self)
                clear()
                print(
                    text_data.get_current_stats(self, game),
                    text["level_up"]
                )

    def attack(self, enemy):
        damage = int((enemy.atk / 100) * (100 - self.arm))
        self.hp -= damage
        attack = int((self.atk / 100) * (100 - enemy.arm))
        enemy.hp -= attack
        return self.hp, enemy.hp

    def get_stats(self):
        stats = {
            "hp": self.hp,
            "max_hp": self.max_hp,
            "stm": self.stm,
            "max_stm": self.max_stm,
            "atk": self.atk,
            "max_atk": self.max_atk,
            "exp": self.exp,
            "level": self.level,
            "arm": self.arm,
            "max_arm": self.max_arm
        }
        return stats

    def apply_stats(self, stats):
        self.hp = stats["hp"]
        self.max_hp = stats["max_hp"]
        self.stm = stats["stm"]
        self.max_stm = stats["max_stm"]
        self.atk = stats["atk"]
        self.max_atk = stats["max_atk"]
        self.exp = stats["exp"]
        self.level = stats["level"]
        self.arm = stats["arm"]
        self.max_arm = stats["max_arm"]

class Items:
    def __init__(self, name, meta, link):
        self.name = name
        self.meta = meta
        self.link = link

    def activate_item(self, player):
        self.link(player, self)
        if self.meta["count"] > 0:
            self.meta["count"] -= 1

    def difficulty_up(self, difficulty):
        self.meta["cost"] = math.ceil(self.meta["cost"] * difficulty)

class Market:
    def __init__(self):
        self.name = "Marketplace"

    def get_allowed_items(all_items, player):
        items = []
        for i in all_items:
            if i.meta["count"] != 0 and i.meta["req"] <= player.level:
                items.append(i)

        return items