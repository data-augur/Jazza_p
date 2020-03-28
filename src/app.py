from flask import Flask, render_template, request, redirect, url_for, Response,json

from .config import app_config
from .models import db, bcrypt
from .views.UserView import user_api as user_blueprint
from .views.NeedyView import needy_api as needy_blueprint
from .views.DonationView import donation_api as donation_blueprint
from .views.AgencyView import agency_api as agency_blueprint

def create_app(env_name):
  """
  Create app
  """
  
  # app initiliazation
  app = Flask(__name__)

  app.config.from_object(app_config[env_name])

  bcrypt.init_app(app) # add this line

  db.init_app(app) # add this line

  from .models.User import UserModel
  from .models.Donation import DonationModel
  from .models.Agency import AgencyModel

  app.register_blueprint(user_blueprint, url_prefix='/api/v1/users')
  app.register_blueprint(needy_blueprint, url_prefix='/api/v1/needy')
  app.register_blueprint(donation_blueprint, url_prefix='/api/v1/donation')
  app.register_blueprint(agency_blueprint, url_prefix='/api/v1/agency')  
   

  @app.route('/', methods=['GET'])
  def index():
    """
    example endpoint
    """
    return 'Congratulations! Your first endpoint is workin'


  @app.route('/login', methods=['GET'])
  def login():
    """
    example endpoint
    """
    return render_template('login.html')


  @app.route('/agency', methods=['GET'])
  def agency():
    """
    example endpoint
    """
    return render_template('agency.html')
  

  

  # @app.route('/add_agency', methods=['POST'])
  # def add_agency():
  #   """
  #   example endpoint
  #   """
  #   if request.method == 'POST':
  #     if 'agency_logo' not in request.files:
  #       return custom_response({'error':"file not found"}, 400)
  #     file = request.files['agency_logo']
  #     data = request.form
  #     name = data['agency_name']
  #     url = data['agency_url']
  #     if file.filename == '':
  #           return custom_response({'error':"file name not found"}, 400)
            
  #     if file and allowed_file(file.filename):
  #         full_path = os.path.realpath(__file__)
  #         full_path = os.path.dirname(full_path)
  #         full_path=full_path.parent
  #         filename = secure_filename(file.filename)
  #         file.save(full_path+ "/static/" +filename)
  #         return custom_response({'success':"file uploaded", "name": name}, 200)

  
  def custom_response(res, status_code):
    """
    Custom Response Function
    """
    return Response(
      mimetype="application/json",
      response=json.dumps(res),
      status=status_code
    )
  
  return app
