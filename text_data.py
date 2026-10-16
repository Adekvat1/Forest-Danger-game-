import time, os
from colorama import Fore, Style
from game import get_bar

def clear(): os.system('cls') if os.name == 'nt' else os.system('clear')

def game_over_screen(player, player_stats, save_data):
    time.sleep(1)
    clear()
    print(
        f"Опыта получено: {player.score}\n"
        f"Монстров убито: {player.kills}\n"
        f"Уровень: {player.level}\n\n"
        "Лучшая статистика за всё время:\n\n"
        f"Опыта получено: {player_stats['max_exp']}\n" 
        f"Монстров убито: {player_stats['max_kills']}\n"
        f"Уровень: {player_stats['max_level']}\n\n"
        "Нажмите Enter чтобы продолжить игру."
    )
    save_data(player_stats)
    player.reset()
    input()
    clear()

def update_data(player, data):
    if data["max_exp"] < player.score:
        data["max_exp"] = player.score
    if data["max_kills"] < player.kills:
        data["max_kills"] = player.kills
    if data["max_level"] < player.level:
        data["max_level"] = player.level
    return data

def string_shreder(text, peak_spaces=5, delay=0.1):
    frames = []
    for i in range(1, len(text) + 1): frames.append(text[-i:] + " ")
    for i in range(1, peak_spaces + 1): frames.append(" " * i + text + " ")
    for _ in range(3): frames.append(" " * peak_spaces + text + " ")
    for i in range(peak_spaces - 1, -1, -1): frames.append(" " * i + text + " ")
    for i in range(1, len(text)): frames.append(text[i:] + " ")
    frames.append(" ")
    for frame in frames:
        print(frame, end="\r")
        time.sleep(delay)
    print()

def get_allowed_items(all_items, player):
    items = []
    for i in all_items:
        if i.meta["count"] != 0 and i.meta["req"] <= player.level:
            items.append(i)

    return items

def get_item_suffix(item, player):
    if player.exp < item.meta["cost"]:
        suffix = Fore.RED + "Not Enough Money" + Style.RESET_ALL
    else:
        suffix = ""
    return suffix

def get_items_visuals(items, player):
    for i in range(len(items)):
        item_number = i + 1
        item = items[i]
        spaces_count = 16 - len(item.name)

        suffix = get_item_suffix(item, player)

        item.meta["buy_word"] = item.meta["placeholder"].format(
            item_number,
            item.name,
            ((" "*spaces_count)+suffix),
            item.meta["cost"],
            item.meta["addition"]
        )
    return items

def marketplace(all_items, player, game, page=1):
    items = get_allowed_items(all_items, player)
    items = get_items_visuals(items, player)
    num_items = len(items)
    item_per_page = 3

    clear()
    print(get_current_stats(player, game) + "\n\n~-~-~ Магазин предметов ~-~-~")
    step = 0
    for _ in range(item_per_page):
        step += 1
    for i in range(len(items)):
        if i < 4:
            print(items[i].meta["buy_word"])
        else:
            print(f"\n~-~-~ <- [Z] {page}/{num_items // item_per_page} [X] -> ~-~-~")
            break
    choice = input()
    return choice, items, page

def get_current_stats(player, game):
    current_stats = f"""
Ваша статистика{"" if game.easy_mode is False else " (Лёгкий режим активен)"}:
HP:  {get_bar(player.hp, player.max_hp)}{"" if player.hp >= 30 else (Fore.RED + " WARN!!" + Style.RESET_ALL)}
STM: {get_bar(player.stm, player.stm_max)}{"" if player.stm >= 25 else (Fore.RED + " WARN!!" + Style.RESET_ALL)}
ATK: {get_bar(player.atk, player.max_hp)}
EXP: {get_bar(player.exp, player.exp_to_next_level)}
ARM: {get_bar(player.arm, 50)}
LVL: {player.level}"""
    return current_stats

def get_current_enemy(enemy):
    current_enemy = f"""
Текущий враг:
NAME: {Fore.RED}{enemy.name}{Style.RESET_ALL}
HP:  {get_bar(enemy.hp, enemy.max_hp)}
ATK: {get_bar(enemy.atk, 100, length=20)}
EXP: {get_bar(enemy.exp, 100, length=20)}"""
    return current_enemy