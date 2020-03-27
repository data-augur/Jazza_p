from flask import request, json, Response, Blueprint
from ..models.Need import NeedyModel, NeedySchema
from ..shared.Authentication import Auth
from random import randint
import sys

needy_api = Blueprint('needy', __name__)
needy_schema = NeedySchema()

@needy_api.route('/', methods=['POST'])
@Auth.auth_required
def create():
  """
  Create Needy Function
  """
  req_data = request.get_json()
  #print(req_data  , file=sys.stderr)
  data = needy_schema.load(req_data)
  #phone_number =req_data.get('phone_number')
  #print(phone_number, file=sys.stderr)



  if not data.get('cnic'):
    return custom_response({'error': 'Cnic missing'}, 400)
  
  # check if user already exist in the db
  user_in_db = NeedyModel.get_needy_by_cnic(data.get('cnic'))
  if user_in_db:
    message = {'error': 'Needy already exist'}
    return custom_response(message, 400)
  else:
      needy = NeedyModel(data)
      needy.save()
  
  return custom_response({"success": "Needy Successfuly added"}, 201)


@needy_api.route('/', methods=['GET'])
@Auth.auth_required
def get_all():
  needy = NeedyModel.get_all_needy()
  ser_needy = needy_schema.dump(needy, many=True)
  return custom_response(ser_needy, 200)


@needy_api.route('/<int:needy_id>', methods=['GET'])
@Auth.auth_required
def get_a_needy(needy_id):
  """
  Get a single needy
  """
  needy = NeedyModel.get_one_needy(needy_id)
  if not needy:
    return custom_response({'error': 'user not found'}, 404)
  
  ser_needy = needy_schema.dump(needy)
  return custom_response(ser_needy, 200)


# @user_api.route('/me', methods=['PUT'])
# @Auth.auth_required
# def update():
#   """
#   Update me
#   """
#   req_data = request.get_json()
#   data, error = user_schema.load(req_data, partial=True)
#   if error:
#     return custom_response(error, 400)

#   user = UserModel.get_one_user(g.user.get('id'))
#   user.update(data)
#   ser_user = user_schema.dump(user).data
#   return custom_response(ser_user, 200)


# @user_api.route('/me', methods=['DELETE'])
# @Auth.auth_required
# def delete():
#   """
#   Delete a user
#   """
#   user = UserModel.get_one_user(g.user.get('id'))
#   user.delete()
#   return custom_response({'message': 'deleted'}, 204)


# @user_api.route('/me', methods=['GET'])
# @Auth.auth_required
# def get_me():
#   """
#   Get me
#   """
#   user = UserModel.get_one_user(g.user.get('id'))
#   ser_user = user_schema.dump(user).data
#   return custom_response(ser_user, 200)


# @user_api.route('/login', methods=['POST'])
# def login():
#   req_data = request.get_json()

#   data = user_schema.load(req_data, partial=True)
#   print(data, file=sys.stderr)
#   #if error:
#    # return custom_response(error, 400)
  
#   if not data.get('phone_number') or not data.get('pin'):
#     return custom_response({'error': 'you need phone_number and pin to sign in'}, 400)
  
#   user = UserModel.get_user_by_phone_number(data.get('phone_number'))

#   if not user:
#     return custom_response({'error': 'invalid credentials'}, 400)
  
#   if not user.check_pin(data.get('pin')):
#     return custom_response({'error': 'invalid credentials'}, 400)
  
#   ser_data = user_schema.dump(user)
#   print(ser_data, file=sys.stderr)
  
#   token = Auth.generate_token(ser_data.get('id'))
#   print(token, file=sys.stderr)

#   return custom_response({'jwt_token': token}, 200)




def custom_response(res, status_code):
  """
  Custom Response Function
  """
  return Response(
    mimetype="application/json",
    response=json.dumps(res),
    status=status_code
  )