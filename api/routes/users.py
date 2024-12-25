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


@user_routes.route("/login", methods = ['POST'])
def authenticate_user():
    try: 
        data = request.get_json()
        current_user = User.find_by_username(data["username"])
        if not current_user:
            return response_with(
                resp.SERVER_ERROR_404,
                message="User not found!"
            )
        
        if User.verify_hash(data['password'], current_user.password):
            access_token = create_access_token(identity=data['username'])
            return response_with(
                resp.SUCCESS_200,
                value={"message": 'Logged in as {}'.format(current_user.username), "access_token": access_token}
            )
        
        else:
            return response_with(resp.UNAUTHORIZED_403)
    except Exception as e:
        logger.error(f"Soemthing went wrong {str(e)}")
        return response_with(resp.INVALID_INPUT_422)