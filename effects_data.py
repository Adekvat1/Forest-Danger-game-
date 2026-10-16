from Classes import Effect

def iron_skin_func(damage, atk, iron_skin):
    if iron_skin.meta["steps"] > 0:
        damage = int(damage / 100 * 90)
        iron_skin.meta["steps"] -= 1
    return damage

iron_skin = Effect(
    name="Iron Skin",
    meta = {
        "cost": 50,
        "count": float('inf'),
    },
    effect=iron_skin_func
)