def get_allowed_items(all_items, player):
    items = []
    for i in all_items:
        if i.meta["count"] != 0 and i.meta["req"] <= player.level:
            items.append(i)

    return items

def get_pages(items, item_per_page=3):
    step = 1
    page = []
    pages = []
    for i in range(len(items)):
        if step == item_per_page:
            step = 0
            page.append(items[i])
            pages.append(page)
            page = []
        else:
            page.append(items[i])
        step += 1

    if page:
        pages.append(page)
    return pages