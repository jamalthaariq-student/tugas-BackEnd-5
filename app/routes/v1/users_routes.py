from flask import Blueprint, request
from app.services import user_service
from app.utils.response_helper import success_response, fail_response

user_bp_v1 = Blueprint('user_v1', __name__, url_prefix='/api/v1/users')

@user_bp_v1.route('', methods=['GET'])
def get_users():
    users = user_service.get_users()
    return success_response(data={"users": users, "total": len(users)})

@user_bp_v1.route('', methods=['POST'])
def register_user():
    if not request.is_json:
        return fail_response(
            [{"field": "Content-Type", "reason": "Header harus application/json"}],
            message="Input tidak valid"
        )
    
    body = request.get_json(silent=True)
    if not isinstance(body, dict):
        return fail_response(
            [{"field": "body", "reason": "Body harus berupa objek JSON"}],
            message="Input tidak valid"
        )

    errors = []
    
    if not isinstance(body.get("username"), str) or not body["username"].strip():
        errors.append({"field": "username", "reason": "Username wajib diisi"})
        
    if not isinstance(body.get("email"), str) or "@" not in body["email"]:
        errors.append({"field": "email", "reason": "Email wajib diisi dengan format yang valid"})

    if body.get("role") != "user":
        errors.append({"field": "role", "reason": "Role pendaftaran hanya boleh bernilai user"})
        
    if errors:
        return fail_response(errors, message="Input tidak valid")
    
        
    new_user = user_service.register_user(
        body["username"],
        body["email"],
        body["role"]
    )
    return success_response(data=new_user, message="User berhasil didaftarkan", status_code=201)

    