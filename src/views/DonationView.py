from flask import request, json, Response, Blueprint
from ..models.Donation import DonationModel, DonationSchema
from ..shared.Authentication import Auth
import sys

donation_api = Blueprint('donation', __name__)
donation_schema = DonationSchema()

@donation_api.route('/', methods=['POST'])
@Auth.auth_required
def create():
  """
  Create Needy Function
  """
  req_data = request.get_json()
  #print(req_data  , file=sys.stderr)
  data = donation_schema.load(req_data)
  #phone_number =req_data.get('phone_number')
  #print(phone_number, file=sys.stderr)



  if not data.get('doner_id') or not data.get('needy_id') or not data.get('item') or not data.get('quantity'):
    return custom_response({'error': 'Data Incomplete missing'}, 400)
  
  
  Donation = DonationModel(data)
  Donation.save()
  
  return custom_response({"success": "Needy Successfuly added"}, 201)


@donation_api.route('/', methods=['GET'])
@Auth.auth_required
def get_all():
  Donation = DonationModel.get_all_Donations()
  ser_Donation = donation_schema.dump(Donation, many=True)
  return custom_response(ser_Donation, 200)


@donation_api.route('/needy/<int:needy_id>', methods=['GET'])
@Auth.auth_required
def get_a_needy(needy_id):
  """
  Get a single needy
  """
  donation = DonationModel.get_one_needys_Donation(needy_id)
  if not donation:
    return custom_response({'Success': 'No donation for this needy'}, 200)
  
  ser_donation = donation_schema.dump(donation, many=True)
  return custom_response(ser_donation, 200)


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