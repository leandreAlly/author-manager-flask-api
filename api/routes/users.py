from flask import Blueprint, request
from api.utils.responses import response_with
from api.utils import responses as resp
from api.models.users import User, UserSchema
from api.utils.database import db
from flask_jwt_extended import create_access_token
from marshmallow import ValidationError
import logging

logger = logging.getLogger(__name__)
user_routes = Blueprint("user_routes", __name__)

@user_routes.route("/", methods=['POST'])
def create_user():
    try:
        data = request.get_json()
        if not data:
            return response_with(
                resp.BAD_REQUEST_400,
                message="The input should be provided"
            )

        if User.find_by_username(data.get('username')):
            return response_with(
                resp.INVALID_INPUT_422,
                message="Username already exists"
            )
        
        if User.find_by_email(data.get("email")):
            return response_with(
                resp.INVALID_INPUT_422,
                message="Email already exists"
            )
        
        try:
            # Hash password
            data["password"] = User.generate_hash(data['password'])

            user_schema = UserSchema()
            user = user_schema.load(data)
            result = user_schema.dump(user.create())

            return response_with(
                resp.SUCCESS_201,
                value={"user": result},
                message="User created successfully"
            )
        
        except ValidationError as e:
            # Catch ValidationError explicitly
            return response_with(
                resp.INVALID_INPUT_422,
                message=f"Validation error: {e.messages}"
            )

    except Exception as e:
        logger.exception("Error while creating user")
        return response_with(
            resp.INVALID_INPUT_422,
            message="An error occurred while creating the user."
        )

