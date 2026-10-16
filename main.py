import random, os, time, json, math

def clear(): os.system('cls') if os.name == 'nt' else os.system('clear')

class Game_settings:
    def __init__(self):
        "difficulty:"
        "1.1 -> infinity, for correct work"
        self.difficulty = 1.1

        self.show_info = True
        self.easy_mode = False

        self.enemy_max_hp = 25
        self.enemy_min_hp = 10

        self.heal_cost = 20
        self.heal_power = 30

Game = Game_settings()

def update_info(Game, player):
    text = {
        "heal": f"\nМед-комплект: Стоимость {Game.heal_cost}EXP. Восстанавливает {Game.heal_power}HP\n",
        "level_up": f"\nПовышение уровня: Стоимость {player.exp_to_next_level}EXP. Увеличивает вашу атаку на +10 ATK\n",
        "help": "---\n[Пример: Space + Enter чтобы применить]\n[Enter чтобы пропустить]\n",
        "buy_medkit": f"\nВы успешно купили мед-комплект!"
    }
    if Game.show_info:
        text['heal'] = text['heal'] + text['help']
        text['level_up'] = text['level_up'] + text['help']
    return text

class Player:
    def __init__(self, name, atk, max_hp, stamina):
        self.name = name
        self.atk = atk
        self.max_atk = atk
        self.hp = max_hp
        self.max_hp = max_hp
        self.exp = 0
        self.is_playable = True
        self.score = 0
        self.kills = 0
        self.inv = []
        self.inv_max_len = 3
        self.level = 1
        self.stamina = stamina
        self.STM_MAX = stamina
        self.atk_up_step = 10
        self.exp_to_next_level = 100

    def regen(self):
        self.hp = self.max_hp

    def level_up(self):
        self.atk += self.atk_up_step
        self.exp -= self.exp_to_next_level
        self.level += 1

    def reset(self):
        self.hp = self.max_hp
        self.exp = 0
        self.atk = self.max_atk
        self.score = 0
        self.inv = []
        self.kills = 0
        self.stamina = self.STM_MAX
        self.exp_to_next_level = 100

    def can_level_up(self):
        if self.exp >= self.exp_to_next_level:
            return True
        else: return False

player = Player(name="You", atk=10, max_hp=100, stamina=100)

class Enemy:
    def __init__(self, name, atk, max_hp, exp):
        self.name = name
        self.atk = atk
        self.hp = max_hp
        self.max_hp = max_hp
        self.exp = exp
        self.is_playable = False
        self.kills = 0

def attack(player, enemy):
    player.hp -= enemy.atk
    enemy.hp -= player.atk

    return player.hp, enemy.hp

def get_bar(current, maximum, length=20):
    if maximum == 0: return "[]"
    filled = int((current / maximum) * length)
    filled = min(filled, length)

    return f"[{'#' * filled}{'_' * (length - filled)}] ({current}/{maximum})"

def get_current_stats(player, easy_mode):
    current_stats = f"""
Ваша статистика{"" if easy_mode is False else " (Лёгкий режим активен)"}:
HP:  {get_bar(player.hp, player.max_hp)}
STM: {get_bar(player.stamina, player.STM_MAX)}
ATK: {get_bar(player.atk, player.max_hp)}
EXP: {get_bar(player.exp, player.exp_to_next_level)}
LVL: {player.level}"""
    return current_stats

def get_current_enemy(enemy):
    current_enemy = f"""
Текущий враг:
NAME: {enemy.name}
HP:  {get_bar(enemy.hp, enemy.max_hp)}
ATK: {get_bar(enemy.atk, player.max_hp, length=20)}
EXP: {get_bar(enemy.exp, player.max_hp, length=20)}"""
    return current_enemy

"""
WIN - 2 is mean, enemy die and player win
LOSE - 1 is mean, player is lose
CONTINUE - 0 is mean, everybody is alive, and game continue
"""

