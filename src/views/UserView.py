from flask import request, json, Response, Blueprint
from ..models.User import UserModel, UserSchema
from marshmallow import ValidationError
from ..shared.Authentication import Auth
from random import randint
import sys

user_api = Blueprint('users', __name__)
user_schema = UserSchema()

@user_api.route('/', methods=['POST'])
def create():
  """
  Create User Function
  """
  data = request.get_json()

  if not data.get('phone_number'):
    return custom_response(error, 400)
  
  # check if user already exist in the db
  user_in_db = UserModel.get_user_by_phone_number(data.get('phone_number'))
  pin = randint(100000,999999)
  if user_in_db:
    user_in_db.update({"pin": pin})
  else:
      data['pin'] = str(pin)
      user = UserModel(data)
      user.save()
  return custom_response({'pin': pin}, 201)


@user_api.route('/', methods=['GET'])
@Auth.auth_required
def get_all():
  users = UserModel.get_all_users()
  ser_users = user_schema.dump(users, many=True).data
  return custom_response(ser_users, 200)


@user_api.route('/<int:user_id>', methods=['GET'])
@Auth.auth_required
def get_a_user(user_id):
  """
  Get a single user
  """
  user = UserModel.get_one_user(user_id)
  if not user:
    return custom_response({'error': 'user not found'}, 404)
  
  ser_user = user_schema.dump(user).data
  return custom_response(ser_user, 200)


@user_api.route('/me', methods=['PUT'])
@Auth.auth_required
def update():
  """
  Update me
  """
  req_data = request.get_json()
  data, error = user_schema.load(req_data, partial=True)
  if error:
    return custom_response(error, 400)

  user = UserModel.get_one_user(g.user.get('id'))
  user.update(data)
  ser_user = user_schema.dump(user).data
  return custom_response(ser_user, 200)


@user_api.route('/me', methods=['DELETE'])
@Auth.auth_required
def delete():
  """
  Delete a user
  """
  user = UserModel.get_one_user(g.user.get('id'))
  user.delete()
  return custom_response({'message': 'deleted'}, 204)


@user_api.route('/me', methods=['GET'])
@Auth.auth_required
def get_me():
  """
  Get me
  """
  user = UserModel.get_one_user(g.user.get('id'))
  ser_user = user_schema.dump(user).data
  return custom_response(ser_user, 200)


@user_api.route('/login', methods=['POST'])
def login():
  req_data = request.get_json()
  try:
    data = user_schema.load(req_data, partial=True)
  except ValidationError as err:
    return custom_response({'error':err.message}, 400)

  if not data.get('phone_number') or not data.get('pin'):
    return custom_response({'error': 'you need phone_number and pin to sign in'}, 400)
  
  user = UserModel.get_user_by_phone_number(data.get('phone_number'))

  if not user:
    return custom_response({'error': 'invalid credentials'}, 400)
  
  if not user.check_pin(data.get('pin')):
    return custom_response({'error': 'invalid credentials'}, 400)
  
  ser_data = user_schema.dump(user)
  print(ser_data, file=sys.stderr)
  
  token = Auth.generate_token(ser_data.get('id'))
  print(token, file=sys.stderr)

  return custom_response({'jwt_token': token, 'user_id':ser_data.get('id') }, 200)




def custom_response(res, status_code):
  """
  Custom Response Function
  """
  return Response(
    mimetype="application/json",
    response=json.dumps(res),
    status=status_code
  )