from Classes import Items

placeholder = "\n{}. {} {}\nСтоимость: {}EXP\nДаёт +{} к "

def check(player, item):
    stats = player.get_stats()
    if stats[item.meta["type"]] >= stats["max_" + item.meta["type"]]:
        return False
    else: return True

def pay(player, item):
    if check(player, item):
        player.exp -= item.meta["cost"]
    return player

def medkit_func(player, medkit):
    player = pay(player, medkit)
    player.hp += medkit.meta["addition"]
    return player

def atk_boost_func(player, atk_boost):
    player = pay(player, atk_boost)
    player.atk += atk_boost.meta["addition"]
    return player

def food_func(player, food):
    player = pay(player, food)
    player.stm += food.meta["addition"]
    return player

def sword_func(player, sword):
    player = pay(player, sword)
    player.atk += sword.meta["addition"]
    return player

def iron_chestplate_func(player, iron_chestplate):
    player = pay(player, iron_chestplate)
    player.arm += iron_chestplate.meta["addition"]
    return player

def test_item_func(player, test_item):
    player = pay(player, test_item)
    player.hp += test_item.meta["addition"]
    return player

medkit = Items(
    name="Medkit",
    meta = {
        "cost": 15,
        "addition": 30,
        "count": -1,
        "type": "hp",
        "buy_word": placeholder + "HP",
        "placeholder": placeholder + "HP",
        "req": 1
    },
    link=medkit_func
    )

food = Items(
    name="Food",
    meta = {
        "cost": 5,
        "addition": 20,
        "count": -1,
        "type": "stm",
        "buy_word": placeholder + "STM",
        "placeholder": placeholder + "STM",
        "req": 1
    },
    link=food_func
)

sword = Items(
    name="Wooden Sword",
    meta = {
        "cost": 50,
        "addition": 5,
        "count": 1,
        "type": "atk",
        "buy_word": placeholder + "ATK",
        "placeholder": placeholder + "ATK",
        "req": 1
    },
    link=sword_func
)

iron_chestplate = Items(
    name="Iron Chestplate",
    meta = {
        "cost": 60,
        "addition": 10,
        "count": 1,
        "type": "arm",
        "buy_word": placeholder + "ARM",
        "placeholder": placeholder + "ARM",
        "req": 1
    },
    link=iron_chestplate_func
)

atk_boost = Items(
    name="ATK Up",
    meta = {
        "cost": 100,
        "addition": 5,
        "count": 1,
        "type": "atk",
        "buy_word": placeholder + "ATK",
        "placeholder": placeholder + "ATK",
        "req": 1
    },
    link=atk_boost_func
)

test_item = Items(
    name="Test Item",
    meta = {
        "cost": 1,
        "addition": 1,
        "count": 1,
        "type": "hp",
        "buy_word": placeholder + "HP",
        "placeholder": placeholder + "HP",
        "req": 1
    },
    link=test_item_func
)

all_items = [medkit, food, sword, iron_chestplate]