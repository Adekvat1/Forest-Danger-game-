import random, os, json
import Classes, text_data
from items_data import all_items

player = Classes.Player(name="You", atk=10, max_hp=100, stm=100)
game = Classes.Game()

try:
    with open("stats.json", "r", encoding="UTF-8") as f:
        player_stats = json.load(f)
except FileNotFoundError:
    player_stats = {
        "max_exp": 0,
        "max_kills": 0,
        "max_level": 0
    }

def clear(): os.system('cls') if os.name == 'nt' else os.system('clear')

def save_data(data):
    with open("stats.json", "w", encoding="UTF-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def update_info(player, game):
    text = game.update_text(player)
    if game.show_info:
        text['level_up_buy'] = text['level_up_buy'] + text['help']
    return text

def attack(player, enemy):
    damage = int(enemy.atk / 100) * (100 - player.arm)
    effect(damage, player.atk, player.inv)
    player.hp -= damage
    enemy.hp -= player.atk
    return player.hp, enemy.hp

def get_win(player, enemy):
    if player.hp <= 0:
        return 1 # lose
    elif player.stm <= 0:
        return 1 # lose
    elif player.hp > 0:
        if enemy.hp <= 0:
            return 2 # win
        elif enemy.hp > 0:
            return 0 # continue

def generate_enemy(game):
    names = [
        "Zombie",
        "Skeleton",
        "Witch",
        "Homeless dog",
        "Spider"
    ]
    new_hp = random.randint(game.enemy_min_hp, game.enemy_max_hp)
    new_atk = int(new_hp / 2)
    new_exp = new_atk * 3

    enemy = Classes.Enemy(random.choice(names), atk=new_atk, max_hp=new_hp, exp=new_exp)

    return enemy

def effect(damage, atk, inventory):
    for item in inventory:
        if item.meta["count"] > 0:
            item.effect(damage, atk)

def main():
    global player_stats
    while True: # main cycle

        current_enemy = generate_enemy(game)
        text = update_info(player, game)

        while True: # attack cycle
            clear()
            state = get_win(player, current_enemy)
            if state == 1:
                text_data.game_over_screen(player, player_stats, save_data)
            print(text_data.get_current_stats(player, game))
            print(text_data.get_current_enemy(current_enemy))
            player_stats = text_data.update_data(player, player_stats)

            choice = input(text["atk"] if game.show_info else "")

            if choice == "": # Enter
                player.stm -= 5
                player.hp, current_enemy.hp = attack(player=player, enemy=current_enemy)
                state = get_win(player, current_enemy)
                if state:

                    if state == 1:
                        text_data.game_over_screen(player, player_stats, save_data)
                        break

                    else: # get_win() == 2
                        player.exp += current_enemy.exp
                        player.score += current_enemy.exp
                        player.kills += 1
                        current_enemy.set_max_stats()
                        clear()
                        print(text_data.get_current_stats(player, game))
                        text_data.string_shreder(text="You win!", peak_spaces=5, delay=0.07)
                        break

                else: # get_win() == 0
                    continue
            else: # anything except Enter
                player.stm -= 25
                break

        if game.easy_mode:
            if player.hp < player.hp // 2:
                player.hp += 10
            if player.stm < player.stm // 2:
                player.stm += 10
        player.min_max()
        state = get_win(player, current_enemy)
        if state == 1:
            text_data.game_over_screen(player, player_stats, save_data)
            break

        text = update_info(player, game)
        player.try_lvlup(game, all_items, text)

        if player.exp > 0:
            current_page = 0
            while True: # marketplace cycle
                choice, current_page, pages, items = text_data.marketplace(all_items, player, game, current_page)

                try:
                    choice = int(choice)
                except:
                    choice = str(choice)

                if type(choice) == str:
                    choice = choice.lower()
                    if choice == "":
                        break
                    elif choice in ["z", "я"]:
                        current_page -= 1
                        if current_page < 0:
                            current_page = len(pages) - 1
                    elif choice in ["x", "ч"]:
                        current_page += 1
                        if current_page > len(pages) - 1:
                            current_page = 0
                elif type(choice) == int:
                    for i in range(len(items)):
                        if choice - 1 == i:
                            if items[i].meta["cost"] < player.exp:
                                items[i].activate_item(player)
                player.min_max()

if __name__ == "__main__":
    clear()
    choice = input("Чтобы включить подсказки, нажмите Space + Enter. Для пропуска Enter.")
    if choice == "": game.show_info = False
    else: game.show_info = True
    clear()
    choice = input("Чтобы включить Лёгкий Режим, нажмите Space + Enter. Для пропуска Enter.")
    if choice == "": game.easy_mode = False
    else: game.easy_mode = True
    clear()
    text = update_info(player, game)
    main()