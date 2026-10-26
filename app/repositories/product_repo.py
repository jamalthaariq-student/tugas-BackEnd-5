categories = [
    {"id": 1, "name": "Elektronik"},
    {"id": 2, "name": "Pakaian"},
    {"id": 3, "name": "Peralatan Rumah Tangga"}
]

items = [
    {"id": 1, "name": "Laptop", "category": "Elektronik", "price": 7500000, "stock": 12},
    {"id": 2, "name": "Smartphone", "category": "Elektronik", "price": 4000000, "stock": 20},
    {"id": 3, "name": "Kaos Polos", "category": "Pakaian", "price": 50000, "stock": 50},
    {"id": 4, "name": "Blender", "category": "Peralatan Rumah Tangga", "price": 350000, "stock": 15},
    {"id": 5, "name": "Headphone", "category": "Elektronik", "price": 450000, "stock": 25},
    {"id": 6, "name": "Keyboard Mekanis", "category": "Elektronik", "price": 650000, "stock": 10},
    {"id": 7, "name": "Kemeja", "category": "Pakaian", "price": 175000, "stock": 35},
    {"id": 8, "name": "Jaket", "category": "Pakaian", "price": 320000, "stock": 12},
    {"id": 9, "name": "Rice Cooker", "category": "Peralatan Rumah Tangga", "price": 400000, "stock": 18},
    {"id": 10, "name": "Kipas Angin", "category": "Peralatan Rumah Tangga", "price": 275000, "stock": 14}
]

def get_all_categories():
    return categories

def get_all_items():
    return items

def get_item_by_id(item_id):
    return next((i for i in items if i['id'] == item_id), None)

def update_item(item_id, name, category, price, stock=None):
    item = get_item_by_id(item_id)
    if item:
        if name: item['name'] = name
        if category: item['category'] = category
        if price is not None: item['price'] = price
        if stock is not None: item['stock'] = stock
    return item

def delete_item(item_id):
    global items
    item = get_item_by_id(item_id)
    if item:
        items = [i for i in items if i['id'] != item_id]
        return True
    return False

def add_item(name, category, price, stock=0):
    global items
    item = {"id": len(items) + 1, "name": name, "category": category, "price": price, "stock": stock}
    items.append(item)
    return item