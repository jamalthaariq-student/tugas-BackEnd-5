from app.repositories import product_repo

def _validate_item_data(data, partial=False):
    errors = []

    if not partial or "name" in data:
        name = data.get("name")
        if not isinstance(name, str) or not name.strip():
            errors.append({"field": "name", "reason": "Nama barang wajib diisi dan tidak boleh kosong"})

    if not partial or "category" in data:
        category = data.get("category")
        valid_categories = [item["name"] for item in product_repo.get_all_categories()]
        if category not in valid_categories:
            errors.append({"field": "category", "reason": "Kategori wajib diisi dengan kategori yang tersedia"})

    if not partial or "price" in data:
        price = data.get("price")
        if isinstance(price, bool) or not isinstance(price, (int, float)):
            errors.append({"field": "price", "reason": "Harga wajib berupa angka"})
        elif price <= 0:
            errors.append({"field": "price", "reason": "Harga harus lebih besar dari 0"})

    if "stock" in data:
        stock = data.get("stock")
        if isinstance(stock, bool) or not isinstance(stock, int):
            errors.append({"field": "stock", "reason": "Stok wajib berupa bilangan bulat"})
        elif stock < 0:
            errors.append({"field": "stock", "reason": "Stok tidak boleh kurang dari 0"})

    return errors


def get_categories():
    return product_repo.get_all_categories()

def get_items(category_query=None, min_price_query=None):
    filtered = product_repo.get_all_items()
    
    if category_query:
        filtered = [i for i in filtered if i['category'].lower() == category_query.lower()]
        
    if min_price_query is not None:
        filtered = [i for i in filtered if i['price'] >= min_price_query]
        
    return filtered

def get_item(item_id):
    return product_repo.get_item_by_id(item_id)

def update_item(item_id, data):
    errors = _validate_item_data(data, partial=True)
    if errors:
        return {"errors": errors}

    return product_repo.update_item(
        item_id,
        data.get('name'),
        data.get('category'),
        data.get('price'),
        data.get('stock')
    )

def delete_item(item_id):
    return product_repo.delete_item(item_id)

def add_item(data):
    errors = _validate_item_data(data)
    if errors:
        return {"errors": errors}

    return product_repo.add_item(
        data.get('name'),
        data.get('category'),
        data.get('price'),
        data.get('stock', 0)
    )