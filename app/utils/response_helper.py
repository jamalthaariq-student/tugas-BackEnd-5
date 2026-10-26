from flask import jsonify

def success_response(data=None, message="Success", status_code=200):
    response = {"status": "success", "message": message}
    if data is not None:
        response["data"] = data
    return jsonify(response), status_code

def fail_response(errors, message="Bad Request", status_code=400):
    """
    errors: list of dict, contoh: [{"field": "price", "reason": "Harga tidak boleh minus"}]
    """
    if isinstance(errors, dict):
        errors = [errors]
    response = {
        "status": "fail",
        "message": message,
        "errors": errors
    }
    return jsonify(response), status_code

def error_response(message="Internal Server Error", status_code=500):
    return jsonify({"status": "error", "message": message}), status_code