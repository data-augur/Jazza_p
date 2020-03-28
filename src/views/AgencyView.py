from flask import request, json, Response, Blueprint
from ..models.Agency import AgencyModel, AgencySchema
from ..shared.Authentication import Auth
from marshmallow import ValidationError
import sys
import os
from werkzeug.utils import secure_filename
from pathlib import Path

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

agency_api = Blueprint('agency', __name__)
agency_schema = AgencySchema()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@agency_api.route('/', methods=['POST'])
def create():
  """
  Create Agency Function
  """
  print("In the create agency funciton", sys.stderr)
  if request.method == 'POST':
      if 'logo' not in request.files:
        return custom_response({'error':"file not found"}, 400)

      file = request.files['logo']
      if file.filename == '':
            return custom_response({'error':"file name not found"}, 400)
            
      if file and allowed_file(file.filename):
          full_path = os.path.realpath(__file__)
          full_path = Path(os.path.dirname(full_path))
          full_path=full_path.parent
          filename = secure_filename(file.filename)
          path = os.path.join(full_path, "static")
          path = os.path.join(path, filename)
          file.save(str(path))
          #return custom_response({'success':"file uploaded", "name": name}, 200)

      req_data = request.form
      try:
        data = agency_schema.load(req_data)
      except ValidationError as err:
        return custom_response({'error': err.messages}, 400)
      data['logo_path']='/static/' + filename
      Agency = AgencyModel(data)
      Agency.save()

  return custom_response({'success':"file uploaded"}, 200)
  
  # Agency = AgencyModel(data)
  # Agency.save()
  
  # return custom_response({"success": "Needy Successfuly added"}, 201)


@agency_api.route('/', methods=['GET'])
def get_all():
  Agency = AgencyModel.get_all_Agencies()
  ser_Agency = agency_schema.dump(Agency, many=True)
  return custom_response(ser_Agency, 200)


# @donation_api.route('/needy/<int:needy_id>', methods=['GET'])
# @Auth.auth_required
# def get_a_needy(needy_id):
#   """
#   Get a single needy
#   """
#   donation = DonationModel.get_one_needys_Donation(needy_id)
#   if not donation:
#     return custom_response({'Success': 'No donation for this needy'}, 200)
  
#   ser_donation = donation_schema.dump(donation, many=True)
#   return custom_response(ser_donation, 200)


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