def get_win(player, enemy):
    if player.hp <= 0:
        return 1
    elif player.stamina <= 0:
        return 1
    elif player.hp > 0:
        if enemy.hp <= 0:
            return 2
        elif enemy.hp > 0:
            return 0

def game_difficulty_up(Game, Player):
    Game.enemy_max_hp = round(Game.enemy_max_hp * Game.difficulty)
    Game.enemy_min_hp = round(Game.enemy_min_hp * Game.difficulty)
    Player.exp_to_next_level = int(Player.exp_to_next_level * Game.difficulty)
    Game.heal_cost = int(Game.heal_cost * Game.difficulty)

    return Game, Player

def generate_enemy(game, player):
    bias = random.randint(0, (player.hp // 10))
    new_hp = max(1, (random.randint(game.enemy_min_hp, game.enemy_max_hp) - bias))
    new_atk = math.ceil(new_hp / 2) + bias
    new_exp = int((new_hp / 2) * (new_atk / 2) * game.difficulty) + bias

    enemy = Enemy("Enemy", atk=new_atk, max_hp=new_hp, exp=new_exp)

    return enemy

def game_over_screen(player):
    time.sleep(1)
    clear()
    print(
        f"Опыта получено: {player.score}\n"
        f"Монстров убито: {player.kills}\n"
        f"Максимальный уровень: {player.level}\n"
        "\n"
        "Нажмите Enter чтобы продолжить игру."
    )
    player.reset()
    input()
    clear()

def main(Game, player):
    while True: # main cycle

        current_enemy = generate_enemy(game=Game, player=player)
        text = update_info(Game, player)

        while True: # attack cycle
            clear()
            now = get_win(player, current_enemy)
            if now == 1:
                game_over_screen(player)
            print(get_current_stats(player, Game.easy_mode))
            print(get_current_enemy(current_enemy))

            choice = input("\nНажмите Enter чтобы ударить врага!\nИли Space + Enter чтобы убежать.")

            if choice == "":
                player.hp, current_enemy.hp = attack(player=player, enemy=current_enemy)
                if get_win(player, current_enemy):
                    if get_win(player, current_enemy) == 1:
                        game_over_screen(player)
                        break
                    else: # get_win() == 2
                        print("You Won")
                        player.exp += current_enemy.exp
                        player.score += current_enemy.exp
                        player.kills += 1
                        time.sleep(1)
                        break
                else: # get_win() == 0
                    continue
            else:
                player.stamina -= 25
                break

        if Game.easy_mode:
            player.hp += 10
            player.stamina += 10
        if player.hp > player.max_hp: player.hp = player.max_hp

        time.sleep(0.5)

        while True: # marketplace cycle
            clear()
            print(get_current_stats(player, Game.easy_mode))
            if player.can_level_up():
                choice = input(text['level_up'])
                if choice != "":
                    player.level_up()
                    Game, player = game_difficulty_up(Game, player)
                    clear()
                    print(get_current_stats(player, Game.easy_mode))
                    print(
                        "\n"
                        f"Вы успешно повысили уровень! Текущий уровень: {player.level}"
                    )
                    time.sleep(2.5)
            text = update_info(Game, player)
            clear()
            print(get_current_stats(player, Game.easy_mode))
            if player.exp >= Game.heal_cost and player.hp < player.max_hp: # heal
                choice = input(text['heal'])
                if choice != "":
                    player.exp -= Game.heal_cost
                    player.hp += Game.heal_power
                    if player.hp > player.max_hp: player.hp = player.max_hp
                    print("\nВы купили мед-комплект и восстановили +30 здоровья!")
                else: break
            else: break

def pre_game(Game):
    choice = input("Чтобы включить подсказки, нажмите Space + Enter. Для пропуска Enter.")
    if choice == "": Game.show_info = False
    else: Game.show_info = True
    clear()
    choice = input("Чтобы включить Лёгкий Режим, нажмите Space + Enter. Для пропуска Enter.")
    if choice == "": Game.easy_mode = False
    else: Game.easy_mode = True
    clear()

if __name__ == "__main__":
    pre_game(Game)
    main(Game, player)