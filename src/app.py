from flask import Flask

from .config import app_config
from .models import db, bcrypt
from .views.UserView import user_api as user_blueprint
from .views.NeedyView import needy_api as needy_blueprint
from .views.DonationView import donation_api as donation_blueprint

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

  app.register_blueprint(user_blueprint, url_prefix='/api/v1/users')
  app.register_blueprint(needy_blueprint, url_prefix='/api/v1/needy')
  app.register_blueprint(donation_blueprint, url_prefix='/api/v1/donation')  
   

  @app.route('/', methods=['GET'])
  def index():
    """
    example endpoint
    """
    return 'Congratulations! Your first endpoint is workin'

  return app
