import os, json, webbrowser
import Classes, text_data
from items_data import all_items

player = Classes.Player(name="You", atk=10, hp=100, stm=100)
game = Classes.Game()

# --------- Not dynamic
STM_PER_STEP = 7

def my_ad(show_ad):
    if show_ad:
        webbrowser.open("https://www.youtube.com/watch?v=M6lF6hee_VA&t=1s")

try:
    with open("stats.json", "r", encoding="UTF-8") as f:
        player_stats = json.load(f)
except FileNotFoundError:
    player_stats = {
        "max_exp": 0,
        "max_kills": 0,
        "max_level": 0
    }

def save_data(data):
    with open("stats.json", "w", encoding="UTF-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def clear(): os.system('cls') if os.name == 'nt' else os.system('clear')

def update_info(player, game):
    text = game.update_text(player)
    if game.show_info:
        text['level_up_buy'] = text['level_up_buy'] + text['help']
    return text

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

def main():
    global player_stats
    while True: # main cycle

        current_enemy = game.generate_enemy()
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
                player.stm -= STM_PER_STEP
                player.hp, current_enemy.hp = player.attack(current_enemy)
                state = get_win(player, current_enemy)
                if state:

                    if state == 1:
                        text_data.game_over_screen(player, player_stats, save_data, game)
                        break

                    else: # get_win() == 2
                        player.exp += current_enemy.exp
                        player.score += current_enemy.exp
                        player.kills += 1
                        clear()
                        print(text_data.get_current_stats(player, game))
                        text_data.string_shreder(text="You win!", peak_spaces=5, delay=0.07)
                        break

                else: # get_win() == 0
                    continue
            else: # anything except Enter
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

        if player.exp > 0: # marketplace cycle
            current_page = 0
            while True:
                choice, current_page, pages, items = text_data.marketplace(all_items, player, game, current_page)

                try:
                    choice = int(choice)
                except ValueError:
                    choice = str(choice)

                if type(choice) == str:
                    choice = choice.lower()
                    if choice == "": # exit
                        break
                    elif choice in ["z", "я"]: # previous page
                        current_page -= 1
                        if current_page < 0:
                            current_page = len(pages) - 1
                    elif choice in ["x", "ч"]: # next page
                        current_page += 1
                        if current_page > len(pages) - 1:
                            current_page = 0
                elif type(choice) == int:
                    for i in range(len(items)):
                        if choice - 1 == i:
                            if items[i].meta["cost"] <= player.exp:
                                items[i].activate_item(player)
                                if current_page > 0: current_page -= 1

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
    choice = input("Чтобы посмотреть обзор на ютубе, нажмите Space + Enter. Для пропуска Enter.")
    my_ad(choice)
    clear()
    text = update_info(player, game)
    main()