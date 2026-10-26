from flask import Blueprint, request
from app.services import product_service
from app.utils.response_helper import success_response, fail_response

product_bp = Blueprint('product_bp', __name__)

@product_bp.route('/api/v1/categories', methods=['GET'])
def get_categories():
    data = product_service.get_categories()
    return success_response(data={"categories": data, "total": len(data)})

@product_bp.route('/api/v1/items', methods=['GET'])
def get_items():
    category_query = request.args.get('category')
    min_price_query = request.args.get('min_price', type=int)
    
    data = product_service.get_items(category_query, min_price_query)
    return success_response(data={"items": data, "total": len(data)})

@product_bp.route('/api/v1/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = product_service.get_item(item_id)
    if not item:
        return fail_response(
            [{"field": "item_id", "reason": "Barang tidak ditemukan"}],
            message="Data tidak ditemukan",
            status_code=404
        )
    return success_response(data=item)

@product_bp.route('/api/v1/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return fail_response(
            [{"field": "body", "reason": "Body harus berupa objek JSON"}],
            message="Input tidak valid"
        )

    result = product_service.update_item(item_id, data)
    
    if isinstance(result, dict) and "errors" in result:
        return fail_response(result["errors"], message="Input tidak valid")
        
    if not result:
        return fail_response(
            [{"field": "item_id", "reason": "Barang tidak ditemukan"}],
            message="Data tidak ditemukan",
            status_code=404
        )
        
    return success_response(data=result, message="Data diperbarui")

@product_bp.route('/api/v1/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    is_deleted = product_service.delete_item(item_id)
    if not is_deleted:
        return fail_response(
            [{"field": "item_id", "reason": "Barang tidak ditemukan"}],
            message="Data tidak ditemukan",
            status_code=404
        )
    return success_response(message="Data berhasil dihapus")

@product_bp.route('/api/v1/items', methods=['POST'])
def add_item():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return fail_response(
            [{"field": "body", "reason": "Body harus berupa objek JSON"}],
            message="Input tidak valid"
        )

    result = product_service.add_item(data)
    
    if isinstance(result, dict) and "errors" in result:
        return fail_response(result["errors"], message="Input tidak valid")
        
    return success_response(data=result, message="Data berhasil ditambahkan", status_code=201)